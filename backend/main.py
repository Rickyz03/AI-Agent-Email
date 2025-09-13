from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from langchain_openai import ChatOpenAI

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
from utils.settings import settings

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


# ----------------------
# Helper utilities
# ----------------------
def _ensure_list_of_str(maybe_list: Optional[Any]) -> List[str]:
    """
    Normalize possible values into a list of strings.
    Accepts: None, list[str], comma-separated string.
    """
    if not maybe_list:
        return []
    if isinstance(maybe_list, list):
        return [str(x) for x in maybe_list]
    if isinstance(maybe_list, str):
        # split by comma if present
        parts = [p.strip() for p in maybe_list.split(",") if p.strip()]
        return parts
    # fallback
    return [str(maybe_list)]


def _encrypt_addr_list(addrs: Optional[Any]) -> Optional[List[str]]:
    """
    Return list of encrypted addresses or None if empty.
    """
    lst = _ensure_list_of_str(addrs)
    if not lst:
        return None
    return [encrypt_data(a) for a in lst]


def _decrypt_addr_list(enc_list: Optional[List[str]]) -> List[str]:
    """
    Try to decrypt each element; if decryption fails, return original element.
    """
    if not enc_list:
        return []
    out = []
    for v in enc_list:
        try:
            out.append(decrypt_data(v))
        except Exception:
            # if it's not encrypted or decryption fails, return original
            out.append(v)
    return out


def _decrypt_single(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    try:
        return decrypt_data(value)
    except Exception:
        return value


# ----------------------
# Root
# ----------------------
@app.get("/")
def root():
    return {"message": "AI Agent Email is running 🚀"}


# ========== INGESTION ==========
@app.post("/ingest", response_model=List[EmailOut])
def ingest_emails(provider: str, db: Session = Depends(get_db)):
    """
    Fetch unread emails from IMAP/Gmail and save them into DB.
    Returns the saved emails (with decrypted addresses for output).
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
        # create or reuse thread (simple approach: always create new thread for now)
        thread = Thread(subject=msg.subject)
        db.add(thread)
        db.flush()  # assign thread.id

        # normalize to_addrs into list
        to_addrs_list = _ensure_list_of_str(msg.to_addrs)

        email_obj = Email(
            thread_id=thread.id,
            from_addr=encrypt_data(msg.from_addr) if msg.from_addr else None,
            to_addrs=_encrypt_addr_list(to_addrs_list),
            body_text=msg.body,
            language=getattr(msg, "language", "it"),
        )
        db.add(email_obj)
        db.flush()
        # collect for output (decrypt addresses)
        db.refresh(email_obj)
        saved_emails.append(email_obj)

    db.commit()

    # prepare decrypted output list matching EmailOut schema
    output_list = []
    for e in saved_emails:
        output_list.append({
            "id": e.id,
            "thread_id": e.thread_id,
            "subject": e.thread.subject if getattr(e, "thread", None) else None,
            "body_text": e.body_text,
            "from_addr": _decrypt_single(e.from_addr),
            "to_addrs": _decrypt_addr_list(e.to_addrs),
            "cc_addrs": _decrypt_addr_list(e.cc_addrs) if getattr(e, "cc_addrs", None) else [],
            "bcc_addrs": _decrypt_addr_list(e.bcc_addrs) if getattr(e, "bcc_addrs", None) else [],
            "ts": e.ts,
            "language": e.language,
            "intent": e.intent,
            "priority": e.priority,
            "attachments": e.attachments,
        })

    return output_list


# ========== DRAFT GENERATION ==========
@app.post("/draft", response_model=DraftOut)
def draft_email(email_in: EmailIn, db: Session = Depends(get_db)):
    """
    Generate AI-assisted drafts for a given email.
    This route now also persists the incoming email (addresses encrypted).
    """

    # --- inizializza LLM condiviso per questa request (creato una volta per request) ---
    llm = ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model_name=settings.OPENAI_MODEL_NAME,
    )
    # -------------------------------------------------------------------------------

    # Persist incoming email (encrypt sensitive fields)
    # If thread_id provided and exists, use it; otherwise create a new thread.
    thread_id = email_in.thread_id
    if thread_id:
        thread = db.query(Thread).filter(Thread.id == thread_id).first()
        if not thread:
            # create thread placeholder if referenced thread doesn't exist
            thread = Thread(subject=email_in.subject)
            db.add(thread)
            db.flush()
        thread_id = thread.id
    else:
        thread = Thread(subject=email_in.subject)
        db.add(thread)
        db.flush()
        thread_id = thread.id

    db_email = Email(
        thread_id=thread_id,
        from_addr=encrypt_data(email_in.from_addr) if email_in.from_addr else None,
        to_addrs=_encrypt_addr_list(email_in.to_addrs),
        cc_addrs=_encrypt_addr_list(email_in.cc_addrs) if email_in.cc_addrs else None,
        bcc_addrs=_encrypt_addr_list(email_in.bcc_addrs) if email_in.bcc_addrs else None,
        body_text=email_in.body,
        language=getattr(email_in, "language", "it"),
    )
    db.add(db_email)
    db.commit()
    db.refresh(db_email)

    # 1. Preprocess
    clean_body = preprocess_text(email_in.body)

    # 2. Classify
    intent, priority = classify_email(clean_body, llm)

    # 3. Retrieve context
    context = build_context(clean_body)

    # 4. Generate drafts
    drafts = generate_drafts(subject=email_in.subject, body=clean_body, context=context, llm=llm)

    # 5. Guardrails & fallback
    valid_drafts = validate_drafts(drafts)
    if not valid_drafts:
        valid_drafts = fallback_templates(email_in.subject)

    # 6. Log feedback placeholder (include email id)
    log_event(event_type="draft_generated", metadata={"email_id": db_email.id, "intent": intent, "priority": priority})

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
