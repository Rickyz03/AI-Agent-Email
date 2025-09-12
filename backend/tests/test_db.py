import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base
from models import Thread, Email


@pytest.fixture(scope="function")
def test_db():
    """
    Use SQLite in-memory DB for fast, isolated testing.
    """
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_insert_thread_and_email(test_db):
    thread = Thread(subject="Test thread")
    test_db.add(thread)
    test_db.flush()

    email = Email(
        thread_id=thread.id,
        from_addr="sender@example.com",
        to_addrs=["receiver@example.com"],
        body_text="Hello test",
        language="en"
    )
    test_db.add(email)
    test_db.commit()

    saved_thread = test_db.query(Thread).first()
    saved_email = test_db.query(Email).first()

    assert saved_thread.subject == "Test thread"
    assert saved_email.from_addr == "sender@example.com"
    assert saved_email.thread_id == saved_thread.id
