from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Dock(Base):
    __tablename__ = "docks"

    # Auto-incremented ID as the primary key
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False, index=True)

    # You can leave this if you still want a code field, but it is no longer your main ID
    code = Column(String(50), unique=True, nullable=False, index=True)

    status = Column(String(20), nullable=False, default="free")
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)  # Soft delete column

    warehouse = relationship("Warehouse", back_populates="docks")
