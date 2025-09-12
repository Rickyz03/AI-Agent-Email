from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict
import datetime


# ========== EMAIL ==========

class EmailIn(BaseModel):
    thread_id: Optional[int] = None
    subject: str
    body: str
    from_addr: EmailStr
    to_addrs: List[EmailStr]
    cc_addrs: Optional[List[EmailStr]] = []
    bcc_addrs: Optional[List[EmailStr]] = []
    attachments: Optional[List[Dict]] = None


class EmailOut(BaseModel):
    id: int
    thread_id: int
    subject: Optional[str]
    body_text: str
    from_addr: EmailStr
    to_addrs: List[EmailStr]
    cc_addrs: Optional[List[EmailStr]]
    bcc_addrs: Optional[List[EmailStr]]
    ts: datetime.datetime
    language: str
    intent: Optional[str]
    priority: Optional[str]
    attachments: Optional[List[Dict]]

    class Config:
        from_attributes = True


# ========== DRAFTS ==========

class DraftOut(BaseModel):
    variants: List[str]
    intent: str
    priority: str
    summary: str


# ========== PREFERENCES ==========

class PreferenceIn(BaseModel):
    tone: Optional[str] = "neutral"
    signature: Optional[str] = None
    language: Optional[str] = "it"


class PreferenceOut(BaseModel):
    id: int
    tone: str
    signature: Optional[str]
    language: str

    class Config:
        from_attributes = True


# ========== KNOWLEDGE BASE ==========

class KBIndexIn(BaseModel):
    documents: List[str] = Field(..., description="List of raw documents to index in KB")
