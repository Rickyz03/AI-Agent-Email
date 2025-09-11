from bs4 import BeautifulSoup
import re


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n")


def extract_text(body_html: str, body_plain: str = None) -> str:
    if body_plain:
        return body_plain
    return clean_html(body_html)


def remove_signatures_and_quotes(text: str) -> str:
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        if line.strip().startswith(">"):
            continue
        if line.strip().startswith("--"):
            break
        cleaned.append(line)
    return "\n".join(cleaned)


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
