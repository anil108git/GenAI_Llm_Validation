# genAI-LLm-evelFramework

A lightweight hybrid framework for exercising a local Python evaluation service through Playwright-based evaluation tests. The repository includes a FastAPI evaluation service, a Playwright test runner, Python generators for realistic test artifacts, and dual reporting (Playwright HTML + Allure).

IMPORTANT: This repository contains deterministic medical-rule examples for adversarial testing. These materials are for testing and research only and are not clinical advice. Do not use this content for patient care.

## Repository layout

```
├── agents/                   # Python agent layer (Requirement → TestPlan → TestCase → Eval)
│   ├── orchestrator.py       #   End-to-end workflow orchestrator
│   ├── requirement_agent.py
│   ├── test_plan_agent.py
│   ├── test_case_agent.py
│   └── eval_agent.py
├── eval_engine/              # FastAPI evaluation service
│   ├── eval_service.py       #   Entry point
│   ├── requirements.txt
│   └── Dockerfile
├── src/
│   ├── helpers/
│   │   ├── generate_test_cases.py       # JSON generator from requirement spec
│   │   ├── generate_playwright_specs.py # JSON → per-metric .spec.js files
│   │   ├── eval_bridge.js / .ts        # Service call helpers
│   │   └── openrouter_judge.py
│   └── test_data/
│       ├── requirement_spec.txt             # Deterministic seed requirements (42 rules)
│       └── generated_test_cases.json        # Output: 87 structured test cases
├── tests/genai/              # Playwright evaluation spec files
│   ├── eval-smoke.spec.js    #   Smoke test (health check)
│   ├── faithfulness.spec.js  #   48 cases
│   ├── relevancy.spec.js     #    7 cases
│   ├── contextual.spec.js    #    8 cases
│   ├── hallucination.spec.js #   13 cases
│   └── bias.spec.js          #   11 cases
├── .github/workflows/
│   └── run-evals.yml         # CI workflow scaffold
├── playwright.config.js      # Playwright config (list + HTML + Allure reporters)
├── package.json
└── AGENTS.md
```

## Setup

```bash
# Node dependencies
npm install
npx playwright install --with-deps chromium

# Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r eval_engine/requirements.txt
```

## Pipeline

Run in this order every time:

```bash
# 1 — Generate JSON test cases from requirement spec
python3 src/helpers/generate_test_cases.py

# 2 — Generate per-metric Playwright spec files from JSON
python3 src/helpers/generate_playwright_specs.py

# 3 — Start the eval service (terminal 1)
source .venv/bin/activate
uvicorn eval_engine.eval_service:app --host 127.0.0.1 --port 8000

# 4 — Run evaluation tests (terminal 2)
npx playwright test tests/genai/
```

The full suite runs **89 tests** (87 metric + 2 smoke) across 5 metrics. Each test calls a dedicated `/evaluate/{metric}` endpoint and asserts the score meets the configured threshold.

## Test case schema

Each generated test case is self-explanatory. A QA engineer can immediately understand what was tested and why.

| Field | Set at generation | Set during evaluation | Description |
|-------|:-:|:-:|-------------|
| `id` | ✓ | — | Unique ID (TC-001 … TC-087) |
| `requirement` | ✓ | — | Original rule from requirement spec |
| `section` | ✓ | — | Section heading |
| `scenario` | ✓ | — | Scenario type: base, missing_context, demographic_bias_probe, unsafe_override |
| `metric` | ✓ | — | Evaluation metric |
| `user_query` | ✓ | — | Realistic clinical question (what the user asked) |
| `system_prompt` | ✓ | — | How the LLM is instructed to respond |
| `expected_answer` | ✓ | — | Ground-truth answer derived from the requirement |
| `actual_llm_response` | — | ✓ | The LLM's actual output (null until evaluation) |
| `evaluation` | — | ✓ | `{metric, threshold, score, pass}` |
| `context` | ✓ | — | Full clinical context |
| `retrieval_context` | ✓ | — | RAG-retrieved chunk |
| `demographic_features` | ✓ | — | Demographics for bias probes |
| `threshold` | ✓ | — | Metric-specific pass/fail threshold |
| `prompt` | ✓ | — | Backward-compat alias for `system_prompt` |
| `response` | ✓ | — | Backward-compat alias for `expected_answer` |
| `expected_outcome` | ✓ | — | Expected pass/fail |

### Field distinctions

| Concept | What it is |
|---------|-----------|
| **Requirement** | The safety rule or clinical guideline being tested |
| **User Query** | What a clinician or patient actually asked |
| **System Prompt** | How the LLM is instructed to behave |
| **Retrieved Context** | What the RAG system retrieved |
| **Expected Answer** | The correct answer the LLM should give |
| **Actual LLM Response** | What the LLM actually answered (set during evaluation) |

## Reports

Two reporters run automatically during step 4:

| Report | View command | Output |
|--------|-------------|--------|
| Playwright HTML | `npm run report:playwright` | `playwright-report/` |
| Allure | `npm run report:allure` | `allure-results/` → `allure-report/` |

Playwright HTML groups tests by spec file (metric). Allure groups by feature (requirement section) and includes severity labels, story links, user query, and full markdown descriptions.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| POST | `/evaluate/faithfulness` | |
| POST | `/evaluate/relevancy` | Returns `{score, success}` |
| POST | `/evaluate/contextual` | |
| POST | `/evaluate/hallucination` | |
| POST | `/evaluate/bias` | |
| POST | `/generate/test-cases` | Generate cases from requirement spec |

## LLM-as-judge configuration

Set these in `.env` (copy from `.env.example`):

```env
OPENROUTER_API_KEY=your_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-4.1-mini
OPENROUTER_HTTP_REFERER=http://localhost:3000
OPENROUTER_X_TITLE=genAI-LLm-evelFramework
```

If the key is present, the service uses OpenRouter for scoring; otherwise it falls back to the built-in heuristic scorer.

## Safety note

Treat all repository content as non-production research material. Avoid using the deterministic medical examples in production systems or as real-world clinical guidance.
