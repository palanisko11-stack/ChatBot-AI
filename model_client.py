import os
from typing import Optional

import requests

LLAMA_SERVER_URL = os.getenv("LLAMA_SERVER_URL", "http://localhost:8080")


def call_llama(prompt: str, max_tokens: int = 180, temperature: float = 0.2, timeout: int = 60):
    payloads = [
        {
            "prompt": prompt,
            "n_predict": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "stop": ["\n\nUživatel:", "\nUživatel:"]
        },
        {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "stop": ["\n\nUživatel:", "\nUživatel:"]
        }
    ]

    errors = []
    for payload in payloads:
        for endpoint in ("/v1/completions", "/completion"):
            url = f"{LLAMA_SERVER_URL.rstrip('/')}{endpoint}"
            try:
                response = requests.post(url, json=payload, timeout=timeout)
            except requests.RequestException as exc:
                errors.append(f"{endpoint}: {exc}")
                continue

            if not response.ok:
                errors.append(f"{endpoint}: {response.status_code} {response.text[:200]}")
                continue

            try:
                data = response.json()
            except ValueError:
                errors.append(f"{endpoint}: invalid JSON")
                continue

            if "choices" in data and data["choices"]:
                result = data["choices"][0].get("text")
                if result:
                    return result.strip()

            if "content" in data:
                content = data["content"]
                if isinstance(content, list):
                    text = "".join(item.get("text", "") for item in content if isinstance(item, dict))
                    if text:
                        return text.strip()
                elif isinstance(content, str):
                    return content.strip()

            errors.append(f"{endpoint}: unexpected response format")

    raise RuntimeError("; ".join(errors) or "llama.cpp endpoint is not reachable")
