import requests
from utils.settings import settings

CHROMA_URL = settings.CHROMA_URL.rstrip("/")


def add_embedding(id: str, embedding: list[float], metadata: dict):
    """
    Add a new embedding into Chroma via REST API.
    """
    payload = {
        "ids": [id],
        "embeddings": [embedding],
        "metadatas": [metadata],
    }
    r = requests.post(f"{CHROMA_URL}/collections/emails/add", json=payload)
    r.raise_for_status()
    return r.json()


def search_embedding(query_emb: list[float], top_k: int = 5):
    """
    Search similar embeddings in Chroma via REST API.
    """
    payload = {"query_embeddings": [query_emb], "n_results": top_k}
    r = requests.post(f"{CHROMA_URL}/collections/emails/query", json=payload)
    r.raise_for_status()
    return r.json()
