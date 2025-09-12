from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db import SessionLocal, Base, engine
from models import Email, Thread, Preference
from schemas import (
    EmailIn, EmailOut, DraftOut, PreferenceIn, PreferenceOut, KBIndexIn
)
from ingestion.imap_client import IMAPClient
from ingestion.gmail_api import GmailAPI
from pipeline.preprocess import preprocess_text
from pipeline.classifier import classify_email
from pipeline.retriever import build_context
from pipeline.generator import generate_drafts
from pipeline.guardrails import validate_drafts
from rag.knowledge_base import index_documents
from feedback.logger import log_event
from feedback.updater import update_preferences
from utils.templates import fallback_templates
from utils.security import encrypt_data, decrypt_data

# Create tables on startup (dev only; use Alembic in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Agent Email")


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


# ========== INGESTION ==========

@app.post("/ingest", response_model=List[EmailOut])
def ingest_emails(provider: str, db: Session = Depends(get_db)):
    """
    Fetch unread emails from IMAP/Gmail and save them into DB.
    """
    if provider == "imap":
        client = IMAPClient()
        messages = client.fetch_unseen()
    elif provider == "gmail":
        client = GmailAPI()
        messages = client.fetch_unread()
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    saved_emails = []
    for msg in messages:
        thread = Thread(subject=msg.subject)
        db.add(thread)
        db.flush()  # get thread.id

        email = Email(
            thread_id=thread.id,
            from_addr=msg.from_addr,
            to_addrs=msg.to_addrs,
            body_text=msg.body,
            language=msg.language,
        )
        db.add(email)
        saved_emails.append(email)

    db.commit()
    return saved_emails


# ========== DRAFT GENERATION ==========

@app.post("/draft", response_model=DraftOut)
def draft_email(email_in: EmailIn, db: Session = Depends(get_db)):
    """
    Generate AI-assisted drafts for a given email.
    """
    # 1. Preprocess
    clean_body = preprocess_text(email_in.body)

    # 2. Classify
    intent, priority = classify_email(clean_body)

    # 3. Retrieve context
    context = build_context(clean_body)

    # 4. Generate drafts
    drafts = generate_drafts(subject=email_in.subject, body=clean_body, context=context)

    # 5. Guardrails & fallback
    valid_drafts = validate_drafts(drafts)
    if not valid_drafts:
        valid_drafts = fallback_templates(email_in.subject)

    # 6. Log feedback placeholder
    log_event(event_type="draft_generated", metadata={"intent": intent, "priority": priority})

    return DraftOut(
        variants=valid_drafts,
        intent=intent,
        priority=priority,
        summary=f"Draft for: {email_in.subject}"
    )


# ========== KNOWLEDGE BASE ==========

@app.post("/kb/index")
def kb_index(data: KBIndexIn):
    """
    Index documents into the Knowledge Base.
    """
    index_documents(data.documents)
    return {"status": "indexed", "count": len(data.documents)}


# ========== PREFERENCES ==========

@app.post("/preferences", response_model=PreferenceOut)
def set_preferences(pref: PreferenceIn, db: Session = Depends(get_db)):
    """
    Update user preferences (tone, signature, etc.).
    """
    updated = update_preferences(db, pref)
    db.commit()
    return updated


@app.get("/preferences", response_model=PreferenceOut)
def get_preferences(db: Session = Depends(get_db)):
    """
    Get current user preferences.
    """
    pref = db.query(Preference).first()
    if not pref:
        raise HTTPException(status_code=404, detail="Preferences not set")
    return pref


# ========== FEEDBACK ==========

@app.post("/feedback")
def feedback(event_type: str, metadata: dict):
    """
    Log user feedback (draft accepted, edited, rejected).
    """
    log_event(event_type=event_type, metadata=metadata)
    return {"status": "logged"}
