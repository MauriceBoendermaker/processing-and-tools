from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DockBase(BaseModel):
    code: str
    name: str
    type: str
    status: str = "free"  # Default status is "free"
    warehouse_id: int


class DockCreate(DockBase):
    pass


class DockUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None  # Allow updating status
    warehouse_id: Optional[int] = None


class DockResponse(DockBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
