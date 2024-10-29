from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services import warehouse_service
from app.schemas import warehouse_schema
from app.database import get_db

router = APIRouter(
    prefix="/api/v2/warehouse",
    tags=["warehouses"]
)


@router.get("/")
def get_warehouses(db: Session = Depends(get_db)):
    warehouses = warehouse_service.get_all_warehouses(db)
    return warehouses
    # warehouses uit database halen en in variabele stoppen
    # de warehouses returnen


@router.post("/")
def create_warehouse(warehouse: warehouse_schema.WarehouseCreate, db: Session = Depends(get_db)):
    # service aanroepen die de warehouse toevoegt aan db
    # resultaat van de service gaat in db_warehouse
    db_warehouse = warehouse_service.create_warehouse(db, warehouse)
    if db_warehouse is None:
        raise HTTPException(status_code=400, detail="User already exists")
    return db_warehouse
