from typing import List, Tuple


RULES = {
    "forbidden_words": ["discount", "password", "confidential"],
}


def validate_drafts(drafts: List[str]) -> Tuple[List[str], float]:
    """
    Validate drafts against rules. Returns (valid_drafts, confidence).
    """
    valid = []
    for d in drafts:
        if any(w in d.lower() for w in RULES["forbidden_words"]):
            continue
        valid.append(d)
    confidence = 0.9 if valid else 0.0
    return valid, confidence


def fallback_template(subject: str) -> str:
    return f"Re: {subject}\n\nThank you for your message. We will get back to you soon."
