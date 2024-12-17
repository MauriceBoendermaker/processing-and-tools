from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.schemas.shipments_schema import *
from CargoHubV2.app.services.shipments_service import *
from typing import Optional, List

router = APIRouter(
    prefix="/api/v2/shipments",
    tags=["shipments"]
)


@router.post("/", response_model=ShipmentResponse)
def create_shipment_endpoint(
    shipment_data: ShipmentCreate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    shipment = create_shipment(db, shipment_data.model_dump())
    return shipment


@router.get("/")
def get_shipments(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    if id:
        shipment = get_shipment(db, id)
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        return shipment
    return get_all_shipments(db)


@router.put("/{id}", response_model=ShipmentResponse)
def update_shipment_endpoint(
    id: int,
    shipment_data: ShipmentUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    shipment = update_shipment(db, id, shipment_data)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment


@router.delete("/{id}")
def delete_shipment_endpoint(
    id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    shipment = delete_shipment(db, id)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment


@router.get("/{shipment_id}/orders")
def get_orders_linked_with_shipment(
    shipment_id:int,
    db:Session = Depends(get_db),
    api_key:str = Header(...)
):
    order = get_orders_by_shipment_id(db, shipment_id)
    if not order:
        raise HTTPException(status_code=404, detail="No orders found")
    return order


@router.put("/{shipment_id}/orders")
def update_orders_linked_with_shipment(
    shipment_id: int,
    shipment_data: ShipmentOrderUpdate,
    db: Session = Depends(get_db),
    api_key:str = Header(...)
):
    shipment = update_orders_in_shipment(db, shipment_id, shipment_data)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment
