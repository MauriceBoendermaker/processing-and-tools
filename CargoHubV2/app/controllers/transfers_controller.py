from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.services import transfers_service
from CargoHubV2.app.schemas import transfers_schema
from CargoHubV2.app.services.api_keys_service import validate_api_key
from CargoHubV2.app.database import get_db
from typing import Optional


router = APIRouter(
    prefix="/api/v2/transfers",
    tags=["transfers"]
)


@router.post("/")
def create_transfer(transfer: transfers_schema.TransferCreate, db: Session = Depends(get_db)):
    db_transfer = transfers_service.create_transfer(db, transfer)
    return db_transfer


@router.get("/")
def get_transfers(
    db: Session = Depends(get_db),
    id: Optional[int] = None,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc",
    api_key: str = Header(...),
):
    validate_api_key("view", api_key, db)
    if id:
        transfer = transfers_service.get_transfer(db, id)
        if not transfer:
            raise HTTPException(status_code=404, detail="Transfer not found")
        return transfer
    return transfers_service.get_all_transfers(db, offset=offset, limit=limit, sort_by=sort_by, order=order)


@router.delete("/{id}")
def delete_transfer(id: int, db: Session = Depends(get_db)):
    return transfers_service.delete_transfer(db, id)


@router.put("/{id}")
def update_transfer(id: int, transfer_data: transfers_schema.TransferUpdate, db: Session = Depends(get_db)):
    updated_transfer = transfers_service.update_transfer(db, id, transfer_data)
    return updated_transfer
