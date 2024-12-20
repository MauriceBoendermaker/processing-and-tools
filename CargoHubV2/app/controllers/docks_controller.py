from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional
from ..services.docks_service import (
    create_dock,
    get_all_docks,
    get_dock_by_id,
    get_docks_by_warehouse_id,
    update_dock,
    delete_dock,
)
from ..models.docks_model import Dock  # Import the Dock model
from ..schemas.docks_schema import DockCreate, DockUpdate
from ..database import get_db

router = APIRouter(
    prefix="/api/v2/docks",
    tags=["docks"],
)


@router.get("/")
def get_docks(
    db: Session = Depends(get_db),
    code: Optional[str] = None,
    warehouse_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc",
    api_key: str = Header(...),
):
    """
    Retrieve all docks or filter by code or warehouse ID. Its optional can be removed.
    """
    if code:
        dock = db.query(Dock).filter(Dock.code == code, Dock.is_deleted == False).first()
        if not dock:
            raise HTTPException(status_code=404, detail="Dock not found")
        return dock

    if warehouse_id:
        return get_docks_by_warehouse_id(db, warehouse_id, offset, limit, sort_by, order)

    return get_all_docks(db, offset, limit, sort_by, order)


@router.get("/warehouse/{warehouse_id}")
def get_docks_by_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc",
    api_key: str = Header(...),
):
    """
    Retrieve all docks for a specific warehouse by its ID.
    """
    return get_docks_by_warehouse_id(db, warehouse_id, offset, limit, sort_by, order)


@router.get("/{dock_id}")
def get_dock_by_id_endpoint(
    dock_id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    """
    Retrieve a single dock by its ID.
    """
    dock = get_dock_by_id(db, dock_id)
    if not dock:
        raise HTTPException(status_code=404, detail="Dock not found")
    return dock


@router.post("/")
def create_dock_endpoint(
    dock_data: DockCreate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    """
    Create a new dock.
    """
    return create_dock(db, dock_data)


@router.put("/{dock_id}")
def update_dock_endpoint(
    dock_id: int,
    dock_data: DockUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    """
    Update an existing dock by its ID.
    """
    return update_dock(db, dock_id, dock_data)


@router.delete("/{dock_id}")
def delete_dock_endpoint(
    dock_id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    """
    Soft delete a dock by its ID.
    """
    return delete_dock(db, dock_id)
