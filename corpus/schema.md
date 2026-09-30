# Schéma a pravidla korpusu

## Povinná pole každé pasáže

`id` — stabilní unikátní identifikátor.

`topic` — jedno nebo více témat, například `transformer`, `training`, `gguf`, `rag`.

`level` — `beginner`, `intermediate` nebo `advanced`.

`text` — samostatně srozumitelná pasáž bez neověřených absolutních tvrzení.

`source` — relativní cesta nebo externí URL.

`updated_at` — datum poslední věcné kontroly ve formátu ISO 8601.

## Pravidla kvality

- Jedna pasáž má jednu hlavní myšlenku.
- Matematické symboly zapisujte jednoznačně a vysvětlete proměnné.
- Oddělujte fakta, intuici, doporučení a omezení.
- U tvrzení závislých na čase uvádějte datum a externí zdroj.
- Nepřidávejte osobní údaje, tajné klíče ani instrukce k obcházení bezpečnosti.
- Zachovejte licenci a původ každého převzatého textu.
- Po změně korpusu spusťte evaluační sadu a aktualizujte `updated_at`.

## RAG metadata

Při indexaci doporučujeme přidat `document_id`, `chunk_index`, `embedding_model`, `language: cs` a hash obsahu. Při odpovědi vraťte identifikátory zdrojových pasáží, aby UI mohlo zobrazit dohledatelné citace.
