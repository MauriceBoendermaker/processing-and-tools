from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.services import transfers_service
from CargoHubV2.app.schemas import transfers_schema
from CargoHubV2.app.database import get_db
from typing import Optional


router = APIRouter(
    prefix="/api/v2/transfers",
    tags=["transfers"]
)


@router.post("/")
def create_transfer(transfer: transfers_schema.TransferCreate, db: Session = Depends(get_db), api_key: str = Header(...),):
    db_transfer = transfers_service.create_transfer(db, transfer)
    return db_transfer


@router.get("/")
def get_transfers(db: Session = Depends(get_db), id: Optional[int] = None, offset: int = 0, limit: int = 100, api_key: str = Header(...),):
    if id:
        transfer = transfers_service.get_transfer(db, id)
        return transfer
    transfers = transfers_service.get_all_transfers(db, offset, limit)
    return transfers


@router.delete("/{id}")
def delete_transfer(id: int, db: Session = Depends(get_db), api_key: str = Header(...),):
    return transfers_service.delete_transfer(db, id)


@router.put("/{id}")
def update_transfer(id: int, transfer_data: transfers_schema.TransferUpdate, db: Session = Depends(get_db), api_key: str = Header(...),):
    updated_transfer = transfers_service.update_transfer(db, id, transfer_data)
    return updated_transfer
