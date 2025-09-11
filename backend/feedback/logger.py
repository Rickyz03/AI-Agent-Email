import datetime
from sqlalchemy.orm import Session
from models import Event


def log_event(db: Session, email_id: int, event_type: str, payload: dict = None):
    event = Event(
        email_id=email_id,
        type=event_type,
        payload=payload or {},
        created_at=datetime.datetime.utcnow(),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
