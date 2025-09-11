from typing import Tuple


def classify_intent_priority(text: str) -> Tuple[str, str]:
    """
    Very simple heuristic placeholder.
    Replace with ML/LLM model in production.
    """
    text_lower = text.lower()
    if "urgent" in text_lower or "asap" in text_lower:
        return "request", "high"
    if "thank" in text_lower:
        return "acknowledgment", "low"
    return "informational", "medium"
