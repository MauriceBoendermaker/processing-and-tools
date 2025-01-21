from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.schemas.item_groups_schema import ItemGroupCreate, ItemGroupUpdate, ItemGroupResponse
from CargoHubV2.app.services.item_groups_service import create_item_group, get_item_group, get_all_item_groups, update_item_group, delete_item_group
from typing import Optional, List


router = APIRouter(
    prefix="/api/v2/item_groups",
    tags=["item_groups"]
)


@router.post("/", response_model=ItemGroupResponse)
def create_item_group_endpoint(
    item_group_data: ItemGroupCreate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),  # API key required
):
    item_group = create_item_group(db, item_group_data.model_dump())
    return item_group


@router.get("/", response_model=List[ItemGroupResponse])
def get_item_groups(
    id: Optional[int] = None,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc",
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    if id:
        item_group = get_item_group(db, id)
        if not item_group:
            raise HTTPException(status_code=404, detail="Item group not found")
        return [item_group]
    return get_all_item_groups(db, offset, limit, sort_by, order)


@router.put("/{id}")
def update_item_group_endpoint(
    id: int,
    item_group_data: ItemGroupUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    item_group = update_item_group(db, id, item_group_data)
    if not item_group:
        raise HTTPException(status_code=404, detail="Item group not found")
    return item_group


@router.delete("/{id}")
def delete_item_group_endpoint(
    id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    item_group = delete_item_group(db, id)
    if not item_group:
        raise HTTPException(status_code=404, detail="Item group not found")
    return {"detail": "Item group deleted"}
