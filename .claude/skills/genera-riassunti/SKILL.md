---
name: genera-riassunti
description: Genera i 3 riassunti (dettagliato, breve, schematico) per una lezione o per tutte le lezioni di una materia, e aggiorna l'ampia panoramica. Se i riassunti esistono già, verifica e decide autonomamente se tenerli, colmarli o rigenerarli. Argomento: percorso relativo a lezione (02_semestre/materia/lezione) o materia (02_semestre/materia). Flag opzionale: "super-forza" per decidere e agire senza mai chiedere conferma.
argument-hint: <semestre/materia> | <semestre/materia/lezione> [super-forza]
---

## Input del workflow

In Claude Code, l'input è disponibile come `$ARGUMENTS`.
In Codex, è il testo che segue `$genera-riassunti`.
L'input può terminare con un flag opzionale separato da spazio.

- Estrai il **path** come tutto ciò che precede il flag finale.
- Il flag è valido solo se è esattamente l'ultima parola.

| Flag | Significato |
|---|---|
| nessuno | Processa; se i file esistono, decide autonomamente l'azione (vedi sotto) |
| `super-forza` | Decide autonomamente l'azione e la esegue senza mai chiedere conferma |

## Come riconoscere il tipo di argomento

Il path ha sempre questa struttura:

```
02_semestre/<materia>/<lezione>
```

- **Materia** → path ha 2 segmenti (es. `02_semestre/salute_mentale`)
- **Lezione** → path ha 3 segmenti (es. `02_semestre/salute_mentale/02_storia_della_follia`)

---

## Caso A — Lezione singola

### 0. Verifica path

Prima di tutto:

```bash
[ -d "<path>" ] || { echo "Errore: path non trovato: <path>"; exit 1; }
```

Se il path non esiste, **interrompi** e avvisa l'utente.

### 1. Controlla file esistenti

Usa `ls` (non un glob dello strumento) per verificare se `<path>/gen/`
contiene file generati (uno qualsiasi tra
`01_`, `02_`, `03_riassunto_*.md`).

Considera **non vuoto** solo un file che supera entrambe
le soglie: più di 3 righe **e** più di 100 parole:

```bash
for f in <path>/gen/*riassunto*.md; do
  [ -f "$f" ] \
    && [ "$(wc -l < "$f")" -gt 3 ] \
    && [ "$(wc -w < "$f")" -gt 100 ] \
    && echo "non-vuoto: $f"
done
```

- **Nessun file non vuoto trovato** → procedi al
  pre-processing e genera normalmente (step 2 → 3 → 4).
- **Almeno un file non vuoto trovato** → vai allo
  **Step 1b — Valutazione autonoma**.

### 1b. Valutazione autonoma (file esistenti)

Lancia un subagente con contesto fresco per valutare
la qualità dei riassunti esistenti. Istruzioni al subagente:

- Leggi `ai_assistant/ai_context.md`
- Leggi le guide:
  - `ai_assistant/ai_guide/01_riassunto_dettagliato.md`
  - `ai_assistant/ai_guide/02_riassunto_breve.md`
  - `ai_assistant/ai_guide/03_riassunto_schematico.md`
- Leggi i riassunti esistenti in `<path>/gen/`
- Leggi tutte le risorse in `<path>/risorse/`
  (file `.txt` preprocessati se presenti, altrimenti raw)
- Per ciascun riassunto, valuta:
  1. **Sezioni**: tutte le sezioni richieste dalla guida
     sono presenti e non vuote?
  2. **Copertura**: il contenuto delle risorse è coperto
     in modo adeguato? Ci sono concetti importanti assenti?
  3. **Qualità**: le spiegazioni sono chiare e complete?
     Il tono e il formato seguono la guida?
  4. **Ridondanze**: ci sono ripetizioni inutili da eliminare?
- Sulla base della valutazione, scegli **una** delle tre azioni:
  - **Azione 1 — Nessun cambiamento**: qualità e copertura
    sono sufficienti, struttura completa. Riporta "tutto ok".
  - **Azione 2 — Colma**: ci sono sezioni mancanti (es.
    "Domande di orientamento allo studio"), concetti non
    coperti, o passaggi da migliorare — ma la struttura
    di base è solida. Aggiorna i file in place senza
    riscrivere tutto.
  - **Azione 3 — Rigenera**: la copertura del materiale è
    insufficiente, la struttura non segue la guida, o la
    qualità complessiva non è adeguata. Rigenera il/i
    riassunto/i da zero.
- Se il flag è `super-forza`, esegui senza chiedere conferma; altrimenti chiedi conferma solo per l'azione 3.

Se l'azione è 3, torna allo step 2 per il pre-processing
e poi al 3 per la generazione.

### 2. Pre-processing

Verifica che ci sia almeno un file `.txt` in
`<path>/risorse/`. Se non ce n'è nessuno, **interrompi**
e avvisa l'utente che non ci sono trascrizioni da elaborare.

Se almeno un `.txt` è presente, esegui:

```bash
make preprocess FOLDER=<path>/risorse
```

Attendi il completamento prima di procedere.

Poi esegui il gate qualità sulle risorse:

```bash
python3 ai_assistant/find_failed_extractions.py --root <path>
```

Se l'output contiene righe EMPTY o GARBLED per questa lezione,
**interrompi** e mostra la lista all'utente. Non lanciare il subagente A.

### 3. Subagente A — Genera i 3 riassunti

Lancia un subagente con contesto fresco e passagli queste
istruzioni (con il percorso lezione già risolto):

- Leggi `ai_assistant/ai_context.md`
- Leggi `ai_assistant/profilo_studente.md`
- Leggi tutte le risorse in `<percorso-lezione-risolto>/risorse/`.
  Per ogni file: se il body è vuoto oppure il testo è palesemente
  corrotto (OCR scrambled, caratteri invertiti, cifre fuse in parole),
  interrompi immediatamente e avvisa l'utente con il nome del file
  e il tipo di problema (EMPTY / GARBLED). Non proseguire.
- Segui `ai_assistant/ai_guide/00_indice.md`
  → scrivi `<percorso-lezione-risolto>/gen/00_indice.md`
- Segui `ai_assistant/ai_guide/01_riassunto_dettagliato.md`
  → scrivi `<percorso-lezione-risolto>/gen/01_riassunto_dettagliato.md`
- Segui `ai_assistant/ai_guide/02_riassunto_breve.md`
  → scrivi `<percorso-lezione-risolto>/gen/02_riassunto_breve.md`
- Segui `ai_assistant/ai_guide/03_riassunto_schematico.md`
  → scrivi `<percorso-lezione-risolto>/gen/03_riassunto_schematico.md`

Dopo che il subagente A ha completato, verifica che i 4 file siano
stati scritti e non vuoti (stessa soglia dello step 1):

```bash
for f in <percorso-lezione-risolto>/gen/{00_indice,01_riassunto_dettagliato,02_riassunto_breve,03_riassunto_schematico}.md; do
  [ -f "$f" ] \
    && [ "$(wc -l < "$f")" -gt 3 ] \
    && [ "$(wc -w < "$f")" -gt 100 ] \
    && echo "ok: $f" || echo "MANCANTE O VUOTO: $f"
done
```

Se uno o più file risultano mancanti o vuoti, avvisa l'utente.

### 4. Subagente B — Aggiorna l'ampia panoramica

Dopo che il subagente A ha completato, la materia è la
cartella padre di `<path>`.

Lancia un subagente con contesto fresco e passagli queste
istruzioni (con i percorsi già risolti):

- Leggi `ai_assistant/ai_context.md`
- Leggi `ai_assistant/ai_guide/gen_ampia_panoramica.md`
- Input: tutti i `*/gen/03_riassunto_schematico.md`
  non vuoti in `<percorso-materia-risolto>/`
- Output: aggiorna `<percorso-materia-risolto>/gen_ampia_panoramica.md`

Dopo che il subagente B ha completato, verifica:

```bash
[ -f "<percorso-materia-risolto>/gen_ampia_panoramica.md" ] \
  && [ "$(wc -w < "<percorso-materia-risolto>/gen_ampia_panoramica.md")" -gt 100 ] \
  && echo "ok" || echo "MANCANTE O VUOTO: gen_ampia_panoramica.md"
```

Se il file risulta mancante o vuoto, avvisa l'utente.

---

## Caso B — Materia intera

### 1. Controlla file esistenti per ogni lezione

Per ogni cartella lezione in `<path>/`, applica lo stesso
controllo del Caso A step 1 (bash check + soglie identiche).

Classifica ogni lezione:
- **Senza file**: da generare.
- **Con file non vuoti**: da valutare autonomamente
  (come step 1b del Caso A).

### 2. Pre-processing di tutte le lezioni da processare

Per ogni lezione che contiene almeno un `.txt`
in `risorse/`, esegui in sequenza:

```bash
make preprocess FOLDER=<percorso-lezione>/risorse
```

Se dopo il pre-processing non ci sono `.txt` in `risorse/`,
salta la lezione e comunica.

### 3. Subagenti A — Una lezione per subagente, max 2 in parallelo

Lancia i subagenti A in batch da **massimo 2 alla volta**.

Per le lezioni **senza file**: ogni subagente riceve le
istruzioni del Caso A step 3.

Per le lezioni **con file esistenti**: ogni subagente
riceve le istruzioni del Caso A step 1b (valutazione
autonoma + azione scelta). Se l'azione è 3 (rigenera),
il subagente esegue anche il pre-processing e la
generazione completa.

Se il flag è `super-forza`, i subagenti agiscono senza chiedere conferma; altrimenti chiedono conferma solo per l'azione 3.

Aspetta che il batch corrente finisca prima di lanciare
il successivo.

### 4. Subagente B — Una sola volta, dopo che tutti gli A sono finiti

Aspetta che **tutti** i subagenti A abbiano completato.
Solo allora lancia **un singolo** subagente B con il path
materia risolto (come descritto nel Caso A step 4).

Questo sovrascrive `gen_ampia_panoramica.md` con la
visione aggiornata di tutte le lezioni della materia.

Dopo che il subagente B ha completato, verifica:

```bash
[ -f "<percorso-materia-risolto>/gen_ampia_panoramica.md" ] \
  && [ "$(wc -w < "<percorso-materia-risolto>/gen_ampia_panoramica.md")" -gt 100 ] \
  && echo "ok" || echo "MANCANTE O VUOTO: gen_ampia_panoramica.md"
```

Se il file risulta mancante o vuoto, avvisa l'utente.
