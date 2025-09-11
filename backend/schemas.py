from pydantic import BaseModel
from typing import List, Optional
import datetime


class EmailIn(BaseModel):
    thread_id: int
    subject: str
    body: str
    from_addr: str
    to_addrs: List[str]
    cc_addrs: Optional[List[str]] = None
    bcc_addrs: Optional[List[str]] = None


class DraftOut(BaseModel):
    variants: List[str]
    intent: str
    priority: str
    summary: str
    confidence: float


class EmailOut(BaseModel):
    id: int
    thread_id: int
    from_addr: str
    to_addrs: List[str]
    ts: datetime.datetime
    body_text: str
    language: str
    intent: Optional[str]
    priority: Optional[str]

    class Config:
        orm_mode = True


class ThreadOut(BaseModel):
    id: int
    subject: Optional[str]
    first_ts: datetime.datetime
    last_ts: datetime.datetime
    emails: List[EmailOut]

    class Config:
        orm_mode = True
