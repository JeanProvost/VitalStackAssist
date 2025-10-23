"""DTOs that define the request and response contracts for supplement interaction analysis.

These models describe the payloads exchanged between the .NET orchestration layer and this
stateless Python calculator service. No persistence-related concerns should leak into these
structures—they are pure data contracts.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class SupplementInteractionRequest(BaseModel):
    """Canonical request from the .NET API describing a stack needing analysis."""

    supplements: List[str] = Field(
        ..., description="Canonical supplement names provided by the .NET system of record.", min_length=1
    )


class InteractionDetail(BaseModel):
    """Shared structure for conveying a specific interaction insight."""

    supplements: List[str] = Field(
        ..., description="Subset of the request supplements involved in this interaction.", min_length=1
    )
    description: str = Field(..., description="Plain-language explanation of the interaction.")
    evidence_level: Optional[str] = Field(
        None, description="Optional maturity or strength descriptor supplied by the .NET backend."
    )
    source_url: Optional[str] = Field(
        None, description="URL pointing to the evidence source used to support this interaction."
    )


class NegativeInteractionDetail(InteractionDetail):
    """Extension of interaction detail with mitigation guidance for risky combinations."""

    severity: Optional[str] = Field(None, description="Structured severity label defined by the .NET backend.")
    recommendation: Optional[str] = Field(
        None, description="Guidance on how the user should adjust their protocol to reduce risk."
    )


class SupplementInteractionResponse(BaseModel):
    """Normalized response payload returned to the .NET API for caching and user display."""

    summary: str = Field(..., description="High-level narrative summarizing the calculator findings.")
    positive_interactions: List[InteractionDetail] = Field(
        default_factory=list,
        description="Evidence-backed synergies to highlight for the user interface.",
    )
    negative_interactions: List[NegativeInteractionDetail] = Field(
        default_factory=list,
        description="Warnings or conflicts that require the user's attention.",
    )
