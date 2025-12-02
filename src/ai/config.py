"""Configuration helpers for selecting and tuning the LLM provider."""

from __future__ import annotations

from enum import Enum
from functools import lru_cache
from typing import Optional

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMProvider(str, Enum):
    """Supported large language model providers."""

    OPENAI = "openai"
    BEDROCK = "bedrock"
    LOCAL = "local"


class LLMSettings(BaseSettings):
    provider: LLMProvider = Field(default=LLMProvider.LOCAL, alias="LLM_PROVIDER")
    timeout_seconds: float = Field(15.0, alias="LLM_TIMEOUT", ge=1.0)
    system_prompt: str = Field(
        default="You are VitalStackAssist's clinical assistant. <placeholder system prompt>",
        alias="LLM_SYSTEM_PROMPT",
    )

    # OpenAI-compatible provider settings.
    openai_api_key: Optional[SecretStr] = Field(None, alias="OPENAI_API_KEY")
    openai_model: Optional[str] = Field(None, alias="OPENAI_MODEL")
    openai_api_base: Optional[str] = Field(None, alias="OPENAI_API_BASE")

    # AWS Bedrock provider settings.
    bedrock_region: Optional[str] = Field(None, alias="BEDROCK_REGION")
    bedrock_model_id: Optional[str] = Field(None, alias="BEDROCK_MODEL_ID")
    bedrock_profile: Optional[str] = Field(None, alias="BEDROCK_PROFILE")
    bedrock_endpoint_url: Optional[str] = Field(None, alias="BEDROCK_ENDPOINT_URL")
    bedrock_max_tokens: Optional[int] = Field(None, alias="BEDROCK_MAX_TOKENS", ge=1)
    bedrock_temperature: Optional[float] = Field(None, alias="BEDROCK_TEMPERATURE", ge=0.0, le=2.0)

    local_model: str = Field(
        #TODO Placeholder LLM
        default="meta-llama/Llama-3.1-8B-Instruct",
        alias="LOCAL_MODEL",
    )
    local_api_base: str = Field(default="http://127.0.0.1:8000/v1", alias="LOCAL_API_BASE")
    local_api_key: Optional[SecretStr] = Field(None, alias="LOCAL_API_KEY")

    model_config = SettingsConfigDict(env_file=(".env.local", ".env"), env_file_encoding="utf-8")

    @model_validator(mode="after")
    def _validate_provider_specific_fields(self) -> "LLMSettings":

        if self.provider == LLMProvider.OPENAI:
            missing: list[str] = []
            if not self.openai_api_key:
                missing.append("OPENAI_API_KEY")
            if not self.openai_model:
                missing.append("OPENAI_MODEL")
            if missing:
                joined = ", ".join(missing)
                raise ValueError(f"Missing required OpenAI settings: {joined}")
        if self.provider == LLMProvider.BEDROCK:
            missing = []
            if not self.bedrock_region:
                missing.append("BEDROCK_REGION")
            if not self.bedrock_model_id:
                missing.append("BEDROCK_MODEL_ID")
            if missing:
                joined = ", ".join(missing)
                raise ValueError(f"Missing required Bedrock settings: {joined}")
        if self.provider == LLMProvider.LOCAL and not self.local_api_base:
            raise ValueError("LOCAL_API_BASE must be provided when LLM_PROVIDER=local")
        return self

    def resolved_model(self) -> str:
        if self.provider == LLMProvider.OPENAI:
            assert self.openai_model is not None  # Guarded by validator.
            return self.openai_model
        if self.provider == LLMProvider.BEDROCK:
            assert self.bedrock_model_id is not None
            return self.bedrock_model_id
        return self.local_model

    def resolved_api_key(self) -> Optional[SecretStr]:
        if self.provider == LLMProvider.OPENAI:
            return self.openai_api_key
        if self.provider == LLMProvider.LOCAL:
            return self.local_api_key
        return None

    def resolved_api_base(self) -> Optional[str]:
        if self.provider == LLMProvider.OPENAI:
            return self.openai_api_base
        if self.provider == LLMProvider.LOCAL:
            return self.local_api_base
        return None


@lru_cache(maxsize=1)
def load_settings() -> LLMSettings:
    """Load environment-backed settings once for the process lifetime."""

    return LLMSettings()  # type: ignore[call-arg]
