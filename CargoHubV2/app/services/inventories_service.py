from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from CargoHubV2.app.models.inventories_model import Inventory
from CargoHubV2.app.services.sorting_service import apply_sorting
from CargoHubV2.app.schemas.inventories_schema import InventoryUpdate, InventoryResponse
from fastapi import HTTPException, status
from datetime import datetime
from typing import Optional



def create_inventory(db: Session, inventory_data: dict):
    inventory = Inventory(**inventory_data)
    db.add(inventory)
    try:
        db.commit()
        db.refresh(inventory)
        return inventory
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An inventory with this item reference already exists."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the inventory."
        )


def get_inventory(db: Session, item_reference: str):
    try:
        inventory = db.query(Inventory).filter(Inventory.item_reference == item_reference).first()
        if not inventory:
            raise HTTPException(status_code=404, detail="inventory not found")
        return inventory
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the inventory."
        )


def get_all_inventories(db: Session, offset: int = 0, limit: int = 100):
    try:
        return db.query(Inventory).offset(offset).limit(limit).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving inventories."
        )


def update_inventory(db: Session, item_reference: str, inven_data: dict):
    try:
        inventory = db.query(Inventory).filter(Inventory.item_reference == item_reference).first()
        if not inventory:
            raise HTTPException(status_code=404, detail="Inventory not found")

        for key, value in inven_data.items():
            setattr(inventory, key, value)
        inventory.updated_at = datetime.now()

        db.commit()
        db.refresh(inventory)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An integrity error occurred while updating the inventory."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the inventory."
        )
    return InventoryResponse.model_validate(inventory)


def delete_inventory(db: Session, item_reference: str):
    try:
        inv = db.query(Inventory).filter(Inventory.item_reference == item_reference).first()
        if not inv:
            raise HTTPException(status_code=404, detail="Inventory not found")
        db.delete(inv)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the inventory."
        )
    return {"detail": "inventory deleted"}


# locations filter using inventory ID
def get_locations_by_inventory(db: Session, item_reference: str):
    try:
        return db.query(Inventory).filter(Inventory.item_reference == item_reference).first().locations
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while getting the locations."
        )
