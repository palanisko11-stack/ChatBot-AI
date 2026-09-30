#!/usr/bin/env python3
import json
import math
import os
import re
from collections import Counter
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent
CORPUS_PATH = BASE_DIR / "corpus" / "knowledge.jsonl"
LLAMA_SERVER_URL = os.getenv("LLAMA_SERVER_URL", "http://localhost:8080")


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def tokenize(text: str):
    text = text.lower()
    text = text.replace("\n", " ")
    return re.findall(r"[a-z0-9áčďéěíňóřšťúůýž]+", text)


def norm_score(query: str, entry: dict) -> float:
    q_tokens = Counter(tokenize(query))
    t_tokens = Counter(tokenize(str(entry.get("text", ""))))
    if not q_tokens or not t_tokens:
        return 0.0

    common = set(q_tokens) & set(t_tokens)
    if not common:
        return 0.0

    dot = sum(q_tokens[k] * t_tokens[k] for k in common)
    q_norm = math.sqrt(sum(v * v for v in q_tokens.values()))
    d_norm = math.sqrt(sum(v * v for v in t_tokens.values()))
    if q_norm == 0 or d_norm == 0:
        return 0.0
    return dot / (q_norm * d_norm)


def load_corpus(path: Path):
    entries = []
    if not path.exists():
        return entries
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


CORPUS = load_corpus(CORPUS_PATH)


def choose_relevant(query: str, limit: int = 4):
    scored = []
    for entry in CORPUS:
        score = norm_score(query, entry)
        if "topic" in entry:
            score += 0.05 * sum(1 for token in tokenize(str(entry["topic"])) if token in tokenize(query))
        if "text" in entry:
            score += 0.03 * sum(1 for token in tokenize(str(entry["text"])) if token in tokenize(query))
        scored.append((score, entry))
    scored = sorted(scored, key=lambda x: x[0], reverse=True)
    return [entry for _, entry in scored[:limit] if _ > 0.0]


def call_model(prompt: str, max_tokens: int = 180, temperature: float = 0.2):
    payloads = [
        {
            "prompt": prompt,
            "n_predict": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "stop": ["\n\nUživatel:", "\nUživatel:", "</s>"]
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
                response = requests.post(url, json=payload, timeout=60)
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

    raise RuntimeError("; ".join(errors) or "Model endpoint is not reachable")


@app.get("/health")
def health():
    return jsonify({"status": "ok", "model_backend": LLAMA_SERVER_URL, "corpus_count": len(CORPUS)})


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Chybí text zprávy."}), 400

    relevant = choose_relevant(message, limit=4)

    if not relevant:
        context_block = "Žádný relevantní korpus nebyl nalezen. Odpověď poskytněte obecně a označte, že nejste jistý."
    else:
        context_block = "\n\n".join(
            f"[{idx + 1}] {entry.get('text', '')}\nZdroj: {entry.get('source', 'interní-korpus')}"
            for idx, entry in enumerate(relevant)
        )

    system_prompt = (
        "Jsi znalostní asistent v češtině. Odpovídej výhradně na základě níže uvedeného kontextu. "
        "Pokud informace v kontextu chybí, řekni, že si nejste jistý, a nabídni, co by bylo vhodné ověřit. "
        "U každé podstatné odpovědi uveď citaci ve formátu [1], [2] podle zdrojů v kontextu."
    )

    prompt = (
        f"{system_prompt}\n\nKontext:\n{context_block}\n\n"
        f"Uživatel: {message}\n\nAsistent:"
    )

    try:
        answer = call_model(prompt, max_tokens=int(data.get("max_tokens", 180)), temperature=float(data.get("temperature", 0.3)))
    except Exception as exc:
        return jsonify({
            "reply": "Model je v tomto okamžiku nedostupný. Prosím zkontrolujte, zda běží llama.cpp server nebo přepněte režim demo.",
            "sources": [],
            "error": str(exc)
        }), 503

    refs = [{
        "id": item.get("id", "unknown"),
        "source": item.get("source", "interní-korpus"),
        "topic": item.get("topic", "general"),
        "score": round(norm_score(message, item), 3)
    } for item in relevant]

    return jsonify({
        "reply": answer.strip(),
        "sources": refs,
        "model": "gguf-rag-backend",
        "retrieved": len(relevant)
    })


if __name__ == "__main__":
    print("\n🤖 ChatBot-AI RAG backend")
    print(f"   Corpus: {CORPUS_PATH}")
    print(f"   llama.cpp endpoint: {LLAMA_SERVER_URL}")
    app.run(host="0.0.0.0", port=5000, debug=False)
