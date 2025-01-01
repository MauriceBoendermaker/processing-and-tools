import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime
from CargoHubV2.app.services.clients_service import (
    create_client, get_client, get_all_clients, update_client, delete_client
)
from unittest.mock import ANY
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

    create_client(db, SAMPLE_CLIENT_DATA)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_create_integrity():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")

    with pytest.raises(HTTPException) as excinfo:
        create_client(db, SAMPLE_CLIENT_DATA)

    assert excinfo.value.status_code == 400
    assert "A client with this name already exists." in str(
        excinfo.value.detail)
    db.rollback.assert_called_once()


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
    filtered_query = query_mock.filter.return_value
    filtered_query.offset.return_value = filtered_query
    filtered_query.limit.return_value = filtered_query
    filtered_query.all.return_value = [Client(**SAMPLE_CLIENT_DATA)]

    with patch("CargoHubV2.app.services.clients_service.apply_sorting", return_value=filtered_query) as mock_sorting:
        results = get_all_clients(db, offset=0, limit=100, sort_by="id", order="asc")

        # Assertions
        assert len(results) == 1
        assert results[0].id == SAMPLE_CLIENT_DATA["id"]

        db.query.assert_called_once_with(Client)
        query_mock.filter.assert_called_once_with(ANY)  # Match any BinaryExpression instance
        mock_sorting.assert_called_once_with(filtered_query, Client, "id", "asc")
        filtered_query.offset.assert_called_once_with(0)
        filtered_query.limit.assert_called_once_with(100)
        filtered_query.all.assert_called_once()




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
    mock_client = Client(**SAMPLE_CLIENT_DATA)
    db.query().filter().first.return_value = mock_client

    result = delete_client(db, 1)

    assert result == {'detail': 'Client soft deleted'}
    assert mock_client.is_deleted is True  # Ensure is_deleted was updated
    db.commit.assert_called_once()
