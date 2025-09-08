from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, ARRAY
from sqlalchemy.orm import relationship
from .db import Base
import datetime

class Thread(Base):
    __tablename__ = "threads"
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String)
    first_ts = Column(DateTime, default=datetime.datetime.utcnow)
    last_ts = Column(DateTime, default=datetime.datetime.utcnow)

class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(Integer, ForeignKey("threads.id"))
    from_addr = Column(String)
    to_addrs = Column(ARRAY(String))
    ts = Column(DateTime, default=datetime.datetime.utcnow)
    body_text = Column(Text)
    language = Column(String, default="it")
    intent = Column(String, nullable=True)
    priority = Column(String, nullable=True)

    thread = relationship("Thread", back_populates="emails")

Thread.emails = relationship("Email", back_populates="thread")
