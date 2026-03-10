from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Auth"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./auth.db"

    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "ilyesbouzayen@hotmail.com"
    EMAIL_FROM_NAME: str = "FastAPI Auth"

    OTP_LENGTH: int = 6
    OTP_EXPIRE_MINUTES: int = 5

    model_config = {"extra": "ignore", "env_file": ".env"}


settings = Settings()
