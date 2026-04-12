---
name: genera-riassunti
description: Genera i 3 riassunti (dettagliato, breve, schematico) per una lezione o per tutte le lezioni di una materia, e aggiorna l'ampia panoramica. Argomento: percorso relativo a lezione (02_semestre/materia/lezione) o materia (02_semestre/materia). Flag opzionali: "forza" per materia (chiede conferma se i file esistono), "super-forza" per rigenerare tutto senza chiedere.
argument-hint: <semestre/materia> | <semestre/materia/lezione> [forza|super-forza]
---

## Parsing degli argomenti

`$ARGUMENTS` può terminare con un flag opzionale separato da spazio.

- Estrai il **path** come tutto ciò che precede il flag finale.
- Il flag è valido solo se è esattamente l'ultima parola.

| Flag | Significato |
|---|---|
| nessuno | Processa; chiedi conferma se i file `gen/` esistono già |
| `forza` | Richiesto per materia intera; chiedi conferma se i file esistono |
| `super-forza` | Rigenerare tutto senza chiedere, in entrambi i casi |

## Come riconoscere il tipo di argomento

Il path ha sempre questa struttura:

```
02_semestre/<materia>/<lezione>
```

- **Materia** → path ha 2 segmenti (es. `02_semestre/salute_mentale`)
- **Lezione** → path ha 3 segmenti (es. `02_semestre/salute_mentale/02_storia_della_follia`)

---

## Caso A — Lezione singola

### 1. Controlla file esistenti

Verifica se `<path>/gen/` contiene già file generati
(uno qualsiasi tra `01_`, `02_`, `03_riassunto_*.md`).

- Se esistono e il flag **non** è `super-forza`:
  chiedi all'utente se vuole rigenerarli. Se risponde no,
  **interrompi**.
- Se esistono e il flag è `super-forza`: procedi senza chiedere.
- Se non esistono: procedi.

### 2. Pre-processing

Verifica che ci sia almeno un file `.txt` in
`<path>/risorse/`. Se non ce n'è nessuno, **interrompi**
e avvisa l'utente che non ci sono trascrizioni da elaborare.

Se almeno un `.txt` è presente, esegui:

```bash
make preprocess FOLDER=<path>/risorse
```

Attendi il completamento prima di procedere.

### 3. Subagente A — Genera i 3 riassunti

Lancia un subagente con contesto fresco e passagli queste
istruzioni (con il percorso lezione già risolto):

- Leggi `ai_assistant/ai_context.md`
- Leggi `ai_assistant/profilo_studente.md`
- Leggi tutte le risorse in `<percorso-lezione-risolto>/risorse/`
- Segui `ai_assistant/ai_guide/01_riassunto_dettagliato.md`
  → scrivi `<percorso-lezione-risolto>/gen/01_riassunto_dettagliato.md`
- Segui `ai_assistant/ai_guide/02_riassunto_breve.md`
  → scrivi `<percorso-lezione-risolto>/gen/02_riassunto_breve.md`
- Segui `ai_assistant/ai_guide/03_riassunto_schematico.md`
  → scrivi `<percorso-lezione-risolto>/gen/03_riassunto_schematico.md`

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

---

## Caso B — Materia intera

**Richiede `forza` o `super-forza`.** Se nessuno dei due è
presente, **interrompi** e avvisa l'utente che processare
un'intera materia è costoso e richiede il flag esplicito.
Esempio: `genera-riassunti 02_semestre/salute_mentale forza`

### 1. Controlla file esistenti (solo con `forza`)

Se il flag è `forza`, verifica quali lezioni hanno già
file generati in `gen/`. Se almeno una ne ha, elenca le
lezioni coinvolte e chiedi all'utente se vuole rigenerarle.
Se risponde no, **interrompi**.

Se il flag è `super-forza`, salta questo controllo.

### 2. Pre-processing di tutte le lezioni

Per ogni cartella lezione che contiene almeno un `.txt`
in `risorse/`, esegui in sequenza:

```bash
make preprocess FOLDER=<percorso-lezione>/risorse
```

Se dopo aver completato il pre-processing di una lezione non ci sono più `.txt` in `risorse/`, salta la lezione e communica.

### 3. Subagenti A — Una lezione per subagente, max 2 in parallelo

Lancia i subagenti A in batch da **massimo 2 alla volta**.
Ogni subagente riceve le istruzioni del Caso A step 3
con il suo percorso lezione.

Aspetta che il batch corrente finisca prima di lanciare
il successivo. Questo evita di esaurire il rate limit
di Claude Pro (~35–70K token per subagente).

### 4. Subagente B — Una sola volta, dopo che tutti gli A sono finiti

Aspetta che **tutti** i subagenti A abbiano completato.
Solo allora lancia **un singolo** subagente B con il path
materia risolto (come descritto nel Caso A step 4).

Questo sovrascrive `gen_ampia_panoramica.md` con la
visione aggiornata di tutte le lezioni della materia.
