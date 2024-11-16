from sqlalchemy.orm import Session
from CargoHubV2.app.models.warehouses_model import Warehouse
from CargoHubV2.app.schemas.warehouses_schema import WarehouseCreate, WarehouseUpdate
from datetime import datetime
from fastapi import HTTPException


def get_all_warehouses(db: Session):
    # geeft alle warehouses
    return db.query(Warehouse).all()


def get_warehouse_by_id(db: Session, id: int):
    return db.query(Warehouse).filter(Warehouse.id == id).first()


def create_warehouse(db: Session, warehouse: dict):
    # voegt een nieuwe warehouse toe aan db
    db_warehouse = Warehouse(**warehouse)
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)  # Refresh om gegenereerde velden te krijgen (Id)
    return db_warehouse


def delete_warehouse(db: Session, id: int):
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
