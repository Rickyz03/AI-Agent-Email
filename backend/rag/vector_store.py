from chromadb import Client
from chromadb.config import Settings

# Initialize Chroma client
client = Client(Settings(persist_directory=".chroma"))

# Create or load collection
collection = client.get_or_create_collection("emails")


def add_embedding(id: str, embedding: list[float], metadata: dict):
    collection.add(ids=[id], embeddings=[embedding], metadatas=[metadata])


def search_embedding(query_emb: list[float], top_k: int = 5):
    results = collection.query(query_embeddings=[query_emb], n_results=top_k)
    return results.get("documents", [])
