from sqlalchemy.orm import Session
from CargoHubV2.app.models.item_groups_model import ItemGroup
from CargoHubV2.app.schemas.item_groups_schema import ItemGroupUpdate
from CargoHubV2.app.services.sorting_service import apply_sorting

from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

#need to add the api key check
def create_item_group(db: Session, item_group_data: dict) -> ItemGroup:
    item_group = ItemGroup(**item_group_data)
    db.add(item_group)
    db.commit()
    db.refresh(item_group)
    return item_group


def get_item_group(db: Session, id: int) -> Optional[ItemGroup]:
    return db.query(ItemGroup).filter(ItemGroup.id == id, ItemGroup.is_deleted == False).first()


def get_all_item_groups(
    db: Session,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc"
) -> List[ItemGroup]:
    try:
        query = db.query(ItemGroup).filter(ItemGroup.is_deleted == False)
        if sort_by:
            query = apply_sorting(query, ItemGroup, sort_by, order)
        return query.offset(offset).limit(limit).all()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving item groups."
        )


def update_item_group(db: Session, id: int, item_group_data: ItemGroupUpdate) -> Optional[ItemGroup]:
    item_group = get_item_group(db, id)
    if item_group:
        for key, value in item_group_data.model_dump().items():
            setattr(item_group, key, value)
        db.commit()
        db.refresh(item_group)
    return item_group


def delete_item_group(db: Session, id: int) -> bool:
    item_group = db.query(ItemGroup).filter(ItemGroup.id == id, ItemGroup.is_deleted == False).first()
    if item_group:
        item_group.is_deleted = True  # Soft delete by updating the flag
        db.commit()
        return True
    return False

