from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from ..schemas.docks_schema import DockCreate, DockUpdate, DockResponse
from ..services.docks_service import (
    create_dock,
    get_all_docks,
    get_dock_by_id,
    update_dock,
    delete_dock
)
from ..services.api_keys_service import validate_api_key

router = APIRouter(
    prefix="/api/v2/docks",
    tags=["docks"]
)

@router.post("/", response_model=DockResponse)
def create_dock_endpoint(
    dock_data: DockCreate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("create", api_key, db)
    return create_dock(db, dock_data)

@router.get("/", response_model=List[DockResponse])
def get_all_docks_endpoint(
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("view", api_key, db)
    return get_all_docks(db, offset, limit)

@router.get("/{dock_id}", response_model=DockResponse)
def get_dock_by_id_endpoint(
    dock_id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("view", api_key, db)
    return get_dock_by_id(db, dock_id)

@router.put("/{dock_id}", response_model=DockResponse)
def update_dock_endpoint(
    dock_id: int,
    dock_data: DockUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("edit", api_key, db)
    return update_dock(db, dock_id, dock_data)

@router.delete("/{dock_id}")
def delete_dock_endpoint(
    dock_id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("delete", api_key, db)
    return delete_dock(db, dock_id)
