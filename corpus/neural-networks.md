# Neuronové sítě — systematický výklad

## 1. Co je neuronová síť

Neuronová síť je parametrizovaná funkce, která převádí vstupní data na výstup. Parametry se obvykle nazývají váhy a biasy. Síť se neučí jako biologický mozek; optimalizuje číselné parametry tak, aby na trénovacích příkladech minimalizovala zvolenou ztrátovou funkci.

Jedna vrstva může být zapsána:

`z = W x + b`

`a = f(z)`

`x` je vstupní vektor, `W` matice vah, `b` bias, `f` aktivační funkce a `a` výstup vrstvy. Složením mnoha vrstev vzniká hluboká síť.

## 2. Data a reprezentace

Model nepracuje přímo s významem slov, obrázků nebo zvuku. Pracuje s čísly. Text se nejprve tokenizuje; token může být celé slovo, část slova, znak nebo speciální symbol. Tokeny se převedou na identifikátory a embeddingová vrstva je mapuje na vektory. U obrázků mohou být vstupem hodnoty pixelů nebo příznaky z předchozích vrstev.

Kvalita dat často ovlivní výsledek více než zvětšení modelu. Důležité jsou reprezentativnost, deduplikace, licence, odstranění osobních údajů, vyvážení tříd a oddělení trénovací, validační a testovací množiny.

## 3. Aktivace

Bez nelineární aktivační funkce by libovolně hluboká posloupnost lineárních vrstev byla stále jen jednou lineární transformací. Časté funkce jsou ReLU `max(0,z)`, sigmoid `1/(1+e^-z)`, tanh a GELU. ReLU je jednoduchá a rychlá, ale může vést k trvale nulovým neuronům. Sigmoid a tanh mohou při velkých absolutních hodnotách saturovat a mít velmi malý gradient.

## 4. Ztráta a učení

Ztrátová funkce měří rozdíl mezi predikcí a cílem. Pro klasifikaci se často používá cross-entropy, pro regresi mean squared error. Optimalizace hledá parametry s menší ztrátou. Nejčastější metodou je gradientní sestup:

`theta_(t+1) = theta_t - eta * grad(L(theta_t))`

`eta` je learning rate. Příliš velký learning rate může učení rozkmitat, příliš malý může vést k pomalému učení nebo uvíznutí v nevhodném řešení.

## 5. Zpětné šíření

Backpropagation používá řetězové pravidlo derivování. Při průchodu vpřed síť vypočítá predikci a ztrátu. Při průchodu zpět spočítá, jak změna každého parametru ovlivňuje ztrátu. Optimalizátor podle gradientů upraví váhy. Gradient není vysvětlení lidského uvažování; je to lokální informace potřebná k optimalizaci.

Praktický trénovací krok má obvykle podobu: načíst batch, provést forward pass, vypočítat loss, vynulovat staré gradienty, provést backward pass, aktualizovat parametry a zaznamenat metriky.

## 6. Generalizace a přeučení

Přeučení (overfitting) nastává, když model dobře zapamatuje trénovací data, ale selhává na nových datech. Rozdíl mezi trénovací a validační chybou je důležitý diagnostický signál. Obrana zahrnuje více kvalitních dat, regularizaci, dropout, weight decay, data augmentation, early stopping a správně navrženou validaci.

Únik dat (data leakage) nastává, když se informace z validace nebo testu dostane do trénování. Pak jsou metriky nerealisticky optimistické. Testovací množina se má použít až na závěrečné vyhodnocení.

## 7. Konvoluční sítě

CNN využívají lokální filtry, sdílení vah a hierarchické příznaky. Konvoluce zachytí například hrany, pozdější vrstvy části objektů a ještě pozdější vrstvy složitější struktury. Pooling nebo stride zmenšuje prostorové rozměry, ale může ztratit přesnou lokalizaci. CNN jsou vhodné zejména pro obrazová a prostorová data.

## 8. Rekurentní sítě

RNN zpracovávají sekvenci postupně a udržují skrytý stav. LSTM a GRU přidávají mechanismy bran, které pomáhají řídit tok informace. Rekurentní zpracování je přirozené pro časové řady, ale špatně se paralelizuje u velmi dlouhých sekvencí.

## 9. Transformery a attention

Self-attention umožňuje tokenu vážit relevantnost ostatních tokenů v kontextu. Pro dotaz, klíč a hodnotu platí zjednodušeně:

`Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V`

Více hlav (multi-head attention) umožní sledovat různé vztahy. Transformer se dobře paralelizuje během trénování, ale standardní attention má s délkou sekvence vysoké paměťové nároky. Poziční informace se přidávají pozičním kódováním nebo jinou poziční reprezentací.

## 10. Jazykové modely

Autoregresivní jazykový model odhaduje pravděpodobnost dalšího tokenu podle předchozího kontextu:

`P(x_1,...,x_n) = product P(x_t | x_<t)`

Při generování se vybírá další token. Greedy decoding volí nejpravděpodobnější token, sampling náhodně vzorkuje z rozdělení, temperature mění jeho ostrost a top-p/top-k omezují množinu kandidátů. Tyto parametry nemění znalosti modelu, pouze strategii výběru.

Model může halucinovat: vytvořit přesvědčivě znějící, ale nepravdivé tvrzení. Pravděpodobnost tokenu není zárukou pravdivosti. Pro aktuální nebo citlivé informace je vhodné použít RAG, nástroje, citace a ověření člověkem.

## 11. Předtrénování, doladění a preference

Předtrénování učí model statistické pravidelnosti z velkého množství textu. Instruction tuning učí reagovat na instrukce. Preference optimization nebo RLHF/DPO upravuje chování podle preferovaných odpovědí. Doladění nepřidává spolehlivě nové znalosti jen tím, že zopakuje data; může také způsobit zapomínání, zkreslení nebo memorování.

## 12. GGUF a inference

GGUF je souborový formát používaný mimo jiné v ekosystému llama.cpp. Obsahuje váhy a metadata potřebná pro načtení modelu. Kvantizace ukládá některé váhy s menší přesností, například Q4 nebo Q5. Tím klesne velikost a nároky na paměť, ale může se změnit kvalita.

Inference je samotné použití již natrénovaného modelu. Provozní parametry jsou mimo jiné počet kontextových tokenů, počet generovaných tokenů, teplota, top-p, počet vláken, batch size a počet vrstev na GPU. Model v GGUF není automaticky bezpečný ani fakticky správný; bezpečnostní pravidla musí být v aplikaci a backendu.

## 13. RAG a vlastní korpus

Retrieval-Augmented Generation odděluje vyhledání zdrojů od generování. Dokument se rozdělí na chunky, každý chunk se převede na embedding a uloží do indexu. Při dotazu se vyhledají podobné chunky, případně se přerangují, a vloží se do promptu. Model pak odpovídá s oporou v dodaném kontextu.

Dobré chunky mají smysluplnou délku, překryv podle potřeby, metadata a stabilní identifikátor. Citace musí odkazovat na konkrétní zdrojový chunk. RAG není důkaz pravdy: špatný dokument může vést ke špatné odpovědi a model může kontext nesprávně interpretovat.

## 14. Vyhodnocování

Jedna metrika nestačí. Sledujte přesnost, úplnost, relevanci, latenci, spotřebu tokenů, halucinace, odmítnutí, stabilitu a chování v češtině. Připravte pevný evaluační soubor s běžnými, hraničními, nejednoznačnými a škodlivými dotazy. Výsledky porovnávejte po změně modelu, promptu, korpusu i kvantizace.

## 15. Bezpečnost a etika

Chraňte osobní údaje, logy a lokální endpointy. Omezte velikost vstupu, čas požadavku a spotřebu zdrojů. Prompt injection může přimět model ignorovat instrukce nebo vyzradit kontext; pokyny z načtených dokumentů zacházejte jako s daty, ne jako s autoritou. Uživatel musí vědět, zda odpověď vznikla z lokálního GGUF modelu, z internetu nebo z demo režimu.

Model není vědomí, osoba ani garant pravdy. Neuronová síť optimalizuje výstup podle vzorů a kontextu; sama od sebe nerozumí světu v lidském smyslu a bez řízeného procesu se nemá „sama učit“ z internetu.

## 16. Mini slovník

- **parametr:** naučená číselná hodnota modelu
- **hyperparametr:** nastavení trénování nebo inference zvolené uživatelem
- **embedding:** vektorová reprezentace položky
- **token:** jednotka textu zpracovaná modelem
- **epoch:** jeden průchod trénovací sadou
- **batch:** skupina příkladů zpracovaná v jednom kroku
- **gradient:** derivace ztráty podle parametrů
- **checkpoint:** uložený stav modelu
- **kvantizace:** snížení přesnosti reprezentace za účelem úspory zdrojů
- **RAG:** vyhledání kontextu před generováním odpovědi
