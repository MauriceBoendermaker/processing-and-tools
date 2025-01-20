from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional, List

from CargoHubV2.app.database import get_db
from CargoHubV2.app.schemas.item_types_schema import ItemTypeCreate, ItemTypeUpdate, ItemTypeResponse
from CargoHubV2.app.services.item_types_service import create_item_type, get_item_type, get_all_item_types, update_item_type, delete_item_type
from CargoHubV2.app.dependencies.api_dependencies import (
    get_valid_api_key,
    role_required
)
from CargoHubV2.app.models.api_key_model import APIKey

router = APIRouter(
    prefix="/api/v2/item_types",  # Use underscore (_) instead of hyphen (-)
    tags=["item_types"]
)


@router.post("/", response_model=ItemTypeResponse)
def create_item_type_endpoint(
    item_type_data: ItemTypeCreate,
    db: Session = Depends(get_db),
    current_api_key: APIKey = Depends(role_required(["Manager", "FloorManager"]))
):
    item_type = create_item_type(db, item_type_data.model_dump())
    return item_type


@router.get("/", response_model=List[ItemTypeResponse])
def get_item_types(
    id: Optional[int] = None,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc",
    db: Session = Depends(get_db),
    current_api_key: APIKey = Depends(role_required(["Manager", "FloorManager", "Worker"])),
):
    if id:
        item_type = get_item_type(db, id)
        if not item_type:
            raise HTTPException(status_code=404, detail="Item type not found")
        return [item_type]
    return get_all_item_types(db, offset, limit, sort_by, order)


@router.put("/{id}")
def update_item_type_endpoint(
    id: int,
    item_type_data: ItemTypeUpdate,
    db: Session = Depends(get_db),
    current_api_key: APIKey = Depends(role_required(["Manager", "FloorManager"]))
):
    item_type = update_item_type(db, id, item_type_data)
    if not item_type:
        raise HTTPException(status_code=404, detail="Item type not found")
    return item_type


@router.delete("/{id}")
def delete_item_type_endpoint(
    id: int,
    db: Session = Depends(get_db),
    current_api_key: APIKey = Depends(role_required(["Manager"]))
):
    item_type = delete_item_type(db, id)
    if not item_type:
        raise HTTPException(status_code=404, detail="Item type not found")
    return {"detail": "Item type deleted"}
