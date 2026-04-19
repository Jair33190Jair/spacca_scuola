---
name: exporta-pdf
description: Converts gen/*.md summaries to PDF and zips them. Accepts a lesson path or a subject path. Lesson → zip next to the lesson. Subject → single zip with all lessons + ampia panoramica.
argument-hint: <02_semestre/materia> | <02_semestre/materia/lezione>
---

## Parsing degli argomenti

`$ARGUMENTS` è un path assoluto o relativo alla lezione o alla materia.

Normalizza il path: se inizia con `projects/social/spacca_scuola/`,
rimuovi quel prefisso per ottenere il path relativo alla root del
progetto (es. `02_semestre/salute_mentale`).

## Come riconoscere il tipo

| Segmenti dopo `02_semestre/` | Tipo |
|---|---|
| 1 (es. `02_semestre/salute_mentale`) | Materia intera |
| 2 (es. `02_semestre/salute_mentale/01_intro`) | Lezione singola |

## Esecuzione

Dalla root del progetto (`projects/social/spacca_scuola`), esegui:

```bash
make export_pdf FOLDER=<path-relativo>
```

Attendi il completamento e riporta all'utente:
- Il path del file zip prodotto
- Quanti PDF sono stati inclusi (conta le righe di output che
  contengono `→`)
- Eventuali errori o lezioni saltate
