from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.schemas.item_lines_schema import ItemLineCreate, ItemLineUpdate, ItemLineResponse
from CargoHubV2.app.services.item_lines_service import create_item_line, get_item_line, get_all_item_lines, update_item_line, delete_item_line
from typing import Optional, List

from CargoHubV2.app.dependencies.api_dependencies import (
    get_valid_api_key,
    role_required
)
from CargoHubV2.app.models.api_key_model import APIKey


router = APIRouter(
    prefix="/api/v2/item_lines",
    tags=["item_lines"]
)


@router.post("/", response_model=ItemLineResponse)
def create_item_line_endpoint(
    item_line_data: ItemLineCreate,
    db: Session = Depends(get_db),
    current_api_key: APIKey = Depends(role_required(["Manager", "FloorManager"]))
):
    item_line = create_item_line(db, item_line_data.model_dump())
    return item_line


@router.get("/")
def get_item_lines(
    id: Optional[int] = None,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",  
    order: Optional[str] = "asc",  
    db: Session = Depends(get_db),
    current_api_key: APIKey = Depends(role_required(["Manager", "FloorManager", "Worker"])),
):
    if id:
        item_line = get_item_line(db, id)
        if not item_line:
            raise HTTPException(status_code=404, detail="Item line not found")
        return item_line
    return get_all_item_lines(db, offset, limit, sort_by, order)


@router.put("/{id}")
def update_item_line_endpoint(
    id: int,
    item_line_data: ItemLineUpdate,
    db: Session = Depends(get_db),
    current_api_key: APIKey = Depends(role_required(["Manager", "FloorManager"]))
):
    item_line = update_item_line(db, id, item_line_data)
    if not item_line:
        raise HTTPException(status_code=404, detail="Item line not found")
    return item_line


@router.delete("/{id}")
def delete_item_line_endpoint(
    id: int,
    db: Session = Depends(get_db),
    current_api_key: APIKey = Depends(role_required(["Manager"]))
):
    item_line = delete_item_line(db, id)
    if not item_line:
        raise HTTPException(status_code=404, detail="Item line not found")
    return {"detail": "Item line deleted"}
