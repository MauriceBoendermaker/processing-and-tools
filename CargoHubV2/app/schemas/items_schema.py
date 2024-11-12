from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Import related schemas
from .item_group_schema import ItemGroupSchema
from .item_type_schema import ItemTypeSchema
from .item_line_schema import ItemLineSchema


class ItemBase(BaseModel):
    uid: str
    code: str
    description: str
    short_description: str
    upc_code: str
    model_number: str
    commodity_code: str
    item_line: int  # Only ID for creation
    item_group: int  # Only ID for creation
    item_type: int  # Only ID for creation
    unit_purchase_quantity: int
    unit_order_quantity: int
    pack_order_quantity: int
    supplier_id: int
    supplier_code: str
    supplier_part_number: str


class ItemCreate(ItemBase):
    pass


class WarehouseUpdate(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    upc_code: Optional[str] = None
    model_number: Optional[str] = None
    commodity_code: Optional[str] = None
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
