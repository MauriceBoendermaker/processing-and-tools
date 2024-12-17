import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from CargoHubV2.app.services.locations_service import create_location, get_all_locations, get_location_by_id, get_locations_by_warehouse_id, update_location, delete_location
from CargoHubV2.app.models.locations_model import Location
from CargoHubV2.app.schemas.locations_schema import LocationCreate, LocationUpdate


SAMPLE_LOCATION_DATA = {
    "id": 1,
    "warehouse_id": 100,
    "code": "B.5.2",
    "name": "Row: B, Rack: 5, Shelf: 2"
}


def test_create_location():
    db = MagicMock()
    location_data = LocationCreate(**SAMPLE_LOCATION_DATA)
    # Pass the LocationCreate object to create_location, not the dict
    new_location = create_location(db, location_data)
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_location)


def test_create_location_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    location_data = LocationCreate(**SAMPLE_LOCATION_DATA)
    with pytest.raises(HTTPException) as excinfo:
        create_location(db, location_data)
    assert excinfo.value.status_code == 400
    assert "A location with this code already exists." in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_get_location_id_found():
    db = MagicMock()
    db.query().filter().first.return_value = Location(**SAMPLE_LOCATION_DATA)
    result = get_location_by_id(db, 1)
    assert result.id == SAMPLE_LOCATION_DATA["id"]
    db.query().filter().first.assert_called_once()


def test_get_location_id_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        get_location_by_id(db, "nonexistent-id")
    assert excinfo.value.status_code == 404
    assert "Location id not found" in str(excinfo.value.detail)


def test_get_location_warehouse_found():
    location = Location(**SAMPLE_LOCATION_DATA)
    db = MagicMock()
    mock_query = db.query.return_value.filter.return_value
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [location]

    with patch("CargoHubV2.app.services.locations_service.apply_sorting", return_value=mock_query) as mock_sorting:
        result = get_locations_by_warehouse_id(db, warehouse_id=100, offset=0, limit=10, sort_by="id", order="asc")

        mock_sorting.assert_called_once_with(mock_query, Location, "id", "asc")
        db.query.assert_called_once_with(Location)
        mock_query.offset.assert_called_once_with(0)
        mock_query.limit.assert_called_once_with(10)
        mock_query.all.assert_called_once()

        assert result[0].warehouse_id == SAMPLE_LOCATION_DATA["warehouse_id"]


def test_get_location_warehouse_not_found():
    db = MagicMock()
    db.query().filter().all.return_value = []  # Return an empty list to simulate no locations found
    with pytest.raises(HTTPException) as excinfo:
        get_locations_by_warehouse_id(db, 999)  # Use an arbitrary warehouse_id for the test
    assert excinfo.value.status_code == 404
    assert "Location warehouse not found" in str(excinfo.value.detail)


def test_get_all_locations():
    db = MagicMock()
    mock_query = db.query.return_value
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [Location(**SAMPLE_LOCATION_DATA)]

    with patch("CargoHubV2.app.services.locations_service.apply_sorting", return_value=mock_query) as mock_sorting:
        results = get_all_locations(db, offset=0, limit=10, sort_by="id", order="asc")

        mock_sorting.assert_called_once_with(mock_query, Location, "id", "asc")
        db.query.assert_called_once_with(Location)
        mock_query.offset.assert_called_once_with(0)
        mock_query.limit.assert_called_once_with(10)
        mock_query.all.assert_called_once()

        assert len(results) == 1


def test_update_location_found():
    db = MagicMock()
    db.query().filter().first.return_value = Location(**SAMPLE_LOCATION_DATA)
    location_update_data = LocationUpdate(code="Updated code")
    updated_location = update_location(db, "B.5.2", location_update_data)
    assert updated_location.code == "Updated code"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(updated_location)


def test_update_location_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    location_update_data = LocationUpdate(code="Updated code")
    with pytest.raises(HTTPException) as excinfo:
        update_location(db, "nonexistent-code", location_update_data)
    assert excinfo.value.status_code == 404
    assert "Location not found" in str(excinfo.value.detail)


def test_update_location_integrity_error():
    db = MagicMock()
    db.query().filter().first.return_value = Location(**SAMPLE_LOCATION_DATA)
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    location_update_data = LocationUpdate(code="Updated code")
    with pytest.raises(HTTPException) as excinfo:
        update_location(db, "B.5.2", location_update_data)
    assert excinfo.value.status_code == 400
    assert "An integrity error occurred while updating the location." in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_delete_location_found():
    db = MagicMock()
    db.query().filter().first.return_value = Location(**SAMPLE_LOCATION_DATA)
    result = delete_location(db, "B.5.2")
    assert result == {"detail": "location deleted"}
    db.delete.assert_called_once()
    db.commit.assert_called_once()


def test_delete_location_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        delete_location(db, "nonexistent-code")
    assert excinfo.value.status_code == 404
    assert "Location not found" in str(excinfo.value.detail)
