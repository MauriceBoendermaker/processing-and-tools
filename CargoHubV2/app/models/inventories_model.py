from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

# many-to-many relatie voor inventory en locaties
inventory_location_association = Table(
    'inventory_location', Base.metadata,
    Column('inventory_id', Integer, ForeignKey('inventory.id'), primary_key=True),
    Column('location_id', Integer, ForeignKey('location.id'), primary_key=True)
)


class Inventory(Base):
    __tablename__ = 'inventories'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'), unique=True, nullable=False)
    description = Column(String, nullable=True)
    item_reference = Column(String, unique=True)
    total_on_hand = Column(Integer)
    total_expected = Column(Integer)
    total_ordered = Column(Integer)
    total_allocated = Column(Integer)
    total_available = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # One-to-one relationship met Item (unidirectional)
    item = relationship("Item")

    # Many-to-many relationship met Location
    locations = relationship(
        "Location",
        secondary=inventory_location_association,
        back_populates=None  # geen reverse relationship vanuit location
    )
