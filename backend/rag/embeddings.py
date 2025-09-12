from typing import List
from langchain_openai import OpenAIEmbeddings

# Initialize embedding model (replace with alternative if needed)
embedder = OpenAIEmbeddings()


def embed_text(text: str) -> List[float]:
    return embedder.embed_query(text)


def embed_texts(texts: List[str]) -> List[List[float]]:
    return embedder.embed_documents(texts)
