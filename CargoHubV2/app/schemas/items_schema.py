from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated
from datetime import datetime
from typing import Optional

UidType = Annotated[
    str,
    StringConstraints(pattern=r"^P\d{6}$")
]

UpcType = Annotated[
    str,
    StringConstraints(pattern=r"^\d{13}$")
]


class ItemBase(BaseModel):
    uid: UidType
    code: str
    description: str
    short_description: str
    upc_code: UpcType
    model_number: str
    commodity_code: str
    hazard_classification: Optional[str] = None
    item_line: int = None
    item_group: int = None
    item_type: int = None
    unit_purchase_quantity: int
    unit_order_quantity: int
    pack_order_quantity: int
    supplier_id: int
    supplier_code: str
    supplier_part_number: str


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    upc_code: Optional[UpcType] = None
    model_number: Optional[str] = None
    commodity_code: Optional[str] = None
    hazard_classification: Optional[str] = None
    item_line: Optional[int] = None
    item_group: Optional[int] = None
    item_type: Optional[int] = None
    unit_purchase_quantity: Optional[int] = None
    unit_order_quantity: Optional[int] = None
    pack_order_quantity: Optional[int] = None
    supplier_id: Optional[int] = None
    supplier_code: Optional[str] = None
    supplier_part_number: Optional[str] = None


class ItemResponse(ItemBase):
    created_at: datetime
    updated_at: datetime

    item_group: int
    item_type: int
    item_line: int

    class Config:
        orm_mode = True
