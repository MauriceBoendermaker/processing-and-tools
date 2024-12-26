from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DockBase(BaseModel):
    warehouse_id: int
    # Keep this if you still want to use a code for reference:
    code: str
    status: Optional[str] = "free"
    description: Optional[str] = None

class DockCreate(DockBase):
    pass

class DockUpdate(BaseModel):
    warehouse_id: Optional[int] = None
    code: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

class DockResponse(DockBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    model_config = {
        "from_attributes": True
    }
