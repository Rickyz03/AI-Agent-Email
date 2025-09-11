from pipeline.preprocess import preprocess_body
from pipeline.classifier import classify_intent_priority
from pipeline.generator import generate_drafts
from pipeline.guardrails import validate_drafts


def test_preprocess():
    text = "Hello\n-- \nSignature\n> quoted text"
    clean = preprocess_body(text)
    assert "Signature" not in clean
    assert "quoted text" not in clean


def test_classifier():
    intent, priority = classify_intent_priority("This is urgent")
    assert priority == "high"


def test_generator():
    drafts = generate_drafts("Subject", "Body", {"summary": "context"})
    assert isinstance(drafts, list)
    assert len(drafts) > 0


def test_guardrails():
    drafts = ["This contains a password", "This is safe"]
    valid, confidence = validate_drafts(drafts)
    assert all("password" not in d.lower() for d in valid)
    assert 0.0 <= confidence <= 1.0
