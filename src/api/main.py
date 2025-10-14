from fastapi import FastAPI
from ..models import SupplementInteractionRequest, SupplementInteractionResponse
from ..services import get_interaction_analysis

app = FastAPI(
    title="VitalStackAssist API",
    description="An API to analyze interactions between dietary supplements.",
    version="1.0.0"
)

@app.post("/generate-interactions", response_model=SupplementInteractionResponse)
def generate_interactions(request: SupplementInteractionRequest):
    """
    Analyzes and returns potential interactions between a given list of supplements.
    """
    return get_interaction_analysis(request.supplements)
