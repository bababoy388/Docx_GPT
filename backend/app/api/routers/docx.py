from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from backend.app.core.config import config
import shutil
import os


router = APIRouter()

@router.post("/add-docx")
def add_docx(document: UploadFile = File(...)):
    with open(config.DATA_DIR / "user_docx" / "TEST.docx", "wb") as f:
        shutil.copyfileobj(document.file, f)
    return {"message": "success"}

@router.post("/delete-docx")
def delete_docx(docx_name: str):
    os.remove(config.DATA_DIR / "user_docx" / docx_name)
    return {"message": "success"}

@router.post("/download-docx")
def download_docx(docx_name: str):
    path = config.DATA_DIR / "user_docx" / docx_name
    return FileResponse(path,
                        filename=docx_name,
                        media_type="application/vnd.openxmlformats.wordprocessingml.document"
                        )

@router.post("/ask")
def ask(text: str, create_docx: bool = False):
    pass

