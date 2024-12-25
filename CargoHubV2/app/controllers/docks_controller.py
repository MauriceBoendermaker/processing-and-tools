from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional
from fastapi.responses import JSONResponse

# Service functions
from ..services.docks_service import (
    create_dock,
    get_all_docks,
    get_dock_by_code,
    get_dock_by_id,
    update_dock,
    delete_dock
)

# Schemas
from ..schemas.docks_schema import DockCreate, DockUpdate

# Database dependency
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
    sort_by: str = "id",
    order: str = "asc",
    api_key: str = Header(...),
):
    """
    GET /api/v2/docks/
    - If 'code' query param is provided, return that specific dock by code (if found).
    - Otherwise, return a paginated, optionally sorted list of all docks.
    """
    if code:
        dock = get_dock_by_code(db, code)
        if dock is None:
            raise HTTPException(status_code=404, detail="Dock not found")
        return dock

    # Retrieve all docks, sorted and paginated
    docks = get_all_docks(
        db, 
        offset=offset, 
        limit=limit, 
        sort_by=sort_by, 
        order=order
    )
    return docks


@router.get("/{dock_id}")
def get_dock_by_id_endpoint(
    dock_id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    """
    GET /api/v2/docks/{dock_id}
    - Retrieve a single dock by its auto-incremented 'id'.
    """
    dock = get_dock_by_id(db, dock_id)
    if dock is None:
        raise HTTPException(status_code=404, detail="Dock not found")
    return dock


@router.post("/")
def create_dock_endpoint(
    dock: DockCreate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    """
    POST /api/v2/docks/
    - Create a new dock. 
    - Returns the created dock (including its auto-incremented 'id').
    """
    db_dock = create_dock(db, dock)
    if db_dock is None:
        raise HTTPException(status_code=400, detail="Dock already exists")

    # Ideally return 201 Created for a newly created resource:
    return JSONResponse(status_code=201, content=db_dock.__dict__)


@router.put("/{dock_id}")
def update_dock_endpoint(
    dock_id: int,
    dock_data: DockUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    """
    PUT /api/v2/docks/{dock_id}
    - Update an existing dock's fields, identified by 'dock_id'.
    """
    if not dock_data:
        raise HTTPException(status_code=400, detail="Invalid request body")

    updated = update_dock(db, dock_id, dock_data)
    return updated  # Returns 200 by default


@router.delete("/{dock_id}")
def delete_dock_endpoint(
    dock_id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    """
    DELETE /api/v2/docks/{dock_id}
    - Soft-delete a dock by setting is_deleted = True.
    """
    success = delete_dock(db, dock_id)
    # success can be a dict or a boolean depending on your service's return
    if success:
        return f"Dock with ID {dock_id} deleted"
    raise HTTPException(status_code=404, detail="Dock not found")
