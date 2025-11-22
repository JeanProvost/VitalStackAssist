"""LLM client wrapper centralizing transport and response validation logic."""

from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from .config import OpenAISettings


class LLMClient:
    """Thin wrapper around the OpenAI chat completions endpoint."""

    def __init__(self, settings: OpenAISettings) -> None:
        self._settings = settings
        timeout = httpx.Timeout(settings.timeout_seconds)
        if settings.api_base:
            self._client = httpx.Client(timeout=timeout, base_url=settings.api_base)
        else:
            self._client = httpx.Client(timeout=timeout)

    def close(self) -> None:
        """Release underlying HTTP resources."""

        self._client.close()

    def create_chat_completion(self, *, prompt: str, response_format: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send a prompt to the configured model and return the raw OpenAI JSON response."""

        headers = {"Authorization": f"Bearer {self._settings.api_key.get_secret_value()}"}
        payload: Dict[str, Any] = {
            "model": self._settings.model,
            "messages": [
                {"role": "system", "content": "You are a clinical supplement interaction analyst."},
                {"role": "user", "content": prompt},
            ],
        }
        if response_format:
            payload["response_format"] = response_format

        url = "/v1/chat/completions"
        response = self._client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def __enter__(self) -> "LLMClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
