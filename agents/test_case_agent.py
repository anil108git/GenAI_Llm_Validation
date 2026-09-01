import json
from pathlib import Path
from typing import Dict, Any

ROOT = Path(__file__).resolve().parents[1]


class TestCaseAgent:
    """Transforms the requirements into structured evaluation cases."""

    def run(self, test_plan: Dict[str, Any]) -> Dict[str, Any]:
        from src.helpers.generate_test_cases import generate_cases

        cases = generate_cases()
        output_path = ROOT / "src" / "test_data" / "generated_test_cases.json"
        return {
            "count": len(cases),
            "output_path": str(output_path),
            "plan": test_plan,
        }
