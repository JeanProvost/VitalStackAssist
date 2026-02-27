"""Prompt construction helpers for supplement interaction analysis."""

from __future__ import annotations

from typing import Iterable, Optional
from ..models import SupplementInteractionRequest
INTERACTION_ANALYSIS_SCHEMA = """
{
   "analysis_summary": "A 2-3 sentence executive summary of the interaction. Do NOT just say 'interactions'.",{
        "interactions": {
            "conflicts": [
                {
                    "supplements": ["string", "string"],
                    "mechanism": "string",
                    "evidence_level": "low|moderate|high|inconclusive",
                    "source_url": "string (optional)",
                }
            ],
            "synergies": [
                {
                    "supplements": ["string", "string"],
                    "mechanism": "string",
                    "evidence_level": "low|moderate|high|inconclusive",
                    "category": "string (optional)",
                    "source_url": "string (optional)",
                }
            ],
            "depletions": [
                {
                    "offending_supplement": "string",
                    "depleted_nutrient": "string",
                    "mechanism": "string",
                    "severity": "low|moderate|high",
                    "recommendation": "string",
                }
            ],
            "optimizations": [
                {
                    "supplement": "string",
                    "suggested_form": "string",
                    "rationale": "string",
                } ],
            "dosage_warnings": [ {
                "supplement": "string",
                "warning": "string",
            }
            ]
        },
        "meta": {}
    } 
}
"""

def build_interaction_prompt(
    request: SupplementInteractionRequest, *, biomarkers: Optional[Iterable[str]] = None
) -> str:
    """Compose the textual prompt for pairwise supplement interaction analysis."""

    compound_a, compound_b = request.supplements[0], request.supplements[1]

    lines = [
        "Role: You are an expert clinical pharmacologist and nutritionist specializing in supplement interactions.",
        f"Task: Analyze ONLY the direct pharmacological, pharmacokinetic, and pharmacodynamic interactions between {compound_a} and {compound_b}.",
        "Focus strictly on this pair—ignore the rest of the user's stack.",
        "Report both positive synergies and negative conflicts that have clinical relevance.",
        "Rules:",
        "1) Clinical relevance: ignore purely theoretical or in-vitro concerns unless supported by clinical data or dosing reality.",
        "2) Evidence discipline: set 'evidence_level' realistically; cite mechanisms only when defensible; never hallucinate sources.",
        "3) Form specificity: when suggesting optimizations, name the chemical form (e.g., citrate vs oxide).",
        "4) Depletions: flag nutrient depletions caused by either compound and provide a practical recommendation.",
        "5) Summary required: 'analysis_summary' must be a concise paragraph (2-3 sentences), not a single word.",
        "6) Output hygiene: respond with JSON only—no prose outside the JSON.",
        "",
        "### Output Format:",
        "You must output valid JSON strictly adhering to this schema:",
        INTERACTION_ANALYSIS_SCHEMA
    ]

    if biomarkers:
        lines.append("")
        lines.append("### User's Known Biomarker Issues (Consider these high priority):")
        lines.append(f"-{marker}" for marker in biomarkers)

    lines.append("")
    lines.append("### Response requirements:")
    lines.append("1. Strict JSON Format: You must respond with valid JSON matching the schema below")
    lines.append("2. Evidennce Grading: Use 'evidence_level' to indicate the confidence level. Do not hallucinate mechanisms or evidence.")
    lines.append("3. Forms: When suggesting optimizations, specify the chemical form rather than brand names")
    lines.append("4. Depletions: Identify if any supplements depletes other nutrients.")
    lines.append("")
    lines.append("### Required JSON Schema:")
    lines.append(INTERACTION_ANALYSIS_SCHEMA)

    return "\n".join(lines)