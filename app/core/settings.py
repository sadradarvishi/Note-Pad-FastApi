from typing import Any, ClassVar, Literal, Mapping

from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str = "dev-secret"
    REFRESH_SECRET_KEY: str = "dev-refresh-secret"
    ALGORITHM: Literal["HS256", "RS256"] = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/notedb_test"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    _DEFAULTS: ClassVar[Mapping[str, Any]] = {
        "ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": 10080,
    }

    @field_validator("ALGORITHM", "ACCESS_TOKEN_EXPIRE_MINUTES", mode="before")
    @classmethod
    def empty_to_default(cls, v, info: ValidationInfo):
        if v in ("", None):
            name = info.field_name
            if name and name in cls._DEFAULTS:
                return cls._DEFAULTS[name]
        return v


settings = Settings()
