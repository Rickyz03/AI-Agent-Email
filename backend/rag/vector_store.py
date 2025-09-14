import chromadb
import json
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
    Normalize the metadata so that each value is compatible with Chroma.
    - If it is a primitive type (str, int, float, bool, None): leave it unchanged
    - If it is a dict or a list: convert it to a JSON string
    - Otherwise: convert it to a simple string
    """
    safe = {}
    for k, v in metadata.items():
        if isinstance(v, (str, int, float, bool)) or v is None:
            safe[k] = v
        elif isinstance(v, (dict, list)):
            safe[k] = json.dumps(v, ensure_ascii=False)  # JSON valido
        else:
            safe[k] = str(v)
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
