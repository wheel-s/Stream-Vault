import os
from werkzeug.utils import secure_filename
from docx import Document
from PyPDF2 import PdfReader



allowed_ext = ["pdf","docx","png","jpg","jpeg","avif","webp","mp4","mov","avi"]


def allowed_file(filename):
    return '.' in filename and filename.rsplit(".", 1)[1].lower() in allowed_ext

def save_file(file, upload_folder):
    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.stream.seek(0)
    file.save(filepath)
    return filename, filepath


def read_docx(filepath):
    doc = Document(filepath)
    return "\n".join([p.text for p in doc.paragraphs])

def read_pdf(filepath):
  
    reader = PdfReader(filepath)
    pages = [page.extract_text() or "" for page in reader.pages]
    return '\n'.join(pages).strip()
