from rag.embeddings import embed_text
from rag.vector_store import search_embedding


def build_context(body: str, top_k: int = 3) -> str:
    """
    Build context for draft generation:
    - Create embedding of email body
    - Retrieve similar docs/emails from vector store
    - Concatenate results as context
    """
    query_emb = embed_text(body)
    results = search_embedding(query_emb, top_k=top_k)

    contexts = []
    for doc in results.get("documents", [[]])[0]:
        contexts.append(doc)

    return "\n\n".join(contexts)
