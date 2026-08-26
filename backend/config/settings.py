"""
Centralized settings loaded from environment variables / .env.

Never hardcode AWS credentials here or anywhere else in the repo.
Use a dedicated IAM role/user with READ-ONLY permissions for the
resources GovernX audits (see docs/architecture.md).
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"

    # AWS — populate via .env or standard AWS credential chain
    # (env vars / ~/.aws/credentials / IAM role). Do not commit real values.
    aws_region: str = "us-east-1"
    aws_profile: str | None = None  # use a named profile for local dev

    # Database
    database_url: str = "sqlite:///./governx.db"

    # Risk engine
    monte_carlo_iterations: int = 10_000


@lru_cache
def get_settings() -> Settings:
    return Settings()
