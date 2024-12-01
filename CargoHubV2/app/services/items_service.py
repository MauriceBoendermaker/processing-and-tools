from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from CargoHubV2.app.models.items_model import Item
from CargoHubV2.app.schemas.items_schema import ItemUpdate
from fastapi import HTTPException, status
from datetime import datetime


def create_item(db: Session, item_data: dict):
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


def get_item(db: Session, uid: str):
    try:
        item = db.query(Item).filter(Item.uid == uid).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the item."
        )


def get_all_items(db: Session, offset: int = 0, limit: int = 10):
    try:
        return db.query(Item).offset(offset).limit(limit).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving items."
        )



def update_item(db: Session, uid: str, item_data: ItemUpdate):
    try:
        item = db.query(Item).filter(Item.uid == uid).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        update_data = item_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)
        item.updated_at = datetime.now()
        db.commit()
        db.refresh(item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An integrity error occurred while updating the item."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the item."
        )
    return item


def delete_item(db: Session, uid: str):
    try:
        item = db.query(Item).filter(Item.uid == uid).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(item)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the item."
        )
    return {"detail": "Item deleted"}
