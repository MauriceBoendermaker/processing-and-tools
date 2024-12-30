from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SuppliersBase(BaseModel):
    code: str
    name: str
    address: str
    address_extra: Optional[str] = None
    city: str
    zip_code: str
    province: str
    country: str
    contact_name: str
    phonenumber: str
    reference: str


class SuppliersCreate(SuppliersBase):
    pass


class SuppliersUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    address_extra: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    contact_name: Optional[str] = None
    phonenumber: Optional[str] = None
    reference: Optional[str] = None


class SuppliersResponse(BaseModel):
    id: int
    code: str
    name: str
    address: str
    address_extra: Optional[str] = None
    city: str
    zip_code: str
    province: str
    country: str
    contact_name: str
    phonenumber: str
    reference: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
