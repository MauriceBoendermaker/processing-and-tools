from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
from datetime import datetime
from CargoHubV2.app.models.docks_model import Dock
from CargoHubV2.app.schemas.docks_schema import DockCreate, DockUpdate, DockResponse
from CargoHubV2.app.services.sorting_service import apply_sorting  # Import sorting helper function

def get_all_docks(
    db: Session,
    offset: int = 0,
    limit: int = 100,
    sort_by: str = "id",
    order: str = "asc"
):
    """
    Retrieve all docks with optional sorting and pagination.
    """
    try:
        query = db.query(Dock).filter(Dock.is_deleted == False)
        query = apply_sorting(query, Dock, sort_by, order)
        return query.offset(offset).limit(limit).all()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving docks."
        )

def get_dock_by_id(db: Session, dock_id: int):
    """
    Retrieve a dock by its ID.
    """
    try:
        dock = db.query(Dock).filter(Dock.id == dock_id, Dock.is_deleted == False).first()
        if not dock:
            raise HTTPException(status_code=404, detail="Dock not found")
        return dock
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the dock."
        )

def create_dock(db: Session, dock_data: DockCreate):
    """
    Create a new dock.
    """
    db_dock = Dock(
        warehouse_id=dock_data.warehouse_id,
        code=dock_data.code,
        status=dock_data.status,
        description=dock_data.description,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(db_dock)

    try:
        db.commit()
        db.refresh(db_dock)
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

def update_dock(db: Session, dock_id: int, dock_data: DockUpdate):
    """
    Update an existing dock.
    """
    dock = db.query(Dock).filter(Dock.id == dock_id, Dock.is_deleted == False).first()
    if not dock:
        raise HTTPException(status_code=404, detail="Dock not found")
    
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
    Soft delete a dock.
    """
    dock = db.query(Dock).filter(Dock.id == dock_id, Dock.is_deleted == False).first()
    if not dock:
        raise HTTPException(status_code=404, detail="Dock not found")

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
    return {"detail": f"Dock with ID {dock_id} soft deleted"}
