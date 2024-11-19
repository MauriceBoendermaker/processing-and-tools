import pytest
from unittest.mock import MagicMock
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime
from CargoHubV2.app.services.clients_service import (
    create_client, get_client_by_id, get_all_clients, get_orders_by_client_id, update_client, delete_client
)
from CargoHubV2.app.models.clients_model import Client
from CargoHubV2.app.models.orders_model import Order
from CargoHubV2.app.schemas.clients_schema import ClientCreate, ClientUpdate

# Sample data for testing
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

SAMPLE_ORDERS = [
    {"id": 1, "ship_to": 1, "bill_to": 1, "order_date": datetime(2023, 1, 1)},
    {"id": 2, "ship_to": 1, "bill_to": 1, "order_date": datetime(2023, 2, 1)}
]


def test_create_client():
    db = MagicMock()
    client_data = ClientCreate(**SAMPLE_CLIENT_DATA)

    new_client = create_client(db, client_data.model_dump())

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_client)


def test_create_client_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")

    client_data = ClientCreate(**SAMPLE_CLIENT_DATA)

    with pytest.raises(HTTPException) as excinfo:
        create_client(db, client_data.model_dump())

    assert excinfo.value.status_code == 400
    assert "A client with this data already exists." in str(excinfo.value.detail)
    db.rollback.assert_called_once()