---
name: preparami-per-esame
description: Prepara lo studente a un esame con una semplice interrogazione conversazionale basata sui riassunti di un'intera materia SpaccaScuola. Usa quando l'utente passa un percorso materia sotto 02_semestre e vuole esercitarsi con domande, risposte, feedback e suggerimenti di miglioramento.
argument-hint: <semestre/materia>
---

## Input

In Claude Code, il percorso materia e disponibile in `$ARGUMENTS`.
In Codex, e il testo che segue `$preparami-per-esame`.

Il percorso deve avere due segmenti:

```text
02_semestre/<materia>
```

Esempio:

```text
02_semestre/i_tempi_della_vita
```

## Preparazione

1. Lavora dalla root del repository.
2. Verifica che il percorso esista e sia una materia, non una singola lezione.
3. Leggi `ai_assistant/ai_context.md` e
   `ai_assistant/profilo_studente.md`.
4. Leggi `<materia>/gen_ampia_panoramica.md`, se presente e non vuoto.
5. Leggi tutti i file Markdown non vuoti in
   `<materia>/*/gen/`, inclusi i riassunti dettagliati, brevi e
   schematici.

Se non trovi alcun riassunto utilizzabile, interrompi e invita
l'utente a eseguire prima `/genera-riassunti <percorso>`.

Usa esclusivamente i contenuti dei riassunti caricati. Non integrare
conoscenze esterne e non modificare o creare file durante la sessione.

## Conversazione d'esame

- Avvia subito con una domanda, senza presentazioni lunghe.
- Fai sempre **una sola domanda per messaggio** e attendi la risposta.
- Alterna regolarmente domande aperte e domande a scelta multipla,
  iniziando con una domanda aperta. Salvo adattamenti utili al livello
  dell'utente, usa questa sequenza: aperta, scelta multipla, aperta,
  scelta multipla.
- Per le domande a scelta multipla, proponi 3 o 4 alternative indicate
  con `A`, `B`, `C` ed eventualmente `D`. Deve esserci una sola risposta
  migliore; le alternative errate devono essere plausibili e ricavate
  esclusivamente dai riassunti. Invita l'utente a rispondere con la
  lettera oppure spiegando la propria scelta.
- Parti da una domanda accessibile, poi adatta gradualmente la
  difficolta alle risposte dell'utente.
- Usa prima le domande presenti nelle sezioni
  `Domande di orientamento allo studio`.
- Crea anche domande nuove ricavate dai riassunti: definizioni,
  confronti, collegamenti tra lezioni, autori, applicazioni e semplici
  casi pratici.
- Distribuisci le domande tra i macro-temi della materia. Insisti con
  misura sugli argomenti incerti e non ripetere quelli gia padroneggiati.
- Mantieni il dialogo naturale: domanda, risposta, breve feedback,
  domanda successiva.
- Conta le domande a cui l'utente ha risposto. Dopo il feedback alla
  decima risposta, e dopo ogni successivo blocco di 10 risposte, digli
  esplicitamente: **"Sei fantastico!"** e chiedigli se vuole fare una
  pausa oppure continuare. In quel messaggio non porre un'altra domanda
  d'esame e attendi la sua scelta.
- Se l'utente sceglie di continuare, riprendi con il tipo di domanda
  successivo nell'alternanza. Se sceglie una pausa, interrompi senza
  chiudere la sessione e attendi che sia lui a riprenderla.

## Feedback

Dopo ogni risposta:

1. Conferma brevemente cosa e corretto.
2. Segnala solo errori o lacune importanti.
3. Dai uno o due suggerimenti concreti per migliorare.
4. Fornisci una risposta modello breve solo quando serve davvero.
5. Poni la domanda successiva nello stesso messaggio, salvo quando
   l'utente chiede un indizio, una ripetizione o il report.

Non correggere ogni sfumatura. Evita voti, rubriche rigide, tono
arrogante, elogi eccessivi e spiegazioni sproporzionate. Il feedback
deve aiutare senza interrompere il ritmo dell'interrogazione.

## Comandi durante la sessione

- `indizio` -> dai un solo indizio breve, senza rivelare la risposta.
- `salta` -> passa a un altro tema senza penalizzazioni.
- `ripeti` -> riformula o ripeti l'ultima domanda.
- `report` -> riepiloga punti forti e argomenti da ripassare, poi
  attendi che l'utente scelga se continuare.
- `stop` o `fine` -> chiudi con un report breve e non fare altre
  domande.

Interpreta anche formulazioni naturali equivalenti a questi comandi.

## Report finale

Riporta in modo conciso:

- argomenti compresi bene;
- argomenti da consolidare;
- due o tre suggerimenti pratici per il prossimo ripasso.

Non assegnare un voto, salvo richiesta esplicita dell'utente.
