from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from CargoHubV2.app.models.items_model import Item
from CargoHubV2.app.models.warehouses_model import Warehouse
from CargoHubV2.app.schemas.items_schema import ItemUpdate
from CargoHubV2.app.services.sorting_service import apply_sorting

from fastapi import HTTPException, status
from datetime import datetime
from typing import Optional


def get_item(db: Session, code: str):
    try:
        item = db.query(Item).filter(Item.code == code, Item.is_deleted == False).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the item."
        )


def get_all_items(db: Session, offset: int = 0, limit: int = 100, sort_by: Optional[str] = "id", order: Optional[str] = "asc"):
    try:
        query = db.query(Item).filter(Item.is_deleted == False)
        sorted_query = apply_sorting(query, Item, sort_by, order)
        return sorted_query.offset(offset).limit(limit).all()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving items."
        )


def create_item(db: Session, item_data: dict):
    warehouse = db.query(Warehouse).filter(Warehouse.id == item_data.get("warehouse_id")).first()
    if warehouse and warehouse.forbidden_classifications:
        if item_data.get("hazard_classification") in warehouse.forbidden_classifications:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item's hazard classification is not allowed in the warehouse."
            )

    item = Item(**item_data)
    db.add(item)
    try:
        db.commit()
        db.refresh(item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An item with this code already exists."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the item."
        )
    return item


def update_item(db: Session, code: str, item_data: ItemUpdate):
    item = db.query(Item).filter(Item.code == code).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    update_data = item_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    item.updated_at = datetime.now()
    try:
        db.commit()
        db.refresh(item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An item with this code already exists."
        )
    return item


def delete_item(db: Session, code: str):
    try:
        item = db.query(Item).filter(Item.code == code, Item.is_deleted == False).first()
        if not item:
            return None
        item.is_deleted = True
        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the item."
        )