from sqlalchemy import Column, Integer, String, JSON, DateTime
from ..database import Base
from datetime import datetime


class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, index=True)
    transfer_from = Column(Integer, nullable=True)
    transfer_to = Column(Integer, nullable=False)
    transfer_status = Column(String, default="Scheduled", index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    items = Column(JSON, index=True)
