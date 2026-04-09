# Guida — Riassunto Schematico

> Contesto: `ai_context.md` · Profilo: `profilo_studente.md`

## Scopo

Colpo d'occhio sulla lezione. Pensato per
la **memoria visiva** e il **ripasso lampo**.
Deve bastare uno sguardo per ricordare la
struttura dell'argomento.

## Input

Il riassunto dettagliato della stessa sessione
(`gen/01_riassunto_dettagliato.md`) oppure, se
non disponibile, i file `.txt` da `risorse/`.

## Output

Un file markdown: `gen/03_riassunto_schematico.md`

## Struttura del file

```
# {Titolo della lezione} — Schema
{Materia} · Sessione {NN}

## {Tema 1}

- **Concetto** → definizione breve
- **Concetto** → definizione breve
  - dettaglio
  - dettaglio

## {Tema N}

---

### Autori / Date / Riferimenti

| Chi | Cosa | Quando |
|-----|------|--------|
| ... | ...  | ...    |

### Parole chiave

`termine1` · `termine2` · `termine3` · ...
```

## Regole di contenuto

- **Solo l'essenziale.** Concetti chiave,
  definizioni, relazioni tra concetti.
- **Niente testo discorsivo.** Ogni elemento
  deve essere una riga, un punto, una cella.
- **Parole chiave e mini-definizioni.**
  Formato: `**Termine** → spiegazione in
  max 10-15 parole`.
- **Relazioni tra concetti** rese esplicite
  con frecce (→), gerarchie (indentazione),
  o tabelle.
- **Autori, date, riferimenti bibliografici**
  in tabella se presenti nella lezione.

## Regole di formato

- **Struttura visiva massima.** Liste indentate,
  tabelle, separatori. Il layout è il contenuto.
- **Grassetto** per ogni termine chiave.
- **Code backticks** per parole chiave nella
  sezione finale.
- **Niente paragrafi.** Se stai scrivendo più
  di una riga continua, stai sbagliando formato.
- **Emoji come marker visivi:** opzionale.
  Se usate, solo per categorizzare
  (es. `📖 Teoria`, `👤 Autore`, `⚠️ Attenzione`).

## Tono

**Zero personalità.** Questo file è uno
strumento, non una conversazione. Niente
battute, niente commenti, niente analogie.
Solo struttura pulita.

## Lunghezza indicativa

~15-25% del riassunto dettagliato.
Per una lezione di ~90 min: 300-600 parole.

_Lunghezza target: da calibrare dopo i primi
output — aggiornare questo campo._
