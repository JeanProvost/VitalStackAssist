class InsightType(str, Enum):
    CORRELATION = "correlation"
    STREAK = "streak"
    EDUCATIONAL = "educational"
    WARNING = "warning"
    
class Insight(BaseModel):
    type: InsightType = Field(..., description="The type of insight.")
    title: str = Field(..., description="A brief title for the insight.")
    content: str = Field(..., description="Detailed content of the insight.")
    related_supplements: List[str] = Field(default_factory=list, description="List of supplements related to the insight.")
    confidence_score: Optional[float] = Field(None, description="A score indicating the confidence level of the insight (0.0 to 1.0).")

class VitalityScore(BaseModel):
    """
    F-007: Reward of the self
    Gamification metrics to show progress
    """
    score: int = Field(..., ge=0, le=100, description="The vitality score ranging from 0 to 100.")
    """WIP Subject to change"""
    level: str = Field(..., description="A descriptive level corresponding to the vitality score (e.g., 'Beginner', 'Intermediate', 'Advanced').")
    positive_factors: List[str] = Field(default_factory=list, description="List of factors the user is doing right.") 
    negative_factors: List[str] = Field(default_factory=list, description="List of factors the user can improve on.")
    
class OptimizationSuggestion(BaseModel):
    """
    F-008: Optimization Suggestions
    Suggestions for optimizing supplement intake based on user data and interactions.
    """
    supplement: str = Field(..., description="The supplement for which the suggestion is made.")
    #--SUBJECT
    suggested_form: str = Field(..., description="The suggested form of the supplement for better efficacy.")
    rationale: str = Field(..., description="Rationale behind the suggestion.")
    
class DosageWarning(BaseModel):
    """
    F-009: Dosage Warnings
    Warnings related to supplement dosages based on user data and interactions.
    """
    supplement: str = Field(..., description="The supplement for which the dosage warning is issued.")
    warning: str = Field(..., description="The dosage warning message.")
    

#TODO: Figure out what components need to be cached