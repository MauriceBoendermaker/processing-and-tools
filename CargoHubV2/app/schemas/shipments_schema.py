from pydantic import BaseModel, constr
from datetime import datetime
from typing import List, Optional

StatusType = constr(regex=r"^(Pending|Transit|Delivered)$")


class ShipmentItem(BaseModel):
    item_id: str
    amount: int


class ShipmentBase(BaseModel):
    order_id: List[int]
    source_id: int
    order_date: datetime
    request_date: datetime
    shipment_date: datetime
    shipment_type: str
    shipment_status: StatusType  # type: ignore
    notes: Optional[str] = None
    carrier_code: str
    carrier_description: str
    service_code: str
    payment_type: str
    transfer_mode: str
    total_package_count: int
    total_package_weight: float
    items: List[ShipmentItem]


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentUpdate(BaseModel):
    order_id: Optional[List[int]] = None
    source_id: Optional[int] = None
    order_date: Optional[datetime] = None
    request_date: Optional[datetime] = None
    shipment_date: Optional[datetime] = None
    shipment_type: Optional[str] = None
    shipment_status: Optional[StatusType] = "Pending"  # type: ignore
    notes: Optional[str] = None
    carrier_code: Optional[str] = None
    carrier_description: Optional[str] = None
    service_code: Optional[str] = None
    payment_type: Optional[str] = None
    transfer_mode: Optional[str] = None
    total_package_count: Optional[int] = None
    total_package_weight: Optional[float] = None
    items: Optional[List[ShipmentItem]] = None


class ShipmentOrderUpdate(BaseModel):
    order_id: List[int] = None


class ShipmentResponse(ShipmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
