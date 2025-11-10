import os
from io import BytesIO
from fastapi import UploadFile, File
import shutil
from backend.app.core.config import config


class CrudDocx:
    def get_docx(self, username, name_docx, type_docx):
        file_path = config.DATA_DIR / "user_docx" / username / type_docx / name_docx
        with open(file_path, "rb") as f:
            file_content = f.read()

        docx_user = BytesIO(file_content)

        upload_file = UploadFile(
            filename="TEST.docx",
            file=docx_user
        )

        return upload_file

    def set_docx(self, username, document: UploadFile = File(...)):
        with open(config.DATA_DIR / "user_docx" / username / "user" / "TEST.docx", "wb") as f:
            shutil.copyfileobj(document.file, f)

        return True

    def delete_docx(self, username, name_docx, type_docx):
        os.remove(config.DATA_DIR / "user_docx" / username / type_docx / name_docx)

        return True

    def replace_docx(self, username, name_docx, type_docx):
        self.delete_docx(username, name_docx, type_docx)
        self.get_docx(username, name_docx, type_docx)

        return True

docx_worker = CrudDocx()
