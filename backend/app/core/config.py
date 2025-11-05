from pathlib import Path
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

    SECRET_KEY = "SECRET_KEY"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 1

config = Settings()
