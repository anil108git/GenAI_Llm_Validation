import json
import os
from pathlib import Path
from typing import Any, Dict
from urllib import error, request


def _load_env_file() -> None:
    project_root = Path(__file__).resolve().parents[2]
    for filename in (".env", ".env.dev"):
        env_path = project_root / filename
        if not env_path.exists():
            continue
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


class OpenRouterJudge:
    def __init__(self) -> None:
        _load_env_file()
        self.api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4.1-mini")
        self.http_referer = os.getenv("OPENROUTER_HTTP_REFERER", "http://localhost:3000")
        self.app_title = os.getenv("OPENROUTER_X_TITLE", "genAI-LLm-evelFramework")

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def score(self, metric_name: str, prompt: str, response: str, context: str | None = None, retrieval_context: str | None = None) -> Dict[str, Any]:
        if not self.is_configured():
            return {"score": 0.0, "success": False, "reason": "OPENROUTER_API_KEY not configured"}

        system_prompt = (
            "You are a strict evaluator for an AI response. "
            "Return valid JSON with keys: score, success, reason. "
            "Score must be between 0 and 1."
        )
        user_prompt = (
            f"Metric: {metric_name}\n"
            f"Prompt: {prompt}\n"
            f"Response: {response}\n"
            f"Context: {context or ''}\n"
            f"Retrieval Context: {retrieval_context or ''}\n"
            "Judge whether the response is acceptable for this metric and provide a numeric score."
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.http_referer,
            "X-Title": self.app_title,
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0,
        }

        try:
            req = request.Request(
                f"{self.base_url}/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with request.urlopen(req, timeout=60) as response:
                raw_content = response.read().decode("utf-8")
            data = json.loads(raw_content)
            content = data["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            return {
                "score": float(parsed.get("score", 0.0)),
                "success": bool(parsed.get("success", False)),
                "reason": parsed.get("reason", "")
            }
        except (error.URLError, error.HTTPError, KeyError, json.JSONDecodeError, ValueError) as exc:
            return {"score": 0.0, "success": False, "reason": f"OpenRouter request failed: {exc}"}
