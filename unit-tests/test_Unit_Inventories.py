import pytest
from unittest.mock import MagicMock
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
    new_inventory = create_inventory(db, inventory_data.model_dump())
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_inventory)


def test_create_inventory_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    inventory_data = InventoryCreate(**inventory_sample_data)
    with pytest.raises(HTTPException) as excinfo:
        create_inventory(db, inventory_data.model_dump())
    assert excinfo.value.status_code == 400
    assert "An inventory with this code already exists." in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_get_inventory_found():
    db = MagicMock()
    db.query().filter().first.return_value = Inventory(**inventory_sample_data)
    result = get_inventory(db, 1)
    assert result.id == inventory_sample_data["id"]
    db.query().filter().first.assert_called_once()


def test_get_inventory_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        get_inventory(db, 999)
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

    # functie met offset
    results = get_all_inventories(db, offset=0, limit=10)

    # Assertions
    assert len(results) == 1
    db.query.assert_called_once()
    mock_query.all.assert_called_once()


def test_update_inventory_found():
    db = MagicMock()
    db.query().filter().first.return_value = Inventory(**inventory_sample_data)
    inventory_update_data = InventoryUpdate(description="Updated inventory")
    updated_inventory = update_inventory(db, 1, inventory_update_data)
    assert updated_inventory.description == "Updated inventory"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(updated_inventory)


def test_update_inventory_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    inventory_update_data = InventoryUpdate(description="Updated inventory")
    with pytest.raises(HTTPException) as excinfo:
        update_inventory(db, 999, inventory_update_data)
    assert excinfo.value.status_code == 404
    assert "Inventory not found" in str(excinfo.value.detail)


def test_update_inventory_integrity_error():
    db = MagicMock()
    db.query().filter().first.return_value = Inventory(**inventory_sample_data)
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    inventory_update_data = InventoryUpdate(name="Updated inventory")
    with pytest.raises(HTTPException) as excinfo:
        update_inventory(db, 1, inventory_update_data)
    assert excinfo.value.status_code == 400
    assert "An integrity error occurred while updating the inventory" in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_delete_inventory_found():
    db = MagicMock()
    db.query().filter().first.return_value = Inventory(**inventory_sample_data)
    result = delete_inventory(db, 1)
    assert result["detail"] == "inventory deleted"
    db.delete.assert_called_once()
    db.commit.assert_called_once()


def test_delete_inventory_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        delete_inventory(db, 999)
    assert excinfo.value.status_code == 404
    assert "Inventory not found" in str(excinfo.value.detail)
