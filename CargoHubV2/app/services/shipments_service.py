from sqlalchemy.orm import Session
from CargoHubV2.app.models.shipments_model import Shipment
from CargoHubV2.app.schemas.shipments_schema import ShipmentCreate, ShipmentUpdate
from datetime import datetime
from fastapi import HTTPException

def get_all_shipments(db: Session):
    return db.query(Shipment).all()

def get_shipment_by_id(db: Session, id: int):
    shipment = db.query(Shipment).filter(Shipment.id == id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment

def create_shipment(db: Session, shipment: ShipmentCreate):
    db_shipment = Shipment(
        order_id=shipment.order_id,
        source_id=shipment.source_id,
        order_date=shipment.order_date,
        request_date=shipment.request_date,
        shipment_date=shipment.shipment_date,
        shipment_type=shipment.shipment_type,
        shipment_status=shipment.shipment_status,
        notes=shipment.notes,
        carrier_code=shipment.carrier_code,
        carrier_description=shipment.carrier_description,
        service_code=shipment.service_code,
        payment_type=shipment.payment_type,
        transfer_mode=shipment.transfer_mode,
        total_package_count=shipment.total_package_count,
        total_package_weight=shipment.total_package_weight,
        items=shipment.items,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment

def delete_shipment(db: Session, id: int):
    to_delete = db.query(Shipment).filter(Shipment.id == id).first()
    if not to_delete:
        return False
    db.delete(to_delete)
    db.commit()
    return True

def update_shipment(db: Session, id: int, shipment_data: ShipmentUpdate):
    to_update = db.query(Shipment).filter(Shipment.id == id).first()
    if not to_update:
        raise HTTPException(status_code=404, detail="Shipment not found")

    for key, value in shipment_data.model_dump(exclude_unset=True).items():
        setattr(to_update, key, value)

    db.commit()
    db.refresh(to_update)
    return to_update
