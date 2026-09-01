import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents.requirement_agent import RequirementAgent
from agents.test_plan_agent import TestPlanAgent
from agents.test_case_agent import TestCaseAgent
from agents.eval_agent import EvalAgent


class AgentOrchestrator:
    """Simple orchestrator for the GenAI/LLM agent workflow."""

    def __init__(self):
        self.requirement_agent = RequirementAgent()
        self.test_plan_agent = TestPlanAgent()
        self.test_case_agent = TestCaseAgent()
        self.eval_agent = EvalAgent()

    def run(self) -> dict:
        requirement_data = self.requirement_agent.run()
        test_plan = self.test_plan_agent.run(requirement_data)
        generated_cases = self.test_case_agent.run(test_plan)
        evaluation_summary = self.eval_agent.run(generated_cases)

        return {
            "requirements": requirement_data,
            "test_plan": test_plan,
            "generated_cases": generated_cases,
            "evaluation": evaluation_summary,
        }


if __name__ == "__main__":
    result = AgentOrchestrator().run()
    print(result)
