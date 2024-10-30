from sqlalchemy.orm import Session
from app.models.warehouse_model import Warehouse
from app.schemas.warehouse_schema import WarehouseCreate
from datetime import datetime
from fastapi import HTTPException


def get_all_warehouses(db: Session):
    # geeft alle warehouses
    return db.query(Warehouse).all()


def create_warehouse(db: Session, warehouse: WarehouseCreate):
    # voegt een nieuwe warehouse toe aan db
    db_warehouse = Warehouse(
        code=warehouse.code,
        name=warehouse.name,
        address=warehouse.address,
        zip=warehouse.zip,
        city=warehouse.city,
        province=warehouse.province,
        country=warehouse.country,
        contact=warehouse.contact,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)  # Refresh om gegenereerde velden te krijgen (Id)
    return db_warehouse


def delete_warehouse(db: Session, id: int):
    to_del = db.query(Warehouse).filter(Warehouse.id == id).first()
    if to_del is None:
        return False

    db.delete(to_del)
    db.commit()

    return True
