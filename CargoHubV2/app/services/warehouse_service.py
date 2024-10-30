from sqlalchemy.orm import Session
from app.models.warehouse_model import Warehouse
from app.schemas.warehouse_schema import WarehouseCreate, WarehouseUpdate
from datetime import datetime
from fastapi import HTTPException


def get_all_warehouses(db: Session):
    # geeft alle warehouses
    return db.query(Warehouse).all()


def get_warehouse_by_id(db: Session, id: int):
    return db.query(Warehouse).filter(Warehouse.id == id).first()


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


def delete_warehouse(db: Session, id: int) -> bool:
    to_del = db.query(Warehouse).filter(Warehouse.id == id).first()
    if not to_del:
        return False

    db.delete(to_del)
    db.commit()

    return True


def update_warehouse(db: Session, id: int, warehouse_data: WarehouseUpdate) -> Warehouse:
    to_update = db.query(Warehouse).filter(Warehouse.id == id).first()
    if not to_update:
        raise HTTPException(status_code=404, detail="Warehouse not found")

    for key, value in warehouse_data.model_dump(exclude_unset=True).items():
        setattr(to_update, key, value)

    db.commit()
    db.refresh(to_update)

    return to_update
