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
    """
    Compose the promnpt
    """
    supplement_list = "\n".join(f"-{name}" for name in request.supplements)

    lines = [
        "Role: You are an expert clinical pharmacologist and nutritionist specializing in supplement interactions.",
        "Task: Identify the CLINICALLY RELEVANT interactions that require intervention.", 
        "",
        "### User's Supplement Stack:"
        "Supplements:\n" + supplement_list,   
        "",
        "### CRITICAL Rules for Anaslysis:",
        "1. IGNORE THEORETICAL CONFLICTS: Do not report 'conflicts' based solely on in-vitro (test tube) chemistry if the combination is standard in clinial practice.",
        "2. FORMS MATTER: When suggesting optimizations, specify chemical forms (e.g., 'magnesium citrate' vs 'magnesium')"
        "3. SUMMARY IS MANDATORY: The 'anaylsis_summary' field must be a helpful paragraph, not a single word.",
        "4. DEPLETIONS: Check if any supplement depletes nutrients (e.g., Diuretics -> potassium, Zinc -> Copper).",
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