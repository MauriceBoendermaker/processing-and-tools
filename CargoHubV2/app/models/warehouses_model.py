from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    zip = Column(String, index=True)
    city = Column(String, index=True)
    province = Column(String, index=True)
    country = Column(String, index=True)
    contact = Column(JSON, index=True)
    forbidden_classifications = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = Column(Boolean, default=False, nullable=False, server_default='0')

    docks = relationship("Dock", back_populates="warehouse", cascade="all, delete-orphan")