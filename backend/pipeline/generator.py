from typing import List, Any
import json
import re

from langchain.schema import SystemMessage, HumanMessage
from utils.settings import settings
from utils.templates import fallback_templates


def _extract_text_from_llm(resp: Any) -> str:
    # same robust extractor used for classifier
    if isinstance(resp, str):
        return resp
    if hasattr(resp, "content"):
        return getattr(resp, "content")
    try:
        if isinstance(resp, (list, tuple)) and len(resp) > 0:
            first = resp[0]
            if hasattr(first, "content"):
                return first.content
    except Exception:
        pass
    try:
        gens = getattr(resp, "generations", None)
        if gens:
            g0 = gens[0]
            if isinstance(g0, (list, tuple)) and len(g0) > 0:
                candidate = getattr(g0[0], "text", None)
                if candidate:
                    return candidate
    except Exception:
        pass
    return str(resp)


def _try_parse_json_array(text: str) -> List[str]:
    text = text.strip()
    # direct parse
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list) and all(isinstance(x, str) for x in parsed):
            return parsed
    except Exception:
        # try to extract first JSON array
        m = re.search(r"(\[.*\])", text, flags=re.DOTALL)
        if m:
            candidate = m.group(1)
            try:
                parsed = json.loads(candidate)
                if isinstance(parsed, list) and all(isinstance(x, str) for x in parsed):
                    return parsed
            except Exception:
                pass
    raise ValueError("No valid JSON array found")


def generate_drafts(subject: str, body: str, context: str, llm: Any) -> List[str]:
    """
    Generate 3 draft replies using the provided LLM instance.
    The LLM is instructed (via system prompt) to return ONLY a JSON array of 3 strings:
      [ "<BREVE>", "<STANDARD>", "<DETTAGLIATA>" ]
    If parsing fails, returns safe fallback templates.
    """
    system_prompt = (
        "Sei un assistente che genera bozze email. RISPOSTA RICHIESTA: SOLO un ARRAY JSON (nessun testo aggiuntivo) "
        "contenente esattamente 3 stringhe nell'ordine: [BREVE, STANDARD, DETTAGLIATA].\n\n"
        "Regole per la generazione:\n"
        "1) Usa solo fatti presenti nel CONTEXT. Se il CONTEXT è vuoto, scrivi risposte generiche e neutrali.\n"
        "2) Se servono chiarimenti, la variante DETTAGLIATA deve terminare con un breve paragrafo di domande (elencate come punti) da porre al mittente.\n"
        f"3) Mantieni il tono: {settings.DEFAULT_TONE}. Lingua: {settings.DEFAULT_LANGUAGE}. Firma consigliata: {settings.DEFAULT_SIGNATURE}.\n"
        "4) NON inventare prezzi, date o impegni.\n"
        "5) Nessun HTML, ritorna testo semplice.\n"
    )

    user_prompt = (
        f"Subject: {subject}\n\n"
        f"Body: {body}\n\n"
        f"Context: {context if context else 'Nessun contesto disponibile'}\n\n"
        "Produci ORA l'array JSON con le 3 varianti."
    )

    try:
        resp = llm([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
        raw = _extract_text_from_llm(resp)
        variants = _try_parse_json_array(raw)
        # ensure exactly 3 variants
        if len(variants) >= 3:
            return variants[:3]
        else:
            raise ValueError("Less than 3 variants returned")
    except Exception:
        # fallback: use local templates
        return fallback_templates(subject)
