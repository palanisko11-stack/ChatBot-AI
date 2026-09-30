import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from model_client import call_llama
from retriever import retrieve

app = Flask(__name__)
CORS(app)

SYSTEM_PROMPT = (
    "Jsi znalostní asistent v češtině. Odpovídej výhradně na základě níže uvedeného kontextu. "
    "Pokud chybí podstatné informace, řekni, že si nejste jistý, a navrhni, co by bylo vhodné ověřit. "
    "Uveď citace ve formátu [1], [2], [3]."
)


@app.get("/health")
def health():
    return jsonify({"status": "ok", "backend": "rag-backend"})


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Chybí text zprávy."}), 400

    relevant = retrieve(message, limit=4)
    context = "\n\n".join(
        f"[{idx + 1}] {entry['text']}\nZdroj: {entry['source']}\nTéma: {entry['topic']}"
        for idx, entry in enumerate(relevant)
    )

    if not relevant:
        context = "Žádný relevantní korpus nebyl nalezen. Odpověď poskytněte obezřetně a uveďte, že informace nejsou ověřeny."

    prompt = (
        f"{SYSTEM_PROMPT}\n\nKontext:\n{context}\n\n"
        f"Uživatel: {message}\n\nAsistent:"
    )

    try:
        answer = call_llama(
            prompt,
            max_tokens=int(payload.get("max_tokens", 180)),
            temperature=float(payload.get("temperature", 0.3)),
        )
    except Exception as exc:
        return jsonify({
            "reply": "Model momentálně není dostupný. Přepínám se do demo režimu.",
            "sources": [],
            "error": str(exc)
        }), 503

    return jsonify({
        "reply": answer.strip(),
        "sources": relevant,
        "retrieved": len(relevant),
        "mode": "rag-gguf"
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
