from pydantic_settings import BaseSettings, SettingsConfigDict
from src.logging_config import logger


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str

    smtp_password: str
    smtp_user: str
    smtp_host: str
    smtp_port: str

    model_config = SettingsConfigDict(env_file_encoding="utf-8", extra="ignore")


settings = Settings()  # type: ignore
logger.info(settings)
