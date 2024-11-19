from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base

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
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
