
A simple AI-powered **Document Question & Answering Agent**.
Upload PDFs (digital or scanned), build a searchable index, and ask questions. The agent retrieves relevant chunks using **FAISS embeddings** and generates answers using a **small LLM** (`google/flan-t5-base` by default).

This project is designed as a **learning-purpose AI agent** and works for both:

* **Digital PDFs** (text-based, selectable text)
* **Scanned PDFs** (image-based, via OCR using `pytesseract` and `pdf2image`)

It also works with **small PDFs** like bank statements.

---

## Features

* PDF ingestion and text extraction (with optional OCR)
* Chunking with overlap for context preservation
* FAISS vector store for semantic search
* LLM-based answer generation (`flan-t5-base`)
* Works for both **short** and **long PDFs**
* Easy command-line interface

---

## Folder Structure

```
document_qa_agent/
├─ src/
│  ├─ main.py           # Entry point for ingestion and query
│  ├─ pdf_reader.py     # PDF text extraction + optional OCR
│  ├─ text_splitter.py  # Text chunking
│  ├─ vector_store.py   # FAISS vector storage
│  └─ qa_agent.py       # LLM for answer generation
├─ data/
│  ├─ pdfs/             # Place all PDFs here
│  ├─ faiss.index       # Saved FAISS index (after ingestion)
│  └─ chunks.json       # JSON with text chunks metadata
├─ agentenv/            # Python virtual environment
└─ README.md
```

---

## Setup Instructions

### 1. Clone / Navigate to Project

```powershell
cd C:\Users\shish\Projects\document_qa_agent
```

### 2. Create Virtual Environment

```powershell
python -m venv agentenv
.\agentenv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install --upgrade pip
pip install PyPDF2 sentence-transformers faiss-cpu transformers torch tqdm pdf2image pytesseract pillow
```

* If using **scanned PDFs**, also install Tesseract OCR: [Tesseract Installation](https://github.com/tesseract-ocr/tesseract)

---

## 4. Prepare PDFs

Place your PDF files in:

```
data/pdfs/
```

* **Digital PDFs**: text must be selectable
* **Scanned PDFs**: OCR will extract text automatically
* **Small PDFs**: one chunk is enough; the agent will still answer questions

---

## 5. Ingest PDFs (Build Index)

```powershell
python src/main.py --ingest data/pdfs/ --index-path data/faiss.index --chunks-path data/chunks.json
```

Output example:

```
🔍 Loading PDFs...
📄 Processing: data/pdfs/bank_statement.pdf
🧱 Total chunks: 1
📦 Building vector store...
💾 Saving chunks...
✅ Ingestion complete.
```

* For **short PDFs**, you may have only 1 chunk.
* For **long PDFs**, text is split into overlapping chunks for better context.

---

## 6. Ask Questions

```powershell
python src/main.py --query "What is the account number?" --index-path data/faiss.index --chunks-path data/chunks.json
```

Output:

```
=== ANSWER ===

Account number is 123456789

==============
```

Tips:

* Ask questions **related to the text actually in the PDF**.
* For tiny PDFs (like bank statements), use **specific questions** instead of "main idea of chapter 2".

---

## 7. Notes & Troubleshooting

* **“I don't know”** usually means:

  1. The answer is not in the PDF chunks
  2. PDF text wasn’t extracted (scanned PDF without OCR)
  3. Question is unrelated to PDF content

* **Check extracted text**:

```python
from src.pdf_reader import load_pdfs

for path, text in load_pdfs("data/pdfs/"):
    print(path, len(text))
```

* **Check retrieved chunks** before asking:

```python
for c in retrieved_chunks:
    print(c["text"])
```

* **Chunk size & overlap** can be adjusted in `text_splitter.py`:

```python
chunk_size = 1500  # default
overlap = 300      # default
```

* **LLM choice**: `flan-t5-base` is CPU-friendly; for large PDFs or complex questions, consider `flan-t5-large` (GPU recommended).

* Windows users may see **symlink warnings** from `huggingface_hub`. Safe to ignore or run Python as admin.

---

## 8. Optional Improvements

* Add **FastAPI** to make a web-based Q/A app
* Store **conversation history** for multi-turn Q/A
* Use **larger LLMs** or **GPU** for better comprehension
* Integrate **logging** to debug retrieved chunks and answers

---

## 9. References

* [PyPDF2 Documentation](https://pypi.org/project/PyPDF2/)
* [FAISS](https://faiss.ai/)
* [Sentence Transformers](https://www.sbert.net/)
* [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
* [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

---

## 10. Author / Learning Notes

* Built for **learning AI agents** with Python
* Demonstrates **PDF ingestion → semantic search → LLM-based Q/A**
* Works on both **short and long documents**
* Supports **OCR for scanned PDFs**
