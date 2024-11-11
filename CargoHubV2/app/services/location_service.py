from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from CargoHubV2.app.models.location_model import Location
from CargoHubV2.app.schemas.location_schema import LocationCreate, LocationUpdate
from datetime import datetime
from fastapi import HTTPException, status


def get_all_locations(db: Session):
    return db.query(Location).all()


def get_location_by_id(db: Session, id: int):
    location = db.query(Location).filter(Location.id == id).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location id not found")
    return location


def get_locations_by_warehouse_id(db: Session, warehouse_id: int):
    locations = db.query(Location).filter(Location.warehouse_id == warehouse_id).all()
    if not locations:  # If no locations are found
        raise HTTPException(status_code=404, detail="Location warehouse not found")
    return locations


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
        db.rollback()  # Roll back the session if there's a conflict
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
    location_to_delete = db.query(Location).filter(Location.id == id).first()
    if not location_to_delete:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(location_to_delete)
    db.commit()
    return {"detail": "location deleted"}


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
