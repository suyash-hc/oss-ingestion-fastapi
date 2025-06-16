from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    # Application settings
    PROJECT_NAME: str = "Outsmart Security Systems"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    APP_URL_PREFIX: str = "/digestion"

    # Database settings
    DATABASE_URL: str = ""

    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPICS: str = ""
    KAFKA_GROUP_ID: str = ""
    KAFKA_CLIENT_ID: str = "kafka-ingestion-api"
    KAFKA_DEFAULT_TOPIC: str = "image-ingestion"

    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Create settings instance
settings = Settings()