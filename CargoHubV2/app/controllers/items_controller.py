from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, List

from CargoHubV2.app.database import get_db
from CargoHubV2.app.schemas.items_schema import *
from CargoHubV2.app.services.items_service import *
from CargoHubV2.app.dependencies.api_dependencies import (
    get_valid_api_key,
    role_required
)
from CargoHubV2.app.models.api_key_model import APIKey

router = APIRouter(
    prefix="/api/v2/items",
    tags=["items"]
)


@router.post("/", response_model=ItemResponse)
def create_item_endpoint(
    item_data: ItemCreate,
    db: Session = Depends(get_db),
    current_api_key: APIKey = Depends(
        role_required(["Manager", "FloorManager"]))
):
    item = create_item(db, item_data.model_dump())
    return item


@router.get("/")
def get_items(
    code: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "uid",
    order: Optional[str] = "asc",
    db: Session = Depends(get_db),
    current_api_key: APIKey = Depends(
        role_required(["Manager", "FloorManager", "Worker"])),
):
    if code:
        item = get_item(db, code)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    return get_all_items(db, offset, limit, sort_by or "id", order)


@router.put("/{code}", response_model=ItemResponse)
def update_item_endpoint(
    code: str,
    item_data: ItemUpdate,
    db: Session = Depends(get_db),
    current_api_key: APIKey = Depends(
        role_required(["Manager", "FloorManager"]))
):
    item = update_item(db, code, item_data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{code}")
def delete_item_endpoint(
    code: str,
    db: Session = Depends(get_db),
    current_api_key: APIKey = Depends(role_required(["Manager"]))
):
    item = delete_item(db, code)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item  # Returns the item with is_deleted=True
