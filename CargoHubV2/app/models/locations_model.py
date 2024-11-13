from sqlalchemy import Column, Integer, String, JSON, DateTime
from ..database import Base


class Location(Base):
    __tablename__ = "locations"

    # Data:
    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, index=True)
    code = Column(String, index=True)
    name = Column(JSON, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
