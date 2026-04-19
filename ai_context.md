# ai_context.md

Porta d'ingresso per lavorare in questo repository.
Mantienilo pratico e aggiornato.

## Panoramica del progetto

SpaccaScuola trasforma PDF, slide e appunti scansionati
delle lezioni universitarie in materiale di studio
strutturato (tre riassunti per lezione + ampia panoramica
di materia).

Utente: studente di Scienze Sociali (30 anni),
lezioni in italiano.

## Stack

→ `stack.md`

## Struttura del repository

```
spacca_scuola/
├── 02_semestre/                ← materiale organizzato per semestre
│   ├── {materia}/              ← una cartella per materia
│   │   ├── gen_ampia_panoramica.md  ← sintesi aggregata di tutte le lezioni
│   │   ├── {NN}_{nome_lezione}/
│   │   │   ├── gen/            ← output generati dall'AI
│   │   │   │   ├── 01_riassunto_dettagliato.md
│   │   │   │   ├── 02_riassunto_breve.md
│   │   │   │   └── 03_riassunto_schematico.md
│   │   │   └── risorse/       ← input: trascrizione_NN.txt + PDF/slide/scansioni
│   │   └── ...
│   └── template_materia/       ← template vuoto da copiare
│
├── ai_assistant/               ← configurazione assistente AI
│   ├── ai_context.md           ← personalità e regole dell'AI
│   ├── profilo_studente.md     ← profilo dello studente (analogie, tono, motivazione)
│   └── ai_guide/               ← istruzioni per i formati di output
│       ├── 01_riassunto_dettagliato.md
│       ├── 02_riassunto_breve.md
│       ├── 03_riassunto_schematico.md
│       └── gen_ampia_panoramica.md
│
├── 02_architettura/decisioni/  ← decisioni architetturali (ADR)
├── aiuto/comandi.md            ← cheatsheet comandi CLI/git
├── src/                        ← script di pre-processing ed export PDF
├── Makefile                    ← comandi `preprocess` / `export_pdf`
├── .claude/skills/             ← skill `genera-riassunti`, `exporta-pdf`
└── README.md                   ← setup e uso quotidiano
```

## Pipeline di elaborazione

L'utente mette in `risorse/`:
- una o più `trascrizione_NN.txt` (scritte a mano, obbligatorio almeno una)
- PDF, slide, scansioni

Poi esegue due comandi:

```
/genera-riassunti <path-lezione-o-materia>
    │
    ├── 1. make preprocess  (invocato dalla skill, non dall'utente)
    │      └── OCR Tesseract + normalizzazione
    │          (src/pdf_to_txt.py, src/txt_normalizer.py)
    │          → risorse/*.txt
    │
    ├── 2. subagente A per ogni lezione
    │      └── legge risorse/*.txt + ai_assistant/ai_guide/
    │          → gen/01_riassunto_dettagliato.md
    │          → gen/02_riassunto_breve.md
    │          → gen/03_riassunto_schematico.md
    │
    └── 3. subagente B (una volta, a livello materia)
           └── aggrega i 03_riassunto_schematico.md
               → gen_ampia_panoramica.md

make export_pdf FOLDER=<path>   (o skill /exporta-pdf)
    └── converte i .md generati in PDF e li comprime in zip
```

**Nota:** `make preprocess` è un dettaglio interno della
skill `/genera-riassunti`, non un passo che l'utente lancia
a mano. Rimane disponibile nel Makefile per debug o
riesecuzione isolata dell'OCR.

## Documenti chiave

| Percorso                                | Contenuto                             |
| --------------------------------------- | ------------------------------------- |
| `README.md`                           | Setup, installazione, uso quotidiano  |
| `02_architettura/decisioni/01_ocr.md` | Confronto soluzioni OCR e decisione   |
| `ai_assistant/ai_guide/*.md`          | Istruzioni per ogni formato di output |
| `02_semestre/template_materia/`       | Template da copiare per nuove materie |
| `aiuto/comandi.md`                    | Riferimento comandi CLI e git         |
