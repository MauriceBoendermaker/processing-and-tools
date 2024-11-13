from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ItemLineBase(BaseModel):
    name: str
    description: Optional[str] = None

class ItemLineCreate(ItemLineBase):
    pass

class ItemLineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ItemLineResponse(ItemLineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
