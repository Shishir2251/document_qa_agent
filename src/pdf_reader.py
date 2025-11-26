# src/pdf_reader.py
import os
from pathlib import Path
from PyPDF2 import PdfReader

# Optional OCR
try:
    import pytesseract
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


def extract_text_from_pdf(path):
    """
    Extract text from PDF. If empty and OCR available, try OCR.
    """
    reader = PdfReader(str(path))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    if text.strip() == "" and OCR_AVAILABLE:
        # fallback to OCR
        images = convert_from_path(str(path))
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"

    return text


def load_pdfs(folder):
    """
    Generator to load PDFs and extract text
    """
    folder_path = Path(folder)
    for pdf_file in folder_path.glob("*.pdf"):
        text = extract_text_from_pdf(pdf_file)
        if text.strip():  # only yield if there is text
            yield str(pdf_file), text
