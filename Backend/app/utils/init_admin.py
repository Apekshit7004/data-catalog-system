from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password


def create_default_admin(db: Session):

    admin = db.query(User).filter(User.username == "admin").first()

    if not admin:
        new_admin = User(
            username="admin",
            email="admin@example.com",
            password=hash_password("admin123"),
            role="SUPER_ADMIN"
        )

        db.add(new_admin)
        db.commit()

        print("✅ Default admin user created")

    else:
        print("ℹ️ Admin already exists")