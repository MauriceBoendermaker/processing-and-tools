from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from CargoHubV2.app.models.inventories_model import Inventory
from CargoHubV2.app.schemas.inventories_schema import InventoryUpdate
from fastapi import HTTPException, status
from datetime import datetime


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
            detail="An inventory with this code already exists."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the inventory."
        )


def get_inventory(db: Session, id: int):
    try:
        inventory = db.query(Inventory).filter(Inventory.id == id).first()
        if not inventory:
            raise HTTPException(status_code=404, detail="inventory not found")
        return inventory
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the inventory."
        )


def get_all_iventories(db: Session, offset: int = 0, limit: int = 100):
    try:
        return db.query(Inventory).offset(offset).limit(limit).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving inventories."
        )


def update_inventory(db: Session, id: int, inven_data: InventoryUpdate):
    try:
        inventory = db.query(Inventory).filter(Inventory.id == id).first()
        if not inventory:
            raise HTTPException(status_code=404, detail="inventory not found")

        update_data = inven_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
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
    return inventory


def delete_inventory(db: Session, id: int):
    try:
        inv = db.query(Inventory).filter(Inventory.id == id).first()
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
    return {"detail": "Iventory deleted"}
