TEMPLATES = {
    "default": "Thank you for your email. We will get back to you shortly.",
    "ask_clarification": "Could you please clarify the details of your request?",
    "fallback": "We have received your message and will provide a response soon.",
}


def get_template(name: str) -> str:
    return TEMPLATES.get(name, TEMPLATES["default"])
