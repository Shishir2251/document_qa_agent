# src/pdf_reader.py
import os
from PyPDF2 import PdfReader

def extract_text_from_pdf(path: str) -> str:
    """Extracts text from a single PDF file."""
    reader = PdfReader(path)
    texts = []
    for page in reader.pages:
        try:
            t = page.extract_text()
            if t:
                texts.append(t)
        except Exception:
            continue
    return "\n".join(texts)

def load_pdfs(folder: str):
    """Yield tuples (filepath, text)."""
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(".pdf"):
                path = os.path.join(root, f)
                yield path, extract_text_from_pdf(path)
