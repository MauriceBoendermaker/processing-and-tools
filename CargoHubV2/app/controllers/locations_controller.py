from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.services import locations_service
from CargoHubV2.app.schemas import locations_schema
from CargoHubV2.app.database import get_db
from typing import Optional
from typing import List

from CargoHubV2.app.dependencies.api_dependencies import (
    get_valid_api_key,
    role_required
)
from CargoHubV2.app.models.api_key_model import APIKey

router = APIRouter(
    prefix="/api/v2/locations",
    tags=["locations"]
)


@router.get("/", response_model=List[locations_schema.Location])
def get_all_locations(
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc",
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    return locations_service.get_all_locations(db, offset=offset, limit=limit, sort_by=sort_by, order=order)


@router.get("/{id}", response_model=locations_schema.Location)
def get_location_by_id(id: int, db: Session = Depends(get_db), api_key: str = Header(...)):
    location = locations_service.get_location_by_id(db, id)
    if not location:
        raise HTTPException(status_code=404, detail="Location id not found")
    return location


@router.get("/warehouse/{warehouse_id}", response_model=List[locations_schema.Location])
def get_locations_by_warehouse_id(
    warehouse_id: int,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc",
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    return locations_service.get_locations_by_warehouse_id(db, warehouse_id, offset=offset, limit=limit, sort_by=sort_by, order=order)


@router.post("/")
def create_location(location: locations_schema.LocationCreate, db: Session = Depends(get_db), api_key: str = Header(...)):
    db_location = locations_service.create_location(db, location)
    return db_location


@router.put("/{id}")
def update_location(id: int, location_data: locations_schema.LocationUpdate, db: Session = Depends(get_db), api_key: str = Header(...)):
    updated_location = locations_service.update_location(db, id, location_data)
    return updated_location


@router.delete("/{id}")
def delete_location(id: int, db: Session = Depends(get_db), api_key: str = Header(...)):
    result = locations_service.delete_location(db, id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Location not found.")
