from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ClientBase(BaseModel):
    name: str = None
    address: str = None
    city: str = None
    zip_code: str = None
    province: str = None
    country: str = None
    contact_name: str = None
    contact_phone: str = None
    contact_email: str = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None


class ClientResponse(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
