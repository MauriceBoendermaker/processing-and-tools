from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated
from datetime import datetime
from typing import Optional

CodeType = Annotated[
                str,
                StringConstraints(
                    pattern=r"^SUP\d{4}$"
                ),
            ]

ReferenceType = Annotated[
    str,
    StringConstraints(
        pattern=r"^[A-Za-z]{1,4}-SUP\d{4}$"
    ),
]


class SuppliersBase(BaseModel):
    code: CodeType
    name: str
    address: str
    address_extra: Optional[str] = None
    city: str
    zip_code: str
    province: str
    country: str
    contact_name: str
    phonenumber: str
    reference: ReferenceType


class SuppliersCreate(SuppliersBase):
    pass


class SuppliersUpdate(BaseModel):
    code: Optional[CodeType] = None
    name: Optional[str] = None
    address: Optional[str] = None
    address_extra: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    contact_name: Optional[str] = None
    phonenumber: Optional[str] = None
    reference: Optional[ReferenceType] = None


class SuppliersResponse(BaseModel):
    id: int
    code: str
    name: str
    address: str
    address_extra: Optional[str] = None
    city: str
    zip_code: str
    province: str
    country: str
    contact_name: str
    phonenumber: str
    reference: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
