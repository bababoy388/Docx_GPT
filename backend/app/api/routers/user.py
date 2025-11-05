from fastapi import APIRouter, Depends
from backend.app.schemas.user import UserCreate, LoginCreate
from backend.app.crud.user import create_user
from backend.app.models.user import User
from backend.app.auth.auth import get_password_hash, create_access_token
from backend.app.crud.database import get_db
from sqlalchemy.orm import Session


router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hs_password = get_password_hash(user.password)

    db_user = User(
    name = user.name,
    password = hs_password,
    email = user.email,
    )

    create_user(db, db_user)

    return {"message": "success"}

@router.post("/login")
def login(user: LoginCreate, db: Session = Depends(get_db)): # Исправить, в токен передается пароль и сделать проверку юзера в бд
    data = dict(**user.model_dump())
    hs_password = get_password_hash(data["password"])

    data["password"] = hs_password

    access_token = create_access_token(data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "username": user.name,
        }
    }