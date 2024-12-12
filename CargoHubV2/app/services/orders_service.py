from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from CargoHubV2.app.models.orders_model import Order
from CargoHubV2.app.models.shipments_model import Shipment
from CargoHubV2.app.schemas.orders_schema import OrderUpdate, OrderShipmentUpdate
from fastapi import HTTPException, status
from datetime import datetime
from typing import List


def create_order(db: Session, order_data: dict):
    order = Order(**order_data)
    db.add(order)
    try:
        db.commit()
        db.refresh(order)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An order with this reference already exists."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the order."
        )
    return order


def get_order(db: Session, id: int):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def get_all_orders(db: Session):
    return db.query(Order).all()


def update_order(db: Session, id: int, order_data: OrderUpdate):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    update_data = order_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(order, key, value)
    order.updated_at = datetime.utcnow()
    try:
        db.commit()
        db.refresh(order)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="order already exists.")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the order."
        )
    return order


def delete_order(db: Session, id: int):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    try:
        db.delete(order)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the order."
        )
    return {"detail": "Order deleted"}


def get_items_in_order(db: Session, id: int):
    order = db.query(Order).filter(Order.id == id).first()
    if not order or not order.items:
        raise HTTPException(
            status_code=404, detail="no items found for this order")
    return order.items


def get_packinglist_for_order(db: Session, order_id: int):
    # Fetch the order and directly access its packing list
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    source_id = order.source_id
    packing_list = order.items
    shipping_notes = order.shipping_notes
    order_date = order.order_date
    request_date = order.request_date
    warehouse_id = order.warehouse_id

    packing_list_id = [
        {
            "Warehouse": warehouse_id,
            "Order picker": source_id,
            "Order date": order_date,
            "Picked before": request_date,
            "Shipping notes": shipping_notes,
            "Items to be picked": packing_list
        }
    ]

    if not packing_list:
        raise HTTPException(
            status_code=404, detail="No items found in the packing list")

    return packing_list_id


def get_shipments_by_order_ids(db: Session, order_ids: List[int]):
    # Check if order_ids is a single ID, convert it to a list for consistency
    if not isinstance(order_ids, list):
        order_ids = [order_ids]

    shipments = db.query(Shipment).filter(
        Shipment.order_id.in_(order_ids)).all()

    if not shipments:
        raise HTTPException(
            status_code=404, detail="No Shipment found for the given orders"
        )
    return shipments


def update_shipments_in_order(db: Session, order_id: int, order_data: OrderShipmentUpdate):
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="No Order found")
        update_data = order_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(order, key, value)
            order.updated_at = datetime.now()
            db.commit()
            db.refresh(order)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="An integrity error occurred while updating the order.")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="An error occurred while updating the order.")
    return order
