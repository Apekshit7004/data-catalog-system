# app/models/subcategory.py It defines the Subcategory model, which represents a subcategory in the database. 
# It includes fields for id, name, and a foreign key to the Category model. 
# The relationship between Subcategory and Category is established using SQLAlchemy's relationship function.

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Subcategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category")
    
    