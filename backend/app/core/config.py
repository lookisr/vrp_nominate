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
    admin_ids: list[int] = Field(default_factory=list)
    voting_open_default: bool = Field(default=True)
    media_folder: str = Field(default="uploads")

    @computed_field
    @property
    def database_url(self) -> str:
        """Эта функция формирует DSN для подключения к БД."""
        if self.postgres_dsn:
            return self.postgres_dsn
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @field_validator("admin_ids", mode="before")
    @classmethod
    def parse_admin_ids(cls, value: Any) -> list[int]:
        """Этот валидатор превращает строку ID в список чисел."""

        if value in (None, "", []):
            return []
        if isinstance(value, list):
            return [int(item) for item in value]
        return [int(item.strip()) for item in str(value).split(",") if item.strip()]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


settings = Settings()

