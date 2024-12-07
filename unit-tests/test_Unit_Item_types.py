import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from CargoHubV2.app.services.item_types_service import (
    create_item_type,
    get_item_type,
    get_all_item_types,
    update_item_type,
    delete_item_type,
)
from CargoHubV2.app.models.item_types_model import ItemType
from CargoHubV2.app.schemas.item_types_schema import ItemTypeCreate, ItemTypeUpdate

SAMPLE_ITEM_TYPE = {"name": "Type X", "description": "Test item type"}

# Test create_item_type
def test_create_item_type():
    db = MagicMock()
    type_data = ItemTypeCreate(**SAMPLE_ITEM_TYPE)
    item_type = create_item_type(db, type_data.model_dump())

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(item_type)
    assert item_type.name == SAMPLE_ITEM_TYPE["name"]


# Test get_item_type
def test_get_item_type_found():
    db = MagicMock()
    db.query().filter().first.return_value = ItemType(**SAMPLE_ITEM_TYPE)

    result = get_item_type(db, 1)

    db.query().filter().first.assert_called_once()
    assert result.name == SAMPLE_ITEM_TYPE["name"]

def test_get_item_type_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    result = get_item_type(db, 999)

    assert result is None

def test_get_all_item_types():
    db = MagicMock()

    # Mock the full chain of method calls
    db.query.return_value.offset.return_value.limit.return_value.all.return_value = [
        ItemType(**SAMPLE_ITEM_TYPE),
        ItemType(name="Type Y", description="Another test type"),
    ]

    # Call the function
    results = get_all_item_types(db)

    # Assert that the chain of calls is correct
    # Assert ItemType is passed to query
    db.query.assert_called_once_with(ItemType)
    db.query().offset.assert_called_once_with(0)  # Assert offset is called with 0
    db.query().offset().limit.assert_called_once_with(100)  # Assert limit is called with 100
    db.query().offset().limit().all.assert_called_once()  # Assert all is called

    # Check the results
    assert len(results) == 2
    assert results[0].name == SAMPLE_ITEM_TYPE["name"]


def test_get_all_item_types_empty():
    db = MagicMock()

    # Mock the full chain of method calls
    db.query.return_value.offset.return_value.limit.return_value.all.return_value = []

    # Call the function
    results = get_all_item_types(db)

    # Assert that the chain of calls is correct
    # Assert ItemType is passed to query
    db.query.assert_called_once_with(ItemType)
    db.query().offset.assert_called_once_with(0)  # Assert offset is called with 0
    db.query().offset().limit.assert_called_once_with(100)  # Assert limit is called with 100
    db.query().offset().limit().all.assert_called_once()  # Assert all is called

    # Check the results
    assert len(results) == 0  # Assert the returned list is empty


# Test update_item_type
def test_update_item_type_found():
    db = MagicMock()
    db.query().filter().first.return_value = ItemType(**SAMPLE_ITEM_TYPE)
    update_data = ItemTypeUpdate(description="Updated description")

    updated_type = update_item_type(db, 1, update_data)

    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(updated_type)
    assert updated_type.description == "Updated description"

def test_update_item_type_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    update_data = ItemTypeUpdate(description="Updated description")

    result = update_item_type(db, 999, update_data)

    assert result is None


# Test delete_item_type
def test_delete_item_type_found():
    db = MagicMock()
    db.query().filter().first.return_value = ItemType(**SAMPLE_ITEM_TYPE)

    result = delete_item_type(db, 1)

    db.delete.assert_called_once()
    db.commit.assert_called_once()
    assert result is True

def test_delete_item_type_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    result = delete_item_type(db, 999)

    assert result is False
