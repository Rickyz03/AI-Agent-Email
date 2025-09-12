from pipeline.preprocess import preprocess_text
from pipeline.classifier import classify_email
from pipeline.guardrails import validate_drafts


def test_preprocess_text():
    raw = "<html><body>Hello<br>--\nSignature</body></html>"
    cleaned = preprocess_text(raw)
    assert "Signature" not in cleaned
    assert "<html>" not in cleaned


def test_classify_email():
    body = "This is urgent! Please fix it ASAP"
    intent, priority = classify_email(body)
    assert intent == "request"
    assert priority == "high"


def test_guardrails_removes_sensitive():
    drafts = ["Here is my password 1234", "All good"]
    safe = validate_drafts(drafts)
    assert len(safe) == 1
    assert "password" not in safe[0].lower()
