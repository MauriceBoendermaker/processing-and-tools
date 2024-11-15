from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from CargoHubV2.app.schemas.suppliers_schema import *
from CargoHubV2.app.database import get_db
from CargoHubV2.app.services.suppliers_service import * 
from typing import Optional, List


router = APIRouter(
    prefix="/api/v2/suppliers",
    tags=["suppliers"]
)


@router.get("/", response_model=List[SuppliersResponse])
def get_suppliers(id: Optional[int] = None, db: Session = Depends(get_db)):
    if id:
        supplier = get_supplier(db, id)
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        return [supplier]
    return get_all_suppliers(db)


@router.post("/", response_model=SuppliersResponse)
def create_supplier_endpoint(supplier_data: SuppliersCreate, db: Session = Depends(get_db)):
    supplier = create_supplier(db, supplier_data)
    return supplier


@router.put("/{id}", response_model=SuppliersResponse)
def update_supplier_endpoint(id: int, supplier_data: SuppliersUpdate, db: Session = Depends(get_db)):
    supplier = update_supplier(db, id, supplier_data)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.delete("/{id}")
def delete_supplier_endpoint(id: int, db: Session = Depends(get_db)):
    supplier = delete_supplier(db, id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return { "detail": "Supplier deleted"}
