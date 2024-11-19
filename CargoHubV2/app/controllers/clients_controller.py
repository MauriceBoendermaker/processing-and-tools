from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from CargoHubV2.app.services import clients_service
from CargoHubV2.app.schemas import clients_schema
from CargoHubV2.app.services.api_keys_service import validate_api_key
from CargoHubV2.app.database import get_db
from typing import Optional

router = APIRouter(
    prefix="/api/v2/clients",
    tags=["clients"]
)

@router.get("/", dependencies=[Depends(validate_api_key)])
def get_clients(db: Session = Depends(get_db), id: Optional[int] = None):
    if id:
        client = clients_service.get_client_by_id(db, id)
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")
        return client
    clients = clients_service.get_all_clients(db)
    return clients

@router.get("/{id}/orders", dependencies=[Depends(validate_api_key)])
def get_orders_by_client_id(id: int, db: Session = Depends(get_db)):
    return clients_service.get_orders_by_client_id(db, id)

@router.post("/", dependencies=[Depends(validate_api_key)])
def create_client(client: clients_schema.ClientCreate, db: Session = Depends(get_db)):
    return clients_service.create_client(db, client)

@router.delete("/{id}", dependencies=[Depends(validate_api_key)])
def delete_client(id: int, db: Session = Depends(get_db)):
    success = clients_service.delete_client(db, id)
    if success:
        return f"Client with id {id} deleted"
    raise HTTPException(status_code=404, detail="Client not found")

@router.put("/{id}", dependencies=[Depends(validate_api_key)])
def update_client(id: int, client_data: clients_schema.ClientUpdate, db: Session = Depends(get_db)):
    if client_data:
        return clients_service.update_client(db, id, client_data)
    raise HTTPException(status_code=400, detail="Invalid request body")
