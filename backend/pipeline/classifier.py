from typing import Tuple


def classify_email(body: str) -> Tuple[str, str]:
    """
    Very simple heuristic classifier.
    Returns (intent, priority).
    TODO: replace with ML/LLM model.
    """
    text = body.lower()

    if "urgent" in text or "asap" in text:
        return "request", "high"
    if "complaint" in text or "problem" in text:
        return "complaint", "medium"
    if "unsubscribe" in text or "spam" in text:
        return "spam", "low"
    return "informational", "low"
