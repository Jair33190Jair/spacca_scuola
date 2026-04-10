---
name: genera-riassunti
description: Genera i 3 riassunti (dettagliato, breve, schematico) per una lezione e lancia un subagente che aggiorna l'ampia panoramica. Argomento: percorso relativo alla cartella lezione, es. per 02_semestre/salute_mentale/02_storia_della_follia 
argument-hint: <materia/lezione>
---

Genera i 3 file di output per la lezione in `$ARGUMENTS`.

## Contesto

- Carica il tuo contesto se non l'hai ancora fatto:
   `ai_context.md` (panoramica progetto) e
   `ai_assistant/ai_context.md` (regole AI).

## Procedura

1. Segui `ai_assistant/ai_guide/01_riassunto_dettagliato.md`
   → scrivi `$ARGUMENTS/gen/01_riassunto_dettagliato.md`

2. Segui `ai_assistant/ai_guide/02_riassunto_breve.md`
   → scrivi `$ARGUMENTS/gen/02_riassunto_breve.md`

3. Segui `ai_assistant/ai_guide/03_riassunto_schematico.md`
   → scrivi `$ARGUMENTS/gen/03_riassunto_schematico.md`

4. Deriva il percorso della materia: è la cartella padre di
   `$ARGUMENTS` (es. se `$ARGUMENTS` =
   `02_semestre/salute_mentale/02_storia_della_follia`
   allora materia = `02_semestre/salute_mentale`).

   Lancia un subagente con contesto fresco.
   Passagli queste istruzioni (con il percorso materia
   già risolto, non il placeholder):
   - Leggi `ai_context.md` e `ai_assistant/ai_context.md`
   - Leggi `ai_assistant/ai_guide/gen_ampia_panoramica.md`
   - Input: tutti i `*/gen/03_riassunto_schematico.md`
     non vuoti in `<percorso-materia-risolto>/`
   - Output: aggiorna `<percorso-materia-risolto>/gen_ampia_panoramica.md`