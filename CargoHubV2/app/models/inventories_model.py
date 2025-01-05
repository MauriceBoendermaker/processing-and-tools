from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Inventory(Base):
    __tablename__ = 'inventories'
    id = Column(Integer, primary_key=True)
    item_id = Column(String, ForeignKey('items.uid'), unique=True, nullable=False)
    description = Column(String, nullable=True)
    item_reference = Column(String, unique=True)
    locations = Column(JSON)
    total_on_hand = Column(Integer)
    total_expected = Column(Integer)
    total_ordered = Column(Integer)
    total_allocated = Column(Integer)
    total_available = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = Column(Boolean, default=False, nullable=False, server_default='0')


    # One-to-one relationship met Item (unidirectional)
    item = relationship("Item", foreign_keys=[item_id], primaryjoin="Inventory.item_id == Item.uid")

    '''
    # Many-to-many relationship met Location
    locations = relationship(
        "Location",
        secondary=inventory_location_association,
        primaryjoin="Inventory.id == inventory_location.c.inventory_id",
        secondaryjoin="Location.id == inventory_location.c.location_id",
        viewonly=True
    )
    '''
