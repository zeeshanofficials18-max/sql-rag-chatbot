from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_faiss_index(texts):
    embeddings = model.encode(texts)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    return index

def retrieve_docs(query, texts, index, k=3):
    query_embedding = model.encode([query])
    _, indices = index.search(np.array(query_embedding), k)
    return [texts[i] for i in indices[0]]
