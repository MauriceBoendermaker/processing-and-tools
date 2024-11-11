from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from CargoHubV2.app.services import location_service
from CargoHubV2.app.schemas import location_schema
from CargoHubV2.app.database import get_db
from typing import List

router = APIRouter(
    prefix="/api/v2/locations",
    tags=["locations"]
)


@router.get("/", response_model=List[location_schema.Location])
def get_all_locations(db: Session = Depends(get_db)):
    return location_service.get_all_locations(db)


@router.get("/{id}", response_model=location_schema.Location)
def get_location_by_id(id: int, db: Session = Depends(get_db)):
    location = location_service.get_location_by_id(db, id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found.")
    return location


@router.get("/warehouse/{warehouse_id}", response_model=List[location_schema.Location])
def get_locations_by_warehouse_id(warehouse_id: int, db: Session = Depends(get_db)):
    locations = location_service.get_locations_by_warehouse_id(db, warehouse_id)
    if not locations:
        raise HTTPException(status_code=404, detail="No locations found for the given warehouse ID")
    return locations


@router.post("/")
def create_location(location: location_schema.LocationCreate, db: Session = Depends(get_db)):

    db_location = location_service.create_location(db, location)
    if db_location is None:
        raise HTTPException(status_code=400, detail="Location already exists")
    return db_location


@router.put("/{id}")
def update_location(id: int, location_data: location_schema.LocationUpdate, db: Session = Depends(get_db)):
    if location_data:
        return location_service.update_location(db, id, location_data)
    raise HTTPException(status_code=400, detail="Invalid request body")


@router.delete("/{id}")
def delete_location(id: int, db: Session = Depends(get_db)):
    success = location_service.delete_location(db, id)
    if success:
        return f"Location with id {id} deleted"
    raise HTTPException(status_code=404, detail="Location not found.")
