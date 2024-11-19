from sqlalchemy.orm import Session
from CargoHubV2.app.models.clients_model import Client
from CargoHubV2.app.models.orders_model import Order  # Assuming orders exist
from CargoHubV2.app.schemas.clients_schema import ClientCreate, ClientUpdate
from datetime import datetime
from fastapi import HTTPException

def get_all_clients(db: Session):
    return db.query(Client).all()

def get_client_by_id(db: Session, id: int):
    return db.query(Client).filter(Client.id == id).first()

def get_orders_by_client_id(db: Session, client_id: int):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    orders = db.query(Order).filter((Order.ship_to == client_id) | (Order.bill_to == client_id)).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this client")
    return orders

def create_client(db: Session, client: ClientCreate):
    db_client = Client(
        name=client.name,
        address=client.address,
        city=client.city,
        zip_code=client.zip_code,
        province=client.province,
        country=client.country,
        contact_name=client.contact_name,
        contact_phone=client.contact_phone,
        contact_email=client.contact_email,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def delete_client(db: Session, id: int):
    to_delete = db.query(Client).filter(Client.id == id).first()
    if not to_delete:
        return False
    db.delete(to_delete)
    db.commit()
    return True

def update_client(db: Session, id: int, client_data: ClientUpdate):
    to_update = db.query(Client).filter(Client.id == id).first()
    if not to_update:
        raise HTTPException(status_code=404, detail="Client not found")

    for key, value in client_data.model_dump(exclude_unset=True).items():
        setattr(to_update, key, value)

    db.commit()
    db.refresh(to_update)
    return to_update
