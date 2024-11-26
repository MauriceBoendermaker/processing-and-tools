from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ItemTypeBase(BaseModel):
    name: str
    description: Optional[str] = None


class ItemTypeCreate(ItemTypeBase):
    pass


class ItemTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ItemTypeResponse(ItemTypeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
