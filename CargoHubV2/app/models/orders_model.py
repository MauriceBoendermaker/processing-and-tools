from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, nullable=False)
    order_date = Column(DateTime, nullable=False)
    request_date = Column(DateTime, nullable=True)
    reference = Column(String, nullable=False)
    reference_extra = Column(String, nullable=True)
    order_status = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    shipping_notes = Column(String, nullable=True)
    picking_notes = Column(String, nullable=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    ship_to = Column(Integer, nullable=True)
    bill_to = Column(Integer, nullable=True)
    shipment_id = Column(JSON, nullable=True)
    total_amount = Column(Float, nullable=False)
    total_discount = Column(Float, nullable=True)
    total_tax = Column(Float, nullable=True)
    total_surcharge = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    items = Column(JSON, nullable=True)
    is_deleted = Column(Boolean, default=False)


    warehouse = relationship("Warehouse")
