from chromadb import HttpClient
from utils.settings import settings

# Connect to Chroma server running in Docker
client = HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)

# Create or load collection
collection = client.get_or_create_collection("emails")


def add_embedding(id: str, embedding: list[float], metadata: dict):
    collection.add(ids=[id], embeddings=[embedding], metadatas=[metadata])


def search_embedding(query_emb: list[float], top_k: int = 5):
    results = collection.query(query_embeddings=[query_emb], n_results=top_k)
    return results.get("documents", [])
