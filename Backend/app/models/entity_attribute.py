from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class EntityAttribute(Base):
    __tablename__ = "entity_attributes"

    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, ForeignKey("entities.id"))
    attribute_name = Column(String(100), nullable=False)
    attribute_value = Column(String(500))
    data_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
















    