import pytest
from unittest.mock import MagicMock
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from CargoHubV2.app.services.item_groups_service import (
    create_item_group,
    get_item_group,
    get_all_item_groups,
    update_item_group,
    delete_item_group,
)
from CargoHubV2.app.models.item_groups_model import ItemGroup
from CargoHubV2.app.schemas.item_groups_schema import ItemGroupCreate, ItemGroupUpdate

SAMPLE_ITEM_GROUP = {"name": "Group A", "description": "Test group"}

# Test create_item_group
def test_create_item_group():
    db = MagicMock()
    group_data = ItemGroupCreate(**SAMPLE_ITEM_GROUP)
    group = create_item_group(db, group_data.model_dump())

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(group)
    assert group.name == SAMPLE_ITEM_GROUP["name"]

def test_create_item_group_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    group_data = ItemGroupCreate(**SAMPLE_ITEM_GROUP)

    with pytest.raises(HTTPException):
        create_item_group(db, group_data.model_dump())

    db.rollback.assert_called_once()

# Test get_item_group
def test_get_item_group_found():
    db = MagicMock()
    db.query().filter().first.return_value = ItemGroup(**SAMPLE_ITEM_GROUP)

    result = get_item_group(db, 1)

    db.query().filter().first.assert_called_once()
    assert result.name == SAMPLE_ITEM_GROUP["name"]

def test_get_item_group_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    result = get_item_group(db, 999)

    assert result is None

# Test get_all_item_groups
def test_get_all_item_groups():
    db = MagicMock()
    db.query().all.return_value = [
        ItemGroup(**SAMPLE_ITEM_GROUP),
        ItemGroup(name="Group B", description="Another test group"),
    ]

    results = get_all_item_groups(db)

    db.query().all.assert_called_once()
    assert len(results) == 2
    assert results[0].name == SAMPLE_ITEM_GROUP["name"]

def test_get_all_item_groups_empty():
    db = MagicMock()
    db.query().all.return_value = []

    results = get_all_item_groups(db)

    db.query().all.assert_called_once()
    assert len(results) == 0

# Test update_item_group
def test_update_item_group_found():
    db = MagicMock()
    db.query().filter().first.return_value = ItemGroup(**SAMPLE_ITEM_GROUP)
    update_data = ItemGroupUpdate(description="Updated description")

    updated_group = update_item_group(db, 1, update_data)

    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(updated_group)
    assert updated_group.description == "Updated description"

def test_update_item_group_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    update_data = ItemGroupUpdate(description="Updated description")

    result = update_item_group(db, 999, update_data)

    assert result is None

def test_update_item_group_integrity_error():
    db = MagicMock()
    db.query().filter().first.return_value = ItemGroup(**SAMPLE_ITEM_GROUP)
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    update_data = ItemGroupUpdate(description="Updated description")

    with pytest.raises(HTTPException):
        update_item_group(db, 1, update_data)

    db.rollback.assert_called_once()

# Test delete_item_group
def test_delete_item_group_found():
    db = MagicMock()
    db.query().filter().first.return_value = ItemGroup(**SAMPLE_ITEM_GROUP)

    result = delete_item_group(db, 1)

    db.delete.assert_called_once()
    db.commit.assert_called_once()
    assert result is True

def test_delete_item_group_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    result = delete_item_group(db, 999)

    assert result is False
