from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.schemas.inventories_schema import InventoryResponse, InventoryCreate, InventoryUpdate
from CargoHubV2.app.schemas.locations_schema import Location
from CargoHubV2.app.services import inventories_service
from typing import Optional, List

from CargoHubV2.app.dependencies.api_dependencies import (
    get_valid_api_key,
    role_required
)
from CargoHubV2.app.models.api_key_model import APIKey

router = APIRouter(
    prefix="/api/v2/inventories",
    tags=["inventories"]
)


@router.post("/", response_model=InventoryResponse)
def create_inventory(
    inventory_data: InventoryCreate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    inv = inventories_service.create_inventory(db, inventory_data.model_dump())
    return inv


@router.get("/")
def get_inventories(
    item_reference: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc",
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    if item_reference:
        inven = inventories_service.get_inventory(db, item_reference)
        if not inven:
            raise HTTPException(status_code=404, detail="Inventory not found")
        return inven
    return inventories_service.get_all_inventories(db, offset, limit, sort_by, order)


@router.put("/{item_reference}", response_model=InventoryResponse)
def update_inventory_endpoint(
    item_reference: str,
    inven_data: InventoryUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),  # api key req
):
    inven = inventories_service.update_inventory(db, item_reference, inven_data.model_dump(exclude_unset=True))
    if not inven:
        raise HTTPException(status_code=404, detail="inventory not found")
    return inven


@router.delete("/{item_reference}")
def delete_inventory_endpoint(
    item_reference: str,
    db: Session = Depends(get_db),
    api_key: str = Header(...),  # api key req
):
    inven = inventories_service.delete_inventory(db, item_reference)
    if not inven:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inven


# locations waar een specifieke inventory is (filter)
@router.get("/{item_reference}/locations")
def get_locations_from(
    item_reference: str = None,
    db: Session = Depends(get_db),
    api_key: str = Header(...),  # api key req
):
    if item_reference:
        inven = inventories_service.get_inventory(db, item_reference)
        if not inven:
            raise HTTPException(status_code=404, detail="Inventory not found")
    return inventories_service.get_locations_by_inventory(db, item_reference)
