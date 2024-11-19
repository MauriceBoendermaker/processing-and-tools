from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from CargoHubV2.app.services import shipments_service
from CargoHubV2.app.schemas import shipments_schema
from CargoHubV2.app.services.api_keys_service import validate_api_key
from CargoHubV2.app.database import get_db
from typing import Optional

router = APIRouter(
    prefix="/api/v2/shipments",
    tags=["shipments"]
)

@router.get("/", dependencies=[Depends(validate_api_key)])
def get_shipments(db: Session = Depends(get_db), id: Optional[int] = None):
    if id:
        shipment = shipments_service.get_shipment_by_id(db, id)
        if shipment is None:
            raise HTTPException(status_code=404, detail="Shipment not found")
        return shipment
    return shipments_service.get_all_shipments(db)

@router.post("/", dependencies=[Depends(validate_api_key)])
def create_shipment(shipment: shipments_schema.ShipmentCreate, db: Session = Depends(get_db)):
    return shipments_service.create_shipment(db, shipment)

@router.delete("/{id}", dependencies=[Depends(validate_api_key)])
def delete_shipment(id: int, db: Session = Depends(get_db)):
    success = shipments_service.delete_shipment(db, id)
    if success:
        return f"Shipment with id {id} deleted"
    raise HTTPException(status_code=404, detail="Shipment not found")

@router.put("/{id}", dependencies=[Depends(validate_api_key)])
def update_shipment(id: int, shipment_data: shipments_schema.ShipmentUpdate, db: Session = Depends(get_db)):
    if shipment_data:
        return shipments_service.update_shipment(db, id, shipment_data)
    raise HTTPException(status_code=400, detail="Invalid request body")
