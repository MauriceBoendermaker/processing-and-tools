from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Dock(Base):
    __tablename__ = "docks"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    status = Column(String(20), nullable=False)
    description = Column(String(255), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)  # Soft delete column
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relationships
    warehouse = relationship("Warehouse", back_populates="docks")  # Add backref to Warehouse
