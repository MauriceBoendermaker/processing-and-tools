import pytest
from unittest.mock import MagicMock
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime
from CargoHubV2.app.services.clients_service import (
    create_client, get_client_by_id, get_all_clients, update_client, delete_client
)
from CargoHubV2.app.models.clients_model import Client
from CargoHubV2.app.schemas.clients_schema import ClientCreate, ClientUpdate

SAMPLE_CLIENT_DATA = {
    "id": 1,
    "name": "Sample Client",
    "address": "123 Main Street",
    "city": "Sample City",
    "zip_code": "12345",
    "province": "Sample Province",
    "country": "Sample Country",
    "contact_name": "John Doe",
    "contact_phone": "123-456-7890",
    "contact_email": "client@example.com",
    "created_at": datetime.now(),
    "updated_at": datetime.now()
}

def test_create_client():
    db = MagicMock()
    client_data = ClientCreate(**SAMPLE_CLIENT_DATA)

    new_client = create_client(db, client_data)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_client)

def test_get_client_by_id_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        get_client_by_id(db, 2)

    assert excinfo.value.status_code == 404
    assert "Client not found" in str(excinfo.value.detail)

def test_get_all_clients():
    db = MagicMock()
    db.query().all.return_value = [Client(**SAMPLE_CLIENT_DATA)]

    results = get_all_clients(db)

    assert len(results) == 1
    db.query().all.assert_called_once()

def test_update_client_found():
    db = MagicMock()
    db.query().filter().first.return_value = Client(**SAMPLE_CLIENT_DATA)
    update_data = ClientUpdate(name="Updated Name")

    updated_client = update_client(db, 1, update_data)

    assert updated_client.name == "Updated Name"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(updated_client)

def test_delete_client_found():
    db = MagicMock()
    db.query().filter().first.return_value = Client(**SAMPLE_CLIENT_DATA)

    result = delete_client(db, 1)

    assert result is True
    db.delete.assert_called_once()
    db.commit.assert_called_once()
