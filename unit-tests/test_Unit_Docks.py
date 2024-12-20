import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime
from CargoHubV2.app.services.docks_service import (
    create_dock, get_dock_by_code, get_all_docks, update_dock, delete_dock
)
from CargoHubV2.app.models.docks_model import Dock
from CargoHubV2.app.schemas.docks_schema import DockCreate, DockUpdate

# Sample data to use in tests
SAMPLE_DOCK_DATA = {
    "id": 1,
    "warehouse_id": 1,
    "code": "DOCK001",
    "type": "loading",
    "is_occupied": False,
    "created_at": datetime.now(),
    "updated_at": datetime.now()
}

UPDATE_DOCK_DATA = {
    "id": 1,
    "warehouse_id": 1,
    "code": "DOCK001",
    "type": "unloading",
    "is_occupied": True,
    "created_at": datetime.now(),
    "updated_at": datetime.now()
}

def test_create_dock():
    db = MagicMock()
    dock_data = DockCreate(**SAMPLE_DOCK_DATA)

    new_dock = create_dock(db, dock_data.model_dump())

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_dock)

def test_create_dock_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")

    dock_data = DockCreate(**SAMPLE_DOCK_DATA)

    with pytest.raises(HTTPException) as excinfo:
        create_dock(db, dock_data.model_dump())

    assert excinfo.value.status_code == 400
    assert "A dock with this code already exists." in str(excinfo.value.detail)
    db.rollback.assert_called_once()

def test_get_dock_by_code_found():
    db = MagicMock()
    db.query().filter().first.return_value = Dock(**SAMPLE_DOCK_DATA)

    result = get_dock_by_code(db, SAMPLE_DOCK_DATA["code"])

    assert result.code == SAMPLE_DOCK_DATA["code"]
    db.query().filter().first.assert_called_once()

def test_get_dock_by_code_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        get_dock_by_code(db, "INVALID_CODE")

    assert excinfo.value.status_code == 404
    assert "Dock not found" in str(excinfo.value.detail)

def test_get_all_docks():
    db = MagicMock()
    mock_query = db.query.return_value
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [Dock(**SAMPLE_DOCK_DATA)]

    with patch("CargoHubV2.app.services.docks_service.apply_sorting", return_value=mock_query) as mock_sorting:
        results = get_all_docks(db, offset=0, limit=100, sort_by="id", order="asc")

        mock_sorting.assert_called_once_with(mock_query, Dock, "id", "asc")
        db.query.assert_called_once_with(Dock)
        mock_query.offset.assert_called_once_with(0)
        mock_query.limit.assert_called_once_with(100)
        mock_query.all.assert_called_once()

        assert len(results) == 1

def test_update_dock_found():
    db = MagicMock()
    db.query().filter().first.return_value = Dock(**SAMPLE_DOCK_DATA)
    dock_update_data = DockUpdate(**UPDATE_DOCK_DATA)

    updated_dock = update_dock(
        db, SAMPLE_DOCK_DATA["code"], dock_update_data.model_dump())

    assert updated_dock.type == "unloading"
    assert updated_dock.is_occupied is True
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

def test_update_dock_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    dock_update_data = DockUpdate(**UPDATE_DOCK_DATA)

    with pytest.raises(HTTPException) as excinfo:
        update_dock(db, "INVALID_CODE", dock_update_data.model_dump())

    assert excinfo.value.status_code == 404
    assert "Dock not found" in str(excinfo.value.detail)

def test_update_dock_integrity_error():
    db = MagicMock()
    db.query().filter().first.return_value = Dock(**SAMPLE_DOCK_DATA)
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    dock_update_data = DockUpdate(**UPDATE_DOCK_DATA)

    with pytest.raises(HTTPException) as excinfo:
        update_dock(
            db, SAMPLE_DOCK_DATA["code"],
            dock_update_data.model_dump())

    assert excinfo.value.status_code == 400
    assert "The code you gave in the body already exists." in str(excinfo.value.detail)
    db.rollback.assert_called_once()

def test_delete_dock_found():
    db = MagicMock()
    db.query().filter().first.return_value = Dock(**SAMPLE_DOCK_DATA)

    result = delete_dock(db, SAMPLE_DOCK_DATA["code"])

    assert result is True
    db.delete.assert_called_once()
    db.commit.assert_called_once()

def test_delete_dock_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    
    with pytest.raises(HTTPException) as excinfo:
        delete_dock(db, "INVALID_CODE")

    assert excinfo.value.status_code == 404
    assert "Dock not found" in str(excinfo.value.detail)
