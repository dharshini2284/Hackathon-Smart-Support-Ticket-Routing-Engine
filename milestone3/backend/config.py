from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):

    # --------------------------------------------
    # App
    # --------------------------------------------

    APP_NAME: str = "AI Ticket Orchestrator"
    ENV: str = "development"

    # --------------------------------------------
    # Redis
    # --------------------------------------------

    REDIS_URL: str = os.getenv("REDIS_URL")
    REDIS_QUEUE: str = "ticket_queue"

    # --------------------------------------------
    # Deduplication
    # --------------------------------------------

    SIMILARITY_THRESHOLD: float = 0.85
    TIME_WINDOW_SECONDS: int = 120
    FLOOD_THRESHOLD: int = 5

    # --------------------------------------------
    # Incident
    # --------------------------------------------

    INCIDENT_TIMEOUT: int = 300

    # --------------------------------------------
    # Circuit Breaker
    # --------------------------------------------

    CIRCUIT_FAILURE_THRESHOLD: int = 3
    CIRCUIT_RESET_TIMEOUT: int = 10

    # --------------------------------------------
    # Model
    # --------------------------------------------

    TRANSFORMER_MODEL_NAME: str = "facebook/bart-large-mnli"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Singleton instance
@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()