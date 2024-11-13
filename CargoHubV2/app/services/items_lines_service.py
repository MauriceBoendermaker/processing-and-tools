from sqlalchemy.orm import Session
from CargoHubV2.app.models.items_lines_model import ItemLine
from CargoHubV2.app.schemas.items_lines_schema import ItemLineCreate, ItemLineUpdate
from typing import List, Optional

def create_item_line(db: Session, item_line_data: dict) -> ItemLine:
    item_line = ItemLine(**item_line_data)
    db.add(item_line)
    db.commit()
    db.refresh(item_line)
    return item_line

def get_item_line(db: Session, id: int) -> Optional[ItemLine]:
    return db.query(ItemLine).filter(ItemLine.id == id).first()

def get_all_item_lines(db: Session) -> List[ItemLine]:
    return db.query(ItemLine).all()

def update_item_line(db: Session, id: int, item_line_data: ItemLineUpdate) -> Optional[ItemLine]:
    item_line = get_item_line(db, id)
    if item_line:
        for key, value in item_line_data.model_dump().items():
            setattr(item_line, key, value)
        db.commit()
        db.refresh(item_line)
    return item_line

def delete_item_line(db: Session, id: int) -> bool:
    item_line = get_item_line(db, id)
    if item_line:
        db.delete(item_line)
        db.commit()
        return True
    return False
