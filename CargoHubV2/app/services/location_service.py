from sqlalchemy.orm import Session
from CargoHubV2.app.models.location_model import Location
from CargoHubV2.app.schemas.location_schema import LocationCreate, LocationUpdate
from datetime import datetime
from fastapi import HTTPException


def get_all_locations(db: Session):
    return db.query(Location).all()


def get_location_by_id(db: Session, id: int):
    return db.query(Location).filter(Location.id == id).first()

def get_locations_by_warehouse_id(db: Session, warehouse_id: int):
    return db.query(Location).filter(Location.warehouse_id == warehouse_id).all()


def create_location(db: Session, location: LocationCreate):
    db_location = Location(
        warehouse_id = location.warehouse_id,
        code = location.code,
        name = location.name,
        created_at = datetime.now(),
        updated_at = datetime.now()
    )

    db.add(db_location)
    db.commit()
    db.refresh(db_location)

    return db_location


def delete_location(db: Session, id: int) -> bool:
    to_delete = db.query(Location).filter(Location.id == id).first()
    if not to_delete:
        return False
    
    db.delete(to_delete)
    db.commit()
    
    return True

def update_location(db: Session, id: int, location_data: LocationUpdate) -> Location:
    to_update = db.query(Location).filter(Location.id == id).first()
    if not to_update:
        raise HTTPException(status_code=404, detail="Location not found")

    for key, value in location_data.model_dump(exclude_unset=True).items():
        setattr(to_update, key, value)

    db.commit()
    db.refresh(to_update)

    return to_update