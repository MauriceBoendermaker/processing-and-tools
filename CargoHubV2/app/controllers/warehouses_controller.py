from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.services import warehouses_service
from CargoHubV2.app.schemas import warehouses_schema
from CargoHubV2.app.database import get_db
from CargoHubV2.app.services.api_keys_service import validate_api_key
from typing import Optional


router = APIRouter(
    prefix="/api/v2/warehouses",
    tags=["warehouses"]
)


@router.get("/")
def get_warehouses(
    db: Session = Depends(get_db),
    code: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
        api_key: str = Header(...)):

    validate_api_key("view", api_key, db)
    if code:
        warehouse = warehouses_service.get_warehouse_by_code(db, code)
        if warehouse is None:
            raise HTTPException(status_code=404, detail="Warehouse not found")
        return warehouse
    warehouses = warehouses_service.get_all_warehouses(db, offset, limit)
    return warehouses


@router.post("/")
def create_warehouse(warehouse: warehouses_schema.WarehouseCreate, db: Session = Depends(get_db), api_key: str = Header(...)):
    validate_api_key("create", api_key, db)
    db_warehouse = warehouses_service.create_warehouse(
        db, warehouse.model_dump())

    if db_warehouse is None:
        raise HTTPException(status_code=400, detail="Warehouse already exists")
    return db_warehouse


@router.delete("/{code}")
def delete_warehouse(
    code: str, db: Session = Depends(get_db),
        api_key: str = Header(...)):

    validate_api_key("delete", api_key, db)
    succes = warehouses_service.delete_warehouse(db, code)
    if succes:
        return f"warehouse with code {code} deleted"
    raise HTTPException(status_code=404, detail="Warehouse not found")


@router.put("/{code}")
def update_warehouse(
    code: str,
    warehouse_data: warehouses_schema.WarehouseUpdate,
    db: Session = Depends(get_db),
        api_key: str = Header(...)):

    validate_api_key("edit", api_key, db)
    if warehouse_data:
        return warehouses_service.update_warehouse(db, code, warehouse_data.model_dump(exclude_unset=True))
    raise HTTPException(status_code=400, detail="invalid request body")
