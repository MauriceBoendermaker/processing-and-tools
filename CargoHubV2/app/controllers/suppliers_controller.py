from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.schemas.suppliers_schema import *
from CargoHubV2.app.schemas import items_schema 
from CargoHubV2.app.database import get_db
from CargoHubV2.app.services.suppliers_service import * 
from CargoHubV2.app.services import suppliers_service 
from CargoHubV2.app.services.api_keys_service import validate_api_key
from typing import Optional, List


router = APIRouter(
    prefix="/api/v2/suppliers",
    tags=["suppliers"]
)


@router.get("/")
def get_suppliers(
    code: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc",
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("view", api_key, db)
    if code:
        supplier = get_supplier(db, code)
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        return supplier
    return get_all_suppliers(db, offset=offset, limit=limit, sort_by=sort_by, order=order)


@router.post("/", response_model=SuppliersResponse)
def create_supplier_endpoint(supplier_data: SuppliersCreate, db: Session = Depends(get_db)):
    supplier = create_supplier(db, supplier_data)
    return supplier


@router.put("/{code}", response_model=SuppliersResponse)
def update_supplier_endpoint(code: str, supplier_data: SuppliersUpdate, db: Session = Depends(get_db)):
    supplier = update_supplier(db, code, supplier_data)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.delete("/{code}")
def delete_supplier_endpoint(code: str, db: Session = Depends(get_db)):
    supplier = delete_supplier(db, code)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return { "detail": "Supplier deleted"}


@router.get("/{supplier_id}/items", response_model=List[items_schema.ItemBase])
def get_items_by_supplier_id_endpoint(supplier_id: int, offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = suppliers_service.get_items_by_supplier_id(db, supplier_id, offset=offset, limit=limit)
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this supplier ID")
    return [items]
