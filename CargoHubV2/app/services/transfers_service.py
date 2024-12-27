from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
from CargoHubV2.app.services.sorting_service import apply_sorting

from CargoHubV2.app.models.transfers_model import Transfer
from CargoHubV2.app.schemas.transfers_schema import TransferCreate, TransferUpdate
from datetime import datetime
from typing import Optional



def create_transfer(db: Session, transfer_data: TransferCreate):
    transfer = Transfer(**transfer_data.model_dump())
    db.add(transfer)
    try:
        db.commit()
        db.refresh(transfer)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A transfer with this reference already exists."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the transfer."
        )
    return transfer


def get_transfer(db: Session, transfer_id: int):
    try:
        transfer = db.query(Transfer).filter(Transfer.id == transfer_id).first()
        if not transfer:
            raise HTTPException(status_code=404, detail="Transfer not found")
        return transfer
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the transfer."
        )


def get_all_transfers(
    db: Session,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc"
):
    try:
        query = db.query(Transfer)
        if sort_by:
            query = apply_sorting(query, Transfer, sort_by, order)
        return query.offset(offset).limit(limit).all()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving transfers."
        )


def update_transfer(db: Session, transfer_id: int, transfer_data: TransferUpdate):
    try:
        transfer = db.query(Transfer).filter(Transfer.id == transfer_id).first()
        if not transfer:
            raise HTTPException(status_code=404, detail="Transfer not found")
        update_data = transfer_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(transfer, key, value)
        transfer.updated_at = datetime.now()
        db.commit()
        db.refresh(transfer)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An integrity error occurred while updating the transfer."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the transfer."
        )
    return transfer


def delete_transfer(db: Session, transfer_id: int):
    try:
        transfer = db.query(Transfer).filter(
            Transfer.id == transfer_id, Transfer.is_deleted == False
        ).first()
        if not transfer:
            raise HTTPException(status_code=404, detail="Transfer not found")
        
        transfer.is_deleted = True  # Soft delete by updating the flag
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the transfer."
        )
    return {"detail": "Transfer soft deleted"}

