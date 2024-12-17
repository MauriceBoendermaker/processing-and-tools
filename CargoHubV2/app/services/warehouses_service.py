from sqlalchemy.orm import Session
from CargoHubV2.app.models.warehouses_model import Warehouse
from CargoHubV2.app.schemas.warehouses_schema import WarehouseCreate, WarehouseResponse
from datetime import datetime
from CargoHubV2.app.services.sorting_service import apply_sorting
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import Optional



def get_all_warehouses(
    db: Session,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc"
):
    try:
        query = db.query(Warehouse)
        if sort_by:
            query = apply_sorting(query, Warehouse, sort_by, order)
        return query.offset(offset).limit(limit).all()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving warehouses."
        )


def get_warehouse_by_code(db: Session, code: str):
    try:
        ware = db.query(Warehouse).filter(Warehouse.code == code).first()
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
            detail="An error occurred while creating the warehouse."
        )
    return db_warehouse


def delete_warehouse(db: Session, code: str):
    to_del = db.query(Warehouse).filter(
        Warehouse.code == code, Warehouse.is_deleted == False
    ).first()
    if not to_del:
        raise HTTPException(status_code=404, detail="Warehouse not found")

    try:
        to_del.is_deleted = True  # Soft delete by updating the flag
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the warehouse"
        )

    return {"detail": "Warehouse soft deleted"}



def update_warehouse(db: Session, code: str, warehouse_data: dict) -> WarehouseResponse:
    try:
        to_update = db.query(Warehouse).filter(Warehouse.code == code).first()
        if not to_update:
            raise HTTPException(status_code=404, detail="Warehouse not found")

        for key, value in warehouse_data.items():
            setattr(to_update, key, value)
        to_update.updated_at = datetime.now()
        db.commit()
        db.refresh(to_update)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The code you gave in the body, already exists"
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the warehouse."
        )
    return WarehouseResponse.model_validate(to_update)
