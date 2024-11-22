from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LocationBase(BaseModel):
    warehouse_id: int
    code: str
    name: str


class LocationUpdate(BaseModel):
    warehouse_id: Optional[int] = None
    code: Optional[str] = None
    name: Optional[str] = None


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
