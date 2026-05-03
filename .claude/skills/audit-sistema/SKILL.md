---
name: audit-sistema
description: Verifica la qualità di tutti gli skill in .claude/skills/ e la loro coerenza come sistema di generazione materiale di studio. Output: tabella findings + decisione per skill + verdetto sistema. Solo findings — nessuna modifica.
argument-hint: (nessuno)
---

## Preparazione

Scopri tutti gli skill presenti:

```bash
find .claude/skills -name SKILL.md | sort
```

Leggi ogni file trovato prima di procedere.

---

## Check individuali (per ogni skill)

| # | Criterio | Gravità |
|---|---|---|
| I1 | Frontmatter descrive chiaramente quando usarlo | Med |
| I2 | Ha una condizione di stop esplicita | High |
| I3 | Tutti i file letti e scritti sono dichiarati | High |
| I4 | Path usa `02_semestre/materia[/lezione]` coerentemente | Med |
| I5 | Subagenti (se presenti): istruzioni includono cosa leggere e cosa scrivere | High |

---

## Check di sistema

Verifica il pipeline `genera-riassunti → verifica-riassunti → exporta-pdf`:

| # | Cosa verificare | Gravità |
|---|---|---|
| S1 | `verifica` cerca `gen/*riassunto*.md` — è esattamente ciò che `genera` produce? | High |
| S2 | `exporta` cerca `gen/*.md` — è ciò che `verifica` aggiorna? | High |
| S3 | La soglia non-vuoto (>3 righe, >100 parole) è identica in tutti i skill che la usano? | Med |
| S4 | Logica duplicata tra skill che dovrebbe avere una sola casa? | Low |
| S5 | Manca qualcosa per coprire il fabbisogno di studio? (es. quiz, ripasso attivo) | Low |

---

## Output

Tabella findings (salta i check che passano):

| Skill | Check | Finding | Gravità | Fix suggerito |
|---|---|---|---|---|

Poi una riga decisione per ogni skill:
- **No-op** — già adeguato
- **Patch** — fix localizzati
- **Rigenera** — scope o struttura da rivedere

Una riga finale per il sistema:
- **Coerente** — pipeline senza gap critici
- **Gap minori** — inconsistenze risolvibili con patch
- **Incoerente** — contratti rotti o pipeline incompleto

**Regole hard:** solo findings, nessuna modifica ai file.
