from sqlalchemy import Column, Integer, String, JSON, DateTime
from ..database import Base
from sqlalchemy.orm import relationship
from inventories_model import inventory_location_association


class Location(Base):
    __tablename__ = "locations"

    # Data:
    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, index=True)
    code = Column(String, index=True)
    name = Column(JSON, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
