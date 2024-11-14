from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from CargoHubV2.app.services import locations_service
from CargoHubV2.app.schemas import locations_schema
from CargoHubV2.app.database import get_db
from typing import List


router = APIRouter(
    prefix="/api/v2/locations",
    tags=["locations"]
)


@router.get("/", response_model=List[locations_schema.Location])
def get_all_locations(db: Session = Depends(get_db)):
    return locations_service.get_all_locations(db)


@router.get("/{id}", response_model=locations_schema.Location)
def get_location_by_id(id: int, db: Session = Depends(get_db)):
    location = locations_service.get_location_by_id(db, id)
    if not location:
        raise HTTPException(status_code=404, detail="Location id not found")
    return location


@router.get("/warehouse/{warehouse_id}", response_model=List[locations_schema.Location])
def get_locations_by_warehouse_id(warehouse_id: int, db: Session = Depends(get_db)):
    locations = locations_service.get_locations_by_warehouse_id(db, warehouse_id)
    if not locations:
        raise HTTPException(status_code=404, detail="Location warehouse not found")
    return locations


@router.post("/")
def create_location(location: locations_schema.LocationCreate, db: Session = Depends(get_db)):
    db_location = locations_service.create_location(db, location)
    return db_location


@router.put("/{id}")
def update_location(id: int, location_data: locations_schema.LocationUpdate, db: Session = Depends(get_db)):
    updated_location = locations_service.update_location(db, id, location_data)
    return updated_location


@router.delete("/{id}")
def delete_location(id: int, db: Session = Depends(get_db)):
    result = locations_service.delete_location(db, id)
    if result:
        return {"detail": "Location deleted"}
    raise HTTPException(status_code=404, detail="Location not found.")
