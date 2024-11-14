from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from CargoHubV2.app.schemas.items_types_schema import ItemTypeCreate, ItemTypeUpdate, ItemTypeResponse
from CargoHubV2.app.database import get_db
from CargoHubV2.app.services.items_types_service import create_item_type, get_item_type, get_all_item_types, update_item_type, delete_item_type
from typing import Optional, List

router = APIRouter(
    prefix="/api/v2/item-types",
    tags=["item_types"]
)

@router.post("/", response_model=ItemTypeResponse)
def create_item_type_endpoint(item_type_data: ItemTypeCreate, db: Session = Depends(get_db)):
    item_type = create_item_type(db, item_type_data.model_dump())
    return item_type

@router.get("/", response_model=List[ItemTypeResponse])
def get_item_types(id: Optional[int] = None, db: Session = Depends(get_db)):
    if id:
        item_type = get_item_type(db, id)
        if not item_type:
            raise HTTPException(status_code=404, detail="Item type not found")
        return [item_type]  # Wrap in a list to match response model
    return get_all_item_types(db)

@router.put("/{id}", response_model=ItemTypeResponse)
def update_item_type_endpoint(id: int, item_type_data: ItemTypeUpdate, db: Session = Depends(get_db)):
    item_type = update_item_type(db, id, item_type_data)
    if not item_type:
        raise HTTPException(status_code=404, detail="Item type not found")
    return item_type

@router.delete("/{id}")
def delete_item_type_endpoint(id: int, db: Session = Depends(get_db)):
    item_type = delete_item_type(db, id)
    if not item_type:
        raise HTTPException(status_code=404, detail="Item type not found")
    return {"detail": "Item type deleted"}
