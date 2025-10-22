# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str  # your Postgres URL
    # DATABASE_URL_SYNC_CONN: str  # your Postgres URL

    class Config:
        # tells Pydantic where to look for env vars
        env_file = "../.env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Instantiate once, pull settings.DATABASE_URL elsewhere
settings = Settings()
