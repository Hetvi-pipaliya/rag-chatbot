import json
import os
import numpy as np
import hashlib
from config import settings

VECTOR_FILE = "vectors.json"

def get_embedding(text: str) -> list:
    hash_val = hashlib.md5(text.encode()).hexdigest()
    np.random.seed(int(hash_val[:8], 16) % (2**31))
    return np.random.rand(384).tolist()

def load_data():
    if os.path.exists(VECTOR_FILE):
        with open(VECTOR_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(VECTOR_FILE, "w") as f:
        json.dump(data, f)

def add_chunks_to_vectorstore(chunks: list, doc_name: str) -> int:
    data = load_data()
    for i, chunk in enumerate(chunks):
        data.append({
            "id": f"{doc_name}_chunk_{i}",
            "text": chunk,
            "source": doc_name,
            "embedding": get_embedding(chunk)
        })
    save_data(data)
    return len(chunks)

def search_relevant_chunks(query: str, n_results: int = 4) -> tuple:
    data = load_data()
    if not data:
        return [], []
    query_emb = np.array(get_embedding(query))
    scores = []
    for item in data:
        emb = np.array(item["embedding"])
        score = np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb))
        scores.append((score, item))
    scores.sort(key=lambda x: x[0], reverse=True)
    top = scores[:n_results]
    chunks = [item["text"] for _, item in top]
    sources = [{"source": item["source"]} for _, item in top]
    return chunks, sources