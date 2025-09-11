from db import Base, engine, SessionLocal
from models import Thread, Email


def test_db_connection():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        thread = Thread(subject="Test Thread")
        db.add(thread)
        db.commit()
        db.refresh(thread)

        email = Email(
            thread_id=thread.id,
            from_addr="test@example.com",
            to_addrs=["dest@example.com"],
            body_text="Test body",
        )
        db.add(email)
        db.commit()
        db.refresh(email)

        assert email.thread_id == thread.id
        assert email.body_text == "Test body"
    finally:
        db.close()
