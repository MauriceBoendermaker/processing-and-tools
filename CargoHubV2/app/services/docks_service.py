from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
from datetime import datetime
from ..models.docks_model import Dock
from ..schemas.docks_schema import DockCreate, DockUpdate
from CargoHubV2.app.services.sorting_service import apply_sorting  # or wherever your helper is

def create_dock(db: Session, dock_data: DockCreate):
    """
    Create a new dock in the database.
    """
    dock = Dock(
        warehouse_id=dock_data.warehouse_id,
        code=dock_data.code,   # or remove if you no longer need a code
        status=dock_data.status,
        description=dock_data.description,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(dock)
    try:
        db.commit()
        db.refresh(dock)
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
    return dock

def get_all_docks(
    db: Session,
    offset: int,
    limit: int,
    sort_by: str,
    order: str
):
    """
    Retrieve all docks with user-supplied sorting and pagination.
    Users must explicitly pass in `sort_by` and `order`; no defaults here.
    """
    if not sort_by:
        raise HTTPException(status_code=400, detail="sort_by parameter is required.")
    if not order:
        raise HTTPException(status_code=400, detail="order parameter is required.")

    try:
        query = db.query(Dock).filter(Dock.is_deleted == False)
        query = apply_sorting(query, Dock, sort_by, order)
        return query.offset(offset).limit(limit).all()
    except ValueError as e:
        # For instance, apply_sorting() might raise ValueError if the sort field is invalid
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving docks."
        )

def get_dock_by_id(db: Session, dock_id: int):
    """
    Retrieve a single dock by its auto-incremented 'id'.
    """
    dock = db.query(Dock).filter(Dock.id == dock_id, Dock.is_deleted == False).first()
    if not dock:
        raise HTTPException(status_code=404, detail="Dock not found.")
    return dock

def update_dock(db: Session, dock_id: int, dock_data: DockUpdate):
    """
    Update an existing dock by its auto-incremented 'id'.
    """
    dock = db.query(Dock).filter(Dock.id == dock_id, Dock.is_deleted == False).first()
    if not dock:
        raise HTTPException(status_code=404, detail="Dock not found.")
    for key, value in dock_data.dict(exclude_unset=True).items():
        setattr(dock, key, value)
    dock.updated_at = datetime.now()
    try:
        db.commit()
        db.refresh(dock)
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
            detail="An error occurred while updating the dock."
        )
    return dock

def delete_dock(db: Session, dock_id: int):
    """
    Soft delete a dock by setting is_deleted to True.
    """
    dock = db.query(Dock).filter(Dock.id == dock_id, Dock.is_deleted == False).first()
    if not dock:
        raise HTTPException(status_code=404, detail="Dock not found.")
    dock.is_deleted = True
    dock.updated_at = datetime.now()
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the dock."
        )
    return {"detail": f"Dock with ID {dock_id} has been soft deleted."}
