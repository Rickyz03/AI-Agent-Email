from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db import SessionLocal, Base, engine
from models import Email, Thread
from schemas import EmailIn, DraftOut
from pipeline.preprocess import preprocess_body
from pipeline.classifier import classify_intent_priority
from pipeline.retriever import build_context
from pipeline.generator import generate_drafts
from pipeline.guardrails import validate_drafts, fallback_template

# Create tables in dev (use Alembic in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Agent Email", version="1.0.0")


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "AI Agent Email is running 🚀"}


@app.post("/draft", response_model=DraftOut)
def draft_email(email: EmailIn, db: Session = Depends(get_db)):
    clean_body = preprocess_body(email.body)
    intent, priority = classify_intent_priority(clean_body)
    context = build_context(thread_id=email.thread_id, db=db)
    drafts = generate_drafts(subject=email.subject, body=clean_body, context=context)
    drafts, confidence = validate_drafts(drafts)

    if not drafts:
        drafts = [fallback_template(subject=email.subject)]

    return DraftOut(
        variants=drafts,
        intent=intent,
        priority=priority,
        summary=context.get("summary", ""),
        confidence=confidence,
    )
