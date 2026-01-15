"""DTOs that define the request and response contracts for supplement interaction analysis.
"""

from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from src.enums.management_strategy import ManagementStrategy
from src.enums.evidence_level import EvidenceLevel
from src.enums.severity_level import SeverityLevel
from src.enums.synergy_category import SynergyCategory
from src.enums.depletion_severity import DepletionSeverity

#Base interaction Models ---
class InteractionBase(BaseModel):
    supplements: List[str] = Field(..., min_length=2, description="List of supplements involved in the interaction.")
    mechanism: str = Field(..., description="The biological rationale behind the interaction.")
    evidence_level: Literal["low", "medium", "high", "inconclusive"] = Field(
        "moderate", description="The strength of clinical evidence"
    )
    source_url: Optional[str] = Field(None)
class ConflictDetail(InteractionBase):
    supplements: List[str] = Field(..., min_length=2, description="List of supplements currently interacting with the conflict.")
    severity: SeverityLevel = Field(..., description="Severity level of the conflict.")
    management_strategy: ManagementStrategy = Field(..., description="Recommended strategy to manage the conflict.")
    management_instruction: str = Field(..., description="Detailed instructions for managing the conflict.")

class SynergyDetail(InteractionBase):
    category: Optional[str] = Field(None, description="Category of the synergy.")

class DepletionDetail(BaseModel):
    """Captures one-way nutrient depletion interactions between supplements."""
    offending_supplement: str = Field(..., description="The supplement that causes the depletion.")
    depleted_nutrient: str = Field(..., description="The nutrient that is being depleted.")
    mechanism: str = Field(..., description="The biological rationale behind the depletion.")
    severity: DepletionSeverity = Field(..., description="Severity level of the depletion.")
    recommendation: str = Field(..., description="Recommended action to address the depletion.")

class OptimizationSuggestion(BaseModel):
    """Bioavailability or form-specific suggestion(the optimizer feature)"""
    supplement: str = Field(..., description="The supplement for which the suggestion is made.")
    suggested_form: str = Field(..., description="The suggested form of the supplement for better efficacy.")
    rationale: str = Field(..., description="Rationale behind the suggestion.")

class DosageWarning(BaseModel):
    """Dosage warning for a specific supplement."""
    supplement: str = Field(..., description="The supplement for which the dosage warning is issued.")
    warning: str = Field(..., description="The dosage warning message.")    

# --- Main Reponse Model ---

class struct_interactions(BaseModel):
    conflicts: List[InteractionBase] = Field(default_factory=list)
    synergies: List[SynergyDetail] = Field(default_factory=list)
    depletions: List[DepletionDetail] = Field(default_factory=list)
    optimizations: List[OptimizationSuggestion] = Field(default_factory=list)
    dosage_warnings: List[DosageWarning] = Field(default_factory=list)
    meta: dict = Field(default_factory=dict, description="Metadata about the interactions.")

class SupplementInteractionResponse(BaseModel):
    """The full report cached by the .NET layer for supplement interaction analysis."""
    meta: dict = Field(default_factory=dict, description="Metadata about the analysis.")
    analysis_summary: str = Field(..., description="A summary of the interaction analysis.")

    interactions: struct_interactions

class SupplementInteractionRequest(BaseModel):
    """Request model for supplement interaction analysis."""
    supplements: List[str] = Field(..., description="List of supplements to analyze.")