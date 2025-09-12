from typing import List


def generate_drafts(subject: str, body: str, context: str) -> List[str]:
    """
    Generate draft replies.
    TODO: integrate with LLM (OpenAI / Anthropic / local model).
    """
    base = f"Re: {subject}\n\n"

    variants = [
        base + "Thank you for your email. We will get back to you shortly.",
        base + "We acknowledge receipt of your message and are reviewing it.",
        base + "Your request has been logged and will be handled soon.",
    ]

    if context:
        variants = [v + f"\n\n(Context: {context[:200]}...)" for v in variants]

    return variants
