from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.schemas.item_groups_schema import ItemGroupCreate, ItemGroupUpdate, ItemGroupResponse
from CargoHubV2.app.services.item_groups_service import create_item_group, get_item_group, get_all_item_groups, update_item_group, delete_item_group
from CargoHubV2.app.services.api_keys_service import validate_api_key
from typing import Optional, List


router = APIRouter(
    prefix="/api/v2/item-groups",
    tags=["item_groups"]
)


@router.post("/", response_model=ItemGroupResponse)
def create_item_group_endpoint(
    item_group_data: ItemGroupCreate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),  # API key required
):
    validate_api_key("create", api_key, db)
    item_group = create_item_group(db, item_group_data.model_dump())
    return item_group


@router.get("/", response_model=List[ItemGroupResponse])
def get_item_groups(
    id: Optional[int] = None,
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    api_key: str = Header(...),  # API key required
):
    validate_api_key("view", api_key, db)
    if id:
        item_group = get_item_group(db, id)
        if not item_group:
            raise HTTPException(status_code=404, detail="Item group not found")
        return [item_group]  # Wrap in a list to match response model
    return get_all_item_groups(db, offset, limit)


@router.put("/{id}", response_model=ItemGroupResponse)
def update_item_group_endpoint(
    id: int,
    item_group_data: ItemGroupUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),  # API key required
):
    validate_api_key("edit", api_key, db)
    item_group = update_item_group(db, id, item_group_data)
    if not item_group:
        raise HTTPException(status_code=404, detail="Item group not found")
    return item_group


@router.delete("/{id}")
def delete_item_group_endpoint(
    id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),  # API key required
):
    validate_api_key("delete", api_key, db)
    item_group = delete_item_group(db, id)
    if not item_group:
        raise HTTPException(status_code=404, detail="Item group not found")
    return {"detail": "Item group deleted"}
