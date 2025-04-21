# src/common/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseServiceSettings(BaseSettings):
    log_level: str

    model_config = SettingsConfigDict(
        env_file='.env',  # optional: each service can have its own .env
        env_prefix='',
        env_file_encoding='utf-8',
        extra='ignore',
    )
