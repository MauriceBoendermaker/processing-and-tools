import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from datetime import datetime
from CargoHubV2.app.services.shipments_service import (
    create_shipment, get_shipment, get_all_shipments, update_shipment, delete_shipment
)
from CargoHubV2.app.models.shipments_model import Shipment
from CargoHubV2.app.schemas.shipments_schema import ShipmentCreate, ShipmentUpdate

SAMPLE_SHIPMENT_DATA = {
    "id": 1,
    "order_id": 101,
    "source_id": 10,
    "order_date": datetime(2023, 1, 10),
    "request_date": datetime(2023, 1, 12),
    "shipment_date": datetime(2023, 1, 15),
    "shipment_type": "Ground",
    "shipment_status": "Pending",
    "notes": "Sample note",
    "carrier_code": "UPS",
    "carrier_description": "United Parcel Service",
    "service_code": "Fast",
    "payment_type": "Prepaid",
    "transfer_mode": "Air",
    "total_package_count": 3,
    "total_package_weight": 25.0,
    "items": [{"item_id": "P123", "amount": 5}],
    "created_at": datetime.now(),
    "updated_at": datetime.now()
}


def test_create_shipment():
    db = MagicMock()
    shipment_data = ShipmentCreate(**SAMPLE_SHIPMENT_DATA)

    new_shipment = create_shipment(db, shipment_data.model_dump())

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_shipment)


def test_get_shipment_by_id_found():
    db = MagicMock()
    db.query().filter().first.return_value = Shipment(**SAMPLE_SHIPMENT_DATA)

    result = get_shipment(db, 1)

    assert result.id == SAMPLE_SHIPMENT_DATA["id"]
    db.query().filter().first.assert_called_once()


def test_get_shipment_by_id_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        get_shipment(db, 2)

    assert excinfo.value.status_code == 404
    assert "Shipment not found" in str(excinfo.value.detail)


def test_get_all_shipments():
    db = MagicMock()
    db.query().all.return_value = [Shipment(**SAMPLE_SHIPMENT_DATA)]

    results = get_all_shipments(db)

    assert len(results) == 1
    db.query().all.assert_called_once()


def test_update_shipment_found():
    db = MagicMock()
    db.query().filter().first.return_value = Shipment(**SAMPLE_SHIPMENT_DATA)
    update_data = ShipmentUpdate(shipment_status="Shipped")

    updated_shipment = update_shipment(db, 1, update_data)

    assert updated_shipment.shipment_status == "Shipped"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(updated_shipment)


def test_delete_shipment_found():
    db = MagicMock()
    db.query().filter().first.return_value = Shipment(**SAMPLE_SHIPMENT_DATA)

    result = delete_shipment(db, 1)

    assert result == {'detail': 'Shipment deleted'}
    db.delete.assert_called_once()
    db.commit.assert_called_once()
