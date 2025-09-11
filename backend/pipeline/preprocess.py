from ingestion.parser import remove_signatures_and_quotes, normalize_whitespace


def preprocess_body(body: str) -> str:
    body = remove_signatures_and_quotes(body)
    body = normalize_whitespace(body)
    return body
