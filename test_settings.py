import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

os.environ["BACKEND_CORS_ORIGINS"] = "http://localhost:5173"

class Settings1(BaseSettings):
    backend_cors_origins: str | list[str] = ["http://localhost:5173"]

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_origins(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",")]
        return value

try:
    print(Settings1().backend_cors_origins)
except Exception as e:
    print(e)
