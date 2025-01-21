from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated
from datetime import datetime
from typing import Optional, List, Dict

ReferenceType = Annotated[
                str,
                StringConstraints(
                    pattern=r"^TR\d{5,6}$"
                ),
            ]

StatusType = Annotated[
                str,
                StringConstraints(
                    pattern=r"^(Scheduled|Completed)$"
                ),
            ]


class TransferBase(BaseModel):
    reference: ReferenceType
    transfer_from: Optional[int] = None
    transfer_to: int
    transfer_status: StatusType
    items: List[Dict]


class TransferCreate(TransferBase):
    pass


class TransferUpdate(BaseModel):
    reference: Optional[ReferenceType] = None
    transfer_from: Optional[int] = None
    transfer_to: Optional[int] = None
    items: Optional[List[Dict]] = None
    transfer_status: Optional[StatusType] = None


class Transfer(TransferBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
