from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.subcategory import Subcategory
from app.models.category import Category

router = APIRouter(
    prefix="/subcategories",
    tags=["Subcategories"]
)


# Create Subcategory
@router.post("/")
def create_subcategory(name: str, category_id: int, db: Session = Depends(get_db)):

    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    subcategory = Subcategory(
        name=name,
        category_id=category_id
    )

    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)

    return subcategory


# Get All Subcategories
@router.get("/")
def get_subcategories(db: Session = Depends(get_db)):

    subcategories = db.query(Subcategory).all()

    return subcategories


# Delete Subcategory
@router.delete("/{subcategory_id}")
def delete_subcategory(subcategory_id: int, db: Session = Depends(get_db)):

    subcategory = db.query(Subcategory).filter(
        Subcategory.id == subcategory_id
    ).first()

    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")

    db.delete(subcategory)
    db.commit()

    return {"message": "Subcategory deleted"}