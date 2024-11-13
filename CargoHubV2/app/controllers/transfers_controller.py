from fastapi import APIRouter, HTTPException, Depends
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
def create_transfer(transfer: transfers_schema.TransferCreate, db: Session = Depends(get_db)):
    db_transfer = transfers_service.create_transfer(db, transfer)
    if db_transfer is None:
        raise HTTPException(status_code=400, detail="Transfer already exists")
    return db_transfer
    

@router.get("/")
def get_transfers(db: Session = Depends(get_db), id: Optional[int] = None):
    if id:
        transfer = transfers_service.get_transfer(db, id)
        if transfer is None:
            raise HTTPException(status_code=404, detail="Transfer not found")
        return transfer
    transfers = transfers_service.get_all_transfers(db)
    return transfers


@router.delete("/{id}")
def delete_transfer(id: int, db: Session = Depends(get_db)):
    success = transfers_service.delete_transfer(db, id)
    if success:
        return {"detail": f"Transfer with id {id} deleted"}
    raise HTTPException(status_code=404, detail="Transfer not found")


@router.put("/{id}")
def update_transfer(id: int, transfer_data: transfers_schema.TransferUpdate, db: Session = Depends(get_db)):
    updated_transfer = transfers_service.update_transfer(db, id, transfer_data)
    if updated_transfer:
        return updated_transfer
    raise HTTPException(status_code=400, detail="Invalid request body or transfer not found")
