import re
from bs4 import BeautifulSoup


def preprocess_text(body: str) -> str:
    """
    Clean email body:
    - Strip HTML tags
    - Remove quoted replies and signatures
    - Normalize whitespace
    """
    # Remove HTML
    if "<html" in body.lower():
        soup = BeautifulSoup(body, "html.parser")
        body = soup.get_text()

    # Remove common signatures
    body = re.sub(r"--\s*\n.*", "", body, flags=re.DOTALL)

    # Remove quoted replies (lines starting with >)
    lines = [line for line in body.splitlines() if not line.strip().startswith(">")]
    body = "\n".join(lines)

    # Normalize whitespace
    body = re.sub(r"\s+", " ", body).strip()

    return body
