from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class InventoryBase(BaseModel):
    description: str = None
    item_reference: str = Field(None, title="Unique item reference")
    total_on_hand: int = None
    total_expected: int = None
    total_ordered: int = None
    total_allocated: int = None
    total_available: int = None
    locations: list[int] = None

    class Config:
        orm_mode = True


class InventoryCreate(InventoryBase):
    item_id: str  # verplichte field om item te linken


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
    item_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }