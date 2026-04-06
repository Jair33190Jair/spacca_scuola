# 📚 SpaccaScuola

##

**Mette asieme registratzioni + Risorsi della lezione e crea:**

1. **Riassunto breve** — la lezione in 500 parole
2. **Bullet points** — concetti gerarchici pronti per il ripasso
3. **Tabella concetti** — definizioni, autori, collegamenti
4. **Mappa mentale** — struttura da ridisegnare a mano per studiare

## Requisiti

- macOS (testato su Sonoma+)
- Homebrew
- Una API key di Anthropic (console.anthropic.com)

## Installazione rapida

```bash
# 1. Installa le dipendenze
brew install node openai-whisper ffmpeg

# 2. Installa Claude Code
npm install -g @anthropic-ai/claude-code

# 3. Configura la API key
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
source ~/.zshrc

# 4. Clona/copia questa cartella
cd ~/SpaccaScuola

# 5. Rendi eseguibili gli script
chmod +x trascrivi.sh elabora.sh
```

## Uso quotidiano

### Due comandi e basta:

```bash
# Passo 1: Trascrivi l'audio
./trascrivi.sh audio/lezione-2026-04-07.m4a

# Passo 2: Genera il materiale di studio
./elabora.sh trascrizioni/lezione-2026-04-07.txt
```

I file verranno salvati in `output/lezione-2026-04-07/`.

### Uso interattivo (per domande specifiche):

```bash
cd ~/SpaccaScuola
claude

# Poi scrivi quello che vuoi:
> Leggi trascrizioni/lezione-01.txt e fammi un riassunto
> Confronta le ultime 3 lezioni in archivio/
> Quali autori sono stati citati più spesso?
```

## Struttura delle cartelle

```
SpaccaScuola/
├── audio/          ← metti qui le registrazioni
├── trascrizioni/   ← testo generato da Whisper
├── output/         ← materiale di studio
├── archivio/       ← lezioni passate (per contesto)
├── CLAUDE.md       ← istruzioni per Claude (PERSONALIZZA!)
├── trascrivi.sh    ← script trascrizione
├── elabora.sh      ← script elaborazione
└── README.md       ← questo file
```

## Personalizzazione

Il file **CLAUDE.md** è il cuore del sistema. Modificalo per:

- Aggiungere il nome del corso e del professore
- Specificare argomenti o terminologia della materia
- Cambiare il formato degli output
- Aggiungere nuovi comandi rapidi

## Costi

| Componente | Costo |
|------------|-------|
| Whisper (locale) | Gratis |
| Claude API | ~€0.10-0.30 per lezione |
| Tutto il resto | Gratis |
| **Totale mensile** | **~€1-3** |

## Troubleshooting

**"whisper: command not found"**
→ `brew install openai-whisper`

**"claude: command not found"**
→ `npm install -g @anthropic-ai/claude-code`

**La trascrizione è imprecisa**
→ Prova `--model large` nello script (più lento ma più preciso)
→ Assicurati che la registrazione audio sia chiara

**L'output di Claude non è buono**
→ Modifica CLAUDE.md con istruzioni più specifiche
→ Usa `claude` interattivo e digli cosa migliorare

## Backup

```bash
git add .
git commit -m "lezione del 7 aprile"
git push  # se hai configurato GitHub
```

---

*Creato con ❤️ per rendere lo studio più efficiente, non più pigro.*
