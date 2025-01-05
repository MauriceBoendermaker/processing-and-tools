from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.schemas.items_schema import *
from CargoHubV2.app.services.items_service import *

from typing import Optional, List

router = APIRouter(
    prefix="/api/v2/items",
    tags=["items"]
)


@router.post("/", response_model=ItemResponse)
def create_item_endpoint(
    item_data: ItemCreate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
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
    api_key: str = Header(...),
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
    api_key: str = Header(...),
):
    item = update_item(db, code, item_data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{code}")
def delete_item_endpoint(
    code: str,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    item = delete_item(db, code)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item  # Returns the item with is_deleted=True
