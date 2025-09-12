import datetime
from db import SessionLocal
from models import Event


def log_event(event_type: str, metadata: dict):
    """
    Save feedback events into DB.
    """
    db = SessionLocal()
    try:
        event = Event(
            event_type=event_type,
            ts=datetime.datetime.now(datetime.timezone.utc),
            event_metadata=metadata
        )
        db.add(event)
        db.commit()
    finally:
        db.close()
