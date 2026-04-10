# ai_context.md

Porta d'ingresso per lavorare in questo repository.
Mantienilo pratico e aggiornato.

## Panoramica del progetto

SpaccaScuola trasforma registrazioni audio, PDF,
slide e appunti scansionati delle lezioni universitarie
in materiale di studio strutturato.

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
│   │   │   └── risorse/       ← input: PDF, audio, slide, scansioni
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
├── src/                        ← script e tool di pre-processing
├── trascrivi.sh                ← audio → testo
└── README.md                   ← setup e uso quotidiano
```

## Pipeline di elaborazione

```
risorse/ (PDF, audio, slide, scansioni)
    │
    ├── audio → ./trascrivi.sh → trascrizione testo
    ├── PDF/slide → (diretto o OCR via Tesseract)
    └── scansioni → OCR Tesseract → testo
    │
    ▼
pre-processing (src/) → input pulito e unificato
    │
    ▼
Claude API + istruzioni (ai_assistant/ai_guide/)
    │
    ▼
gen/
├── 01_riassunto_dettagliato.md
├── 02_riassunto_breve.md
└── 03_riassunto_schematico.md

Dopo tutte le lezioni di una materia:
    ▼
gen_ampia_panoramica.md  (a livello materia)
```

## Formati di output

Ogni lezione produce 3 file in `gen/`.
Le istruzioni dettagliate per ciascun formato
sono in `ai_assistant/ai_guide/`:

| Output | Guida AI | Scopo |
| --- | --- | --- |
| Riassunto dettagliato | `ai_guide/01_riassunto_dettagliato.md` | Contenuto completo e strutturato |
| Riassunto breve | `ai_guide/02_riassunto_breve.md` | Sintesi rapida per il ripasso |
| Riassunto schematico | `ai_guide/03_riassunto_schematico.md` | Concetti chiave in formato visivo |
| Ampia panoramica | `ai_guide/gen_ampia_panoramica.md` | Aggregazione di tutte le lezioni di una materia |

## Regole di elaborazione

- **Lingua:** input e output in italiano.
- Correggi errori evidenti di trascrizione
  (nomi storpiati, parole troncate).
- Mantieni la terminologia tecnica della materia.
- Distingui fatti, teorie e opinioni del professore.
- Non aggiungere informazioni non presenti
  nelle risorse.
- Segnala ambiguità con [?].
- Collega a lezioni precedenti se il contesto
  è disponibile.
- **Conflitti tra fonti:** in caso di
  informazioni contrastanti tra la trascrizione
  e un file `manuale_<numero>.txt`, il manuale
  ha sempre la precedenza. Segnala il conflitto
  con una nota inline, es:
  _[Trascrizione dice X — manuale corregge in Y]_

## Documenti chiave

| Percorso | Contenuto |
| --- | --- |
| `README.md` | Setup, installazione, uso quotidiano |
| `02_architettura/decisioni/01_ocr.md` | Confronto soluzioni OCR e decisione |
| `ai_assistant/ai_guide/*.md` | Istruzioni per ogni formato di output |
| `02_semestre/template_materia/` | Template da copiare per nuove materie |
| `aiuto/comandi.md` | Riferimento comandi CLI e git |

## Stato attuale

**Funzionante:**
- `trascrivi.sh` (audio → testo)
- Struttura cartelle per `salute_mentale`
  (2 lezioni create)

**In costruzione:**
- Tool di pre-processing in `src/`
- Istruzioni AI in `ai_assistant/ai_guide/`
  (file creati ma vuoti)
- `elabora.sh` (referenziato in README
  ma non ancora implementato)

**Materie attive:**
- `salute_mentale` (2 lezioni)
- `mondi_del_lavoro` (cartella vuota)

## Comandi

```bash
# Trascrivi audio
./trascrivi.sh percorso/al/file/audio.m4a

# Elabora (non ancora implementato)
./elabora.sh trascrizioni/file.txt
```
