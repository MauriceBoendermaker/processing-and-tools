import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime
from CargoHubV2.app.services.clients_service import (
    create_client, get_client, get_all_clients, update_client, delete_client
)
from CargoHubV2.app.models.clients_model import Client
from CargoHubV2.app.schemas.clients_schema import ClientCreate, ClientUpdate
from CargoHubV2.app.services.sorting_service import apply_sorting


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
    "created_at": "2015-02-19 16:08:24",
    "updated_at": "2024-09-17 19:06:56"
}


def test_create_client():
    db = MagicMock()
    client_data = ClientCreate(**SAMPLE_CLIENT_DATA)

    new_client = create_client(db, SAMPLE_CLIENT_DATA)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_get_client_by_id_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        get_client(db, 2)

    assert excinfo.value.status_code == 404
    assert "Client not found" in str(excinfo.value.detail)


def test_get_all_clients():
    db = MagicMock()
    query_mock = db.query.return_value
    query_mock.offset.return_value = query_mock
    query_mock.limit.return_value = query_mock
    query_mock.all.return_value = [Client(**SAMPLE_CLIENT_DATA)]

    with patch("CargoHubV2.app.services.clients_service.apply_sorting", return_value=query_mock) as mock_sorting:
        results = get_all_clients(db, offset=0, limit=100, sort_by="id", order="asc")

        assert len(results) == 1
        db.query.assert_called_once()
        mock_sorting.assert_called_once_with(query_mock, Client, "id", "asc")
        query_mock.offset.assert_called_once_with(0)
        query_mock.limit.assert_called_once_with(100)



def test_update_client_found():
    db = MagicMock()
    db.query().filter().first.return_value = Client(**SAMPLE_CLIENT_DATA)
    update_data = ClientUpdate(name="Updated Name")

    updated_client = update_client(db, 1, update_data)

    assert updated_client.name == "Updated Name"
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_delete_client_found():
    db = MagicMock()
    db.query().filter().first.return_value = Client(**SAMPLE_CLIENT_DATA)

    result = delete_client(db, 1)

    assert result == {'detail': 'Client deleted'}
    db.delete.assert_called_once()
    db.commit.assert_called_once()
