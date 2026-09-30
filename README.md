# ChatBot-AI

Moderní, soukromý a přívětivý chatovací prototyp v češtině. Aplikace funguje ihned po otevření v prohlížeči bez backendu nebo API klíče.

## Co umí

- responzivní chatovací rozhraní v češtině
- rychlé akce pro začátek konverzace
- lokální ukládání zpráv v prohlížeči
- simulované odpovědi s kontextem posledních zpráv
- přepínač světlého a tmavého režimu
- klávesové zkratky: `Enter` odešle zprávu, `Shift + Enter` vloží nový řádek
- export konverzace do textového souboru a vymazání historie

## Spuštění

Otevřete `index.html` v prohlížeči, nebo spusťte libovolný lokální server:

```bash
python3 -m http.server 8000
```

Poté navštivte <http://localhost:8000>.

## Napojení skutečného modelu

Demo odpovědi jsou záměrně lokální. Pro produkci nahraďte funkci `generateReply()` v `app.js` voláním vlastního bezpečného backendu. API klíče nikdy nevkládejte do frontendového JavaScriptu.

## Principy

- **Soukromí:** data zůstávají v tomto prohlížeči.
- **Transparentnost:** aplikace jasně označuje, že odpovědi v demo režimu nejsou generovány externím modelem.
- **Přístupnost:** sémantické prvky, focus states, aria atributy a respektování `prefers-reduced-motion`.
