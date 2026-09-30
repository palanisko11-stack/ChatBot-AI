# Vlastní znalostní korpus: neuronové sítě

Tento adresář je vzdělávací korpus pro ChatBot-AI. Je psaný tak, aby ho mohl číst člověk i retrieval systém (RAG). Korpus **není tréninkový dataset sám o sobě** a nečiní model automaticky pravdivým; při použití je nutné uvádět zdroj, verzi a datum ověření.

## Obsah

- `neural-networks.md` — souvislý český výklad od základů po moderní architektury.
- `knowledge.jsonl` — atomické znalostní pasáže s identifikátorem, tématy a úrovní.
- `schema.md` — pravidla pro rozšiřování a validaci korpusu.

## Doporučené použití

1. Korpus načtěte do vektorové databáze (např. Chroma, Qdrant nebo pgvector).
2. Dokumenty rozdělte podle nadpisů, zachovejte `id`, `source` a `updated_at`.
3. Při dotazu vyhledejte nejrelevantnější pasáže a vložte je do kontextu modelu.
4. Odpověď označte jako znalost z korpusu a nabídněte odkaz na zdrojový dokument.
5. Nové pasáže přidávejte až po odborné kontrole; internetový obsah není automaticky pravdivý.

## Zásada přesnosti

Výklad záměrně rozlišuje matematický popis, praktickou intuici a omezení. Pokud je tvrzení závislé na konkrétní knihovně, hardwaru nebo aktuálním výzkumu, musí být doplněn externí a časově označený zdroj.
