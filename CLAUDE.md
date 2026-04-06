# SpaccaScuola — Configurazione Claude

## Chi sono
Studente universitario di Scienze Sociali (30 anni). Le lezioni sono in italiano.
Ho bisogno di trasformare le trascrizioni delle lezioni in materiale di studio strutturato.

## Materia e contesto
<!-- PERSONALIZZA: aggiungi qui la materia specifica -->
- Corso: [NOME DEL CORSO]
- Professore: [NOME]
- Semestre: [ES. Primavera 2026]
- Argomenti principali del corso: [ELENCO MACRO-TEMI]

## Come elaborare le lezioni

Quando ricevi una trascrizione di una lezione, segui queste regole:

### Lingua
- Input: italiano (trascrizione da audio, potrebbe avere errori)
- Output: italiano
- Correggi errori evidenti di trascrizione (nomi propri storpiati, parole troncate)
- Mantieni la terminologia tecnica della materia

### Struttura degli output

#### 1. Riassunto breve (`riassunto.md`)
- Massimo 500 parole
- Scrivi in prosa fluida, NON in elenchi puntati
- Cattura: argomento principale, tesi del professore, autori citati, conclusioni
- Se il professore ha espresso opinioni personali, segnalale come tali
- Concludi con "Collegamento con le lezioni precedenti:" se hai contesto

#### 2. Bullet points (`bullet-points.md`)
- Gerarchia a massimo 3 livelli
- Primo livello: macro-temi della lezione (massimo 5)
- Secondo livello: concetti chiave per ogni tema
- Terzo livello: dettagli, esempi, citazioni importanti
- Usa **grassetto** per i termini tecnici alla prima occorrenza
- Usa *corsivo* per nomi di autori e opere

#### 3. Tabella concetti (`tabella-concetti.md`)
Formato markdown con queste colonne:
| Concetto | Definizione | Autore/Fonte | Collegamento con altri concetti |
- Massimo 15 righe
- Concentrati su concetti che potrebbero essere domande d'esame
- La colonna "Collegamento" è fondamentale: come si relaziona con il resto?

#### 4. Mappa mentale (`mappa-mentale.md`)
NON generare un'immagine. Genera una struttura testuale che posso ridisegnare a mano.
Formato:
```
TEMA CENTRALE: [titolo della lezione]

├── Ramo 1: [macro-tema]
│   ├── [sotto-concetto]
│   │   └── collegato a: [altro concetto]
│   └── [sotto-concetto]
│
├── Ramo 2: [macro-tema]
│   ├── [sotto-concetto]
│   └── [sotto-concetto]
│       └── in contrasto con: Ramo 1 > [concetto]
│
└── Ramo 3: [macro-tema]
    └── [sotto-concetto]
        └── sviluppo di: [concetto dalla lezione precedente]

RELAZIONI TRASVERSALI:
- [Concetto A] ←→ [Concetto B]: [tipo di relazione]
- [Concetto C] → [Concetto D]: [causa/effetto/evoluzione]
```

### Contesto dalle lezioni precedenti
Se nella cartella `archivio/` ci sono elaborati di lezioni precedenti, usali per:
- Identificare temi ricorrenti
- Segnalare evoluzioni del discorso del professore
- Collegare nuovi concetti a quelli già visti
- Evidenziare contraddizioni o approfondimenti

## Comandi rapidi

Quando l'utente usa questi comandi, esegui l'azione corrispondente:

- `/riassumi [file]` → Genera solo il riassunto breve
- `/bullet [file]` → Genera solo i bullet points
- `/tabella [file]` → Genera solo la tabella concetti
- `/mappa [file]` → Genera solo la mappa mentale
- `/tutto [file]` → Genera tutti e 4 gli output
- `/confronta [file1] [file2]` → Confronta due lezioni, evidenzia evoluzioni
- `/esame [cartella]` → Analizza tutte le lezioni e genera una guida d'esame
- `/migliora` → Suggerisci come migliorare questo file CLAUDE.md

## Stile e tono
- Sii diretto e conciso
- Non aggiungere informazioni che NON sono nella lezione
- Se qualcosa nella trascrizione è ambiguo, segnalalo con [?]
- Distingui sempre tra fatti, teorie e opinioni del professore
