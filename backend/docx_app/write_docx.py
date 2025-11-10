from docx import Document
from python_docx_replace import docx_replace


def write_docx(answer, template):
    doc = Document(template)
    print(answer)

    docx_replace(doc, **answer)
    doc.save("result.docx")

    return True
