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

update_data = {
    "id": 1,
    "name": "Updated name",
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

    result = get_warehouse_by_code(db, SAMPLE_WAREHOUSE_DATA["code"])

    assert result.code == SAMPLE_WAREHOUSE_DATA["code"]
    db.query().filter().first.assert_called_once()


def test_get_warehouse_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        get_warehouse_by_code(db, "onzin")

    assert excinfo.value.status_code == 404
    assert "Warehouse not found" in str(excinfo.value.detail)


def test_get_all_warehouses():
    db = MagicMock()
    mock_query = db.query.return_value
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [Warehouse(**SAMPLE_WAREHOUSE_DATA)]

    with patch("CargoHubV2.app.services.warehouses_service.apply_sorting", return_value=mock_query) as mock_sorting:
        results = get_all_warehouses(db, offset=0, limit=100, sort_by="id", order="asc")

        mock_sorting.assert_called_once_with(mock_query, Warehouse, "id", "asc")
        db.query.assert_called_once_with(Warehouse)
        mock_query.offset.assert_called_once_with(0)
        mock_query.limit.assert_called_once_with(100)
        mock_query.all.assert_called_once()

        assert len(results) == 1


def test_update_warehouse_found():
    db = MagicMock()
    db.query().filter().first.return_value = Warehouse(**SAMPLE_WAREHOUSE_DATA)
    warehouse_update_data = WarehouseUpdate(**update_data)

    updated_warehouse = update_warehouse(
        db, SAMPLE_WAREHOUSE_DATA["code"], warehouse_update_data.model_dump())

    assert updated_warehouse.name == "Updated name"
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_update_warehouse_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    warehouse_update_data = WarehouseUpdate(**update_data)

    with pytest.raises(HTTPException) as excinfo:
        update_warehouse(db, "onzin", warehouse_update_data.model_dump())

    assert excinfo.value.status_code == 404
    assert "Warehouse not found" in str(excinfo.value.detail)


def test_update_warehouse_integrity_error():
    db = MagicMock()
    db.query().filter().first.return_value = Warehouse(**SAMPLE_WAREHOUSE_DATA)
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    warehouse_update_data = WarehouseUpdate(**update_data)

    with pytest.raises(HTTPException) as excinfo:
        update_warehouse(
            db, SAMPLE_WAREHOUSE_DATA["code"],
            warehouse_update_data.model_dump())

    assert excinfo.value.status_code == 400
    assert "The code you gave in the body, already exists" in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_delete_warehouse_found():
    db = MagicMock()
    mock_warehouse = Warehouse(**SAMPLE_WAREHOUSE_DATA)
    db.query().filter().first.return_value = mock_warehouse

    result = delete_warehouse(db, SAMPLE_WAREHOUSE_DATA["code"])

    assert result == {"detail": "Warehouse soft deleted"}
    assert mock_warehouse.is_deleted is True
    db.commit.assert_called_once()
    db.delete.assert_not_called()



def test_delete_warehouse_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        delete_warehouse(db, "onzin")
    assert excinfo.value.status_code == 404
    assert "not found" in str(excinfo.value.detail)

    '''
    with pytest.raises(HTTPException) as excinfo:
        delete_warehouse(db, 2)

    assert excinfo.value.status_code == 404
    assert "Warehouse not found" in str(excinfo.value.detail)
    '''
