from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.schemas.clients_schema import *
from CargoHubV2.app.services.clients_service import *
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
    if id:
        client = get_client(db, id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client
    return get_all_clients(db, offset, limit, sort_by, order)


@router.get("/{country}")
def get_clients_by_country(
    country: str,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc",
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    return get_country_clients(db, country, offset, limit, sort_by, order)


@router.put("/{id}", response_model=ClientResponse)
def update_client_endpoint(
    id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
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
    client = delete_client(db, id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client
