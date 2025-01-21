from pydantic import BaseModel, StringConstraints
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

StatusType = Annotated[
                str,
                StringConstraints(
                    pattern=r"^(Occupied|Free)$"
                ),
            ]


class DockBase(BaseModel):
    warehouse_id: int
    code: str
    status: Optional[StatusType] = "free"
    description: Optional[str] = None


class DockCreate(DockBase):
    pass


class DockUpdate(BaseModel):
    warehouse_id: Optional[int] = None
    code: Optional[str] = None
    status: Optional[StatusType] = None
    description: Optional[str] = None


class DockResponse(DockBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    model_config = {
        "from_attributes": True
    }
