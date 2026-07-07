from functools import cached_property
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEYS_DIR = BASE_DIR / "secret_keys"

Path(SECRET_KEYS_DIR).mkdir(
    parents=True,
    exist_ok=True,
)


class ApiConfig(BaseModel):
    version: str = "1.0.0"
    prefix: str = "/api/v1"
    title: str = "FastChat Notifications"
    description: str = "API для работы с уведомлениями мессенджера Fast Chat"


class CorsConfig(BaseModel):
    allowed_origins: list[str] = Field(
        default_factory=lambda: [
            # "http://localhost:5173",
            # "http://localhost:8080",
            # "http://localhost:8081",
            # "http://localhost:80",
            # "https://localhost",
            # "http://localhost",
            # "https://localhost:443",
            "http://fastchat_proxy:80",
            "https://fastchat_proxy:443",
        ]
    )


class RunConfig(BaseModel):
    scheme: Literal["http", "https"] = "https"
    host: str = "localhost"
    port: int = 8001


class DatabaseConfig(BaseModel):
    dev_dsn: MongoDsn
    name: str = "notifications"


class KafkaConfig(BaseModel):
    bootstrap_server: str = "localhost:9092"
    notifications_topic: str = "notifications"
    notifications_group: str = "notifications"
    fanout_notifications_topic: str = "fanout-notifications"

    @property
    def bootstrap_servers(self) -> list[str]:
        return [self.bootstrap_server]


class SecurityConfig(BaseModel):
    access_token_cookie_name: str = "fastchat_access_token"
    algorithm: str

    @cached_property
    def public_key(self) -> str:
        with Path.open(SECRET_KEYS_DIR / "public.pem") as file:
            return file.read()


class Settings(BaseSettings):
    database: DatabaseConfig
    kafka: KafkaConfig = Field(default_factory=KafkaConfig)
    security: SecurityConfig
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
