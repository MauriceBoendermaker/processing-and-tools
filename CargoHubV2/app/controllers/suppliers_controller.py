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


@router.get("/", response_model=List[SuppliersResponse])
def get_suppliers(id: Optional[int] = None, offset: int = 0, limit: int = 100, db: Session = Depends(get_db), api_key: str = Header(...)):
    validate_api_key("view", api_key, db)
    if id:
        supplier = get_supplier(db, id)
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        return [supplier]
    return get_all_suppliers(db, offset=offset, limit=limit)


@router.post("/", response_model=SuppliersResponse)
def create_supplier_endpoint(supplier_data: SuppliersCreate, db: Session = Depends(get_db), api_key: str = Header(...)):
    validate_api_key("create", api_key, db)
    supplier = create_supplier(db, supplier_data)
    return supplier


@router.put("/{id}", response_model=SuppliersResponse)
def update_supplier_endpoint(id: int, supplier_data: SuppliersUpdate, db: Session = Depends(get_db), api_key: str = Header(...)):
    validate_api_key("edit", api_key, db)
    supplier = update_supplier(db, id, supplier_data)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.delete("/{id}")
def delete_supplier_endpoint(id: int, db: Session = Depends(get_db), api_key: str = Header(...)):
    validate_api_key("delete", api_key, db)
    supplier = delete_supplier(db, id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return { "detail": "Supplier deleted"}


@router.get("/{supplier_id}/items", response_model=List[items_schema.ItemBase])
def get_items_by_supplier_id_endpoint(supplier_id: int, offset: int = 0, limit: int = 100, db: Session = Depends(get_db), api_key: str = Header(...)):
    validate_api_key("view", api_key, db)
    items = suppliers_service.get_items_by_supplier_id(db, supplier_id, offset=offset, limit=limit)
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this supplier ID")
    return items

