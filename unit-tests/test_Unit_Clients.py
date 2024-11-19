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


def test_get_client_by_id_found():
    db = MagicMock()
    db.query().filter().first.return_value = Client(**SAMPLE_CLIENT_DATA)

    result = get_client_by_id(db, 1)

    assert result.id == SAMPLE_CLIENT_DATA["id"]
    db.query().filter().first.assert_called_once()


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


def test_get_orders_by_client_id_found():
    db = MagicMock()
    db.query(Client).filter().first.return_value = Client(**SAMPLE_CLIENT_DATA)
    db.query(Order).filter().all.return_value = SAMPLE_ORDERS

    result = get_orders_by_client_id(db, 1)

    assert len(result) == 2
    assert result[0]["id"] == SAMPLE_ORDERS[0]["id"]
    db.query(Client).filter().first.assert_called_once()
    db.query(Order).filter().all.assert_called_once()


def test_get_orders_by_client_id_no_orders():
    db = MagicMock()
    db.query(Client).filter().first.return_value = Client(**SAMPLE_CLIENT_DATA)
    db.query(Order).filter().all.return_value = []

    with pytest.raises(HTTPException) as excinfo:
        get_orders_by_client_id(db, 1)

    assert excinfo.value.status_code == 404
    assert "No orders found for this client" in str(excinfo.value.detail)


def test_get_orders_by_client_id_not_found():
    db = MagicMock()
    db.query(Client).filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        get_orders_by_client_id(db, 2)

    assert excinfo.value.status_code == 404
    assert "Client not found" in str(excinfo.value.detail)


def test_update_client_found():
    db = MagicMock()
    db.query().filter().first.return_value = Client(**SAMPLE_CLIENT_DATA)
    update_data = ClientUpdate(name="Updated Name")

    updated_client = update_client(db, 1, update_data)

    assert updated_client.name == "Updated Name"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(updated_client)


def test_update_client_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    update_data = ClientUpdate(name="Updated Name")

    with pytest.raises(HTTPException) as excinfo:
        update_client(db, 5, update_data)

    assert excinfo.value.status_code == 404
    assert "Client not found" in str(excinfo.value.detail)


def test_delete_client_found():
    db = MagicMock()
    db.query().filter().first.return_value = Client(**SAMPLE_CLIENT_DATA)

    result = delete_client(db, 1)

    assert result is True
    db.delete.assert_called_once()
    db.commit.assert_called_once()


def test_delete_client_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    assert delete_client(db, 2) is False
    # Uncomment the following lines if you want to raise an exception instead
    # with pytest.raises(HTTPException) as excinfo:
    #     delete_client(db, 2)
    # assert excinfo.value.status_code == 404
    # assert "Client not found" in str(excinfo.value.detail)
