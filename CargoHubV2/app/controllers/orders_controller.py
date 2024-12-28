from fastapi import APIRouter, HTTPException, Depends, Header, Query
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.schemas.orders_schema import OrderResponse, OrderCreate, OrderUpdate
from CargoHubV2.app.services.orders_service import *
from typing import List, Optional
from datetime import datetime

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
    order = create_order(db, order_data.model_dump())
    return order


@router.get("/")
def get_orders(
    id: Optional[int] = None,
    date: Optional[datetime] = Query(None, description="Filter orders by a specific date"),
    offset: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = "order_date",
    sort_order: Optional[str] = "asc",
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    if id:
        order = get_order(db, id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    orders = get_all_orders(db, date=date, offset=offset, limit=limit, sort_by=sort_by, sort_order=sort_order)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for the specified date")
    return orders


@router.get("/{id}/items")
def get_order_items(
    id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
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
    result = delete_order(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted"}


@router.get("/{order_id}/packinglist")
def get_pack_list(
    order_id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    packlist = get_packinglist_for_order(db, order_id)
    if not packlist:
        raise HTTPException(status_code=404, detail="Packlist not found")
    return packlist


@router.get("/{order_id}/shipments")
def get_shipments_linked_with_order(
    order_id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    shipment = get_shipments_by_order_id(db, order_id)
    if not shipment:
        raise HTTPException(status_code=404, detail="No shipments found")
    return shipment


@router.put("/{order_id}/shipments")
def update_shipments_linked_with_order(
    order_id: int,
    order_data: OrderShipmentUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    order = update_shipments_in_order(db, order_id, order_data)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
