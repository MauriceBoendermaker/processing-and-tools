from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ItemGroupBase(BaseModel):
    name: str
    description: Optional[str] = None


class ItemGroupCreate(ItemGroupBase):
    pass


class ItemGroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ItemGroupResponse(ItemGroupBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
