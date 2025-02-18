from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
from datetime import datetime
from ..models.docks_model import Dock
from ..schemas.docks_schema import DockCreate, DockUpdate
from CargoHubV2.app.services.sorting_service import apply_sorting  # Import sorting helper function


def create_dock(db: Session, dock_data: DockCreate):    
    """
    Create a new dock in the database.
    """
    dock = Dock(
        warehouse_id=dock_data.warehouse_id,
        code=dock_data.code,
        status=dock_data.status,
        description=dock_data.description,  # Add this line
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
    offset: int = 0, 
    limit: int = 100, 
    sort_by: str = "id", 
    order: str = "asc"
):
    try:
        query = db.query(Dock).filter(Dock.is_deleted == False)  # Filter out deleted docks
        query = apply_sorting(query, Dock, sort_by, order)
        return query.offset(offset).limit(limit).all()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving docks: {str(e)}"
        )



def get_docks_by_warehouse_id(
    db: Session, 
    warehouse_id: int, 
    offset: int = 0, 
    limit: int = 100, 
    sort_by: str = "id", 
    order: str = "asc"
):
    """
    Retrieve docks for a specific warehouse with sorting and pagination.
    """
    try:
        # Base query for docks filtered by warehouse
        query = db.query(Dock).filter(Dock.warehouse_id == warehouse_id, Dock.is_deleted == False)
        query = apply_sorting(query, Dock, sort_by, order)  # Apply sorting using the sorting_service
        docks = query.offset(offset).limit(limit).all()  # Paginate results

        if not docks:
            raise HTTPException(status_code=404, detail="No docks found for the given warehouse.")
        return docks
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving docks: {str(e)}"
        )


def get_dock_by_code(db: Session, code: str):
    """
    Retrieve a single dock by its ID.
    """
    return db.query(Dock).filter(Dock.code == code, Dock.is_deleted == False).first()


def update_dock(db: Session, dock_id: int, dock_data: DockUpdate):
    """
    Update an existing dock by its ID with the provided fields.
    """
    dock = db.query(Dock).filter(Dock.id == dock_id).first()
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
    Soft delete a dock by setting is_deleted to True.
    """
    dock = db.query(Dock).filter(Dock.id == dock_id).first()
    if not dock:
        raise HTTPException(status_code=404, detail="Dock not found")
    
    dock.is_deleted = True  # Soft delete flag
    dock.updated_at = datetime.now()  # Update timestamp
    
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the dock."
        )
    return {"detail": "Dock deleted"}
