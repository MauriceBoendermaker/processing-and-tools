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
    mock_query = db.query.return_value
    filtered_query = mock_query.filter.return_value  # Mock the filtered query
    filtered_query.offset.return_value = filtered_query
    filtered_query.limit.return_value = filtered_query
    filtered_query.all.return_value = [
        ItemType(**{**SAMPLE_ITEM_TYPE, "is_deleted": False}),
        ItemType(name="Type Y", description="Another test type", is_deleted=False),
    ]

    with patch("CargoHubV2.app.services.item_types_service.apply_sorting", return_value=filtered_query) as mock_sorting:
        results = get_all_item_types(db, offset=0, limit=100, sort_by="name", order="asc")

        mock_sorting.assert_called_once_with(filtered_query, ItemType, "name", "asc")
        db.query.assert_called_once_with(ItemType)
        assert mock_query.filter.call_count == 1

        filter_args = mock_query.filter.call_args[0][0]
        assert str(filter_args) == str(ItemType.is_deleted == False)

        filtered_query.offset.assert_called_once_with(0)
        filtered_query.limit.assert_called_once_with(100)
        filtered_query.all.assert_called_once()

        assert len(results) == 2
        assert results[0].name == SAMPLE_ITEM_TYPE["name"]


def test_get_all_item_types_empty():
    db = MagicMock()
    mock_query = db.query.return_value
    filtered_query = mock_query.filter.return_value  # Mock the filtered query
    filtered_query.offset.return_value = filtered_query
    filtered_query.limit.return_value = filtered_query
    filtered_query.all.return_value = []

    with patch("CargoHubV2.app.services.item_types_service.apply_sorting", return_value=filtered_query) as mock_sorting:
        results = get_all_item_types(db, offset=0, limit=100, sort_by="name", order="asc")

        mock_sorting.assert_called_once_with(filtered_query, ItemType, "name", "asc")
        db.query.assert_called_once_with(ItemType)
        assert mock_query.filter.call_count == 1

        filter_args = mock_query.filter.call_args[0][0]
        assert str(filter_args) == str(ItemType.is_deleted == False)

        filtered_query.offset.assert_called_once_with(0)
        filtered_query.limit.assert_called_once_with(100)
        filtered_query.all.assert_called_once()

        assert len(results) == 0



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


def test_delete_item_type_found():
    db = MagicMock()
    mock_item_type = ItemType(**SAMPLE_ITEM_TYPE)
    db.query().filter().first.return_value = mock_item_type

    result = delete_item_type(db, 1)

    assert result is True
    assert mock_item_type.is_deleted is True
    db.commit.assert_called_once()
    db.delete.assert_not_called()


def test_delete_item_type_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    result = delete_item_type(db, 999)

    assert result is False
