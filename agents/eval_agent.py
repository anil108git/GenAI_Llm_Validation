import json
from pathlib import Path
from typing import Dict, Any

ROOT = Path(__file__).resolve().parents[1]


class EvalAgent:
    """Runs the generated cases through the evaluation service."""

    def run(self, generated_cases: Dict[str, Any]) -> Dict[str, Any]:
        output_path = ROOT / "src" / "test_data" / "generated_test_cases.json"
        if output_path.exists():
            cases = json.loads(output_path.read_text(encoding="utf-8"))
        else:
            cases = []

        return {
            "case_count": len(cases),
            "status": "ready_for_evaluation",
            "summary": "Cases are prepared and can be evaluated by the service.",
        }
