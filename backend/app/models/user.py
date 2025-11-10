from sqlalchemy import Column, Integer, String, DateTime
from backend.app.crud.database import Base
from datetime import datetime, UTC


class User(Base):
    __tablename__  = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    password = Column(String)
    email = Column(String)

class Chat(Base):
    __tablename__ = "chats"

    id = Column(String, primary_key=True)
    name_chat = Column(String)

class ChatMessage(Base):
    __tablename__ = "chat_message"

    id = Column(Integer, primary_key=True)
    id_chat = Column(String)
    message = Column(String)
    role = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))