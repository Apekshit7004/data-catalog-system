from fastapi import FastAPI
from app.routes import category
from app.routes import subcategory
from app.database import engine
from app.models import user  # make sure models package has __init__.py
from app.routes import auth
from app.routes import dataset

# Create FastAPI app
app = FastAPI(
    title="Data Classification System API",
    version="1.0.0"
)

# Create database tables
user.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(category.router)
app.include_router(subcategory.router)
app.include_router(dataset.router)

# Optional health check route
@app.get("/")

def root():
    return {"message": "API is running successfully 🚀"}

