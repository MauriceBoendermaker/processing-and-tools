import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from CargoHubV2.app.services.inventories_service import (
    create_inventory,
    get_inventory,
    get_all_inventories,
    update_inventory,
    delete_inventory)
from CargoHubV2.app.models.inventories_model import Inventory

from CargoHubV2.app.schemas.inventories_schema import InventoryCreate, InventoryUpdate


# Sample inventory data
inventory_sample_data = {
        "id": 1,
        "item_id": "P000001",
        "description": "updated",
        "item_reference": "sjQ23408K",
        "locations": [
            1,
            2,
            3
        ],
        "total_on_hand": 262,
        "total_expected": 0,
        "total_ordered": 80,
        "total_allocated": 41,
        "total_available": 141,
        "created_at": "2015-02-19 16:08:24",
        "updated_at": "2024-09-17T19:06:56.366055Z"
    }


def test_create_inventory():
    db = MagicMock()
    inventory_data = InventoryCreate(**inventory_sample_data)
    create_inventory(db, inventory_data.model_dump())
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_create_inventory_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    inventory_data = InventoryCreate(**inventory_sample_data)
    with pytest.raises(HTTPException) as excinfo:
        create_inventory(db, inventory_data.model_dump())
    assert excinfo.value.status_code == 400
    assert "An inventory with this item reference already exists." in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_get_inventory_found():
    db = MagicMock()
    db.query().filter().first.return_value = Inventory(**inventory_sample_data)
    result = get_inventory(db, inventory_sample_data["item_reference"])
    assert result.item_reference == inventory_sample_data["item_reference"]
    db.query().filter().first.assert_called_once()


def test_get_inventory_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        get_inventory(db, "random reference")
    assert excinfo.value.status_code == 404
    assert "inventory not found" in str(excinfo.value.detail)


def test_get_all_inventories():
    # Mock the database session
    db = MagicMock()

    # Mock the query chain
    mock_query = db.query.return_value
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [Inventory(**inventory_sample_data)]

    # Patch apply_sorting
    with patch("CargoHubV2.app.services.inventories_service.apply_sorting", return_value=mock_query) as mock_sorting:
        results = get_all_inventories(db, offset=0, limit=10, sort_by="id", order="asc")

        # Assertions
        assert len(results) == 1
        db.query.assert_called_once()
        mock_sorting.assert_called_once_with(mock_query, Inventory, "id", "asc")
        mock_query.offset.assert_called_once_with(0)
        mock_query.limit.assert_called_once_with(10)


def test_update_inventory_found():
    db = MagicMock()
    db.query().filter().first.return_value = Inventory(**inventory_sample_data)
    updated_inventory = update_inventory(db, inventory_sample_data["item_reference"], {"description": "Updated inventory"})
    assert updated_inventory.description == "Updated inventory"
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_update_inventory_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        update_inventory(db, "nonsense reference", {"description": "Updated inventory 2"})
    assert excinfo.value.status_code == 404
    assert "Inventory not found" in str(excinfo.value.detail)


def test_update_inventory_integrity_error():
    db = MagicMock()
    db.query().filter().first.return_value = Inventory(**inventory_sample_data)
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    with pytest.raises(HTTPException) as excinfo:
        update_inventory(db, inventory_sample_data["item_reference"], {"description": "Updated inventory 3"})
    assert excinfo.value.status_code == 400
    assert "An integrity error occurred while updating the inventory" in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_delete_inventory_found():
    db = MagicMock()
    db.query().filter().first.return_value = Inventory(**inventory_sample_data)
    result = delete_inventory(db, inventory_sample_data["item_reference"])
    assert result["detail"] == "inventory deleted"
    db.delete.assert_called_once()
    db.commit.assert_called_once()


def test_delete_inventory_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        delete_inventory(db, "nonsens")
    assert excinfo.value.status_code == 404
    assert "Inventory not found" in str(excinfo.value.detail)
