from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "MasteryLoop"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Security & JWT
    SECRET_KEY: str = "masteryloop-secret-key-change-in-production-only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Database: Supports PostgreSQL and SQLite
    DATABASE_URL: str = "sqlite:///./masteryloop.db"

    # Qdrant Vector Store
    QDRANT_URL: str = ":memory:"
    QDRANT_PATH: Optional[str] = None  # e.g. "./qdrant_storage" for persistent local disk storage
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION: str = "masteryloop_curriculum"

    # AI & Embedding Providers
    EMBEDDING_PROVIDER: str = "bag-of-words"  # "bag-of-words", "sentence-transformers", "openai"
    EMBEDDING_MODEL_NAME: str = "paraphrase-multilingual-MiniLM-L12-v2"
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"
    LLM_PROVIDER: str = "mock"  # "mock", "openai", "gemini"
    LLM_TIMEOUT_SECONDS: float = 8.0

    # Assessment & Psychometrics Settings
    DEFAULT_TARGET_SE: float = 0.30
    DEFAULT_TARGET_QUESTIONS: int = 15
    MIN_USABLE_TOPIC_QUESTIONS: int = 10
    MAX_ADAPTIVE_QUESTIONS: int = 15
    MIN_ADAPTIVE_QUESTIONS: int = 5
    PILOT_MIX_PROBABILITY: float = 0.15
    EXPOSURE_CONTROL_CAP: int = 50

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
