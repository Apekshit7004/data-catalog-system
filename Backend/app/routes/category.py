from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


# Create Category
@router.post("/")
def create_category(name: str, description: str = "", db: Session = Depends(get_db)):
    
    category = Category(
        name=name,
        description=description
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


# Get All Categories
@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories


# Duplicate Category Check
@router.post("/")
def create_category(name: str, description: str = "", db: Session = Depends(get_db)):

    existing_category = db.query(Category).filter(Category.name == name).first()

    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")

    category = Category(
        name=name,
        description=description
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category

# Get Single Category
@router.get("/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):

    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


# Delete Category
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):

    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()

    return {"message": "Category deleted"}

# Update Category
@router.put("/{category_id}")
def update_category(category_id: int, name: str, description: str = "", db: Session = Depends(get_db)):

    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.name = name
    category.description = description

    db.commit()
    db.refresh(category)

    return category

# Search Categories
@router.get("/search/")
def search_categories(query: str, db: Session = Depends(get_db)):

    categories = db.query(Category).filter(
        Category.name.ilike(f"%{query}%")
    ).all()

    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")

    return categories







