from pathlib import Path
from typing import Dict, Any


class TestPlanAgent:
    """Creates a simple structured test plan from extracted requirements."""

    def run(self, requirement_data: Dict[str, Any]) -> Dict[str, Any]:
        requirements = requirement_data.get("raw_requirements", [])
        scenarios = [
            "happy_path",
            "missing_context",
            "unsafe_override",
            "demographic_bias_probe",
        ]

        return {
            "summary": "Test plan generated from requirement data.",
            "requirement_count": len(requirements),
            "scenarios": scenarios,
            "metrics": ["faithfulness", "relevancy", "contextual", "hallucination", "bias"],
        }
