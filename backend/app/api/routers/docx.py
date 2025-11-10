from backend.docx_app.write_docx import write_docx
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from backend.app.core.config import config
from backend.docx_app.parser import parser_docx
from backend.docx_app.api_gpt import apigpt
from backend.app.crud.docx import docx_worker


router = APIRouter()

@router.post("/add-docx")
def add_docx(username: str, document: UploadFile = File(...)):
    docx_worker.set_docx(username, document)
    return {"message": "success"}

@router.post("/delete-docx")
def delete_docx(username: str, name_docx: str, type_docx: str):
    docx_worker.delete_docx(username, name_docx, type_docx)
    return {"message": "success"}

@router.post("/download-docx")
def download_docx(docx_name: str):
    path = config.DATA_DIR / "user_docx" / docx_name
    return FileResponse(path,
                        filename=docx_name,
                        media_type="application/vnd.openxmlformats.wordprocessingml.document"
                        )

@router.post("/ask")
def ask(text: str, username: str, docx_name: str, type_docx: str,
        create_docx: bool = False, include_docx: bool = False):

    if include_docx:
        pass # добавить проверку на наличие документа юзера

    docx_user = docx_worker.get_docx(username, docx_name, type_docx)
    read_docx = parser_docx(docx_user)
    message = read_docx + " " + text
    answer = apigpt(message)

    write_docx(answer, "D:\PyCharm\Project\Docx_GPT\\backend\data\\user_docx\CocoJambo\\user\Шаблон.docx")




