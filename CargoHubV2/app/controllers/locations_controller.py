from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.services import locations_service
from CargoHubV2.app.schemas import locations_schema
from CargoHubV2.app.database import get_db
from CargoHubV2.app.services.api_keys_service import validate_api_key
from typing import Optional
from typing import List


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
    validate_api_key("view", api_key, db)
    return locations_service.get_all_locations(db, offset=offset, limit=limit, sort_by=sort_by, order=order)


@router.get("/{id}", response_model=locations_schema.Location)
def get_location_by_id(id: int, db: Session = Depends(get_db), api_key: str = Header(...)):
    validate_api_key("view", api_key, db)
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
    validate_api_key("view", api_key, db)
    return locations_service.get_locations_by_warehouse_id(db, warehouse_id, offset=offset, limit=limit, sort_by=sort_by, order=order)


@router.post("/")
def create_location(location: locations_schema.LocationCreate, db: Session = Depends(get_db), api_key: str = Header(...)):
    validate_api_key("create", api_key, db)
    db_location = locations_service.create_location(db, location)
    return db_location


@router.put("/{id}")
def update_location(id: int, location_data: locations_schema.LocationUpdate, db: Session = Depends(get_db), api_key: str = Header(...)):
    validate_api_key("edit", api_key, db)
    updated_location = locations_service.update_location(db, id, location_data)
    return updated_location


@router.delete("/{id}")
def delete_location(id: int, db: Session = Depends(get_db), api_key: str = Header(...)):
    validate_api_key("delete", api_key, db)
    result = locations_service.delete_location(db, id)
    if result:
        return {"detail": "Location deleted"}
    raise HTTPException(status_code=404, detail="Location not found.")
