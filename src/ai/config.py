"""Configuration helpers for wiring the calculator to an OpenAI-compatible endpoint."""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class OpenAISettings(BaseSettings):
    """Runtime configuration for the LLM client."""

    api_key: SecretStr = Field(..., alias="OPENAI_API_KEY")
    model: str = Field(..., alias="OPENAI_MODEL")
    api_base: Optional[str] = Field(None, alias="OPENAI_API_BASE")
    timeout_seconds: float = Field(15.0, alias="OPENAI_TIMEOUT", ge=1.0)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = ""


@lru_cache(maxsize=1)
def load_settings() -> OpenAISettings:
    """Load environment-backed settings once for the process lifetime."""

    return OpenAISettings()  # type: ignore[call-arg]
