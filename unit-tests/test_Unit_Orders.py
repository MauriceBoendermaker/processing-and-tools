import pytest
from unittest.mock import MagicMock, patch, ANY
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from CargoHubV2.app.services.orders_service import (
    create_order,
    get_order,
    get_all_orders,
    update_order,
    delete_order,
    get_items_in_order,
    get_packinglist_for_order
)
from CargoHubV2.app.models.orders_model import Order
from CargoHubV2.app.models.inventories_model import Inventory
from CargoHubV2.app.schemas.orders_schema import OrderCreate, OrderUpdate
from datetime import datetime as dt
import datetime

SAMPLE_ORDER_DATA = {
    "id": 1,
    "source_id": 33,
    "order_date": dt.now(datetime.timezone.utc),
    "request_date": dt.now(datetime.timezone.utc),
    "reference": "ORD00001",
    "order_status": "Pending",
    "warehouse_id": 1,
    "total_amount": 9905.13,
    "total_discount": 150.77,
    "total_tax": 372.72,
    "total_surcharge": 77.6,
    "created_at": "2019-04-03T11:33:15Z",
    "updated_at": "2019-04-05T07:33:15Z",
    "shipping_notes": "Handle with care",
    "items": [
        {"item_id": "P009557", "amount": 1}
    ]
}
SAMPLE_INVEN_DATA = {
    "id": 9557,
    "item_id": "P009557",
    "description": "Advanced eco-centric orchestration",
    "item_reference": "gjg98549Y",
    "locations": [9199, 13459, 13402,
                  22498, 26120, 19728, 19882,
                  28260, 27159, 27314, 14417,
                  14246, 16824, 16857, 27185, 27602],
    "total_on_hand": 205,
    "total_expected": 0,
    "total_ordered": 49,
    "total_allocated": 60,
    "total_available": 96,
    "created_at": "2008-05-19T00:14:42",
    "updated_at": "2013-04-24 16:19:43.000000",
    "is_deleted": False
}
# fix later, mock db werkt nu niet ivm andere queries in de service
'''
def test_create_order():
    db = MagicMock()
    db.query().filter().first.return_value = None
    order_data = OrderCreate(**SAMPLE_ORDER_DATA)
    new_order = create_order(db, order_data.model_dump())
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(new_order)

def test_create_order_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    order_data = OrderCreate(**SAMPLE_ORDER_DATA)
    with pytest.raises(HTTPException) as excinfo:
        create_order(db, order_data.model_dump())
    assert excinfo.value.status_code == 400
    assert "An order with this reference already exists." in str(excinfo.value.detail)
    db.rollback.assert_called_once()
'''


def test_get_order_found():
    db = MagicMock()
    db.query().filter().first.return_value = Order(**SAMPLE_ORDER_DATA)
    result = get_order(db, 1)
    assert result.id == SAMPLE_ORDER_DATA["id"]
    db.query().filter().first.assert_called_once()


def test_get_order_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        get_order(db, 99)
    assert excinfo.value.status_code == 404
    assert "Order not found" in str(excinfo.value.detail)


def test_get_all_orders():
    db = MagicMock()
    mock_query = db.query.return_value
    filtered_query = mock_query.filter.return_value  # Mock the filtered query
    filtered_query.offset.return_value = filtered_query
    filtered_query.limit.return_value = filtered_query
    filtered_query.all.return_value = [Order(**{**SAMPLE_ORDER_DATA, "is_deleted": False})]

    with patch("CargoHubV2.app.services.orders_service.apply_sorting", return_value=filtered_query) as mock_sorting:
        results = get_all_orders(db, offset=0, limit=100, sort_by="id")

        mock_sorting.assert_called_once_with(filtered_query, Order, "id", "asc")
        db.query.assert_called_once_with(Order)
        assert mock_query.filter.call_count == 1

        filter_args = mock_query.filter.call_args[0][0]

        filtered_query.offset.assert_called_once_with(0)
        filtered_query.limit.assert_called_once_with(100)
        filtered_query.all.assert_called_once()

        assert len(results) == 1
        assert results[0].id == SAMPLE_ORDER_DATA["id"]


def test_get_all_orders_by_date():
    db = MagicMock()
    mock_query = db.query.return_value
    mock_query.filter.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [Order(**SAMPLE_ORDER_DATA)]

    with patch("CargoHubV2.app.services.orders_service.apply_sorting", return_value=mock_query) as mock_sorting:
        results = get_all_orders(db, date=SAMPLE_ORDER_DATA["order_date"], offset=0, limit=100, sort_by="id", sort_order="asc")

        mock_sorting.assert_called_once_with(mock_query, Order, "id", "asc")
        db.query.assert_called_once_with(Order)
        mock_query.filter.assert_called_once_with(ANY)
        mock_query.offset.assert_called_once_with(0)
        mock_query.limit.assert_called_once_with(100)
        mock_query.all.assert_called_once()

        assert len(results) == 1


def test_get_all_orders_no_results():
    db = MagicMock()
    mock_query = db.query.return_value
    mock_query.filter.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = []

    with patch("CargoHubV2.app.services.orders_service.apply_sorting", return_value=mock_query) as mock_sorting:
        results = get_all_orders(db, date=SAMPLE_ORDER_DATA["order_date"], offset=0, limit=100, sort_by="id", sort_order="asc")

        mock_sorting.assert_called_once_with(mock_query, Order, "id", "asc")
        db.query.assert_called_once_with(Order)
        mock_query.filter.assert_called_once_with(ANY)
        mock_query.offset.assert_called_once_with(0)
        mock_query.limit.assert_called_once_with(100)
        mock_query.all.assert_called_once()

        assert len(results) == 0


def test_update_order_found():
    db = MagicMock()
    db.query().filter().first.return_value = Order(**SAMPLE_ORDER_DATA)
    order_update_data = OrderUpdate(order_status="Shipped")
    updated_order = update_order(db, 1, order_update_data)
    assert updated_order.order_status == "Shipped"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(updated_order)


def test_update_order_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    order_update_data = OrderUpdate(order_status="Shipped")
    with pytest.raises(HTTPException) as excinfo:
        update_order(db, 99, order_update_data)
    assert excinfo.value.status_code == 404
    assert "Order not found" in str(excinfo.value.detail)


def test_update_order_integrity_error():
    db = MagicMock()
    db.query().filter().first.return_value = Order(**SAMPLE_ORDER_DATA)
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    order_update_data = OrderUpdate(order_status="Shipped")
    with pytest.raises(HTTPException) as excinfo:
        update_order(db, 1, order_update_data)
    assert excinfo.value.status_code == 400
    assert "order already exists." in str(excinfo.value.detail)
    db.rollback.assert_called_once()


def test_delete_order_found():
    db = MagicMock()
    mock_order = Order(**SAMPLE_ORDER_DATA)
    mock_inven = Inventory(**SAMPLE_INVEN_DATA)
    db.query().filter().first.side_effect = [mock_order, mock_inven]

    result = delete_order(db, 1)

    assert result == {"detail": "Order soft deleted"}
    assert mock_order.is_deleted is True
    db.commit.assert_called_once()
    db.delete.assert_not_called()


def test_delete_order_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        delete_order(db, 99)
    assert excinfo.value.status_code == 404
    assert "Order not found" in str(excinfo.value.detail)


def test_get_order_items_found():
    db = MagicMock()
    mock_items = [
        MagicMock(is_deleted=False),  # Mock an item object with is_deleted=False
        MagicMock(is_deleted=False),
    ]
    db.query().filter().first.return_value = MagicMock(items=mock_items)

    result = get_items_in_order(db, 1)

    assert len(result) == len(mock_items)
    db.query().filter().first.assert_called_once()


def test_get_order_items_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    with pytest.raises(HTTPException) as excinfo:
        get_items_in_order(db, 99)

    assert excinfo.value.status_code == 404
    assert "No items found for this order" in str(excinfo.value.detail)  # Correct casing


def test_get_packinglist_for_order_success():
    db = MagicMock()
    db.query().filter().first.return_value = Order(**SAMPLE_ORDER_DATA)

    result = get_packinglist_for_order(db, 1)

    expected_result = [{
        "Warehouse": SAMPLE_ORDER_DATA["warehouse_id"],
        "Order picker": SAMPLE_ORDER_DATA["source_id"],
        "Order date": SAMPLE_ORDER_DATA["order_date"],
        "Picked before": SAMPLE_ORDER_DATA["request_date"],
        "Shipping notes": SAMPLE_ORDER_DATA["shipping_notes"],
        "Items to be picked": SAMPLE_ORDER_DATA["items"]
    }]

    assert result == expected_result
    db.query().filter().first.assert_called_once()


def test_get_packinglist_for_order_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        get_packinglist_for_order(db, 99)

    assert excinfo.value.status_code == 404
    assert "Order not found" in str(excinfo.value.detail)
    db.query().filter().first.assert_called_once()


def test_get_packinglist_for_order_no_items():
    db = MagicMock()
    order_data_no_items = SAMPLE_ORDER_DATA.copy()
    order_data_no_items["items"] = []
    db.query().filter().first.return_value = Order(**order_data_no_items)

    with pytest.raises(HTTPException) as excinfo:
        get_packinglist_for_order(db, 1)

    assert excinfo.value.status_code == 404
    assert "No items found in the packing list" in str(excinfo.value.detail)
    db.query().filter().first.assert_called_once()
