"""DTOs used to exchange biomarker observations with the .NET orchestration layer.

"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class BiomarkerObservation(BaseModel):

    name: str = Field(..., description="Display name used in the user interface (e.g., 'Vitamin D').")
    value: float = Field(..., description="Numeric reading provided by the lab result.")
    unit: str = Field(..., description="Measurement unit normalized (e.g., 'ng/mL').")
    reference_min: Optional[float] = Field(
        None, description="Optional lower bound of the reference range supplied by the .NET backend."
    )
    reference_max: Optional[float] = Field(
        None, description="Optional upper bound of the reference range supplied by the .NET backend."
    )
    notes: Optional[str] = Field(None, description="Any free-form annotations captured by the .NET backend.")
