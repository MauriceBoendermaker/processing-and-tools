from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.schemas.shipments_schema import *
from CargoHubV2.app.services.shipments_service import *
from CargoHubV2.app.services.api_keys_service import validate_api_key
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
    validate_api_key("create", api_key, db)
    shipment = create_shipment(db, shipment_data.model_dump())
    return shipment


@router.get("/", response_model=List[ShipmentResponse])
def get_shipments(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("view", api_key, db)
    if id:
        shipment = get_shipment(db, id)
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        return [shipment]
    return get_all_shipments(db)


@router.put("/{id}", response_model=ShipmentResponse)
def update_shipment_endpoint(
    id: int,
    shipment_data: ShipmentUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("edit", api_key, db)
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
    validate_api_key("delete", api_key, db)
    shipment = delete_shipment(db, id)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment
