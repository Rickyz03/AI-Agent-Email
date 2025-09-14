import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "email-agent-user"
    DB_PASSWORD: str = "email-agent-psw"
    DB_NAME: str = "email-agent-db"

    # OpenAI
    OPENAI_API_KEY: str = "changeme"
    OPENAI_MODEL_NAME: str = "gpt-4o-mini"

    # Chroma
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000
    CHROMA_COLLECTION: str = "emails"

    # Security
    SECRET_KEY: str = "changeme"

    class Config:
        env_file = ".env"


settings = Settings()
