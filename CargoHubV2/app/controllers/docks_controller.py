from fastapi import APIRouter, HTTPException, Depends, Header, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..services.docks_service import (
    create_dock,
    get_all_docks,
    get_dock_by_id,
    update_dock,
    delete_dock,
)
from ..schemas.docks_schema import DockCreate, DockUpdate
from ..database import get_db

router = APIRouter(
    prefix="/api/v2/docks",
    tags=["docks"]
)

@router.get("/")
def get_docks(
    db: Session = Depends(get_db),
    dock_id: Optional[int] = None,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    sort_by: str = Query(..., description="The field to sort by (e.g., 'id', 'code')."),
    order: str = Query(..., description="The order: 'asc' or 'desc'."),
    api_key: str = Header(...)
):
    """
    Retrieve docks. If `dock_id` is supplied, return that one dock; otherwise return all.
    Must also supply `sort_by` and `order`.
    """
    if dock_id is not None:
        return get_dock_by_id(db, dock_id)
    return get_all_docks(db, offset=offset, limit=limit, sort_by=sort_by, order=order)

@router.post("/")
def create_dock_endpoint(
    dock: DockCreate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    """
    Create a new dock. The 'id' is auto-incremented by the database.
    """
    return create_dock(db, dock)

@router.put("/{dock_id}")
def update_dock_endpoint(
    dock_id: int,
    dock_data: DockUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    """
    Update a dock by its auto-incremented 'id'.
    """
    return update_dock(db, dock_id, dock_data)

@router.delete("/{dock_id}")
def delete_dock_endpoint(
    dock_id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    """
    Soft delete a dock by setting 'is_deleted' to True.
    """
    return delete_dock(db, dock_id)
