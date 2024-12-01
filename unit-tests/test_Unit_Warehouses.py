import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime
from CargoHubV2.app.services.warehouses_service import create_warehouse, get_warehouse_by_code, get_all_warehouses, update_warehouse, delete_warehouse
from CargoHubV2.app.models.warehouses_model import Warehouse
from CargoHubV2.app.schemas.warehouses_schema import WarehouseCreate, WarehouseUpdate


# Sample data to use in tests
SAMPLE_WAREHOUSE_DATA = {
    "id": 1,
    "name": "test hub",
    "zip": "4002 AS",
    "province": "Friesland",
    "contact": {
      "name": "Fem Keijzer",
      "phone": "(078) 0013363",
      "email": "blamore@example.net"
    },
    "code": "YQZZNL56",
    "address": "Wijnhaven 107",
    "city": "Rotterdam",
    "country": "NL",
    "created_at": datetime.now(),
    "updated_at": datetime.now()
  }


def test_create_warehouse():
    db = MagicMock()
    warehouse_data = WarehouseCreate(**SAMPLE_WAREHOUSE_DATA)

    new_warehouse = create_warehouse(db, warehouse_data.model_dump())

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_warehouse)


def test_create_warehouse_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")

    warehouse_data = WarehouseCreate(**SAMPLE_WAREHOUSE_DATA)

    with pytest.raises(HTTPException) as excinfo:
        create_warehouse(db, warehouse_data.model_dump())

    assert excinfo.value.status_code == 400
    assert "A warehouse with this code already exists." in str(excinfo.value.detail)
    db.rollback.assert_called_once()


# Test for get_warehouse
def test_single_warehouse_found():
    db = MagicMock()
    db.query().filter().first.return_value = Warehouse(**SAMPLE_WAREHOUSE_DATA)

    result = get_warehouse_by_id(db, 1)

    assert result.id == SAMPLE_WAREHOUSE_DATA["id"]
    db.query().filter().first.assert_called_once()


def test_get_warehouse_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        get_warehouse_by_id(db, 2)

    assert excinfo.value.status_code == 404
    assert "Warehouse not found" in str(excinfo.value.detail)


def test_get_all_warehouses():
    db = MagicMock()
    db.query().offset().limit().all.return_value = [Warehouse(**SAMPLE_WAREHOUSE_DATA)]

    results = get_all_warehouses(db)

    assert len(results) == 1
    db.query().offset().limit().all.assert_called_once()


def test_update_warehouse_found():
    db = MagicMock()
    db.query().filter().first.return_value = Warehouse(**SAMPLE_WAREHOUSE_DATA)
    warehouse_update_data = WarehouseUpdate(name="Updated name")

    updated_warehouse = update_warehouse(db, 1, warehouse_update_data)

    assert updated_warehouse.name == "Updated name"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(updated_warehouse)


def test_update_warehouse_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    warehouse_update_data = WarehouseUpdate(name="Updated name")

    with pytest.raises(HTTPException) as excinfo:
        update_warehouse(db, 5, warehouse_update_data)

    assert excinfo.value.status_code == 404
    assert "Warehouse not found" in str(excinfo.value.detail)


def test_update_warehouse_integrity_error():
    db = MagicMock()
    db.query().filter().first.return_value = Warehouse(**SAMPLE_WAREHOUSE_DATA)
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    warehouse_update_data = WarehouseUpdate(description="Updated description")

    with pytest.raises(HTTPException) as excinfo:
        update_warehouse(db, 1, warehouse_update_data)

    assert excinfo.value.status_code == 400
    assert "The code you gave in the body, already exists" in str(excinfo.value.detail)
    db.rollback.assert_called_once()


# Test for delete_warehouse
def test_delete_warehouse_found():
    db = MagicMock()
    db.query().filter().first.return_value = Warehouse(**SAMPLE_WAREHOUSE_DATA)

    result = delete_warehouse(db, 1)

    assert result is True
    db.delete.assert_called_once()
    db.commit.assert_called_once()


def test_delete_warehouse_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    assert delete_warehouse(db, 2) is False
    '''
    with pytest.raises(HTTPException) as excinfo:
        delete_warehouse(db, 2)

    assert excinfo.value.status_code == 404
    assert "Warehouse not found" in str(excinfo.value.detail)
    '''
