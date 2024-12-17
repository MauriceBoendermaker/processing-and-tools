from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DockBase(BaseModel):
    warehouse_id: int
    code: str
    status: Optional[str] = "free"

class DockCreate(DockBase):
    pass

class DockUpdate(BaseModel):
    warehouse_id: Optional[int] = None
    code: Optional[str] = None
    status: Optional[str] = None

class DockResponse(DockBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True