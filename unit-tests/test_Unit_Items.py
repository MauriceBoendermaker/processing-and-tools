import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime
from CargoHubV2.app.services.items_service import create_item, get_item, get_all_items, update_item, delete_item
from CargoHubV2.app.models.items_model import Item
from CargoHubV2.app.schemas.items_schema import ItemCreate, ItemUpdate


SAMPLE_ITEM_DATA = {
    "uid": "123e4567-e89b-12d3-a456-426614174000",
    "code": "ITEM-TEST",
    "description": "Test item",
    "short_description": "A test item",
    "upc_code": "123456789012",
    "model_number": "MN-TEST",
    "commodity_code": "CC-TEST",
    "item_line": 1,
    "item_group": 2,
    "item_type": 3,
    "unit_purchase_quantity": 100,
    "unit_order_quantity": 50,
    "pack_order_quantity": 25,
    "supplier_id": 10,
    "supplier_code": "SUP-TEST",
    "supplier_part_number": "SPN-TEST",
    "created_at": datetime.now(),
    "updated_at": datetime.now()
}


def test_create_item():
    db = MagicMock()
    item_data = ItemCreate(**SAMPLE_ITEM_DATA)

    # Simulate adding and committing the item without issues
    new_item = create_item(db, item_data.model_dump())

    # Ensure the item was added and committed
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_item)


def test_create_item_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")

    item_data = ItemCreate(**SAMPLE_ITEM_DATA)

    with pytest.raises(HTTPException) as excinfo:
        create_item(db, item_data.model_dump())

    assert excinfo.value.status_code == 400
    assert "An item with this code already exists." in str(
        excinfo.value.detail)
    db.rollback.assert_called_once()


def test_get_item_found():
    db = MagicMock()
    db.query().filter().first.return_value = Item(**SAMPLE_ITEM_DATA)

    result = get_item(db, "ITEM-TEST")

    assert result.uid == SAMPLE_ITEM_DATA["uid"]
    db.query().filter().first.assert_called_once()


def test_get_item_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        get_item(db, "nonexistent-uid")

    assert excinfo.value.status_code == 404
    assert "Item not found" in str(excinfo.value.detail)


def test_get_all_items():
    db = MagicMock()
    mock_query = db.query.return_value
    filtered_query = mock_query.filter.return_value  # Mock the filtered query
    filtered_query.offset.return_value = filtered_query
    filtered_query.limit.return_value = filtered_query
    filtered_query.all.return_value = [
        Item(**{**SAMPLE_ITEM_DATA, "is_deleted": False})  # Include is_deleted=False in mock data
    ]

    with patch("CargoHubV2.app.services.items_service.apply_sorting", return_value=filtered_query) as mock_sorting:
        results = get_all_items(db, offset=0, limit=100, sort_by="code", order="asc")

        # Verify the sorting function was called
        mock_sorting.assert_called_once_with(filtered_query, Item, "code", "asc")

        # Verify the query chain
        db.query.assert_called_once_with(Item)

        # Check that filter was called
        assert mock_query.filter.call_count == 1

        # Validate filter arguments using string comparison
        filter_args = mock_query.filter.call_args[0][0]
        assert str(filter_args) == str(Item.is_deleted == False)  # Compare string representations

        filtered_query.offset.assert_called_once_with(0)
        filtered_query.limit.assert_called_once_with(100)
        filtered_query.all.assert_called_once()

        # Check the result
        assert len(results) == 1
        assert results[0].code == SAMPLE_ITEM_DATA["code"]




def test_update_item_found():
    db = MagicMock()
    db.query().filter().first.return_value = Item(**SAMPLE_ITEM_DATA)
    item_update_data = ItemUpdate(description="Updated description")

    updated_item = update_item(
        db, "ITEM-DATA", item_update_data)

    assert updated_item.description == "Updated description"
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_update_item_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    item_update_data = ItemUpdate(description="Updated description")

    with pytest.raises(HTTPException) as excinfo:
        update_item(db, "nonexistent-code", item_update_data)

    assert excinfo.value.status_code == 404
    assert "Item not found" in str(excinfo.value.detail)


def test_update_item_integrity_error():
    db = MagicMock()
    db.query().filter().first.return_value = Item(**SAMPLE_ITEM_DATA)
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    item_update_data = ItemUpdate(description="Updated description")

    with pytest.raises(HTTPException) as excinfo:
        update_item(db, "ITEM-DATA",
                    item_update_data)

    assert excinfo.value.status_code == 400
    assert "An integrity error occurred while updating the item." in str(
        excinfo.value.detail)
    db.rollback.assert_called_once()


def test_delete_item_found():
    db = MagicMock()
    mock_item = Item(**SAMPLE_ITEM_DATA)
    db.query().filter().first.return_value = mock_item

    result = delete_item(db, "TEST-DATA")

    assert result == {"detail": "Item soft deleted"}
    assert mock_item.is_deleted is True
    db.commit.assert_called_once()
    db.delete.assert_not_called()



def test_delete_item_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        delete_item(db, "nonexistent-code")

    assert excinfo.value.status_code == 404
    assert "Item not found" in str(excinfo.value.detail)
