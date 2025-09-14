from rag.embeddings import embed_texts
from rag.vector_store import add_embedding
import uuid
from typing import List, Dict, Any
import json


def index_documents(documents: List[Dict[str, Any]]):
    """
    Index a list of structured documents into the vector store.
    Each document should contain at least a 'text' field.
    Other optional fields: id, title, source.
    """
    # Extract the required texts
    texts = [doc["text"] for doc in documents if "text" in doc]

    # Generate embeddings
    embeddings = embed_texts(texts)

    for doc, emb in zip(documents, embeddings):
        # Document ID
        doc_id = doc.get("id") or str(uuid.uuid4())

        # Build normalized metadata
        metadata: Dict[str, Any] = {}

        if "title" in doc and doc["title"] is not None:
            metadata["title"] = str(doc["title"])

        if "source" in doc and doc["source"] is not None:
            if isinstance(doc["source"], (dict, list)):
                metadata["source"] = json.dumps(doc["source"], ensure_ascii=False)
            else:
                metadata["source"] = str(doc["source"])

        # Text always included
        metadata["text"] = doc["text"]

        # Add embedding to Chroma
        add_embedding(
            id=doc_id,
            embedding=emb,
            metadata=metadata
        )
