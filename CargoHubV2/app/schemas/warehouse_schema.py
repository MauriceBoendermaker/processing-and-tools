from pydantic import BaseModel
from datetime import datetime


class WarehouseBase(BaseModel):
    code: str
    name: str
    address: str
    zip: str
    city: str
    province: str
    country: str
    contact: dict


class WarehouseCreate(WarehouseBase):
    pass


class Warehouse(WarehouseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
