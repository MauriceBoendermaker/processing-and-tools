from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean
from ..database import Base
from datetime import datetime


class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, unique=True)
    transfer_from = Column(Integer, nullable=True)
    transfer_to = Column(Integer, nullable=False)
    transfer_status = Column(String, default="Scheduled", index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    is_deleted = Column(Boolean, default=False)
    items = Column(JSON, index=True)
