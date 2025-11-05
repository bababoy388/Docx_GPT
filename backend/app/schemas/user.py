from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class LoginCreate(BaseModel):
    name: str
    password: str