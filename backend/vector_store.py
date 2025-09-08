from chromadb import Client
from chromadb.config import Settings

# Inizializza client Chroma
client = Client(Settings(
    persist_directory=".chroma"  # cartella locale dove salvare il DB vettoriale
))

# Crea una collection (se non esiste)
collection = client.get_or_create_collection("emails")

def add_embedding(id: str, embedding: list[float], metadata: dict):
    collection.add(
        ids=[id],
        embeddings=[embedding],
        metadatas=[metadata]
    )

def search_embedding(query_emb: list[float], top_k: int = 5):
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k
    )
    return results
