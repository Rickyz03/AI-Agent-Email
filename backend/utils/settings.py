from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "email-agent-user"
    DB_PASSWORD: str = "email-agent-psw"
    DB_NAME: str = "email-agent-db"

    # External APIs
    OPENAI_API_KEY: str = "changeme"

    # Chroma
    CHROMA_URL: str = "http://localhost:8000"

    # Security
    SECRET_KEY: str = "changeme"

    class Config:
        env_file = ".env"


settings = Settings()
