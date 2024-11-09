from sqlalchemy.orm import Session
from CargoHubV2.app.models.items_model import Item
from CargoHubV2.app.schemas.items_schema import ItemCreate, ItemUpdate
from fastapi import HTTPException
from datetime import datetime

def create_item(db: Session, item_data: ItemCreate):
    item = Item(**item_data.model_dump())  # Use model_dump instead of dict
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_item(db: Session, uid: str):
    return db.query(Item).filter(Item.uid == uid).first()

def get_all_items(db: Session):
    return db.query(Item).all()

def update_item(db: Session, uid: str, item_data: ItemUpdate):
    item = db.query(Item).filter(Item.uid == uid).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    update_data = item_data.model_dump(exclude_unset=True)  # Use model_dump with exclude_unset
    for key, value in update_data.items():
        setattr(item, key, value)
    item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, uid: str):
    item = db.query(Item).filter(Item.uid == uid).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"detail": "Item deleted"}
