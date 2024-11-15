from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from ..database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String)
    address = Column(String)
    address_extra = Column(String)
    city = Column(String)
    zip_code = Column(String)
    province = Column(String)
    country = Column(String)
    contact_name = Column(String)
    phonenumber = Column(String)
    reference = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
