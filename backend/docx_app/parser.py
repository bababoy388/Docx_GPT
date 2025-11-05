from docx import Document
from fastapi import UploadFile


def parser_docx(document: UploadFile):
    doc = Document(document.file)
    text = []
    for item in doc.paragraphs:
        text.append(item.text)
    return "\n".join(text)