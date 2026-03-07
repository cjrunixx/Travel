from functools import lru_cache
from typing import Any

from pydantic import field_validator

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "local"
    api_v1_prefix: str = "/api/v1"

    jwt_secret_key: str = "change_me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    database_url: str = "postgresql+psycopg://travel_user:travel_password@postgres:5432/travel_planner"
    redis_url: str = "redis://redis:6379/0"

    backend_cors_origins: Any = ["http://localhost:5173"]

    maps_provider: str = "mapbox"
    mapbox_api_key: str = ""
    google_maps_api_key: str = ""

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_origins(cls, value: Any) -> list[str]:
        if isinstance(value, str):
            # Handle JSON-like list strings: ["a", "b"] -> a, b
            if value.startswith("[") and value.endswith("]"):
                import json
                try:
                    return json.loads(value)
                except:
                    value = value[1:-1]
            return [item.strip().strip('"').strip("'") for item in value.split(",") if item.strip()]
        # Ensure that if it's not a string, it's converted to a list of strings if possible, or returned as is if already a list
        if isinstance(value, list):
            return [str(item).strip().strip('"').strip("'") for item in value if str(item).strip()]
        return [] # Default to empty list if value is neither string nor list



@lru_cache
def get_settings() -> Settings:
    return Settings()
