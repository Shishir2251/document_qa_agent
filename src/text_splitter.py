# src/text_splitter.py

def chunk_text(text, chunk_size=1500, overlap=300):
    """
    Split text into chunks for embeddings
    """
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks
