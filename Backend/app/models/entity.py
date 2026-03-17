from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from datetime import datetime
from app.database import Base

class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    status = Column(String(50), default="active")
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
















    