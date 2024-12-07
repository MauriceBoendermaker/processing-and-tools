import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from CargoHubV2.app.services.suppliers_service import (
    create_supplier,
    get_supplier,
    get_all_suppliers,
    update_supplier,
    delete_supplier
)
from CargoHubV2.app.models.suppliers_model import Supplier
from CargoHubV2.app.schemas.suppliers_schema import SuppliersCreate, SuppliersUpdate


# Sample supplier data
supplier_sample_data = {
    "id": 1,
    "code": "SUP001",
    "name": "Supplier One",
    "address": "123 Main St",
    "address_extra": "Suite 100",
    "city": "Metropolis",
    "zip_code": "12345",
    "province": "Central",
    "country": "Fictionland",
    "contact_name": "John Doe",
    "phonenumber": "555-1234",
    "reference": "REF001",
    "created_at": "2024-11-15T12:00:00",
    "updated_at": "2024-11-15T12:00:00"
}


def test_create_supplier():
    db = MagicMock()
    supplier_data = SuppliersCreate(**supplier_sample_data)
    new_supplier = create_supplier(db, supplier_data)
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_supplier)


def test_create_supplier_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    supplier_data = SuppliersCreate(**supplier_sample_data)
    with pytest.raises(HTTPException) as excinfo:
        create_supplier(db, supplier_data)
    assert excinfo.value.status_code == 500
    assert "An error occurred while creating the supplier" in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_get_supplier_found():
    db = MagicMock()
    db.query().filter().first.return_value = Supplier(**supplier_sample_data)
    result = get_supplier(db, 1)
    assert result.id == supplier_sample_data["id"]
    db.query().filter().first.assert_called_once()


def test_get_supplier_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        get_supplier(db, 999)
    assert excinfo.value.status_code == 404
    assert "Supplier not found" in str(excinfo.value.detail)


def test_get_all_suppliers():
    
    # Mock the database session
    db = MagicMock()
    
    # Mock the query chain
    mock_query = db.query.return_value
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [Supplier(**supplier_sample_data)]
    
    # Call the function
    results = get_all_suppliers(db, offset=0, limit=10)
    
    # Assertions
    assert len(results) == 1
    db.query.assert_called_once()
    mock_query.all.assert_called_once()



def test_update_supplier_found():
    db = MagicMock()
    db.query().filter().first.return_value = Supplier(**supplier_sample_data)
    supplier_update_data = SuppliersUpdate(name="Updated Supplier")
    updated_supplier = update_supplier(db, 1, supplier_update_data)
    assert updated_supplier.name == "Updated Supplier"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(updated_supplier)


def test_update_supplier_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    supplier_update_data = SuppliersUpdate(name="Updated Supplier")
    with pytest.raises(HTTPException) as excinfo:
        update_supplier(db, 999, supplier_update_data)
    assert excinfo.value.status_code == 404
    assert "Supplier not found" in str(excinfo.value.detail)


def test_update_supplier_integrity_error():
    db = MagicMock()
    db.query().filter().first.return_value = Supplier(**supplier_sample_data)
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    supplier_update_data = SuppliersUpdate(name="Updated Supplier")
    with pytest.raises(HTTPException) as excinfo:
        update_supplier(db, 1, supplier_update_data)
    assert excinfo.value.status_code == 400
    assert "An integrity error occurred while updating the supplier" in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_delete_supplier_found():
    db = MagicMock()
    db.query().filter().first.return_value = Supplier(**supplier_sample_data)
    result = delete_supplier(db, 1)
    assert result["detail"] == "supplier deleted"
    db.delete.assert_called_once()
    db.commit.assert_called_once()


def test_delete_supplier_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        delete_supplier(db, 999)
    assert excinfo.value.status_code == 404
    assert "Supplier not found" in str(excinfo.value.detail)
