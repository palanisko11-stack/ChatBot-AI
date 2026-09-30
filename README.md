# ChatBot-AI

Moderní chatovací aplikace se znalostním korpusem a možností připojit GGUF model přes lokální backend.

## Co je v projektu

- `index.html` - webové rozhraní
- `styles.css` - vzhled a responzivita
- `app.js` - klientská logika a fallback režim
- `rag_backend.py` - backend s RAG a korpusem
- `corpus/` - strukturální český znalostní korpus
- `config.example.js` - konfigurace pro budoucí výkon
- `SETUP_GGUF.md` - návod na připojení GGUF modelu

## Spuštění lokálního demo

```bash
python3 -m http.server 8000
```

Pak otevřete <http://localhost:8000>.

## Spuštění backendu s RAG a korpusem

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python rag_backend.py
```

Backend běží na:

- http://localhost:5000/health
- http://localhost:5000/api/chat

## Povinné nastavení GGUF modelu

1. Nainstalujte llama.cpp.
2. Stáhněte GGUF model.
3. Spusťte server:

```bash
./server -m mistral-7b.Q4_K_M.gguf --host 0.0.0.0 --port 8080 --gpu-layers 35
```

4. Potom spusťte backend:

```bash
LLAMA_SERVER_URL=http://localhost:8080 python rag_backend.py
```

## Principy projektu

- model nesmí bez kontroly učit z internetu
- odpovědi čerpají z vlastního korpusu a ověřených zdrojů
- pokud model neví, má říct "nejsem si jistý"
- UI vždy umožňuje přepnout do demo režimu, když backend není dostupný
