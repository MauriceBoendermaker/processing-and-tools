from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.schemas.item_lines_schema import ItemLineCreate, ItemLineUpdate, ItemLineResponse
from CargoHubV2.app.services.item_lines_service import create_item_line, get_item_line, get_all_item_lines, update_item_line, delete_item_line
from CargoHubV2.app.services.api_keys_service import validate_api_key
from typing import Optional, List


router = APIRouter(
    prefix="/api/v2/item_lines",
    tags=["item_lines"]
)


@router.post("/", response_model=ItemLineResponse)
def create_item_line_endpoint(
    item_line_data: ItemLineCreate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),  # API key required
):
    validate_api_key("create", api_key, db)
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
    api_key: str = Header(...),
):
    validate_api_key("view", api_key, db)
    if id:
        item_line = get_item_line(db, id)
        if not item_line:
            raise HTTPException(status_code=404, detail="Item line not found")
        return item_line
    return get_all_item_lines(db, offset, limit, sort_by, order)


@router.put("/{id}", response_model=ItemLineResponse)
def update_item_line_endpoint(
    id: int,
    item_line_data: ItemLineUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),  # API key required
):
    validate_api_key("edit", api_key, db)
    item_line = update_item_line(db, id, item_line_data)
    if not item_line:
        raise HTTPException(status_code=404, detail="Item line not found")
    return item_line


@router.delete("/{id}")
def delete_item_line_endpoint(
    id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),  # API key required
):
    validate_api_key("delete", api_key, db)
    item_line = delete_item_line(db, id)
    if not item_line:
        raise HTTPException(status_code=404, detail="Item line not found")
    return {"detail": "Item line deleted"}
