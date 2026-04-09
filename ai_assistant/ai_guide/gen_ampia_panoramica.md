# Guida — Ampia Panoramica

> Contesto: `ai_context.md` · Profilo: `profilo_studente.md`

## Scopo

Visione d'insieme di **un'intera materia**.
Collega i concetti di tutte le lezioni in
un unico documento coerente. Pensato per
l'orientamento pre-esame: "cosa ho studiato,
come si collega tutto, cosa è importante."

## Input

I riassunti schematici di tutte le sessioni
della materia:

```
{materia}/
├── 01_{lezione}/gen/03_riassunto_schematico.md
├── 02_{lezione}/gen/03_riassunto_schematico.md
├── ...
└── NN_{lezione}/gen/03_riassunto_schematico.md
```

Se uno schematico manca, usa il riassunto
breve o dettagliato di quella sessione.

## Output

Un file markdown a livello materia:
`{materia}/gen_ampia_panoramica.md`

## Struttura del file

```
# {Nome materia} — Panoramica completa
Semestre {NN} · {numero} lezioni

> {2-3 righe che danno il senso del percorso:
>  da dove siamo partiti, dove siamo arrivati,
>  qual è il filo conduttore}

## Mappa dei temi

| # | Lezione | Tema centrale |
|---|---------|---------------|
| 01 | {nome} | {tema} |
| 02 | {nome} | {tema} |
| ... | ... | ... |

## {Macro-tema A}

Raggruppa concetti trasversali a più lezioni.

- **Concetto** → definizione · (Lez. 01, 03)
- **Concetto** → definizione · (Lez. 02)
  - dettaglio
  - dettaglio

## {Macro-tema N}

---

### Autori e riferimenti principali

| Chi | Contributo | Lezione |
|-----|-----------|---------|
| ... | ...       | ...     |

### Parole chiave della materia

`termine1` · `termine2` · `termine3` · ...

### Filo conduttore

{Breve narrativa — max 5-6 righe — che
collega i macro-temi e dà il senso del
percorso complessivo}
```

## Regole di contenuto

- **Riorganizza per temi, non per lezione.**
  Questa non è una lista di riassunti — è una
  sintesi che trova i fili comuni e li esplicita.
- **Collega i concetti tra lezioni.** Se la
  lezione 01 introduce un autore e la lezione
  04 lo critica, collegali esplicitamente.
- **Mappa dei temi** all'inizio: tabella rapida
  che dice cosa si trova in ogni lezione.
- **Riferimenti alla lezione di origine**
  tra parentesi: `(Lez. 03)` — così sa
  dove approfondire.
- **Nessun contenuto nuovo.** Solo ciò che è
  presente negli schematici/riassunti.
- **Elimina ripetizioni** tra lezioni diverse
  — unifica in un'unica voce.

## Regole di formato

- Come lo schematico: **visivo e rapido da
  scorrere.** Liste, tabelle, grassetto.
- **Niente testo discorsivo** tranne la
  frase introduttiva e il filo conduttore.
- **Grassetto** per ogni termine chiave.
- **Indentazione** per le gerarchie concettuali.

## Tono

Minimo. Puoi permetterti:

- La frase introduttiva (caldo, motivazionale)
- Il filo conduttore finale (narrativo ma breve)
- Il resto è pura struttura.

## Quando generarla

Dopo che tutte (o la maggior parte) delle
lezioni di una materia sono state elaborate.
Rigenerarla quando vengono aggiunte nuove
lezioni.

## Lunghezza indicativa

Proporzionale al numero di lezioni.
Per ~10 lezioni: 800-1500 parole.

_Lunghezza target: da calibrare dopo i primi
output — aggiornare questo campo._
