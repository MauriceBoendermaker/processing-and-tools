from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
from CargoHubV2.app.models.transfers_model import Transfer
from CargoHubV2.app.schemas.transfers_schema import TransferCreate, TransferUpdate
from datetime import datetime


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


def get_all_transfers(db: Session):
    try:
        return db.query(Transfer).all()
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
        transfer = db.query(Transfer).filter(Transfer.id == transfer_id).first()
        if not transfer:
            raise HTTPException(status_code=404, detail="Transfer not found")
        db.delete(transfer)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the transfer."
        )
    return {"detail": "Transfer deleted"}
