from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.schemas.inventories_schema import InventoryResponse, InventoryCreate, InventoryUpdate
from CargoHubV2.app.schemas.locations_schema import Location
from CargoHubV2.app.services import inventories_service
from CargoHubV2.app.services.api_keys_service import validate_api_key
from typing import Optional, List

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
    validate_api_key("create", api_key, db)
    item = inventories_service.create_inventory(db, inventory_data.model_dump())
    return item


@router.get("/", response_model=List[InventoryResponse])
def get_inventories(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    api_key: str = Header(...),  # api key req
    offset=0,
    limit=100
):
    validate_api_key("view", api_key, db)
    if id:
        inven = inventories_service.get_inventory(db, id)
        if not inven:
            raise HTTPException(status_code=404, detail="Inventory not found")
        return [inven]
    return inventories_service.get_all_inventories(db, offset, limit)


@router.put("/{id}", response_model=InventoryResponse)
def update_inventory_endpoint(
    id: int,
    inven_data: InventoryUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),  # api key req
):
    validate_api_key("edit", api_key, db)
    inven = inventories_service.update_inventory(db, id, inven_data.model_dump(exclude_unset=True))
    if not inven:
        raise HTTPException(status_code=404, detail="inventory not found")
    return inven


@router.delete("/{id}")
def delete_inventory_endpoint(
    id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),  # api key req
):
    validate_api_key("delete", api_key, db)
    inven = inventories_service.delete_inventory(db, id)
    if not inven:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inven


# locations waar een specifieke inventory is (filter)
@router.get("/{id}/locations", response_model=List[Location])
def get_locations_from(
    id: int = None,
    db: Session = Depends(get_db),
    api_key: str = Header(...),  # api key req
):
    validate_api_key("view", api_key, db)
    if id:
        inven = inventories_service.get_inventory(db, id)
        if not inven:
            raise HTTPException(status_code=404, detail="Inventory not found")
    return inventories_service.get_locations_by_inventory(db, id)
