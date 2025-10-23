"""DTOs used to exchange biomarker observations with the .NET orchestration layer.

The .NET monolith remains the source of truth for biomarker persistence. These structures merely
express the payload shapes this calculator service understands when asked to run analytics that
include biomarker context.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BiomarkerObservation(BaseModel):
    """Single biomarker measurement supplied by the .NET backend."""

    name: str = Field(..., description="Display name used in the user interface (e.g., 'Vitamin D').")
    value: float = Field(..., description="Numeric reading provided by the lab result.")
    unit: str = Field(..., description="Measurement unit normalized by the .NET backend (e.g., 'ng/mL').")
    collected_at: datetime = Field(..., description="Timestamp recorded by the .NET backend for this sample.")
    reference_min: Optional[float] = Field(
        None, description="Optional lower bound of the reference range supplied by the .NET backend."
    )
    reference_max: Optional[float] = Field(
        None, description="Optional upper bound of the reference range supplied by the .NET backend."
    )
    notes: Optional[str] = Field(None, description="Any free-form annotations captured by the .NET backend.")
