from typing import List
from utils.templates import fallback_templates


FORBIDDEN_WORDS = ["password", "credit card", "ssn"]


def validate_drafts(drafts: List[str]) -> List[str]:
    """
    Validate generated drafts:
    - Remove drafts containing forbidden words
    - Return safe list, or empty if all invalid
    """
    safe = []
    for draft in drafts:
        if not any(word in draft.lower() for word in FORBIDDEN_WORDS):
            safe.append(draft)
    return safe


def safe_or_fallback(drafts: List[str], subject: str) -> List[str]:
    """
    Return validated drafts, or fallback templates if none are safe.
    """
    valid = validate_drafts(drafts)
    if valid:
        return valid
    return fallback_templates(subject)
