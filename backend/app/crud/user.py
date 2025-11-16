from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.app.schemas.user import LoginCreate
from backend.app.auth.auth import verify_password


def get_user(db: Session, username: str):
    return db.query(User).filter(User.name == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def auth_user(db: Session, user_login: LoginCreate):
    user = get_user(db, user_login.name)
    if not user:
        return False
    hash_password = user.password
    if verify_password(user_login.password, hash_password):
        return True
    return False

def create_user(db: Session, user: User): # Замени на схему
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, username: str):
    db_user = db.query(User).filter(User.name_chat == username).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user