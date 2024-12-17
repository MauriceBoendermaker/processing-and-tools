from sqlalchemy import Column, Integer, String, DateTime, Boolean
from ..database import Base
from sqlalchemy.orm import relationship


class Location(Base):
    __tablename__ = "locations"

    # Data:
    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, index=True)
    code = Column(String, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    is_deleted = Column(Boolean, default=False)

