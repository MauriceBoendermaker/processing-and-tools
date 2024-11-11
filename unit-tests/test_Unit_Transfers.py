import pytest
from unittest.mock import MagicMock
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime
from ..CargoHubV2.app.services.transfer_service import create_transfer, get_transfer, get_all_transfers, update_transfer, delete_transfer
from ..CargoHubV2.app.models.transfers_model import Transfer
from ..CargoHubV2.app.schemas.transfers_schema import TransferCreate, TransferUpdate

# Sample data to use in tests
sample_transfer_data = {
    "id": 1,
    "reference": "TR00001",
    "transfer_from": 9229,
    "transfer_to": 9284,
    "transfer_status": "Scheduled",
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
    "items": [{"item_id": "P007435", "amount": 23}]
}


def test_create_transfer():
    db = MagicMock()
    transfer_data = TransferCreate(**sample_transfer_data)

    new_transfer = create_transfer(db, transfer_data)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_transfer)


def test_create_transfer_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")

    transfer_data = TransferCreate(**sample_transfer_data)

    with pytest.raises(HTTPException) as excinfo:
        create_transfer(db, transfer_data)

    assert excinfo.value.status_code == 400
    assert "A transfer with this reference already exists." in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_get_transfer_found():
    db = MagicMock()
    db.query().filter().first.return_value = Transfer(**sample_transfer_data)

    result = get_transfer(db, 1)

    assert result.id == sample_transfer_data["id"]
    db.query().filter().first.assert_called_once()


def test_get_transfer_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        get_transfer(db, 2)

    assert excinfo.value.status_code == 404
    assert "Transfer not found" in str(excinfo.value.detail)


def test_get_all_transfers():
    db = MagicMock()
    db.query().all.return_value = [Transfer(**sample_transfer_data)]

    results = get_all_transfers(db)

    assert len(results) == 1
    db.query().all.assert_called_once()


def test_update_transfer_found():
    db = MagicMock()
    db.query().filter().first.return_value = Transfer(**sample_transfer_data)
    transfer_update_data = TransferUpdate(transfer_status="Processed")

    updated_transfer = update_transfer(db, 1, transfer_update_data)

    assert updated_transfer.transfer_status == "Processed"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(updated_transfer)


def test_update_transfer_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    transfer_update_data = TransferUpdate(transfer_status="Processed")

    with pytest.raises(HTTPException) as excinfo:
        update_transfer(db, 5, transfer_update_data)

    assert excinfo.value.status_code == 404
    assert "Transfer not found" in str(excinfo.value.detail)


def test_update_transfer_integrity_error():
    db = MagicMock()
    db.query().filter().first.return_value = Transfer(**sample_transfer_data)
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    transfer_update_data = TransferUpdate(transfer_status="Processed")

    with pytest.raises(HTTPException) as excinfo:
        update_transfer(db, 1, transfer_update_data)

    assert excinfo.value.status_code == 400
    assert "An integrity error occurred while updating the transfer." in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_delete_transfer_found():
    db = MagicMock()
    db.query().filter().first.return_value = Transfer(**sample_transfer_data)

    result = delete_transfer(db, 1)

    assert result == {"detail": "Transfer deleted"}
    db.delete.assert_called_once()
    db.commit.assert_called_once()


def test_delete_transfer_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        delete_transfer(db, 2)

    assert excinfo.value.status_code == 404
    assert "Transfer not found" in str(excinfo.value.detail)
