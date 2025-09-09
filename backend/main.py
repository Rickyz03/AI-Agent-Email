from fastapi import FastAPI
from pydantic import BaseModel
from db import SessionLocal, Base, engine
from models import Email, Thread

# Crea le tabelle (solo per dev, in prod usa Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Schemi Pydantic
class EmailIn(BaseModel):
    thread_id: int
    subject: str
    body: str
    from_addr: str
    to_addrs: list[str]

class DraftOut(BaseModel):
    variants: list[str]
    intent: str
    priority: str
    summary: str

@app.get("/")
def root():
    return {"message": "AI Agent Email is running 🚀"}

@app.post("/draft", response_model=DraftOut)
def draft_email(email: EmailIn):
    # TODO: preprocess, classify, retrieve, generate, guardrails
    return DraftOut(
        variants=[
            "Grazie per la tua email, ti risponderemo presto.",
            "Abbiamo ricevuto la tua richiesta, stiamo verificando.",
            "La tua email è stata presa in carico."
        ],
        intent="informational",
        priority="low",
        summary=f"Bozza automatica per: {email.subject}"
    )
