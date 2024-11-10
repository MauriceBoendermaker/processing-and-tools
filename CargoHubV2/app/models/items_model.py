from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from CargoHubV2.app.database import Base


class Item(Base):
    __tablename__ = "items"

    uid = Column(String, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    description = Column(String)
    short_description = Column(String)
    upc_code = Column(String)
    model_number = Column(String)
    commodity_code = Column(String)
    item_line = Column(Integer)
    item_group = Column(Integer)
    item_type = Column(Integer)
    unit_purchase_quantity = Column(Integer)
    unit_order_quantity = Column(Integer)
    pack_order_quantity = Column(Integer)
    supplier_id = Column(Integer)
    supplier_code = Column(String)
    supplier_part_number = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
