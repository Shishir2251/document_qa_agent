# src/qa_agent.py
from transformers import pipeline
import torch

class QAAgent:
    def __init__(self, model_name="google/flan-t5-base"):
        device = 0 if torch.cuda.is_available() else -1
        self.pipe = pipeline("text2text-generation", model=model_name, device=device)

    def answer(self, question, chunks):
        context_text = "\n\n".join([c["text"] for c in chunks])
        prompt = f"""
You are a helpful assistant. Use the context below to answer the question.
Context:
{context_text}

Question: {question}
Answer in clear, concise language based only on the context.
If the answer is not present, reply 'I don't know.'
"""
        result = self.pipe(prompt, max_new_tokens=256, do_sample=False)
        return result[0]["generated_text"]
