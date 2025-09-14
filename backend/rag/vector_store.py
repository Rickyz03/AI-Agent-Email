import chromadb
from utils.settings import settings

# Initialize the Chroma client
chroma_client = chromadb.HttpClient(
    host=settings.CHROMA_HOST,
    port=settings.CHROMA_PORT,
)

# Get or create the collection
collection = chroma_client.get_or_create_collection(
    name=settings.CHROMA_COLLECTION
)


def sanitize_metadata(metadata: dict) -> dict:
    """
    Normalize metadata so that every value is a primitive JSON-serializable type.
    Non-primitive values are converted to their string representation.
    """
    safe = {}
    for k, v in metadata.items():
        if isinstance(v, (str, int, float, bool)) or v is None:
            safe[k] = v
        else:
            safe[k] = str(v)  # fallback: serialize to string
    return safe


def add_embedding(id: str, embedding: list[float], metadata: dict):
    """
    Add an embedding to Chroma.
    """
    metadata = sanitize_metadata(metadata)

    collection.add(
        ids=[id],
        embeddings=[embedding],
        metadatas=[metadata],
    )
    return {"status": "ok", "id": id}


def search_embedding(query_emb: list[float], top_k: int = 5):
    """
    Search for similar embeddings in Chroma.
    """
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k,
    )
    return results
