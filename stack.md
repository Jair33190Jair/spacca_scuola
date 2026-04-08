# Stack

> **Fonte unica** per le scelte tecnologiche del progetto.
> Aggiorna qui, poi propaga.

---

## Trascrizione audio

| Campo | Valore | Stato |
| --- | --- | --- |
| Tool | Whisper (OpenAI, locale) | Confermato |
| Modello | medium | Confermato |
| Lingua | italiano | Confermato |
| Formato output | txt | Confermato |
| Costo | Gratis (esecuzione locale) | — |
| Script | `trascrivi.sh` | Funzionante |

---

## OCR (documenti scansionati)

Decisione documentata in
`02_architettura/decisioni/01_ocr.md`.

| Campo | Valore | Stato |
| --- | --- | --- |
| Tool | Tesseract | Confermato |
| Esecuzione | Locale | Confermato |
| Costo | Gratis | — |
| Script | TBD (in `src/`) | In costruzione |

---

## Elaborazione AI

| Campo | Valore | Stato |
| --- | --- | --- |
| Provider | Anthropic (Claude API) | Confermato |
| Interfaccia | Claude Code CLI | Confermato |
| Costo | ~€0.10–0.30 per lezione | — |
| Istruzioni | `ai_assistant/ai_guide/*.md` | In costruzione |

---

## Dipendenze

| Campo | Valore |
| --- | --- |
| Runtime | Python 3.x |
| Packages | `requirements.txt` |
| Sistema | ffmpeg, Node.js (per Claude Code) |
| OS testato | macOS Sonoma+ |

---

## Pre-processing (pianificato)

Tool per unificare input eterogenei (audio, PDF,
slide, scansioni) in un formato pulito prima
dell'elaborazione AI.

| Campo | Valore | Stato |
| --- | --- | --- |
| Posizione | `src/` | In costruzione |
| Input supportati | audio, PDF, PPT, scansioni | Pianificato |
| Output | testo unificato per Claude | Pianificato |
