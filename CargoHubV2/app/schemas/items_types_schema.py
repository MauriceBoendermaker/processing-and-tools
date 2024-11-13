from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ItemTypeSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
