# 📚 SpaccaScuola

Trasforma i materiali delle lezioni (PDF, slide, scansioni,
trascrizioni) in riassunti di studio strutturati:

1. **Riassunto dettagliato**
2. **Riassunto breve**
3. **Riassunto schematico**

Dopo aver generato tutte le lezioni di una materia, produce
anche un'**ampia panoramica** di materia.

## Requisiti

- Python 3.9+
- Node.js (per Claude Code CLI)
- Tesseract OCR + Poppler (per estrarre testo dai PDF)
- Claude Code CLI (nessuna API key richiesta: basta l'account
  Claude usato da `claude`)

## Installazione

### macOS

```bash
brew install tesseract poppler node
npm install -g @anthropic-ai/claude-code

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Linux / WSL

```bash
sudo apt update
sudo apt install -y tesseract-ocr tesseract-ocr-ita \
  poppler-utils nodejs npm
npm install -g @anthropic-ai/claude-code

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Ogni volta che apri il progetto: `source .venv/bin/activate`

## Come si usa

### 1. Aggiungi i materiali di una lezione

Metti tutto nella cartella `risorse/` della lezione:

```
02_semestre/<materia>/<NN>_<nome_lezione>/risorse/
├── trascrizione_01.txt   ← trascrizione della lezione
├── slide.pdf             ← slide del professore
├── appunti_scansione.pdf ← scansioni di appunti
└── ...
```

- **Trascrizioni** → le crei tu (tipicamente come
  `trascrizione_NN.txt`) e le metti qui. Almeno **una**
  trascrizione `.txt` deve essere presente, altrimenti
  `/genera-riassunti` si interrompe.
- **PDF, slide, scansioni** → basta copiarli. Vengono
  convertiti automaticamente in `.txt` via OCR quando
  lanci `/genera-riassunti`.

Per una nuova materia, copia `02_semestre/template_materia/`
come punto di partenza.

### 2. Genera i riassunti con Claude Code

Apri Claude Code dalla root del progetto:

```bash
claude
```

Poi usa la skill:

```
/genera-riassunti 02_semestre/<materia>/<NN>_<lezione>
```

Per tutta la materia (operazione più lunga, richiede il flag):

```
/genera-riassunti 02_semestre/<materia> forza
```

La skill fa in automatico:

1. OCR dei PDF in `risorse/` (equivale a `make preprocess`).
2. Generazione dei 3 riassunti in `<lezione>/gen/`.
3. Aggiornamento di `<materia>/gen_ampia_panoramica.md`.

### 3. Esporta i PDF

Sempre dentro Claude Code, usa la skill:

```
/exporta-pdf 02_semestre/<materia>/<NN>_<lezione>
```

Per tutta la materia (un unico zip con tutte le lezioni +
ampia panoramica):

```
/exporta-pdf 02_semestre/<materia>
```

Lo zip viene salvato accanto alla cartella della lezione
(o della materia).

## Struttura del repository

```
spacca_scuola/
├── 02_semestre/
│   ├── <materia>/
│   │   ├── gen_ampia_panoramica.md
│   │   └── <NN>_<lezione>/
│   │       ├── risorse/   ← input: PDF, slide, scansioni, .txt
│   │       └── gen/       ← output generati dall'AI
│   └── template_materia/
│
├── ai_assistant/          ← istruzioni per l'AI
│   ├── ai_context.md
│   ├── profilo_studente.md
│   └── ai_guide/          ← formati di output
│
├── src/                   ← script di pre-processing ed export
├── Makefile               ← comandi preprocess / export_pdf
└── requirements.txt
```

## Personalizzazione

Modifica `ai_assistant/profilo_studente.md` e
`ai_assistant/ai_context.md` per adattare tono, analogie e
stile dei riassunti al tuo modo di studiare.

I formati di output si modificano in `ai_assistant/ai_guide/`.

## Troubleshooting

**`claude: command not found`**
→ `npm install -g @anthropic-ai/claude-code`

**`ModuleNotFoundError` durante `make`**
→ Attiva il venv: `source .venv/bin/activate`

**OCR impreciso su una scansione**
→ Aumenta il DPI: `make preprocess FOLDER=... DPI=400`
