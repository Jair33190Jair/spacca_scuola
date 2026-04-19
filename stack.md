# Stack

> **Fonte unica** per le scelte tecnologiche del progetto.
> Aggiorna qui, poi propaga.

---

## OCR (PDF e documenti scansionati)

Decisione documentata in
`02_architettura/decisioni/01_ocr.md`.

| Campo | Valore | Stato |
| --- | --- | --- |
| Tool | Tesseract (+ Poppler) | Confermato |
| Esecuzione | Locale | Confermato |
| Lingua | italiano | Confermato |
| Costo | Gratis | — |
| Script | `src/pdf_to_txt.py`, `src/txt_normalizer.py` | Funzionante |
| Orchestrazione | `make preprocess FOLDER=...` | Funzionante |

---

## Elaborazione AI

| Campo | Valore | Stato |
| --- | --- | --- |
| Provider | Anthropic | Confermato |
| Interfaccia | Claude Code CLI (nessuna API key) | Confermato |
| Skill principali | `/genera-riassunti`, `/exporta-pdf` | Funzionanti |
| Istruzioni | `ai_assistant/ai_guide/*.md` | In costruzione |

---

## Export PDF

| Campo | Valore | Stato |
| --- | --- | --- |
| Tool | weasyprint + markdown2 | Confermato |
| Script | `src/md_to_pdf.py` | Funzionante |
| Orchestrazione | `make export_pdf FOLDER=...` | Funzionante |

---

## Dipendenze

| Campo | Valore |
| --- | --- |
| Runtime | Python 3.9+ |
| Packages | `requirements.txt` |
| Sistema | Tesseract, Poppler, Node.js (per Claude Code) |
| OS testato | macOS Sonoma+, Linux/WSL (Ubuntu) |
