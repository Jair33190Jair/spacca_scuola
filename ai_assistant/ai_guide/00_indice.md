# Guida — Indice delle risorse

> Contesto: `ai_context.md`

## Scopo

Registro bibliografico delle risorse usate nella sessione.
Permette di sapere da dove vengono i contenuti del riassunto
e di ritrovare rapidamente un documento originale.

## Input

Tutti i file `.txt` in `risorse/`. Ogni `.txt` inizia con
`[FONTE: filename]` — usare quella riga come fonte primaria
dei metadati. Leggere le prime ~20 righe per ricavare
la descrizione del contenuto.

## Output

`gen/00_indice.md`

## Struttura del file

```
# Indice delle risorse

## {Titolo}
*{Autore}, {Anno}*
{Descrizione: 1–2 frasi}

## {Titolo}
*{Autore}*
{Descrizione}

...
```

## Regole di contenuto

- **Titolo, autore, anno**: estrarre dal valore di `[FONTE: ...]`
  in cima al `.txt`. Pulire artefatti tipografici
  (`Lapproccio` → `L'approccio`, underscore → spazio).
  - Formato `Autore - Anno - Titolo.pdf`:
    → titolo = terzo segmento, autore = primo, anno = secondo
  - Formato `Titolo in Autore, A. (Anno), Opera.pdf`:
    → titolo = capitolo, autore = nome in parentesi, anno = anno
  - Se il formato non è riconoscibile: usa il nome file come
    titolo, ometti autore e anno.
- **Descrizione**: 1–2 frasi che descrivono l'oggetto del documento
  (non un riassunto — cosa tratta). Basarsi sulle prime righe del `.txt`.
- **File senza metadati** (es. `trascrizione_01.txt`): nome file
  come titolo, niente autore/anno, descrizione dal contenuto.
- **Pagine illeggibili.** Se il `.txt` contiene uno o più
  `[⚠ PAGINA ILLEGGIBILE: pagina N]`, aggiungili sotto la
  descrizione del documento usando HTML inline per il colore rosso:
  `<span style="color:red">⚠ Pagine non leggibili: N, M</span>`
- **Ordine**: alfabetico per nome file.

## Regole di formato

- Un blocco `##` per risorsa.
- Riga `*corsivo*` per autore/anno subito sotto il titolo.
  Omettere la riga se autore e anno sono entrambi assenti —
  non lasciare righe vuote.
- Nessun commento motivazionale. Solo dati.
