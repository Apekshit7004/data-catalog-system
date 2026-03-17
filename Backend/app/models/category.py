from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)





    











