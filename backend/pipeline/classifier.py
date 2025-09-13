from typing import Tuple
from langchain_openai import ChatOpenAI
from utils.llm_helpers import extract_text_from_llm


def classify_email(body: str, llm: ChatOpenAI) -> Tuple[str, str]:
    """
    Classify the intent and priority of an email using the provided LLM.
    Returns (intent, priority).
    """

    system_prompt = (
        "You are an email classification assistant. "
        "Analyze the given email body and respond strictly in the following format:\n\n"
        "<intent>;<priority>\n\n"
        "Where:\n"
        "- intent is one of: request, complaint, spam, informational\n"
        "- priority is one of: high, medium, low\n\n"
        "Do not add any other text."
    )

    user_prompt = f"Email body:\n{body}"

    response = llm.invoke([{"role": "system", "content": system_prompt},
                           {"role": "user", "content": user_prompt}])
    raw_output = extract_text_from_llm(response)

    # Expect "intent;priority"
    try:
        intent, priority = raw_output.strip().lower().split(";")
        return intent.strip(), priority.strip()
    except ValueError:
        return "informational", "low"
