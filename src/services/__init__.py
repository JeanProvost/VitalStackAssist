from typing import List, Dict, Any

INTERACTIONS_DB: Dict[str, Dict[str, Any]] = {
    "magnesium_vitamin d": {
        "summary": "Magnesium is required for the conversion of vitamin D into its active form.",
        "positive_interactions": [
            {
                "supplements": ["magnesium", "vitamin d"],
                "description": "Magnesium assists in the activation of vitamin D, which regulates calcium and phosphate absorption for healthy bones and immune function.",
                "evidence_level": "Strong",
                "source_url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6429623/"
            }
        ],
        "negative_interactions": []
    },
    "iron_zinc": {
        "summary": "High doses of iron and zinc can compete for absorption in the gut.",
        "positive_interactions": [],
        "negative_interactions": [
            {
                "supplements": ["iron", "zinc"],
                "description": "Iron and zinc are both divalent metals and compete for the same absorption pathways in the small intestine. Taking them together can reduce the absorption of both minerals.",
                "severity": "Moderate",
                "recommendation": "It is recommended to take iron and zinc supplements at least 2 hours apart to maximize absorption.",
                "source_url": "https://pubmed.ncbi.nlm.nih.gov/11465501/"
            }
        ]
    }
}

def get_interaction_analysis(supplements: List[str]) -> Dict[str, Any]:
    """
    Analyzes the interaction between a list of supplements.
    """
    if not supplements or len(supplements) < 2:
        return {
            "summary": "At least two supplements are required for an interaction analysis.",
            "positive_interactions": [],
            "negative_interactions": []
        }

    standardized_supplements = sorted([s.lower() for s in supplements])
    interaction_key = "_".join(standardized_supplements)

    return INTERACTIONS_DB.get(interaction_key, {
        "summary": "No significant interactions were found for the given combination of supplements.",
        "positive_interactions": [],
        "negative_interactions": []
    })