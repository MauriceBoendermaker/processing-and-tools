from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from CargoHubV2.app.schemas.items_schema import *
from CargoHubV2.app.database import get_db
from CargoHubV2.app.services.items_service import *
from typing import Optional, List


router = APIRouter(
    prefix="/api/v2/items",
    tags=["items"]
)


@router.post("/", response_model=ItemResponse)
def create_item_endpoint(item_data: ItemCreate, db: Session = Depends(get_db)):
    item = create_item(db, item_data.model_dump())
    return item


@router.get("/", response_model=List[ItemResponse])
def get_items(uid: Optional[str] = None, db: Session = Depends(get_db)):
    if uid:
        item = get_item(db, uid)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return [item]  # Wrap in a list to match response model
    return get_all_items(db)


@router.put("/{uid}", response_model=ItemResponse)
def update_item_endpoint(uid: str, item_data: WarehouseUpdate, db: Session = Depends(get_db)):
    item = update_item(db, uid, item_data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item



@router.delete("/{uid}")
def delete_item_endpoint(uid: str, db: Session = Depends(get_db)):
    item = delete_item(db, uid)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Item deleted"}
