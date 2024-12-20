from sqlalchemy.orm import Session
from CargoHubV2.app.models.item_types_model import ItemType
from CargoHubV2.app.schemas.item_types_schema import ItemTypeUpdate
from CargoHubV2.app.services.sorting_service import apply_sorting

from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status



#need to add the api key check

def create_item_type(db: Session, item_type_data: dict) -> ItemType:
    item_type = ItemType(**item_type_data)
    db.add(item_type)
    db.commit()
    db.refresh(item_type)
    return item_type


def get_item_type(db: Session, id: int) -> Optional[ItemType]:
    return db.query(ItemType).filter(ItemType.id == id).first()


def get_all_item_types(
    db: Session,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",  # Default sort by "name"
    order: Optional[str] = "asc"     # Default order is ascending
) -> List[ItemType]:
    try:
        query = db.query(ItemType)
        if sort_by:  # Apply sorting only if sort_by is specified
            query = apply_sorting(query, ItemType, sort_by, order)
        return query.offset(offset).limit(limit).all()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving item types."
        )



def update_item_type(db: Session, id: int, item_type_data: ItemTypeUpdate) -> Optional[ItemType]:
    item_type = get_item_type(db, id)
    if item_type:
        for key, value in item_type_data.model_dump().items():
            setattr(item_type, key, value)
        db.commit()
        db.refresh(item_type)
    return item_type


def delete_item_type(db: Session, id: int) -> bool:
    item_type = db.query(ItemType).filter(ItemType.id == id, ItemType.is_deleted == False).first()
    if item_type:
        item_type.is_deleted = True  # Soft delete by updating the flag
        db.commit()
        return True
    return False

