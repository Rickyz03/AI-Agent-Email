from typing import List
from langchain_openai import ChatOpenAI
from utils.llm_helpers import extract_text_from_llm


def generate_drafts(subject: str, body: str, context: str, llm: ChatOpenAI) -> List[str]:
    """
    Generate draft replies for an email using the provided LLM.
    """

    system_prompt = (
        "You are an AI email assistant. "
        "Generate three different professional draft replies to the given email. "
        "Each draft should:\n"
        "- Be polite and professional.\n"
        "- Respect the detected intent and priority.\n"
        "- Be concise and clear.\n"
        "- Adapt to the provided context if available.\n\n"
        "Return only the three drafts separated by '---', without extra explanations."
    )

    user_prompt = f"Subject: {subject}\n\nBody:\n{body}\n\nContext:\n{context or 'N/A'}"

    response = llm.invoke([{"role": "system", "content": system_prompt},
                           {"role": "user", "content": user_prompt}])
    raw_output = extract_text_from_llm(response)

    drafts = [d.strip() for d in raw_output.split("---") if d.strip()]
    return drafts[:3]
