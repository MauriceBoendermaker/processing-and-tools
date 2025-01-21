from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated
from datetime import datetime
from typing import Optional, List

CountryType = Annotated[
    str,
    StringConstraints(
        pattern=r"^[A-Z]{2}$"
    ),
]


class WarehouseBase(BaseModel):
    code: str
    name: str
    address: str
    zip: str
    city: str
    province: str
    country: CountryType
    contact: dict
    forbidden_classifications: Optional[List[str]] = None


class WarehouseUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    zip: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    country: Optional[CountryType] = None
    contact: Optional[dict] = None
    forbidden_classifications: Optional[List[str]] = None


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseResponse(WarehouseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
