# app/models/column.py It defines the Column model, which represents a column in the database. 
# It includes fields for id, name, and a foreign key to the Subcategory model.
# The relationship between Column and Subcategory is established using SQLAlchemy's relationship function.
# The Column model is used to store information about the columns in a dataset, including the column name and the detected data type.
# The dataset_id field is a foreign key that links the column to a specific dataset, allowing for organization and retrieval of columns based on their associated dataset.

from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class DatasetColumn(Base):

    __tablename__ = "dataset_columns"

    id = Column(Integer, primary_key=True, index=True)

    dataset_id = Column(Integer, ForeignKey("datasets.id"))

    column_name = Column(String(255))

    detected_type = Column(String(100))

    Category = Column(String(100))




