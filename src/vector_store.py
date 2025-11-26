# src/vector_store.py
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self, embed_model="sentence-transformers/all-MiniLM-L6-v2"):
        self.embed_model_name = embed_model
        self.model = SentenceTransformer(embed_model)
        self.index = None
        self.metas = []

    def build(self, texts, metas, index_path="data/faiss.index"):
        if len(texts) == 0:
            raise ValueError("No texts provided to build the index.")
        self.metas = metas
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)
        faiss.write_index(self.index, index_path)

    def load(self, index_path="data/faiss.index"):
        self.index = faiss.read_index(index_path)

    def query(self, query_text, top_k=3):
        embedding = self.model.encode([query_text], convert_to_numpy=True)
        D, I = self.index.search(embedding, top_k)
        results = [{"id": i, "distance": float(d)} for i, d in zip(I[0], D[0])]
        return results
