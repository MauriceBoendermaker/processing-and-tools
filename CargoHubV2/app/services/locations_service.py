from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from CargoHubV2.app.models.locations_model import Location
from CargoHubV2.app.services.sorting_service import apply_sorting

from CargoHubV2.app.schemas.locations_schema import LocationCreate, LocationUpdate
from datetime import datetime
from fastapi import HTTPException, status
from typing import Optional



def get_all_locations(
    db: Session,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc"
):
    try:
        query = db.query(Location).filter(Location.is_deleted == False)
        if sort_by:
            query = apply_sorting(query, Location, sort_by, order)
        return query.offset(offset).limit(limit).all()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving locations."
        )


def get_location_by_id(db: Session, id: int):
    location = db.query(Location).filter(Location.id == id, Location.is_deleted == False).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location id not found")
    return location


def get_locations_by_warehouse_id(
    db: Session,
    warehouse_id: int,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc"
):
    try:
        query = db.query(Location).filter(Location.warehouse_id == warehouse_id, Location.is_deleted == False)
        if sort_by:
            query = apply_sorting(query, Location, sort_by, order)
        locations = query.offset(offset).limit(limit).all()
        if len(locations) == 0:
            raise HTTPException(status_code=404, detail="Location warehouse not found")
        return locations
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving locations."
        )



def create_location(db: Session, location_data: LocationCreate):
    location = Location(
        warehouse_id=location_data.warehouse_id,
        code=location_data.code,
        name=location_data.name,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(location)
    try:
        db.commit()
        db.refresh(location)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A location with this code already exists."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the location."
        )
    return location


def delete_location(db: Session, id: str) -> dict:
    location_to_delete = db.query(Location).filter(Location.id == id, Location.is_deleted == False).first()
    if not location_to_delete:
        raise HTTPException(status_code=404, detail="Location not found")
    
    location_to_delete.is_deleted = True  # Soft delete by updating the flag
    db.commit()
    return {"detail": "Location soft deleted"}



def update_location(db: Session, id: int, location_data: LocationUpdate) -> Location:
    to_update = db.query(Location).filter(Location.id == id).first()
    if not to_update:
        raise HTTPException(status_code=404, detail="Location not found")
    for key, value in location_data.model_dump(exclude_unset=True).items():
        setattr(to_update, key, value)
    try:
        db.commit()
        db.refresh(to_update)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="An integrity error occurred while updating the location.")
    return to_update
