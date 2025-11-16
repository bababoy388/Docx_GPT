from sqlalchemy.orm import Session
from backend.app.models.user import Chat
from backend.app.schemas.user import LoginCreate
from backend.app.auth.auth import verify_password


def get_char(db: Session, username: str):
    return db.query(Chat).filter(Chat.name == username).first()

def get_chats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Chat).offset(skip).limit(limit).all()

def create_chat(db: Session, user: Chat): # Замени на схему
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_chat(db: Session, username: str):
    db_user = db.query(Chat).filter(Chat.name_chat == username).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user