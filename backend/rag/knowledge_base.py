from rag.embeddings import embed_texts
from rag.vector_store import add_embedding
import uuid


def index_documents(documents: list[str]):
    """
    Index a list of raw documents into the vector store.
    """
    embeddings = embed_texts(documents)

    for doc, emb in zip(documents, embeddings):
        add_embedding(
            id=str(uuid.uuid4()),
            embedding=emb,
            metadata={"text": doc}
        )
