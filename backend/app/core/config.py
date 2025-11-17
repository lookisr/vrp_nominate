from typing import Any

from pydantic import Field, field_validator, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Эти настройки собирают важные переменные окружения."""

    app_name: str = Field(default="Premiya Goda VRP API")
    api_prefix: str = Field(default="/api")
    postgres_dsn: str | None = Field(default=None)
    postgres_db: str = Field(default="vrp")
    postgres_user: str = Field(default="vrp_user")
    postgres_password: str = Field(default="vrp_password")
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    telegram_bot_token: str = Field(default="")
    required_channel: str = Field(default="@vrpnews")
    admin_ids: str = Field(default="")
    voting_open_default: bool = Field(default=True)
    media_folder: str = Field(default="uploads")
    development_mode: bool = Field(default=False)

    @computed_field
    @property
    def database_url(self) -> str:
        """Эта функция формирует DSN для подключения к БД."""
        if self.postgres_dsn:
            return self.postgres_dsn
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @computed_field
    @property
    def admin_ids_list(self) -> list[int]:
        """Парсит admin_ids из строки в список."""
        if not self.admin_ids:
            return []
        try:
            return [int(item.strip()) for item in self.admin_ids.split(",") if item.strip()]
        except (ValueError, TypeError):
            return []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


settings = Settings()

