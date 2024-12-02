from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from CargoHubV2.app.models.suppliers_model import Supplier
from CargoHubV2.app.models.items_model import Item
from CargoHubV2.app.schemas.suppliers_schema import SuppliersCreate, SuppliersUpdate
from fastapi import HTTPException, status
from datetime import datetime


def create_supplier(db: Session, suppliers_data: SuppliersCreate):
    suppliers = Supplier(
        code=suppliers_data.code,
        name=suppliers_data.name,
        address=suppliers_data.address,
        address_extra=suppliers_data.address_extra,
        city=suppliers_data.city,
        zip_code=suppliers_data.zip_code,
        province=suppliers_data.province,
        country=suppliers_data.country,
        contact_name=suppliers_data.contact_name,
        phonenumber=suppliers_data.phonenumber,
        reference=suppliers_data.reference,
    )
    db.add(suppliers)
    try:
        db.commit()
        db.refresh(suppliers)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the supplier"
        )
    return suppliers


def get_supplier(db: Session, code: str):
    try:
        supplier = db.query(Supplier).filter(Supplier.code == code).first()
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        return supplier
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the supplier"
        )


def get_all_suppliers(db: Session, offset: int = 0, limit: int = 100):
    try:
        return db.query(Supplier).offset(offset).limit(limit).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the suppliers"
        )


def update_supplier(db: Session, code: str, supplier_data: SuppliersUpdate):
    to_update = db.query(Supplier).filter(Supplier.code == code).first()
    if not to_update:
        raise HTTPException(status_code=404, detail="Supplier not found")
    for key, value in supplier_data.model_dump(exclude_unset=True).items():
        setattr(to_update, key, value)
    try:
        db.commit()
        db.refresh(to_update)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="An integrity error occurred while updating the supplier.")
    return to_update


def delete_supplier(db: Session, code: str):
    supplier_to_delete = db.query(Supplier).filter(Supplier.code == code).first()
    if not supplier_to_delete:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db.delete(supplier_to_delete)
    db.commit()
    return {"detail": "supplier deleted"}


def get_items_by_supplier_id(db: Session, supplier_id: int, offset: int = 0, limit: int = 100):
    items = db.query(Item).filter(Item.supplier_id == supplier_id).offset(offset).limit(limit).all()
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="This supplier does not exist")
    if not items:
        raise HTTPException(status_code=404, detail="No Items found for this supplier")
    return items
