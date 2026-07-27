import os

from pydantic import BaseModel

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5433/cadflow")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

class Settings(BaseModel):
    db_url: str = DATABASE_URL
    redis_url: str = REDIS_URL
    groq_api_key: str = GROQ_API_KEY

settings = Settings()
