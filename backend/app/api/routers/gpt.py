from pyexpat.errors import messages

from backend.docx_app.write_docx import write_docx
from fastapi import APIRouter, Depends, Request
from backend.docx_app.parser import parser_docx
from backend.docx_app.api_gpt import apigpt
from backend.app.crud.docx import docx_worker
from sqlalchemy.orm import Session
from backend.app.models.user import Chat
from backend.app.crud.database import get_db
from backend.app.auth.auth import get_current_user
from backend.app.crud.user import get_user
from backend.app.crud.chat import delete_chat, get_chats
from backend.app.models.user import ChatMessage


router = APIRouter()

@router.post("/ask")
def ask(
        id_chat: int,
        message: str,
        username: str,
        docx_name: str,
        type_docx: str,
        create_docx: bool = False,
        include_docx: bool = False,
        db = Depends(get_db)
):
    if not create_docx:
        message_user = ChatMessage(
            id_chat=id_chat,
            message=message,
            role="user"
        )

        db.add(message_user)
        db.commit()
        db.refresh(message_user)

        answer = apigpt(message)
        if isinstance(answer, dict): # исправить чтобы передавалось нормальное сообщение gpt
            answer = str(answer)

        message_gpt = ChatMessage(
            id_chat=id_chat,
            message=answer,
            role="gpt"
        )

        db.add(message_gpt)
        db.commit()
        db.refresh(message_gpt)

        return answer

    if include_docx:
        pass # добавить проверку на наличие документа юзера

    docx_user = docx_worker.get_docx(username, docx_name, type_docx)
    read_docx = parser_docx(docx_user)
    message = read_docx + " " + message
    answer = apigpt(message)

    write_docx(answer, "D:\PyCharm\Project\Docx_GPT\\backend\data\\user_docx\CocoJambo\\user\Шаблон.docx")

@router.post("/create_chat")
async def create_chat(
    name_chat: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user_db = get_user(db, current_user)
    user_id = user_db.id

    chat = Chat(
        user_id=user_id,
        name_chat=name_chat
    )

    db.add(chat)
    db.commit()
    return {"message": "success"}

@router.post("/delete_chat")
def delete_char(name_chat: str, db: Session = Depends(get_db)):
    delete_chat(db, name_chat)
    return {"message": "success"}

@router.get("/chats")
def get_chats_user(db: Session = Depends(get_db)):
    data = get_chats(db)
    return data




