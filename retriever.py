import json
import math
import re
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CORPUS_PATH = BASE_DIR / "corpus" / "knowledge.jsonl"


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def tokenize(text: str):
    text = (text or "").lower()
    text = text.replace("\n", " ")
    return re.findall(r"[a-z0-9áčďéěíňóřšťúůýž]+", text)


def compute_similarity(query: str, entry: dict) -> float:
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


def retrieve(query: str, limit: int = 4):
    scored = []
    q_tokens = set(tokenize(query))

    for entry in CORPUS:
        score = compute_similarity(query, entry)
        topic = str(entry.get("topic", ""))
        score += 0.08 * sum(1 for token in tokenize(topic) if token in q_tokens)
        score += 0.04 * sum(1 for token in tokenize(entry.get("text", "")) if token in q_tokens)
        scored.append((score, entry))

    scored = sorted(scored, key=lambda x: x[0], reverse=True)
    return [{
        "id": item.get("id", "unknown"),
        "topic": item.get("topic", "general"),
        "level": item.get("level", "unknown"),
        "source": item.get("source", "internal-corpus"),
        "text": item.get("text", ""),
        "score": round(score, 4),
    } for score, item in scored[:limit] if score > 0.0]
