from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.schemas.orders_schema import OrderResponse, OrderCreate, OrderUpdate
from CargoHubV2.app.services.orders_service import *
from CargoHubV2.app.services.api_keys_service import validate_api_key
from typing import List, Optional

router = APIRouter(
    prefix="/api/v2/orders",
    tags=["orders"]
)


@router.post("/", response_model=OrderResponse)
def create_order_endpoint(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("create", api_key, db)
    order = create_order(db, order_data.model_dump())
    return order


@router.get("/")
def get_orders(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("view", api_key, db)
    if id:
        order = get_order(db, id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    return get_all_orders(db)


@router.get("/{id}/items")
def get_order_items(
    id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("view", api_key, db)
    items = get_items_in_order(db, id)
    if not items:
        raise HTTPException(
            status_code=404, detail="Items not found for this order")
    return items


@router.put("/{id}", response_model=OrderResponse)
def update_order_endpoint(
    id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("edit", api_key, db)
    order = update_order(db, id, order_data)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{id}")
def delete_order_endpoint(
    id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    validate_api_key("delete", api_key, db)
    result = delete_order(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted"}


@router.get("/{order_id}/packinglist")
def get_pack_list(
    order_id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...)
):
    validate_api_key("view", api_key, db)
    packlist = get_packinglist_for_order(db, order_id)
    if not packlist:
        raise HTTPException(status_code=404, detail="Packlist not found")
    return packlist


@router.get("/{order_id}/shipments")
def get_shipments_linked_with_order(
    order_id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...)
):
    validate_api_key("view", api_key, db)
    shipment = get_shipments_by_order_id(db, order_id)
    if not shipment:
        raise HTTPException(status_code=404, detail="No shipments found")
    return shipment


@router.put("/{order_id}/shipments")
def update_shipments_linked_with_order(
    order_id: int,
    order_data: OrderShipmentUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...)
):
    validate_api_key("edit", api_key, db)
    order = update_shipments_in_order(db, order_id, order_data)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
