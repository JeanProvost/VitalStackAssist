"""High-level orchestration for generating supplement interaction reports via LLM."""

from __future__ import annotations

from json import JSONDecodeError

from pydantic import ValidationError

from ..models import SupplementInteractionRequest, SupplementInteractionResponse
from .client import LLMClient
from .config import load_settings
from .prompts import build_interaction_prompt


def _response_format_schema() -> dict[str, object]:
    """Return the structured response schema consumed by the OpenAI API."""

    schema = SupplementInteractionResponse.model_json_schema()
    return {"type": "json_schema", "json_schema": {"name": "interaction_report", "schema": schema}}


def generate_interaction_report(request: SupplementInteractionRequest) -> SupplementInteractionResponse:
    """Invoke the LLM to produce an interaction report for the given request."""

    settings = load_settings()
    prompt = build_interaction_prompt(request)
    with LLMClient(settings) as client:
        raw_response = client.create_chat_completion(
            prompt=prompt,
            response_format=_response_format_schema(),
        )

    choice = raw_response["choices"][0]["message"]
    content = choice.get("content", "{}")

    try:
        return SupplementInteractionResponse.model_validate_json(content)
    except (ValidationError, JSONDecodeError) as exc:  # pragma: no cover - thin wrapper
        raise ValueError("Unable to parse LLM response into SupplementInteractionResponse") from exc
