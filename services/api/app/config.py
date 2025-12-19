"""
Configuration Module
Loads settings from environment variables
"""
import os
from typing import List
from functools import lru_cache


class Settings:
    """Application settings"""

    # Application
    APP_NAME: str = "Cloud-Native Microservices Learning Platform API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("API_DEBUG", "false").lower() == "true"

    # Server
    HOST: str = os.getenv("API_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("API_PORT", "8000"))
    ROOT_PATH: str = os.getenv("API_ROOT_PATH", "/api")  # Para funcionar detrás de proxy (Traefik)

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://mlp_user:mlp_secret@postgres:5432/mlp_db"
    )
    DB_MIN_POOL_SIZE: int = int(os.getenv("POSTGRES_MIN_POOL_SIZE", "5"))
    DB_MAX_POOL_SIZE: int = int(os.getenv("POSTGRES_MAX_POOL_SIZE", "20"))
    DB_POOL_TIMEOUT: int = int(os.getenv("POSTGRES_POOL_TIMEOUT", "30"))

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:80",
        "http://localhost:8050",
    ]

    # Security
    SECRET_KEY: str = os.getenv("API_SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("API_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("API_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Logging
    LOG_LEVEL: str = os.getenv("API_LOG_LEVEL", "INFO")

    def get_db_url_asyncpg(self) -> str:
        """
        Get database URL for asyncpg
        Converts postgresql+asyncpg:// to postgresql://
        """
        return self.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    """
    return Settings()


# Global settings instance
settings = get_settings()
