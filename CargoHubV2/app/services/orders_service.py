from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from CargoHubV2.app.models.orders_model import Order
from CargoHubV2.app.services.sorting_service import apply_sorting
from CargoHubV2.app.schemas.orders_schema import OrderUpdate
from fastapi import HTTPException, status
from datetime import datetime
from typing import Optional



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


def get_all_orders(
    db: Session,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc"
):
    try:
        query = db.query(Order)
        if sort_by:
            query = apply_sorting(query, Order, sort_by, order)
        return query.offset(offset).limit(limit).all()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving orders."
        )


def get_packinglist_for_order(db: Session, order_id: int):
    # Fetch the order and directly access its packing list
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Assuming the packing list is a list of dictionaries or objects stored within the order
    source_id = order.source_id
    packing_list = order.items
    shipping_notes = order.shipping_notes
    order_date = order.order_date
    request_date = order.request_date
    warehouse_id =  order.warehouse_id
    
    packing_list_id = [
            {
                "Warehouse":warehouse_id,
                "Order picker":source_id,
                "Order date":order_date,
                "Picked before":request_date,
                "Shipping notes":shipping_notes,
                "Items to be picked": packing_list
            }
            ]

    if not packing_list:
        raise HTTPException(status_code=404, detail="No items found in the packing list")

    return packing_list_id
    

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
        raise HTTPException(status_code=404, detail="no items found for this order")
    return order.items
