# src/main.py
import argparse
import json
from pathlib import Path

from pdf_reader import load_pdfs
from text_splitter import chunk_text
from vector_store import VectorStore
from qa_agent import QAAgent

def ingest(pdfs_folder, index_path, chunks_path):
    print("\n🔍 Loading PDFs...")
    all_texts = []
    metas = []

    for path, text in load_pdfs(pdfs_folder):
        print(f"📄 Processing: {path}")
        chunks = chunk_text(text)
        for c in chunks:
            all_texts.append(c)
            metas.append({"source": path, "text": c})

    print(f"\n🧱 Total chunks: {len(all_texts)}")

    print("\n📦 Building vector store...")
    vs = VectorStore()
    vs.build(all_texts, metas, index_path=index_path)

    print("\n💾 Saving chunks...")
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(metas, f, ensure_ascii=False, indent=2)

    print("\n✅ Ingestion complete.")

def query_system(question, index_path, chunks_path):
    print("\n🔍 Loading vector index...")
    vs = VectorStore()
    vs.load(index_path)

    print("📄 Loading chunks...")
    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print("🔎 Retrieving relevant chunks...")
    results = vs.query(question, top_k=3)
    retrieved_chunks = [chunks[int(r["id"])] for r in results]

    print("🤖 Generating answer...")
    agent = QAAgent()
    answer = agent.answer(question, retrieved_chunks)
    print("\n=== ANSWER ===\n")
    print(answer)
    print("\n==============\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ingest", type=str, help="PDF folder path")
    parser.add_argument("--query", type=str, help="Question")
    parser.add_argument("--index-path", type=str, default="data/faiss.index")
    parser.add_argument("--chunks-path", type=str, default="data/chunks.json")

    args = parser.parse_args()

    if args.ingest:
        ingest(args.ingest, args.index_path, args.chunks_path)

    if args.query:
        query_system(args.query, args.index_path, args.chunks_path)
