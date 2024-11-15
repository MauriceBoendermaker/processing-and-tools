from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from CargoHubV2.app.models.suppliers_model import Suppliers
from CargoHubV2.app.schemas.suppliers_schema import SuppliersCreate, SuppliersUpdate
from fastapi import HTTPException, status
from datetime import datetime


def create_supplier(db: Session, suppliers_data: SuppliersCreate):
    suppliers = Suppliers(**suppliers_data)
    db.add(suppliers)
    try:
        db.commit()
        db.refresh(suppliers)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occured while creating the supplier"
        )
    return suppliers


def get_supplier(db: Session, id: int):
    try:
        supplier = db.query(Suppliers).filter(Suppliers.id == id).first()
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        return supplier
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occured while retrieving the supplier"
        )


def get_all_suppliers(db: Session):
    try:
        return db.query(Suppliers).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occured while retrieving the suppliers"
        )


def update_supplier(db: Session, id: int, supplier_data: SuppliersUpdate):
    try:
        supplier = db.query(Suppliers).filter(Suppliers.id == id).first()
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        update_data = supplier_data.model_dump(exclude_unset=True)
        for key, value in update_data.suppliers():
            setattr(supplier, key, value)
        supplier.updated_at = datetime.now()
        db.commit()
        db.refresh(supplier)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An integrity error occured while updating the supplier"
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occured while updating the supplier"
        )
    return supplier


def delete_supplier(db: Session, id: int):
    try:
        supplier = db.query(Suppliers).filter(Suppliers.id == id).first()
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        db.delete(supplier)
        db.commit
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occured while deleting the supplier"
        )
    return {"detail": "Supplier deleted"}
