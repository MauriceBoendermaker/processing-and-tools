from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional
from ..services.docks_service import (
    create_dock,
    get_all_docks,
    get_dock_by_code,
    get_dock_by_id,
    update_dock,
    delete_dock
)
from ..schemas.docks_schema import DockCreate, DockUpdate
from ..models.docks_model import Dock
from ..database import get_db

router = APIRouter(
    prefix="/api/v2/docks",
    tags=["docks"]
)


@router.get("/")
def get_docks(
    db: Session = Depends(get_db),
    code: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",  # Default sorting column is `id`
    order: Optional[str] = "asc",  # Default sorting order is `asc`
    api_key: str = Header(...),
):
    """
    Retrieve docks with optional filtering by code, pagination, and sorting.
    """
    # If `code` is provided, retrieve a single dock by code
    if code:
        dock = get_dock_by_code(db, code)
        if dock is None:
            raise HTTPException(status_code=404, detail="Dock not found")
        return dock

    # Otherwise, retrieve all docks with sorting and pagination
    return get_all_docks(db, offset=offset, limit=limit, sort_by=sort_by, order=order)


@router.get("/{dock_id}")
def get_dock_by_id_endpoint(dock_id: int, db: Session = Depends(get_db), api_key: str = Header(...)):
    """
    Retrieve a specific dock by its ID.
    """
    return get_dock_by_id(db, dock_id)


@router.post("/")
def create_dock_endpoint(dock: DockCreate, db: Session = Depends(get_db), api_key: str = Header(...)):
    db_dock = create_dock(db, dock)

    if db_dock is None:
        raise HTTPException(status_code=400, detail="Dock already exists")
    return db_dock


@router.delete("/{dock_id}")
def delete_dock_endpoint(
    dock_id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...)):
    """
    Soft delete a dock by its ID.
    """
    success = delete_dock(db, dock_id)
    if success:
        return {"detail": f"Dock with ID {dock_id} deleted"}
    raise HTTPException(status_code=404, detail="Dock not found")


@router.put("/{dock_id}")
def update_dock_endpoint(
    dock_id: int,
    dock_data: DockUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...)):
    """
    Update a specific dock by its ID.
    """
    if dock_data:
        return update_dock(db, dock_id, dock_data)
    raise HTTPException(status_code=400, detail="Invalid request body")
