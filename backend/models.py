from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, ARRAY, JSON
from sqlalchemy.orm import relationship
from db import Base
import datetime


class Thread(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=True)
    first_ts = Column(DateTime, default=datetime.datetime.utcnow)
    last_ts = Column(DateTime, default=datetime.datetime.utcnow)

    emails = relationship("Email", back_populates="thread")


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(Integer, ForeignKey("threads.id"))
    from_addr = Column(String, nullable=False)
    to_addrs = Column(ARRAY(String), nullable=False)
    cc_addrs = Column(ARRAY(String), nullable=True)
    bcc_addrs = Column(ARRAY(String), nullable=True)
    ts = Column(DateTime, default=datetime.datetime.utcnow)
    body_text = Column(Text, nullable=False)
    body_html = Column(Text, nullable=True)
    attachments = Column(JSON, nullable=True)
    language = Column(String, default="it")
    intent = Column(String, nullable=True)
    priority = Column(String, nullable=True)

    thread = relationship("Thread", back_populates="emails")


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    tone_default = Column(String, default="standard")
    sign_off = Column(String, default="Cordiali saluti")
    signature_block = Column(Text, nullable=True)
    blacklist_words = Column(ARRAY(String), default=[])


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id"))
    type = Column(String, nullable=False)
    payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
