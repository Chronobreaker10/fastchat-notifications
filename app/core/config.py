from typing import Literal

from pydantic import BaseModel, Field, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiConfig(BaseModel):
    version: str = "1.0.0"
    prefix: str = "/api/v1"
    title: str = "FastChat Notifications"
    description: str = "API для работы с уведомлениями мессенджера Fast Chat"


class CorsConfig(BaseModel):
    allowed_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://localhost:8080",
            "http://localhost:8081",
        ]
    )


class RunConfig(BaseModel):
    scheme: Literal["http", "https"] = "http"
    host: str = "localhost"
    port: int = 8000


class DatabaseConfig(BaseModel):
    dev_dsn: MongoDsn
    name: str = "notifications"


class Settings(BaseSettings):
    database: DatabaseConfig
    # security: SecurityConfig
    env: Literal["prod", "dev", "test"] = "dev"
    default_limit: int = 10
    websockets_limit_per_user: int = 20
    cors: CorsConfig = Field(default_factory=CorsConfig)
    run_config: RunConfig = Field(default_factory=RunConfig)
    api_config: ApiConfig = Field(default_factory=ApiConfig)
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
    )


settings = Settings()
