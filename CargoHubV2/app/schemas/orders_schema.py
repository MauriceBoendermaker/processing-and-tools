from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime


class OrderBase(BaseModel):
    source_id: int
    order_date: datetime
    request_date: Optional[datetime] = None
    reference: str
    reference_extra: Optional[str] = None
    order_status: str
    notes: Optional[str] = None
    shipping_notes: Optional[str] = None
    picking_notes: Optional[str] = None
    warehouse_id: int
    ship_to: Optional[int] = None
    bill_to: Optional[int] = None
    shipment_id: Optional[int] = None
    total_amount: float
    total_discount: Optional[float] = None
    total_tax: Optional[float] = None
    total_surcharge: Optional[float] = None
    items: Optional[List[Dict]] = None

    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    order_status: Optional[str] = None
    notes: Optional[str] = None
    total_amount: Optional[float] = None

    class Config:
        orm_mode = True


class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
