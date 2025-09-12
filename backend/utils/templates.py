from typing import List


def fallback_templates(subject: str) -> List[str]:
    """
    Provide safe fallback email drafts.
    """
    base = f"Re: {subject}\n\n"
    return [
        base + "Thank you for reaching out. We will reply as soon as possible.",
        base + "Your email has been received and is being reviewed.",
        base + "We acknowledge your request and will get back to you shortly.",
    ]
