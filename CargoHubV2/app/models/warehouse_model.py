from sqlalchemy import Column, Integer, String, JSON, DateTime
from database import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    zip = Column(String, index=True)
    city = Column(String, index=True)
    province = Column(String, index=True)
    country = Column(String, index=True)
    contact = Column(JSON, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
