from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.dialects.sqlite import JSON  # Optional for permissions
from datetime import datetime
from app.database import Base

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    permissions = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
