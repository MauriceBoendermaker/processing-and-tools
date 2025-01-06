from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated
from datetime import datetime
from typing import Optional

CodeType = Annotated[
                str,
                StringConstraints(
                    pattern=r"^[A-Z]\.\d+\.\d+$"
                ),
            ]


class LocationBase(BaseModel):
    warehouse_id: int
    code: CodeType
    name: str
    max_weight: Optional[float] = None
    stock: list[dict]


class LocationUpdate(BaseModel):
    warehouse_id: Optional[int] = None
    code: Optional[CodeType] = None
    name: Optional[str] = None
    max_weight: Optional[float] = None
    stock: Optional[list[dict]] = None


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
