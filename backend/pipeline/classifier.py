from typing import Tuple, Any
import json
import re

from langchain.schema import SystemMessage, HumanMessage
from utils.templates import fallback_templates

ALLOWED_INTENTS = {"request", "complaint", "acknowledgment", "informational", "spam"}
ALLOWED_PRIORITIES = {"high", "medium", "low"}


def _extract_text_from_llm(resp: Any) -> str:
    """
    Robustly extract text from possible llm return types.
    """
    # direct string
    if isinstance(resp, str):
        return resp

    # common langchain ChatOpenAI reply (AIMessage-like)
    if hasattr(resp, "content"):
        return getattr(resp, "content")

    # ChatOpenAI may return a list-like AIMessage
    try:
        # resp could be a list of messages
        if isinstance(resp, (list, tuple)) and len(resp) > 0:
            first = resp[0]
            if hasattr(first, "content"):
                return first.content
    except Exception:
        pass

    # try generational structure
    try:
        gens = getattr(resp, "generations", None)
        if gens:
            # gens[0][0].text or similar
            g0 = gens[0]
            if isinstance(g0, (list, tuple)) and len(g0) > 0:
                candidate = getattr(g0[0], "text", None)
                if candidate:
                    return candidate
    except Exception:
        pass

    # fallback to str
    return str(resp)


def _try_parse_json_only(text: str) -> dict:
    """
    Try to extract the JSON object from text and parse it.
    Allows for surrounding whitespace but no other text.
    Attempts to locate the first {...} block if whole text is not valid JSON.
    """
    text = text.strip()
    # if text looks like pure JSON, parse directly
    try:
        return json.loads(text)
    except Exception:
        # try to extract JSON object between first { and last }
        m = re.search(r"(\{.*\})", text, flags=re.DOTALL)
        if m:
            candidate = m.group(1)
            try:
                return json.loads(candidate)
            except Exception:
                pass
    raise ValueError("No valid JSON payload found")


def classify_email(body: str, llm: Any) -> Tuple[str, str]:
    """
    Classify an email body using the provided LLM instance.
    The LLM is asked (via a system prompt) to RETURN ONLY a JSON object:
      {"intent": "<one-of-allowed>", "priority": "<high|medium|low>"}
    The function returns (intent, priority) as strings. If parsing fails, returns default fallback.
    """
    system_prompt = (
        "Sei un classificatore automatico di email. "
        "Dovrai RISpondere ESCLUSIVAMENTE con un OGGETTO JSON valido (niente testo, niente spiegazioni) "
        "contenente esattamente due campi: \"intent\" e \"priority\".\n\n"
        "Regole:\n"
        "- Il campo \"intent\" deve essere una delle seguenti parole, minuscole e senza spazi:\n"
        "  request, complaint, acknowledgment, informational, spam\n"
        "- Il campo \"priority\" deve essere una delle: high, medium, low\n"
        "- Non inserire altre chiavi, non aggiungere punti, virgole o commenti esterni.\n"
        "- Se sei incerto, scegli \"informational\" per intent e \"low\" per priority.\n"
    )

    user_prompt = f"Email body:\n{body}\n\nProduci ORA il JSON richiesto."

    # call LLM
    try:
        resp = llm([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
    except Exception as e:
        # fallback heuristic if llm call fails
        # simple keyword fallback
        text = body.lower()
        if "urgent" in text or "asap" in text:
            return "request", "high"
        if "complaint" in text or "problem" in text:
            return "complaint", "medium"
        if "unsubscribe" in text or "spam" in text:
            return "spam", "low"
        return "informational", "low"

    raw = _extract_text_from_llm(resp)

    # parse JSON from model response
    try:
        parsed = _try_parse_json_only(raw)
        intent = parsed.get("intent", "").strip().lower()
        priority = parsed.get("priority", "").strip().lower()

        if intent not in ALLOWED_INTENTS or priority not in ALLOWED_PRIORITIES:
            raise ValueError("Values out of allowed set")

        return intent, priority
    except Exception:
        # fallback heuristic if LLM response not parseable or invalid
        # Using a small rule-based fallback:
        text = body.lower()
        if "urgent" in text or "asap" in text:
            return "request", "high"
        if "complaint" in text or "problem" in text:
            return "complaint", "medium"
        if "unsubscribe" in text or "spam" in text:
            return "spam", "low"
        return "informational", "low"
