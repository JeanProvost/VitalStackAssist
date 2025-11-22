"""DTOs that define the request and response contracts for supplement interaction analysis.
"""

from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field
from src.enums.management_strategy import ManagementStrategy

class InteractionBase(BaseModel):
    mechanism: str = Field(..., description="The biological rationale behind the interaction.")
    evidence_level: str = Field(..., description="The strength of evidence supporting the interaction.")
    source_url: Optional[str] = Field(None, description="URL to the source of the information.")

class ConflictDetail(InteractionBase):
    supplements: List[str] = Field(..., min_length=2, description="List of supplements currently interacting with the conflict.")
    severity: str = Field(..., description="The severity level of the conflict.")
    management_strategy: ManagementStrategy = Field(..., description="Recommended strategy to manage the conflict.")
    management_instruction: str = Field(..., description="Detailed instructions for managing the conflict.")

class SynergyDetail(InteractionBase):
    supplements: List[str] = Field(..., min_length=2, description="List of supplements involved in the synergy.")
    category: str = Field(..., description="The category of synergy (e.g., metabolic, immune).")

class DepletionDetail(BaseModel):
    """Captures one-way nutrient depletion interactions between supplements."""
    offending_supplement: str
    depleted_nutrient: str
    mechanism: str
    severity: str
    recommendation: str

class SupplementInteractionResponse(BaseModel):
    """The full report cached by the .NET layer for supplement interaction analysis."""
    meta: dict = Field(defult_factory=dict, description="Metadata about the analysis.")
    analysis_summary: str = Field(..., description="A summary of the interaction analysis.")

    interactions: struct_interactions

class struct_interactions(BaseModel):
    conficts: List[ConflictDetail] = Field(default_factory=list)
    synergies: List[SynergyDetail] = Field(default_factory=list)
    depletions: List[DepletionDetail] = Field(default_factory=list)
    

