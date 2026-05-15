from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DB_PATH = Path(__file__).resolve().parent.parent / "cmta.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL:        str  = f"sqlite:///{BACKEND_DB_PATH.as_posix()}"
    OPENROUTER_API_KEY:  str  = ""
    OPENROUTER_BASE_URL: str  = "https://openrouter.ai/api/v1"
    AI_MODEL:            str  = "google/gemini-2.0-flash-lite-001"
    APP_NAME:            str  = "CMTA Metro Bus API"
    DEBUG:               bool = True


settings = Settings()
