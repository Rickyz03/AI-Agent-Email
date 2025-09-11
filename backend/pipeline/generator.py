from typing import List


def generate_drafts(subject: str, body: str, context: dict) -> List[str]:
    """
    Placeholder generator. Replace with LLM integration.
    """
    drafts = [
        f"Re: {subject}\n\nThank you for your email. We will review and reply shortly.",
        f"Re: {subject}\n\nWe have received your request and will provide an update soon.",
        f"Re: {subject}\n\nYour message has been noted. Expect our response in due course.",
    ]
    return drafts
