from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, Boolean
from ..database import Base
from datetime import datetime


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(JSON)
    source_id = Column(Integer, index=True)
    order_date = Column(DateTime, index=True)
    request_date = Column(DateTime, index=True)
    shipment_date = Column(DateTime, index=True)
    shipment_type = Column(String, index=True)
    shipment_status = Column(String, index=True)
    notes = Column(String, nullable=True)
    carrier_code = Column(String, index=True)
    carrier_description = Column(String, index=True)
    service_code = Column(String, index=True)
    payment_type = Column(String, index=True)
    transfer_mode = Column(String, index=True)
    total_package_count = Column(Integer)
    total_package_weight = Column(Float)
    items = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = Column(Boolean, default=False)

