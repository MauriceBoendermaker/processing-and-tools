import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime

from CargoHubV2.app.services.docks_service import (
    create_dock,
    get_dock_by_code,
    get_all_docks,
    get_docks_by_warehouse_id,
    update_dock,
    delete_dock
)
from CargoHubV2.app.models.docks_model import Dock
from CargoHubV2.app.schemas.docks_schema import DockCreate, DockUpdate

# Sample Dock Data for Tests
SAMPLE_DOCK_DATA = {
    "id": 1,
    "warehouse_id": 101,
    "code": "D1",
    "status": "Free",
    "description": "Dock 1 for loading",
    "is_deleted": False,
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
}

UPDATED_DOCK_DATA = {
    "status": "Occupied",
    "description": "Dock 1 is now occupied",
}


def test_create_dock():
    db = MagicMock()
    dock_data = DockCreate(
        warehouse_id=SAMPLE_DOCK_DATA["warehouse_id"],
        code=SAMPLE_DOCK_DATA["code"],
        status=SAMPLE_DOCK_DATA["status"],
        description=SAMPLE_DOCK_DATA["description"],
    )

    new_dock = create_dock(db, dock_data)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_dock)


def test_create_dock_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    dock_data = DockCreate(
        warehouse_id=SAMPLE_DOCK_DATA["warehouse_id"],
        code=SAMPLE_DOCK_DATA["code"],
        status=SAMPLE_DOCK_DATA["status"],
        description=SAMPLE_DOCK_DATA["description"],
    )

    with pytest.raises(HTTPException) as excinfo:
        create_dock(db, dock_data)

    assert excinfo.value.status_code == 400
    assert "A dock with this code already exists." in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_get_dock_by_code_found():
    db = MagicMock()
    db.query().filter().first.return_value = Dock(**SAMPLE_DOCK_DATA)

    result = get_dock_by_code(db, "D1")

    assert result.code == SAMPLE_DOCK_DATA["code"]
    assert result.description == SAMPLE_DOCK_DATA["description"]
    db.query().filter().first.assert_called_once()


def test_get_dock_by_code_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    result = get_dock_by_code(db, "NonExistent")

    assert result is None
    db.query().filter().first.assert_called_once()


def test_get_all_docks():
    db = MagicMock()
    mock_query = db.query.return_value
    filtered_query = mock_query.filter.return_value  # Mock the filtered query
    filtered_query.offset.return_value = filtered_query
    filtered_query.limit.return_value = filtered_query
    filtered_query.all.return_value = [Dock(**{**SAMPLE_DOCK_DATA, "is_deleted": False})]

    with patch("CargoHubV2.app.services.docks_service.apply_sorting", return_value=filtered_query) as mock_sorting:
        results = get_all_docks(db, offset=0, limit=10, sort_by="id", order="asc")

        assert len(results) == 1
        assert results[0].id == SAMPLE_DOCK_DATA["id"]

        db.query.assert_called_once_with(Dock)
        assert mock_query.filter.call_count == 1

        filter_args = mock_query.filter.call_args[0][0]
        assert str(filter_args) == str(Dock.is_deleted == False)

        mock_sorting.assert_called_once_with(filtered_query, Dock, "id", "asc")
        filtered_query.offset.assert_called_once_with(0)
        filtered_query.limit.assert_called_once_with(10)


def test_get_docks_by_warehouse_id_found():
    db = MagicMock()
    mock_query = db.query.return_value.filter.return_value
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [Dock(**SAMPLE_DOCK_DATA)]

    with patch("CargoHubV2.app.services.docks_service.apply_sorting", return_value=mock_query) as mock_sorting:
        result = get_docks_by_warehouse_id(db, 101, offset=0, limit=10, sort_by="id", order="asc")

        mock_sorting.assert_called_once_with(mock_query, Dock, "id", "asc")
        db.query.assert_called_once_with(Dock)
        assert len(result) == 1


def test_get_docks_by_warehouse_id_not_found():
    db = MagicMock()
    mock_query = db.query.return_value.filter.return_value
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = []

    with patch("CargoHubV2.app.services.docks_service.apply_sorting", return_value=mock_query) as mock_sorting:
        with pytest.raises(HTTPException) as excinfo:
            get_docks_by_warehouse_id(db, 999, offset=0, limit=10, sort_by="id", order="asc")

        mock_sorting.assert_called_once_with(mock_query, Dock, "id", "asc")
        db.query.assert_called_once_with(Dock)
        assert excinfo.value.status_code == 404
        assert "No docks found for the given warehouse." in str(excinfo.value.detail)


def test_update_dock_found():
    db = MagicMock()
    db.query().filter().first.return_value = Dock(**SAMPLE_DOCK_DATA)
    dock_update_data = DockUpdate(**UPDATED_DOCK_DATA)

    updated_dock = update_dock(db, 1, dock_update_data)

    assert updated_dock.status == "occupied"
    assert updated_dock.description == "Dock 1 is now occupied"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(updated_dock)


def test_delete_dock_found():
    db = MagicMock()
    mock_dock = Dock(**SAMPLE_DOCK_DATA)
    db.query().filter().first.return_value = mock_dock

    result = delete_dock(db, 1)

    assert result["detail"] == "Dock deleted"
    assert mock_dock.is_deleted is True  # Ensure soft delete flag is set
    db.commit.assert_called_once()


def test_delete_dock_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        delete_dock(db, 999)

    assert excinfo.value.status_code == 404
    assert "Dock not found" in str(excinfo.value.detail)
