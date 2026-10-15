import os

from docx import Document
from pypdf import PdfReader


def extract_text(upload):
    ext = os.path.splitext(upload.filename)[1].lower()
    if ext == ".docx":
        return "\n".join(p.text for p in Document(upload).paragraphs)
    if ext == ".pdf":
        return "\n".join(p.extract_text() for p in PdfReader(upload).pages)
    if ext in (".txt", ".md"):
        return upload.read().decode("utf-8")
    raise ValueError("Formato não suportado. Envie .docx, .pdf, .txt ou .md.")
