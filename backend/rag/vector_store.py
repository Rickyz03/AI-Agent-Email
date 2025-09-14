import chromadb
from utils.settings import settings


# Inizializza il client Chroma
chroma_client = chromadb.HttpClient(
    host=settings.CHROMA_HOST,
    port=settings.CHROMA_PORT,
)

# Ottieni o crea la collezione
collection = chroma_client.get_or_create_collection(
    name=settings.CHROMA_COLLECTION
)


def add_embedding(id: str, embedding: list[float], metadata: dict):
    """
    Aggiunge un embedding a Chroma.
    """
    collection.add(
        ids=[id],
        embeddings=[embedding],
        metadatas=[metadata],
    )
    return {"status": "ok", "id": id}


def search_embedding(query_emb: list[float], top_k: int = 5):
    """
    Cerca embeddings simili in Chroma.
    """
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k,
    )
    return results
