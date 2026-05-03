---
name: verifica-riassunti
description: Verifica i riassunti di una lezione o di un'intera materia contro le guide e le risorse originali. Controlla copertura, allucinazioni, struttura e chiarezza, poi decide autonomamente se tenerli, colmarli o rigenerarli. Argomento: percorso relativo a lezione (02_semestre/materia/lezione) o materia (02_semestre/materia).
argument-hint: <semestre/materia> | <semestre/materia/lezione>
---

## Parsing degli argomenti

`$ARGUMENTS` è il path alla lezione o alla materia.

- **Materia** → 2 segmenti (es. `02_semestre/salute_mentale`)
- **Lezione** → 3 segmenti (es. `02_semestre/salute_mentale/02_storia_della_follia`)

---

## Prerequisiti

Verifica che esistano riassunti non vuoti prima di procedere.
Un file è non vuoto se supera entrambe le soglie (più di 3
righe **e** più di 100 parole):

```bash
for f in <path>/gen/*riassunto*.md; do
  [ -f "$f" ] \
    && [ "$(wc -l < "$f")" -gt 3 ] \
    && [ "$(wc -w < "$f")" -gt 100 ] \
    && echo "non-vuoto: $f"
done
```

Se non ci sono riassunti, **interrompi** e avvisa l'utente
di generarli prima con `/genera-riassunti`.

---

## Caso A — Lezione singola

Lancia un subagente con contesto fresco e passagli queste
istruzioni (con il percorso lezione già risolto):

**Cosa leggere:**
- `ai_assistant/ai_context.md`
- `ai_assistant/profilo_studente.md`
- Le tre guide: `ai_assistant/ai_guide/01_riassunto_dettagliato.md`,
  `02_riassunto_breve.md`, `03_riassunto_schematico.md`
- I riassunti esistenti in `<path>/gen/`
- Tutte le risorse in `<path>/risorse/` (solo file `.txt`)

**Cosa verificare:**

#### 1. Copertura del materiale
Scorri le risorse concetto per concetto. Per ogni argomento
rilevante (concetti chiave, autori, esempi significativi,
posizioni del professore), verifica che appaia nel
`01_riassunto_dettagliato.md`. Ignora divagazioni brevi
e aneddoti minori — considera solo ciò che uno studente
deve conoscere per l'esame.

#### 2. Allucinazioni
Scorri il `01_riassunto_dettagliato.md` affermazione per
affermazione. Ogni fatto, definizione, autore, data o
citazione deve essere rintracciabile nelle risorse.
- Affermazione non supportata da nessuna parte → rimuovi.
- Potrebbe essere corretta ma non verificabile → marca `[?]`.

#### 3. Struttura e conformità alle guide
Per ciascuno dei tre riassunti verifica:
- Tutte le sezioni richieste dalla guida sono presenti
  e non vuote (incluse le "Domande di orientamento allo
  studio" con risposte).
- Formato corretto (heading, tabelle, grassetto).
- Tono corretto (caldo/discorsivo per il dettagliato,
  asciutto per il breve, visivo per lo schematico).
- Coerenza interna: il breve non aggiunge concetti nuovi;
  lo schematico è allineato al dettagliato.

#### 4. Chiarezza
Segnala i passaggi ambigui o difficili da seguire. Usa
questo criterio: "capirei questo alle 2 di notte prima
di un esame?". Non toccare ciò che è già chiaro.

**Dopo la verifica — scegli una delle tre azioni:**

| Azione | Quando |
|--------|--------|
| **1 — Nessun cambiamento** | Copertura buona, nessuna allucinazione rilevata, struttura completa, testo chiaro |
| **2 — Colma** | Lacune minori: sezioni mancanti (es. Domande di orientamento), concetti non coperti, passaggi da chiarire — ma la struttura di base è solida. Aggiorna i file in place. |
| **3 — Rigenera** | Problemi sostanziali: copertura insufficiente, allucinazioni diffuse, struttura che non segue la guida, qualità complessiva inadeguata. Rigenera i riassunti da zero seguendo le guide. |

Esegui l'azione scelta senza chiedere conferma.

Al termine, produci un report sintetico in output:

```
## Verifica — <nome lezione>

Azione: [Nessun cambiamento | Colma | Rigenera]

Problemi trovati:
- [copertura] <concetto X non coperto> → aggiunto
- [allucinazione] <affermazione Y> → rimossa / marcata [?]
- [struttura] <sezione mancante> → aggiunta
- [chiarezza] <passaggio Z riscritto>

(Se azione 1: "Nessun problema rilevato.")
```

---

## Caso B — Materia intera

### 1. Subagenti per le lezioni — max 2 in parallelo

Per ogni cartella lezione con riassunti non vuoti,
lancia un subagente con le istruzioni del Caso A.

Procedi in batch da massimo 2 alla volta. Aspetta il
completamento di ogni batch prima di lanciare il
successivo.

### 2. Subagente per l'ampia panoramica

Dopo che tutti i subagenti lezione hanno completato,
lancia un subagente separato. Istruzioni:

**Cosa leggere:**
- `ai_assistant/ai_context.md`
- `ai_assistant/ai_guide/gen_ampia_panoramica.md`
- `<path>/gen_ampia_panoramica.md`
- Tutti i `*/gen/03_riassunto_schematico.md` non vuoti
  nella materia (questi sono la fonte della panoramica,
  non le risorse originali)

**Cosa verificare:**
1. Tutti i macro-temi delle lezioni sono rappresentati?
2. Ci sono affermazioni non rintracciabili negli schematici?
3. Le sezioni richieste dalla guida sono presenti?
   (incluse le "Domande di orientamento allo studio"
   trasversali con risposte)
4. Il documento riorganizza per temi e non per lezione?

Stessa logica decisionale (azione 1/2/3) applicata alla
panoramica. Esegui senza chiedere conferma.

### 3. Report finale

Riporta all'utente un riepilogo: lezioni verificate,
azioni eseguite per ciascuna, eventuali problemi
non risolvibili che richiedono revisione umana.
