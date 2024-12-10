import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime
from CargoHubV2.app.services.transfers_service import create_transfer, get_transfer, get_all_transfers, update_transfer, delete_transfer
from CargoHubV2.app.models.transfers_model import Transfer
from CargoHubV2.app.schemas.transfers_schema import TransferCreate, TransferUpdate

# Sample data to use in tests
SAMPLE_TRANSFER_DATA = {
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
    transfer_data = TransferCreate(**SAMPLE_TRANSFER_DATA)

    new_transfer = create_transfer(db, transfer_data)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_transfer)


def test_create_transfer_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")

    transfer_data = TransferCreate(**SAMPLE_TRANSFER_DATA)

    with pytest.raises(HTTPException) as excinfo:
        create_transfer(db, transfer_data)

    assert excinfo.value.status_code == 400
    assert "A transfer with this reference already exists." in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_get_transfer_found():
    db = MagicMock()
    db.query().filter().first.return_value = Transfer(**SAMPLE_TRANSFER_DATA)

    result = get_transfer(db, 1)

    assert result.id == SAMPLE_TRANSFER_DATA["id"]
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
    mock_query = db.query.return_value
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [Transfer(**SAMPLE_TRANSFER_DATA)]

    with patch("CargoHubV2.app.services.transfers_service.apply_sorting", return_value=mock_query) as mock_sorting:
        results = get_all_transfers(db, offset=0, limit=100, sort_by="id", order="asc")

        mock_sorting.assert_called_once_with(mock_query, Transfer, "id", "asc")
        db.query.assert_called_once_with(Transfer)
        mock_query.offset.assert_called_once_with(0)
        mock_query.limit.assert_called_once_with(100)
        mock_query.all.assert_called_once()

        assert len(results) == 1


def test_update_transfer_found():
    db = MagicMock()
    db.query().filter().first.return_value = Transfer(**SAMPLE_TRANSFER_DATA)
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
    db.query().filter().first.return_value = Transfer(**SAMPLE_TRANSFER_DATA)
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    transfer_update_data = TransferUpdate(transfer_status="Processed")

    with pytest.raises(HTTPException) as excinfo:
        update_transfer(db, 1, transfer_update_data)

    assert excinfo.value.status_code == 400
    assert "An integrity error occurred while updating the transfer." in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_delete_transfer_found():
    db = MagicMock()
    db.query().filter().first.return_value = Transfer(**SAMPLE_TRANSFER_DATA)

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
