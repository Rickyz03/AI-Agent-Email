from sqlalchemy.orm import Session
from models import Thread, Email
from rag.vector_store import search_embedding
from rag.embeddings import embed_text


def build_context(thread_id: int, db: Session):
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if not thread:
        return {"summary": "", "emails": []}

    emails = (
        db.query(Email)
        .filter(Email.thread_id == thread_id)
        .order_by(Email.ts.asc())
        .all()
    )

    summary = f"Thread: {thread.subject} ({len(emails)} messages)"
    body_concat = " ".join([e.body_text for e in emails if e.body_text])

    query_emb = embed_text(body_concat)
    kb_results = search_embedding(query_emb, top_k=3)

    return {
        "summary": summary,
        "emails": [e.body_text for e in emails],
        "kb_chunks": kb_results,
    }
