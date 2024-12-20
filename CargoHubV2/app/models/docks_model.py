from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Dock(Base):
    __tablename__ = "docks"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True)  # Indicates dock type (e.g., loading/unloading zone, big/small loads, etc.)
    status = Column(String, default="free", index=True)  # Tracks availability (e.g., free, occupied)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    warehouse = relationship("Warehouse", back_populates="docks")
