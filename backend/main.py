from fastapi import FastAPI
from pydantic import BaseModel
from db import SessionLocal, Base, engine
from models import Email, Thread

# Create tables (only for dev, use Alembic in prod)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic schemas
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
            "Thank you for your email, we will respond soon.",
            "We have received your request, we are verifying.",
            "Your email has been taken into consideration."
        ],
        intent="informational",
        priority="low",
        summary=f"Automatic draft for: {email.subject}"
    )
