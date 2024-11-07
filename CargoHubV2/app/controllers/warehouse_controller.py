from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from CargoHubV2.app.services import warehouse_service
from CargoHubV2.app.schemas import warehouse_schema
from CargoHubV2.app.database import get_db
from typing import Optional

router = APIRouter(
    prefix="/api/v2/warehouses",
    tags=["warehouses"]
)


@router.get("/")
def get_warehouses(db: Session = Depends(get_db), id: Optional[int] = None):

    if id:
        warehouse = warehouse_service.get_warehouse_by_id(db, id)
        if warehouse is None:
            raise HTTPException(status_code=404, detail="Warehouse not found")
        return warehouse
    warehouses = warehouse_service.get_all_warehouses(db)
    return warehouses


@router.post("/")
def create_warehouse(warehouse: warehouse_schema.WarehouseCreate, db: Session = Depends(get_db)):
    # service aanroepen die de warehouse toevoegt aan db
    # resultaat van de service gaat in db_warehouse
    db_warehouse = warehouse_service.create_warehouse(db, warehouse)
    if db_warehouse is None:
        raise HTTPException(status_code=400, detail="Warehouse already exists")
    return db_warehouse


@router.delete("/{id}")
def delete_warehouse(id: int, db: Session = Depends(get_db)):
    succes = warehouse_service.delete_warehouse(db, id)
    if succes:
        return f"warehouse with id {id} deleted"
    raise HTTPException(status_code=404, detail="Warehouse not found")


@router.put("/{id}")
def update_warehouse(id: int, warehouse_data: warehouse_schema.WarehouseUpdate, db: Session = Depends(get_db)):
    if warehouse_data:
        return warehouse_service.update_warehouse(db, id, warehouse_data)
    raise HTTPException(status_code=400, detail="invalid request body")
