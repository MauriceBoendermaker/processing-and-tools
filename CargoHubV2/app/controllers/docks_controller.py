from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional
from ..services.docks_service import (
    create_dock,
    get_all_docks,
    get_dock_by_code,
    update_dock,
    delete_dock
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
    code: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc",
    api_key: str = Header(...),
):
    if code:
        dock = get_dock_by_code(db, code)
        if dock is None:
            raise HTTPException(status_code=404, detail="Dock not found")
        return dock
    return get_all_docks(db, offset=offset, limit=limit)


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

    success = delete_dock(db, dock_id)
    if success:
        return f"Dock with ID {dock_id} deleted"
    raise HTTPException(status_code=404, detail="Dock not found")


@router.put("/{dock_id}")
def update_dock_endpoint(
    dock_id: int,
    dock_data: DockUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...)):

    if dock_data:
        return update_dock(db, dock_id, dock_data)
    raise HTTPException(status_code=400, detail="Invalid request body")
