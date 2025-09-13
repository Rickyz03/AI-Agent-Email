from typing import List
from langchain_openai import ChatOpenAI
from utils.settings import settings


def generate_drafts(subject: str, body: str, context: str) -> List[str]:
    """
    Generate draft replies using OpenAI LLM (gpt-4o-mini or configured model).
    Produces 3 variants: short, standard, detailed.
    """

    llm = ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model_name=settings.OPENAI_MODEL_NAME,
        temperature=0.7,
        max_tokens=800,
    )

    system_prompt = (
        "Sei un assistente email professionale. Obiettivi:\n"
        "1) Rispondi con fatti presenti nel CONTEXT.\n"
        "2) Se mancano informazioni, chiedi chiarimenti con elenco puntato.\n"
        f"3) Mantieni il tono: {settings.DEFAULT_TONE}. "
        f"Lingua: {settings.DEFAULT_LANGUAGE}. "
        f"Firma da usare: {settings.DEFAULT_SIGNATURE}.\n"
        "4) NON inventare prezzi, date, impegni. NON promettere sconti.\n"
        "5) Proponi 3 varianti: [BREVE], [STANDARD], [DETTAGLIATA].\n"
        "6) Mantieni formattazione semplice (nessun HTML complesso)."
    )

    user_prompt = (
        f"Subject: {subject}\n\n"
        f"Body: {body}\n\n"
        f"Context: {context if context else 'Nessun contesto disponibile'}"
    )

    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ])

    # Estrarre le 3 varianti dal testo
    raw_text = response.content.strip()
    variants = [v.strip() for v in raw_text.split("\n") if v.strip()]

    # Limita a max 3 varianti
    return variants[:3]
