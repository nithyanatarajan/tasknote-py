# src/common/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseServiceSettings(BaseSettings):
    log_level: str
    db_username: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    model_config = SettingsConfigDict(
        env_file='.env',  # optional: each service can have its own .env
        env_prefix='',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    @property
    def db_url_async(self) -> str:
        return (
            f'postgresql+asyncpg://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'
        )

    @property
    def db_url_sync(self) -> str:
        return (
            f'postgresql+psycopg2://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'
        )
