from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Dock(Base):
    __tablename__ = "docks"

    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, default="free")  # Can be "occupied" or "free"
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    warehouse = relationship("Warehouse", back_populates="docks")
