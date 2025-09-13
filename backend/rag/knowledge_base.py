from rag.embeddings import embed_texts
from rag.vector_store import add_embedding
import uuid
from typing import List, Dict, Any

def index_documents(documents: List[Dict[str, Any]]):
    """
    Index a list of structured documents into the vector store.
    Each document should contain at least a 'text' field.
    Other optional fields: id, title, source.
    """
    # Take only the texts (mandatory)
    texts = [doc["text"] for doc in documents if "text" in doc]

    # Generate embeddings for the texts
    embeddings = embed_texts(texts)

    for doc, emb in zip(documents, embeddings):
        # If id is not provided, we create a new one
        doc_id = doc.get("id") or str(uuid.uuid4())

        metadata = {
            "title": doc.get("title"),
            "source": doc.get("source"),
            "text": doc["text"]
        }

        add_embedding(
            id=doc_id,
            embedding=emb,
            metadata=metadata
        )
