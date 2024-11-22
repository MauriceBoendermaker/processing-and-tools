from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from CargoHubV2.app.models.clients_model import Client
from CargoHubV2.app.schemas.clients_schema import ClientCreate, ClientUpdate
from fastapi import HTTPException, status
from datetime import datetime


def create_client(db: Session, client_data: dict):
    client = Client(**client_data)
    db.add(client)
    try:
        db.commit()
        db.refresh(client)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A client with this name already exists."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the client."
        )
    return client


def get_client(db: Session, client_id: int):
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the client."
        )


def get_all_clients(db: Session):
    try:
        return db.query(Client).all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving clients."
        )


def update_client(db: Session, client_id: int, client_data: ClientUpdate):
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        update_data = client_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(client, key, value)
        client.updated_at = datetime.now()
        db.commit()
        db.refresh(client)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An integrity error occurred while updating the client."
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the client."
        )
    return client


def delete_client(db: Session, client_id: int):
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        db.delete(client)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the client."
        )
    return {"detail": "Client deleted"}


# Commented out due to missing orders_model
# def get_orders_by_client_id(db: Session, client_id: int):
#     client = db.query(Client).filter(Client.id == client_id).first()
#     if not client:
#         raise HTTPException(status_code=404, detail="Client not found")
#     orders = db.query(Order).filter((Order.ship_to == client_id) | (Order.bill_to == client_id)).all()
#     if not orders:
#         raise HTTPException(status_code=404, detail="No orders found for this client")
#     return orders
