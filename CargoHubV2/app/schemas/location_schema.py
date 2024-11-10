from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LocationBase(BaseModel):
    location_id: int
    code: str
    name: dict


class LocationUpdate(BaseModel):
    location_id: Optional[int] = None
    code: Optional[str] = None
    name: Optional[dict] = None


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
