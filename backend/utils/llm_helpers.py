import json
from typing import Any, Dict, Optional


def extract_text_from_llm(response: Any) -> str:
    """
    Extracts plain text content from an LLM response.
    Handles both LangChain and raw OpenAI-style responses.
    """
    if hasattr(response, "content"):
        return response.content
    if hasattr(response, "response_metadata"):
        # LangChain ChatResult
        try:
            return response.content
        except Exception:
            pass
    if isinstance(response, dict) and "choices" in response:
        return response["choices"][0]["message"]["content"]
    return str(response)


def try_parse_json_only(response_text: str) -> Optional[Dict]:
    """
    Attempts to parse JSON safely from LLM text output.
    Returns dict if successful, None otherwise.
    """
    try:
        return json.loads(response_text)
    except (json.JSONDecodeError, TypeError):
        return None
