from typing import List
from src.models import SupplementInteractionRequest, SupplementInteractionResponse
from src.ai.analysis import generate_interaction_report

def get_interaction_analysis(supplements: List[str]) -> SupplementInteractionResponse:
    """
    Orchestrates the interaction analysis by creating a request object
    and calling the AI analysis service.
    """
    request = SupplementInteractionRequest(supplements=supplements)
    return generate_interaction_report(request)
