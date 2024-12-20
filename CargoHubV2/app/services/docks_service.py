from sqlalchemy.orm import Session
from CargoHubV2.app.models.docks_model import Dock
from CargoHubV2.app.schemas.docks_schema import DockCreate, DockResponse
from CargoHubV2.app.services.sorting_service import apply_sorting
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime
from typing import Optional

def get_all_docks(
    db: Session,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc"
):
    try:
        query = db.query(Dock)
        if sort_by:
            query = apply_sorting(query, Dock, sort_by, order)
        return query.offset(offset).limit(limit).all()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving docks."
        )

def get_dock_by_code(db: Session, code: str):
    try:
        dock = db.query(Dock).filter(Dock.code == code).first()
        if not dock:
            raise HTTPException(status_code=404, detail="Dock not found")
        return dock
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving this dock."
        )

def create_dock(db: Session, dock: dict):
    db_dock = Dock(**dock)
    db.add(db_dock)

    try:
        db.commit()
        db.refresh(db_dock)  # Refresh to get generated fields (e.g., ID)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A dock with this code already exists."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the dock."
        )
    return db_dock

def delete_dock(db: Session, code: str):
    to_del = db.query(Dock).filter(Dock.code == code).first()
    if not to_del:
        raise HTTPException(status_code=404, detail="Dock not found")

    try:
        db.delete(to_del)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the dock."
        )
    return True

def update_dock(db: Session, code: str, dock_data: dict) -> DockResponse:
    try:
        to_update = db.query(Dock).filter(Dock.code == code).first()
        if not to_update:
            raise HTTPException(status_code=404, detail="Dock not found")

        for key, value in dock_data.items():
            setattr(to_update, key, value)
        to_update.updated_at = datetime.now()
        db.commit()
        db.refresh(to_update)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The code provided already exists."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the dock."
        )
    return DockResponse.model_validate(to_update)
