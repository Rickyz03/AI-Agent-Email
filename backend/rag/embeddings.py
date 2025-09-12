from typing import List
from langchain_openai import OpenAIEmbeddings
from utils.settings import settings

# Initialize embedding model
embedder = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)


def embed_text(text: str) -> List[float]:
    return embedder.embed_query(text)


def embed_texts(texts: List[str]) -> List[List[float]]:
    return embedder.embed_documents(texts)
