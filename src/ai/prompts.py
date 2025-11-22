"""Prompt construction helpers for supplement interaction analysis."""

from __future__ import annotations

from typing import Iterable

from ..models import SupplementInteractionRequest


def build_interaction_prompt(
    request: SupplementInteractionRequest, *, biomarkers: Iterable[str] | None = None
) -> str:
    """Compose the textual prompt sent to the LLM."""

    supplements = "\n".join(f"- {name}" for name in request.supplements)
    lines = [
        "Evaluate the following supplement stack for clinically relevant interactions.",
        "List both positive synergies and negative conflicts.",
        "Supplements:",
        supplements,
    ]
    if biomarkers:
        lines.append("Biomarkers to consider:")
        lines.extend(f"- {marker}" for marker in biomarkers)
    lines.append("Respond in the requested JSON schema without additional commentary.")
    return "\n".join(lines)
