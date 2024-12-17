import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from CargoHubV2.app.services.docks_service import (
    create_dock, get_all_docks, get_dock_by_id, get_docks_by_warehouse_id,
    update_dock, delete_dock
)
from CargoHubV2.app.models.docks_model import Dock
from CargoHubV2.app.schemas.docks_schema import DockCreate, DockUpdate

SAMPLE_DOCK_DATA = {
    "id": 1,
    "warehouse_id": 101,
    "code": "D1",
    "status": "free",
    "description": "Dock 1 for loading",
}

def test_create_dock():
    db = MagicMock()
    dock_data = DockCreate(**SAMPLE_DOCK_DATA)
    new_dock = create_dock(db, dock_data)
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_dock)

def test_create_dock_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    dock_data = DockCreate(**SAMPLE_DOCK_DATA)
    with pytest.raises(HTTPException) as excinfo:
        create_dock(db, dock_data)
    assert excinfo.value.status_code == 400
    assert "A dock with this code already exists." in str(excinfo.value.detail)
    db.rollback.assert_called_once()

def test_get_dock_by_id_found():
    db = MagicMock()
    db.query().filter().first.return_value = Dock(**SAMPLE_DOCK_DATA)
    result = get_dock_by_id(db, 1)
    assert result.id == SAMPLE_DOCK_DATA["id"]
    db.query().filter().first.assert_called_once()

def test_get_dock_by_id_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        get_dock_by_id(db, 999)
    assert excinfo.value.status_code == 404
    assert "Dock not found" in str(excinfo.value.detail)

def test_get_docks_by_warehouse_found():
    dock = Dock(**SAMPLE_DOCK_DATA)
    db = MagicMock()
    mock_query = db.query.return_value.filter.return_value
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [dock]

    with patch("CargoHubV2.app.services.docks_service.apply_sorting", return_value=mock_query) as mock_sorting:
        result = get_docks_by_warehouse_id(db, warehouse_id=101, offset=0, limit=10, sort_by="id", order="asc")

        mock_sorting.assert_called_once_with(mock_query, Dock, "id", "asc")
        db.query.assert_called_once_with(Dock)
        mock_query.offset.assert_called_once_with(0)
        mock_query.limit.assert_called_once_with(10)
        mock_query.all.assert_called_once()

        assert result[0].warehouse_id == SAMPLE_DOCK_DATA["warehouse_id"]

def test_get_docks_by_warehouse_not_found():
    db = MagicMock()
    db.query().filter().all.return_value = []
    with pytest.raises(HTTPException) as excinfo:
        get_docks_by_warehouse_id(db, 999)
    assert excinfo.value.status_code == 404
    assert "No docks found for the given warehouse." in str(excinfo.value.detail)

def test_get_all_docks():
    db = MagicMock()
    mock_query = db.query.return_value
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [Dock(**SAMPLE_DOCK_DATA)]

    with patch("CargoHubV2.app.services.docks_service.apply_sorting", return_value=mock_query) as mock_sorting:
        results = get_all_docks(db, offset=0, limit=10, sort_by="id", order="asc")

        mock_sorting.assert_called_once_with(mock_query, Dock, "id", "asc")
        db.query.assert_called_once_with(Dock)
        mock_query.offset.assert_called_once_with(0)
        mock_query.limit.assert_called_once_with(10)
        mock_query.all.assert_called_once()

        assert len(results) == 1

def test_update_dock_found():
    db = MagicMock()
    db.query().filter().first.return_value = Dock(**SAMPLE_DOCK_DATA)
    dock_update_data = DockUpdate(status="occupied")
    updated_dock = update_dock(db, 1, dock_update_data)
    assert updated_dock.status == "occupied"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(updated_dock)

def test_update_dock_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    dock_update_data = DockUpdate(status="occupied")
    with pytest.raises(HTTPException) as excinfo:
        update_dock(db, 999, dock_update_data)
    assert excinfo.value.status_code == 404
    assert "Dock not found" in str(excinfo.value.detail)

def test_update_dock_integrity_error():
    db = MagicMock()
    db.query().filter().first.return_value = Dock(**SAMPLE_DOCK_DATA)
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    dock_update_data = DockUpdate(status="occupied")
    with pytest.raises(HTTPException) as excinfo:
        update_dock(db, 1, dock_update_data)
    assert excinfo.value.status_code == 400
    assert "An integrity error occurred while updating the dock." in str(excinfo.value.detail)
    db.rollback.assert_called_once()

def test_delete_dock_found():
    db = MagicMock()
    db.query().filter().first.return_value = Dock(**SAMPLE_DOCK_DATA)
    result = delete_dock(db, 1)
    assert result == {"detail": "Dock deleted"}
    db.delete.assert_called_once()
    db.commit.assert_called_once()

def test_delete_dock_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        delete_dock(db, 999)
    assert excinfo.value.status_code == 404
    assert "Dock not found" in str(excinfo.value.detail)
