from typing import List, Dict
from rag.vector_store import add_embedding
from rag.embeddings import embed_texts


def index_documents(docs: List[Dict]):
    """
    docs: [{"id": str, "title": str, "text": str}]
    """
    texts = [d["text"] for d in docs]
    embeddings = embed_texts(texts)
    for d, emb in zip(docs, embeddings):
        metadata = {"title": d["title"]}
        add_embedding(d["id"], emb, metadata)
