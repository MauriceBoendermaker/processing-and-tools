from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from CargoHubV2.app.schemas.items_lines_schema import ItemLineCreate, ItemLineUpdate, ItemLineResponse
from CargoHubV2.app.database import get_db
from CargoHubV2.app.services.items_lines_service import create_item_line, get_item_line, get_all_item_lines, update_item_line, delete_item_line
from typing import Optional, List

router = APIRouter(
    prefix="/api/v2/item-lines",
    tags=["item_lines"]
)

@router.post("/", response_model=ItemLineResponse)
def create_item_line_endpoint(item_line_data: ItemLineCreate, db: Session = Depends(get_db)):
    item_line = create_item_line(db, item_line_data.model_dump())
    return item_line

@router.get("/", response_model=List[ItemLineResponse])
def get_item_lines(id: Optional[int] = None, db: Session = Depends(get_db)):
    if id:
        item_line = get_item_line(db, id)
        if not item_line:
            raise HTTPException(status_code=404, detail="Item line not found")
        return [item_line]  # Wrap in a list to match response model
    return get_all_item_lines(db)

@router.put("/{id}", response_model=ItemLineResponse)
def update_item_line_endpoint(id: int, item_line_data: ItemLineUpdate, db: Session = Depends(get_db)):
    item_line = update_item_line(db, id, item_line_data)
    if not item_line:
        raise HTTPException(status_code=404, detail="Item line not found")
    return item_line

@router.delete("/{id}")
def delete_item_line_endpoint(id: int, db: Session = Depends(get_db)):
    item_line = delete_item_line(db, id)
    if not item_line:
        raise HTTPException(status_code=404, detail="Item line not found")
    return {"detail": "Item line deleted"}
