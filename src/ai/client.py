"""LLM client wrapper centralizing transport and response validation logic."""

from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from .config import LLMProvider, LLMSettings


class LLMClient:
    """Thin wrapper that supports OpenAI-compatible, Bedrock, and local providers."""

    def __init__(self, settings: LLMSettings) -> None:
        self._settings = settings
        self._provider = settings.provider
        timeout = httpx.Timeout(settings.timeout_seconds)

        self._http_client: Optional[httpx.Client] = None
        self._bedrock_client: Any = None

        if self._provider in {LLMProvider.OPENAI, LLMProvider.LOCAL}:
            api_base = settings.resolved_api_base()
            if api_base:
                self._http_client = httpx.Client(timeout=timeout, base_url=api_base)
            else:
                self._http_client = httpx.Client(timeout=timeout)
        elif self._provider == LLMProvider.BEDROCK:
            try:
                import boto3  # type: ignore import-not-found
            except ImportError as exc:  # pragma: no cover - defensive guard
                raise RuntimeError(
                    "boto3 is required for the Bedrock provider. Install it with `pip install boto3`."
                ) from exc

            session_kwargs: Dict[str, str] = {}
            if settings.bedrock_profile:
                session_kwargs["profile_name"] = settings.bedrock_profile
            session = boto3.Session(**session_kwargs)
            self._bedrock_client = session.client(
                "bedrock-runtime",
                region_name=settings.bedrock_region,
                endpoint_url=settings.bedrock_endpoint_url,
            )
        else:  # pragma: no cover - exhaustive safety branch
            raise ValueError(f"Unsupported LLM provider: {self._provider}")

    def close(self) -> None:
        """Release underlying HTTP resources."""

        if self._http_client is not None:
            self._http_client.close()

    def create_chat_completion(
        self,
        *,
        prompt: str,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Send a prompt to the configured model and return the raw JSON response."""

        if self._provider == LLMProvider.BEDROCK:
            return self._create_bedrock_completion(prompt=prompt, response_format=response_format)
        return self._create_openai_compatible_completion(prompt=prompt, response_format=response_format)

    def _create_openai_compatible_completion(
        self,
        *,
        prompt: str,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if self._http_client is None:  # pragma: no cover - defensive guard
            raise RuntimeError("HTTP client is not configured for the selected provider.")

        headers: Dict[str, str] = {}
        api_key = self._settings.resolved_api_key()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key.get_secret_value()}"

        payload: Dict[str, Any] = {
            "model": self._settings.resolved_model(),
            "messages": [
                {"role": "system", "content": self._settings.system_prompt},
                {"role": "user", "content": prompt},
            ],
        }
        if response_format:
            payload["response_format"] = response_format

        url = "/v1/chat/completions"
        if self._settings.resolved_api_base() is None:
            url = "https://api.openai.com/v1/chat/completions"

        response = self._http_client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def _create_bedrock_completion(
        self,
        *,
        prompt: str,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if self._bedrock_client is None:  # pragma: no cover - defensive guard
            raise RuntimeError("Bedrock client is not configured.")

        request: Dict[str, Any] = {
            "modelId": self._settings.resolved_model(),
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}],
                }
            ],
        }
        if self._settings.system_prompt:
            request["system"] = [{"text": self._settings.system_prompt}]

        inference_config: Dict[str, Any] = {}
        if self._settings.bedrock_temperature is not None:
            inference_config["temperature"] = self._settings.bedrock_temperature
        if self._settings.bedrock_max_tokens is not None:
            inference_config["maxTokens"] = self._settings.bedrock_max_tokens
        if inference_config:
            request["inferenceConfig"] = inference_config

        if response_format:
            schema = response_format.get("json_schema", {}).get("schema")
            if schema:
                request["responseFormat"] = {"json": {"schema": schema}}

        response = self._bedrock_client.converse(**request)
        output = response.get("output", {})
        message = output.get("message", {})
        content_parts = message.get("content", [])
        content = "".join(part.get("text", "") for part in content_parts)

        return {"choices": [{"message": {"content": content}}]}

    def __enter__(self) -> "LLMClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
