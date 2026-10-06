from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import User, Order, OrderItem

def create_user(db: Session, name: str, email: str) -> User:
    db_user = User(name=name, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.scalars(stmt).first()