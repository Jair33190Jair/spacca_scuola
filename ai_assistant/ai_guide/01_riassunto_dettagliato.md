# Guida — Riassunto Dettagliato

> Contesto: `ai_context.md` · Profilo: `profilo_studente.md`

## Scopo

Base di studio completa per una sessione di
lezione. Chi legge questo file deve poter
**capire l'argomento in profondità** senza
tornare al materiale originale.

## Input

Tutti i file `.txt` della cartella `risorse/`
della sessione, unificati in un unico testo.

## Output

Un file markdown: `gen/01_riassunto_dettagliato.md`

## Struttura del file

```
# {Titolo della lezione}
{Materia} · Sessione {NN} · {data se disponibile}

> {Frase introduttiva: di cosa parla questa
>  lezione e perché è importante — tono caldo,
>  max 2-3 righe}

## {Sezione tematica 1}

{Contenuto discorsivo, spiegazioni, esempi}

### {Sottosezione se necessaria}

...

## {Sezione tematica N}

---

## Concetti chiave

| Termine | Significato |
|---------|-------------|
| ...     | ...         |

---

## Domande di orientamento allo studio

**{Domanda 1 — tipica domanda d'esame}**
{Risposta: diretta, completa, 2-5 frasi. Usa i termini
tecnici corretti. Non fare l'elenco puntato se non serve —
ragiona come se rispondessi a voce all'esame.}

**{Domanda 2}**
{Risposta}

...

## Collegamenti

- Lezioni precedenti collegate (se disponibili)
- Temi aperti / da approfondire
```

## Regole di contenuto

### Domande di orientamento allo studio

- **Estrai dalle risorse** le domande d'esame esplicite se
  presenti (il prof le enuncia spesso a inizio o fine lezione,
  nelle slide riepilogative, o come "su cosa vi chiederò").
- **Se non ci sono domande esplicite**, genera 4–6 domande
  basate sui concetti che il prof ha enfatizzato di più,
  sulle definizioni tecniche e sui nodi concettuali centrali
  della lezione.
- **Aggiungi sempre le risposte.** Ogni domanda deve avere
  una risposta: diretta, concreta, 2–5 frasi. Usa i termini
  tecnici esatti usati a lezione. Scrivi come risponderesti
  a voce durante un esame orale — non come un saggio.
- **Non fare elenchi puntati nelle risposte** a meno che il
  contenuto sia genuinamente una lista (es. "le 3 fasi di...").
  Ragiona in paragrafo discorsivo quando possibile.
- **Copri le diverse tipologie di domanda:** definizione
  di un concetto, distinzione tra due termini simili,
  "perché è importante X", applicazione pratica.

---

- **Integra tutte le fonti** in un unico testo
  coerente. Non giustapporre — riorganizza.
- **Mantieni tutti i concetti importanti.**
  Elimina ripetizioni e divagazioni del prof,
  ma non perdere nessun contenuto sostanziale.
- **Spiegazioni chiare.** Ogni concetto nuovo
  va spiegato in modo accessibile. Usa analogie
  dal mondo di Jony (→ `profilo_studente.md`).
- **Terminologia tecnica:** usala sempre (serve
  all'esame), ma accompagnala con una
  spiegazione chiara la prima volta che appare.
- **Esempi:** includi quelli del professore.
  Se un esempio è confuso nella trascrizione,
  riformulalo mantenendo il senso.
- **Opinioni del prof:** segnalale esplicitamente.
  Es: _"Secondo il professore..."_ o
  _"Il prof sottolinea che..."_
- **Ambiguità:** segnala con [?] i passaggi
  poco chiari nella trascrizione.

## Regole di formato

- **Markdown ben strutturato.** Heading, liste,
  tabelle dove servono.
- **Paragrafi brevi.** Max 4-5 righe per blocco.
  Il muro di testo uccide la lettura.
- **Tabelle** per confronti, classificazioni,
  elenchi di autori/date/definizioni.
- **Grassetto** per i termini chiave alla prima
  occorrenza.
- **Citazioni** (`>`) per frasi importanti del
  professore o di autori citati.

## Tono

Questo è il formato più "personale". Qui puoi:
- Usare analogie e riferimenti al mondo di Jony
- Inserire brevi commenti motivazionali tra
  sezioni ("Fin qui ci siamo? Bene, ora viene
  la parte interessante.")
- Rendere il testo piacevole da leggere, come
  se un amico preparato ti spiegasse la lezione

Ma sempre: **chiarezza > intrattenimento.**

## Lunghezza indicativa

Proporzionale al materiale. Per una lezione
di ~90 min con trascrizione densa: 1500-3000
parole. Non tagliare per rientrare in un
limite — meglio lungo e completo che corto
e incompleto.

_Lunghezza target: da calibrare dopo i primi
output — aggiornare questo campo._
