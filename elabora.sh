#!/bin/bash
# ============================================================
# elabora.sh — Genera materiale di studio da una trascrizione
# Uso: ./elabora.sh trascrizioni/nome-lezione.txt
# ============================================================

set -e

# Colori
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Controlla che sia stato passato un file
if [ -z "$1" ]; then
    echo -e "${RED}❌ Errore: specifica un file di trascrizione.${NC}"
    echo "Uso: ./elabora.sh trascrizioni/nome-lezione.txt"
    exit 1
fi

INPUT_FILE="$1"

# Controlla che il file esista
if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${RED}❌ File non trovato: $INPUT_FILE${NC}"
    exit 1
fi

# Controlla che ANTHROPIC_API_KEY sia configurata
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${RED}❌ ANTHROPIC_API_KEY non configurata.${NC}"
    echo "Esegui: export ANTHROPIC_API_KEY='la-tua-chiave'"
    exit 1
fi

# Prepara cartella output
BASENAME=$(basename "$INPUT_FILE" .txt)
OUTPUT_DIR="output/${BASENAME}"
mkdir -p "$OUTPUT_DIR"

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   📚 SpaccaScuola — Elaborazione       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""
echo "   Input: $INPUT_FILE"
echo "   Output: $OUTPUT_DIR/"
echo ""

# Costruisci il contesto dalle lezioni precedenti (se esistono)
CONTEXT=""
if [ -d "archivio" ] && [ "$(ls -A archivio/ 2>/dev/null)" ]; then
    echo -e "${YELLOW}📂 Caricamento contesto lezioni precedenti...${NC}"
    # Prendi gli ultimi 3 riassunti dall'archivio
    for f in $(ls -t archivio/*/riassunto.md 2>/dev/null | head -3); do
        CONTEXT="$CONTEXT\n\n--- Lezione precedente: $(dirname $f | xargs basename) ---\n$(cat $f)"
    done
    echo "   Trovate $(ls -d archivio/*/ 2>/dev/null | wc -l | tr -d ' ') lezioni precedenti"
    echo ""
fi

TRANSCRIPT=$(cat "$INPUT_FILE")

# ---- Genera tutti e 4 gli output con Claude Code ----

echo -e "${YELLOW}🤖 Generazione materiale di studio...${NC}"
echo ""

# Usa Claude Code in modalità non interattiva
# Il flag --print (-p) esegue un singolo prompt e stampa il risultato
claude -p "
Sei un assistente per lo studio universitario in scienze sociali.

CONTESTO LEZIONI PRECEDENTI:
$CONTEXT

TRASCRIZIONE DELLA LEZIONE DI OGGI:
$TRANSCRIPT

Per favore genera i seguenti 4 file di output, separandoli chiaramente con le intestazioni indicate.

===FILE: riassunto.md===
Riassunto breve della lezione (max 500 parole, in prosa fluida, in italiano).
Cattura: argomento principale, tesi del professore, autori citati, conclusioni.
Se ci sono lezioni precedenti nel contesto, aggiungi un paragrafo di collegamento.

===FILE: bullet-points.md===
Bullet points gerarchici (max 3 livelli):
- Livello 1: macro-temi (max 5)
- Livello 2: concetti chiave
- Livello 3: dettagli, esempi, citazioni
Usa **grassetto** per termini tecnici, *corsivo* per autori/opere.

===FILE: tabella-concetti.md===
Tabella markdown con colonne:
| Concetto | Definizione | Autore/Fonte | Collegamento con altri concetti |
Max 15 righe. Concentrati su possibili domande d'esame.

===FILE: mappa-mentale.md===
Struttura testuale per mappa mentale da ridisegnare a mano:
- Tema centrale con rami e sotto-rami
- Usa ├── └── │ per la struttura ad albero
- Aggiungi RELAZIONI TRASVERSALI tra concetti
- Se ci sono lezioni precedenti, collega i nuovi concetti ai vecchi
" > "$OUTPUT_DIR/_raw_output.txt" 2>/dev/null

# Splitta l'output nei singoli file
echo -e "${YELLOW}📄 Separazione output...${NC}"

python3 -c "
import re

with open('$OUTPUT_DIR/_raw_output.txt', 'r') as f:
    content = f.read()

# Split by file markers
files = {
    'riassunto.md': '',
    'bullet-points.md': '',
    'tabella-concetti.md': '',
    'mappa-mentale.md': ''
}

patterns = [
    (r'===FILE:\s*riassunto\.md===\s*\n(.*?)(?====FILE:|$)', 'riassunto.md'),
    (r'===FILE:\s*bullet-points\.md===\s*\n(.*?)(?====FILE:|$)', 'bullet-points.md'),
    (r'===FILE:\s*tabella-concetti\.md===\s*\n(.*?)(?====FILE:|$)', 'tabella-concetti.md'),
    (r'===FILE:\s*mappa-mentale\.md===\s*\n(.*?)(?====FILE:|$)', 'mappa-mentale.md'),
]

for pattern, filename in patterns:
    match = re.search(pattern, content, re.DOTALL)
    if match:
        file_content = match.group(1).strip()
        with open('$OUTPUT_DIR/' + filename, 'w') as f:
            f.write(file_content + '\n')
        print(f'   ✅ {filename}')
    else:
        print(f'   ⚠️  {filename} non trovato nell\'output')

# If splitting failed, save the whole output as a single file
if not any(re.search(p, content, re.DOTALL) for p, _ in patterns):
    print('   ℹ️  Output non strutturato, salvato come output-completo.md')
    with open('$OUTPUT_DIR/output-completo.md', 'w') as f:
        f.write(content)
"

# Pulisci il file raw
rm -f "$OUTPUT_DIR/_raw_output.txt"

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   ✅ Elaborazione completata!          ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo "   📁 File generati in: $OUTPUT_DIR/"
ls -1 "$OUTPUT_DIR/" | while read f; do echo "      📄 $f"; done
echo ""

# Chiedi se archiviare
echo -e "${YELLOW}Vuoi archiviare questa lezione per il contesto futuro? (s/n)${NC}"
read -r ARCHIVE
if [ "$ARCHIVE" = "s" ] || [ "$ARCHIVE" = "S" ]; then
    mkdir -p "archivio/$BASENAME"
    cp "$OUTPUT_DIR"/*.md "archivio/$BASENAME/"
    echo -e "${GREEN}✅ Lezione archiviata in archivio/$BASENAME/${NC}"
fi

echo ""
echo -e "${BLUE}Buono studio! 📚${NC}"
