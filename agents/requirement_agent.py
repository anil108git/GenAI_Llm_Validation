from pathlib import Path
from typing import Dict, Any

ROOT = Path(__file__).resolve().parents[1]


class RequirementAgent:
    """Extracts structured requirements from a requirement source file."""

    def __init__(self, source_path: str | None = None):
        self.source_path = Path(source_path) if source_path else ROOT / "src" / "test_data" / "requirement_spec.txt"

    def run(self) -> Dict[str, Any]:
        text = self.source_path.read_text(encoding="utf-8")
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        return {
            "source": str(self.source_path),
            "line_count": len(lines),
            "summary": "Requirements loaded for test plan generation.",
            "raw_requirements": lines,
        }
