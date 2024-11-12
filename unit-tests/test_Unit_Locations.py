import pytest
from unittest.mock import MagicMock
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from CargoHubV2.app.services.location_service import create_location, get_all_locations, get_location_by_id, get_locations_by_warehouse_id, update_location, delete_location
from CargoHubV2.app.models.location_model import Location
from CargoHubV2.app.schemas.location_schema import LocationCreate, LocationUpdate


location_sample_data = {
    "id": 1,
    "warehouse_id": 100,
    "code": "B.5.2",
    "name":
    {
        "Row": "B",
        "Rack": "5",
        "Shelf": "2"
    }
}


def test_create_location():
    db = MagicMock()
    location_data = LocationCreate(**location_sample_data)
    # Pass the LocationCreate object to create_location, not the dict
    new_location = create_location(db, location_data)
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_location)


def test_create_location_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    location_data = LocationCreate(**location_sample_data)
    with pytest.raises(HTTPException) as excinfo:
        create_location(db, location_data)
    assert excinfo.value.status_code == 400
    assert "A location with this code already exists." in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_get_location_id_found():
    db = MagicMock()
    db.query().filter().first.return_value = Location(**location_sample_data)
    result = get_location_by_id(db, 1)
    assert result.id == location_sample_data["id"]
    db.query().filter().first.assert_called_once()


def test_get_location_id_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        get_location_by_id(db, "nonexistent-id")
    assert excinfo.value.status_code == 404
    assert "Location id not found" in str(excinfo.value.detail)


def test_get_location_warehouse_found():
    # Create a Location instance with the sample data
    location = Location(**location_sample_data)
    # Mock the database session
    db = MagicMock()
    db.query().filter().all.return_value = [location]  # Return a list of locations
    # Call the service function
    result = get_locations_by_warehouse_id(db, 100)
    # Assert that the warehouse_id matches the expected value
    assert result[0].warehouse_id == location_sample_data["warehouse_id"]
    # Ensure that the mock method was called correctly
    db.query().filter().all.assert_called_once()


def test_get_location_warehouse_not_found():
    db = MagicMock()
    db.query().filter().all.return_value = []  # Return an empty list to simulate no locations found
    with pytest.raises(HTTPException) as excinfo:
        get_locations_by_warehouse_id(db, 999)  # Use an arbitrary warehouse_id for the test
    assert excinfo.value.status_code == 404
    assert "Location warehouse not found" in str(excinfo.value.detail)


def test_get_all_locations():
    db = MagicMock()
    db.query().all.return_value = [Location(**location_sample_data)]
    results = get_all_locations(db)
    assert len(results) == 1
    db.query().all.assert_called_once()


def test_update_location_found():
    db = MagicMock()
    db.query().filter().first.return_value = Location(**location_sample_data)
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
    db.query().filter().first.return_value = Location(**location_sample_data)
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    location_update_data = LocationUpdate(code="Updated code")
    with pytest.raises(HTTPException) as excinfo:
        update_location(db, "B.5.2", location_update_data)
    assert excinfo.value.status_code == 400
    assert "An integrity error occurred while updating the location." in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_delete_location_found():
    db = MagicMock()
    db.query().filter().first.return_value = Location(**location_sample_data)
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
