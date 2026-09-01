# Agent workflow for genAI-LLm-evelFramework

This repository includes a starter agent layer for GenAI/LLM evaluation tasks and a Playwright-based evaluation runner with dual reporting (HTML + Allure).

## Available agents

- **RequirementAgent**: reads requirement input and extracts a structured summary.
- **TestPlanAgent**: converts requirements into a simple test plan with scenario categories.
- **TestCaseAgent**: generates structured evaluation cases from the requirement source.
- **EvalAgent**: prepares generated cases for evaluation.
- **AgentOrchestrator**: runs the workflow end to end.

## Full pipeline

```bash
source .venv/bin/activate

# Step 1 — Generate JSON test cases from requirement spec
python3 src/helpers/generate_test_cases.py

# Step 2 — Convert JSON into per-metric Playwright spec files
python3 src/helpers/generate_playwright_specs.py

# Step 3 — Start the eval service (in a separate terminal)
uvicorn eval_engine.eval_service:app --host 127.0.0.1 --port 8000

# Step 4 — Run all evaluation tests
npx playwright test tests/genai/
```

## View reports

```bash
# Playwright HTML report
npm run report:playwright

# Allure report (requires previously run tests with allure-results/)
npm run report:allure
```

## Test case schema

Each generated test case contains these fields:

| Field | Generation time | Evaluation time | Description |
|-------|----------------|-----------------|-------------|
| `id` | ✓ | — | Unique test case ID (TC-001 … TC-087) |
| `requirement` | ✓ | — | Original requirement rule from spec |
| `section` | ✓ | — | Section heading from requirement spec |
| `scenario` | ✓ | — | Scenario type: base / missing_context / demographic_bias_probe / unsafe_override |
| `metric` | ✓ | — | Evaluation metric: faithfulness / relevancy / contextual / hallucination / bias |
| `user_query` | ✓ | — | Realistic clinical question generated from the requirement |
| `system_prompt` | ✓ | — | System prompt instructing the LLM how to respond |
| `expected_answer` | ✓ | — | Ground-truth answer the LLM should produce |
| `actual_llm_response` | — | ✓ | The LLM's actual response (null at generation time) |
| `evaluation` | — | ✓ | Nested object: `{metric, threshold, score, pass}` (null at generation) |
| `context` | ✓ | — | Full clinical context for the scenario |
| `retrieval_context` | ✓ | — | Shorter retrieved chunk (simulates RAG retrieval) |
| `demographic_features` | ✓ | — | Demographic attributes for bias probes |
| `threshold` | ✓ | — | Pass/fail threshold for the metric |
| `prompt` | ✓ | — | Backward-compat alias for `system_prompt` |
| `response` | ✓ | — | Backward-compat alias for `expected_answer` |
| `expected_outcome` | ✓ | — | Expected pass/fail outcome |

## Notes

- The current implementation is intentionally lightweight and modular.
- It uses the existing generator and evaluation service as the execution backbone.
- Step 2 produces one `.spec.js` per metric (faithfulness, relevancy, contextual, hallucination, bias) with inline test data — no runtime file reads.
- Both reporters are configured in `playwright.config.js`; Allure results are generated automatically during test execution.
- Each spec file shows the full test case details (user query, system prompt, expected answer, context) in Allure descriptions and Playwright annotations.
