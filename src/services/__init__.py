from typing import Dict, List

from ..models import (
    InteractionDetail,
    NegativeInteractionDetail,
    SupplementInteractionResponse,
)

# Static reference data used to emulate the behavior of the downstream AI model. The .NET layer
# is responsible for caching these responses. We keep them as DTO instances to ensure type safety
# throughout the calculator.
INTERACTIONS_DB: Dict[str, SupplementInteractionResponse] = {
    "magnesium_vitamin d": SupplementInteractionResponse(
        summary="Magnesium is required for the conversion of vitamin D into its active form.",
        positive_interactions=[
            InteractionDetail(
                supplements=["magnesium", "vitamin d"],
                description=(
                    "Magnesium assists in the activation of vitamin D, supporting calcium and "
                    "phosphate homeostasis for healthier bones and immune function."
                ),
                evidence_level="Strong",
                source_url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6429623/",
            )
        ],
    ),
    "iron_zinc": SupplementInteractionResponse(
        summary="High doses of iron and zinc can compete for absorption in the gut.",
        negative_interactions=[
            NegativeInteractionDetail(
                supplements=["iron", "zinc"],
                description=(
                    "Iron and zinc share intestinal transporters. Taking large doses together "
                    "can reduce the absorption of both minerals."
                ),
                severity="Moderate",
                recommendation="Separate iron and zinc supplementation by at least two hours.",
                source_url="https://pubmed.ncbi.nlm.nih.gov/11465501/",
            )
        ],
    ),
}


def get_interaction_analysis(supplements: List[str]) -> SupplementInteractionResponse:
    """Analyze interactions for a given supplement list and return a normalized DTO."""

    if len(supplements) < 2:
        return SupplementInteractionResponse(
            summary="At least two supplements are required for an interaction analysis.",
            positive_interactions=[],
            negative_interactions=[],
        )

    standardized_supplements = sorted(s.strip().lower() for s in supplements)
    interaction_key = "_".join(standardized_supplements)

    return INTERACTIONS_DB.get(
        interaction_key,
        SupplementInteractionResponse(
            summary="No significant interactions were found for the given combination of supplements.",
            positive_interactions=[],
            negative_interactions=[],
        ),
    )
