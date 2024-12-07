from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.schemas.clients_schema import *
from CargoHubV2.app.services.clients_service import *
from CargoHubV2.app.services.api_keys_service import validate_api_key
from typing import Optional, List

router = APIRouter(
    prefix="/api/v2/clients",
    tags=["clients"]
)


@router.post("/", response_model=ClientResponse)
def create_client_endpoint(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("create", api_key, db)
    client = create_client(db, client_data.model_dump())
    return client


@router.get("/")
def get_clients(
    id: Optional[int] = None,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc",
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("view", api_key, db)
    if id:
        client = get_client(db, id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client
    return get_all_clients(db, offset, limit, sort_by, order)


@router.put("/{id}", response_model=ClientResponse)
def update_client_endpoint(
    id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("edit", api_key, db)
    client = update_client(db, id, client_data)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.delete("/{id}")
def delete_client_endpoint(
    id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("delete", api_key, db)
    client = delete_client(db, id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client
