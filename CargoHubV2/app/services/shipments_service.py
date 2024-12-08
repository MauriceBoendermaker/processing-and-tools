from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from CargoHubV2.app.models.shipments_model import Shipment
from CargoHubV2.app.models.orders_model import Order
from CargoHubV2.app.services.sorting_service import apply_sorting
from CargoHubV2.app.schemas.shipments_schema import ShipmentCreate, ShipmentUpdate
from fastapi import HTTPException, status
from datetime import datetime
from typing import Optional


def create_shipment(db: Session, shipment_data: dict):
    shipment = Shipment(**shipment_data)
    db.add(shipment)
    try:
        db.commit()
        db.refresh(shipment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A shipment with this ID already exists."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the shipment."
        )
    return shipment


def get_shipment(db: Session, shipment_id: int):
    try:
        shipment = db.query(Shipment).filter(
            Shipment.id == shipment_id).first()
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        return shipment
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the shipment."
        )


def get_all_shipments(
    db: Session,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc"
):
    try:
        query = db.query(Shipment)
        if sort_by:
            query = apply_sorting(query, Shipment, sort_by, order)
        return query.offset(offset).limit(limit).all()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving shipments."
        )


def update_shipment(db: Session, shipment_id: int, shipment_data: ShipmentUpdate):
    try:
        shipment = db.query(Shipment).filter(
            Shipment.id == shipment_id).first()
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        update_data = shipment_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(shipment, key, value)
        shipment.updated_at = datetime.now()
        db.commit()
        db.refresh(shipment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An integrity error occurred while updating the shipment."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the shipment."
        )
    return shipment


def delete_shipment(db: Session, shipment_id: int):
    try:
        shipment = db.query(Shipment).filter(
            Shipment.id == shipment_id).first()
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        db.delete(shipment)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the shipment."
        )
    return {"detail": "Shipment deleted"}


def get_orders_by_shipment_id(db: Session, shipment_id:int):
    orders = db.query(Order).filter(Order.shipment_id == shipment_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders
