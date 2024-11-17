from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict


class TransferBase(BaseModel):
    reference: str
    transfer_from: Optional[int] = None
    transfer_to: int
    transfer_status: str
    items: List[Dict]


class TransferCreate(TransferBase):
    pass


class TransferUpdate(BaseModel):
    reference: Optional[str] = None
    transfer_from: Optional[int] = None
    transfer_to: Optional[int] = None
    items: Optional[List[Dict]] = None
    transfer_status: Optional[str] = None


class Transfer(TransferBase):
    id: int
    transfer_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
