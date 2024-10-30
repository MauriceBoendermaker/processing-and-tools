from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WarehouseBase(BaseModel):
    code: str
    name: str
    address: str
    zip: str
    city: str
    province: str
    country: str
    contact: dict


class WarehouseUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    zip: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    contact: Optional[dict] = None


class WarehouseCreate(WarehouseBase):
    pass


class Warehouse(WarehouseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
