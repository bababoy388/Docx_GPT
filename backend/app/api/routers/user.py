import os
from fastapi import APIRouter, Depends
from backend.app.schemas.user import UserCreate, LoginCreate
from backend.app.crud.user import create_user
from backend.app.models.user import User
from backend.app.auth.auth import get_password_hash, create_access_token
from backend.app.crud.database import get_db
from sqlalchemy.orm import Session
from backend.app.core.config import config
from backend.app.crud.user import get_user, auth_user
from fastapi import Form

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    user_db = get_user(db, user.name)
    if user_db:
        return {"message": "This username is occupied"}

    hs_password = get_password_hash(user.password)

    db_user = User(
    name = user.name,
    password = hs_password,
    email = user.email,
    )

    os.mkdir(config.DATA_DIR / "user_docx" / user.name)
    os.mkdir(config.DATA_DIR / "user_docx" / user.name / "user")
    os.mkdir(config.DATA_DIR / "user_docx" / user.name / "gpt")

    create_user(db, db_user)

    return {"message": "success"}


@router.post("/login")
def login(
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    user_data = LoginCreate(name=username, password=password)

    if not auth_user(db, user_data):
        return {"message": "Error"}

    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}