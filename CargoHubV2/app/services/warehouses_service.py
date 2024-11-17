from sqlalchemy.orm import Session
from CargoHubV2.app.models.warehouses_model import Warehouse
from CargoHubV2.app.schemas.warehouses_schema import WarehouseCreate, WarehouseUpdate
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


def get_all_warehouses(db: Session):
    try:
        return db.query(Warehouse).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving warehouses."
        )


def get_warehouse_by_id(db: Session, id: int):
    try:
        ware = db.query(Warehouse).filter(Warehouse.id == id).first()
        if not ware:
            raise HTTPException(status_code=404, detail="Warehouse not found")
        return ware
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving this warehouse."
        )


def create_warehouse(db: Session, warehouse: dict):
    # voegt een nieuwe warehouse toe aan db
    db_warehouse = Warehouse(**warehouse)
    db.add(db_warehouse)

    try:
        db.commit()
        db.refresh(db_warehouse)  # Refresh om gegenereerde velden te krijgen (Id)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A warehouse with this code already exists."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the item."
        )
    return db_warehouse


def delete_warehouse(db: Session, id: int):
    to_del = db.query(Warehouse).filter(Warehouse.id == id).first()
    if not to_del:
        return False

    db.delete(to_del)
    db.commit()

    return True


def update_warehouse(db: Session, id: int, warehouse_data: WarehouseUpdate) -> Warehouse:
    try:
        to_update = db.query(Warehouse).filter(Warehouse.id == id).first()
        if not to_update:
            raise HTTPException(status_code=404, detail="Warehouse not found")

        for key, value in warehouse_data.model_dump(exclude_unset=True).items():
            setattr(to_update, key, value)
        to_update.updated_at = datetime.now
        db.commit()
        db.refresh(to_update)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An integrity error occurred while updating the warehouse."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the warehouse."
        )
    return to_update
