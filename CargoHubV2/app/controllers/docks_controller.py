from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.services import docks_service
from CargoHubV2.app.schemas import docks_schema
from CargoHubV2.app.database import get_db
from CargoHubV2.app.services.api_keys_service import validate_api_key
from typing import Optional

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
    validate_api_key("view", api_key, db)
    if code:
        dock = docks_service.get_dock_by_code(db, code)
        if dock is None:
            raise HTTPException(status_code=404, detail="Dock not found")
        return dock
    return docks_service.get_all_docks(db, offset=offset, limit=limit, sort_by=sort_by, order=order)

@router.post("/")
def create_dock(dock: docks_schema.DockCreate, db: Session = Depends(get_db), api_key: str = Header(...)):
    validate_api_key("create", api_key, db)
    db_dock = docks_service.create_dock(db, dock.model_dump())
    if db_dock is None:
        raise HTTPException(status_code=400, detail="Dock already exists")
    return db_dock

@router.delete("/{code}")
def delete_dock(
    code: str, db: Session = Depends(get_db), api_key: str = Header(...)):

    validate_api_key("delete", api_key, db)
    success = docks_service.delete_dock(db, code)
    if success:
        return f"Dock with code {code} deleted"
    raise HTTPException(status_code=404, detail="Dock not found")

@router.put("/{code}")
def update_dock(
    code: str,
    dock_data: docks_schema.DockUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...)):

    validate_api_key("edit", api_key, db)
    if dock_data:
        return docks_service.update_dock(db, code, dock_data.model_dump(exclude_unset=True))
    raise HTTPException(status_code=400, detail="Invalid request body")