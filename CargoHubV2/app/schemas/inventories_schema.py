from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class InventoryBase(BaseModel):
    description: Optional[str] = None
    item_reference: Optional[str] = Field(None, title="Unique item reference")
    total_on_hand: Optional[int] = None
    total_expected: Optional[int] = None
    total_ordered: Optional[int] = None
    total_allocated: Optional[int] = None
    total_available: Optional[int] = None

    class Config:
        orm_mode = True


class InventoryCreate(InventoryBase):
    item_id: int  # verplichte field om item te linken


class InventoryUpdate(BaseModel):
    description: Optional[str] = None
    total_on_hand: Optional[int] = None
    total_expected: Optional[int] = None
    total_ordered: Optional[int] = None
    total_allocated: Optional[int] = None
    total_available: Optional[int] = None

    class Config:
        orm_mode = True


class InventoryResponse(InventoryBase):
    id: int
    item_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
