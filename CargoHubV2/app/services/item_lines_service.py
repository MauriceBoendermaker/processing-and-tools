from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from CargoHubV2.app.models.item_lines_model import ItemLine
from CargoHubV2.app.schemas.item_lines_schema import ItemLineUpdate
from CargoHubV2.app.services.sorting_service import apply_sorting

from typing import List, Optional
from fastapi import HTTPException, status

#need to add the api key check

def create_item_line(db: Session, item_line_data: dict) -> ItemLine:
    item_line = ItemLine(**item_line_data)
    db.add(item_line)
    try:
        db.commit()
        db.refresh(item_line)
        return item_line
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item line already exists"
        )


def get_item_line(db: Session, id: int) -> Optional[ItemLine]:
    return db.query(ItemLine).filter(ItemLine.id == id).first()


def get_all_item_lines(
    db: Session,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",  # Default sort by "id"
    order: Optional[str] = "asc"   # Default order is ascending
) -> List[ItemLine]:
    try:
        query = db.query(ItemLine)
        if sort_by:  # Apply sorting only if sort_by is specified
            query = apply_sorting(query, ItemLine, sort_by, order)
        return query.offset(offset).limit(limit).all()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving item lines."
        )



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
