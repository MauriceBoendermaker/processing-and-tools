from sqlalchemy import Column, Integer, String, DateTime, Boolean
from ..database import Base
from datetime import datetime

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    city = Column(String, index=True)
    zip_code = Column(String, index=True)
    province = Column(String, index=True)
    country = Column(String, index=True)
    contact_name = Column(String, index=True)
    contact_phone = Column(String, index=True)
    contact_email = Column(String, index=True)
    created_at = Column(DateTime, index=True, default=datetime.now)
    updated_at = Column(DateTime, index=True, default=datetime.now, onupdate=datetime.now)
    is_deleted = Column(Boolean, default=False, nullable=False, server_default='0')

