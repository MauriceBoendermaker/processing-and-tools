from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Item(Base):
    __tablename__ = "items"

    uid = Column(String, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    description = Column(String)
    short_description = Column(String)
    upc_code = Column(String)
    model_number = Column(String)
    commodity_code = Column(String)
    item_line = Column(Integer, ForeignKey("item_lines.id"))  # Foreign Key to ItemLine
    item_group = Column(Integer, ForeignKey("item_groups.id"))  # Foreign Key to ItemGroup
    item_type = Column(Integer, ForeignKey("item_types.id"))  # Foreign Key to ItemType
    unit_purchase_quantity = Column(Integer)
    unit_order_quantity = Column(Integer)
    pack_order_quantity = Column(Integer)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    supplier_code = Column(String)
    supplier_part_number = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = Column(Boolean, default=False, nullable=False, server_default='0')


    item_group_rel = relationship("ItemGroup", back_populates="items")
    item_type_rel = relationship("ItemType", back_populates="items")
    item_line_rel = relationship("ItemLine", back_populates="items")

    # Specify foreign_keys argument to disambiguate
    suppliers_rel = relationship(
        "Supplier",
        back_populates="items",
        foreign_keys=[supplier_id],  # Explicitly reference supplier_id
    )
