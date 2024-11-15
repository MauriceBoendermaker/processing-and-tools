from sqlalchemy.orm import Session
from CargoHubV2.app.models.item_groups_model import ItemGroup
from CargoHubV2.app.schemas.item_groups_schema import ItemGroupCreate, ItemGroupUpdate
from typing import List, Optional


def create_item_group(db: Session, item_group_data: dict) -> ItemGroup:
    item_group = ItemGroup(**item_group_data)
    db.add(item_group)
    db.commit()
    db.refresh(item_group)
    return item_group


def get_item_group(db: Session, id: int) -> Optional[ItemGroup]:
    return db.query(ItemGroup).filter(ItemGroup.id == id).first()


def get_all_item_groups(db: Session) -> List[ItemGroup]:
    return db.query(ItemGroup).all()


def update_item_group(db: Session, id: int, item_group_data: ItemGroupUpdate) -> Optional[ItemGroup]:
    item_group = get_item_group(db, id)
    if item_group:
        for key, value in item_group_data.model_dump().items():
            setattr(item_group, key, value)
        db.commit()
        db.refresh(item_group)
    return item_group


def delete_item_group(db: Session, id: int) -> bool:
    item_group = get_item_group(db, id)
    if item_group:
        db.delete(item_group)
        db.commit()
        return True
    return False
