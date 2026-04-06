#!/bin/bash
# ============================================================
# trascrivi.sh — Trascrivi un file audio in testo con Whisper
# Uso: ./trascrivi.sh percorso/al/file/audio.m4a
# ============================================================

set -e

# Colori per output leggibile
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Controlla che sia stato passato un file
if [ -z "$1" ]; then
    echo -e "${RED}❌ Errore: specifica un file audio.${NC}"
    echo "Uso: ./trascrivi.sh audio/nome-lezione.m4a"
    echo ""
    echo "Formati supportati: m4a, mp3, wav, ogg, flac, webm"
    exit 1
fi

INPUT_FILE="$1"

# Controlla che il file esista
if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${RED}❌ File non trovato: $INPUT_FILE${NC}"
    exit 1
fi

# Estrai il nome senza estensione
BASENAME=$(basename "$INPUT_FILE" | sed 's/\.[^.]*$//')
OUTPUT_DIR="trascrizioni"
OUTPUT_FILE="$OUTPUT_DIR/${BASENAME}.txt"

# Crea la cartella output se non esiste
mkdir -p "$OUTPUT_DIR"

echo -e "${YELLOW}🎙  Trascrizione in corso...${NC}"
echo "   File: $INPUT_FILE"
echo "   Lingua: italiano"
echo "   Modello: medium (buon compromesso velocità/qualità)"
echo ""

# Esegui Whisper
# Opzioni:
#   --model medium  → buon compromesso (small = veloce, large = preciso)
#   --language it   → forza italiano
#   --output_format txt → solo testo
#   --output_dir    → cartella output
whisper "$INPUT_FILE" \
    --model medium \
    --language it \
    --output_format txt \
    --output_dir "$OUTPUT_DIR" \
    2>/dev/null

# Rinomina se necessario (Whisper usa il nome del file originale)
WHISPER_OUTPUT="$OUTPUT_DIR/${BASENAME}.txt"
if [ -f "$WHISPER_OUTPUT" ]; then
    echo ""
    echo -e "${GREEN}✅ Trascrizione completata!${NC}"
    echo "   Output: $WHISPER_OUTPUT"
    echo ""

    # Mostra statistiche
    WORDS=$(wc -w < "$WHISPER_OUTPUT" | tr -d ' ')
    LINES=$(wc -l < "$WHISPER_OUTPUT" | tr -d ' ')
    echo "   📊 Parole: $WORDS"
    echo "   📊 Righe: $LINES"
    echo ""
    echo -e "${YELLOW}Prossimo passo:${NC} ./elabora.sh $WHISPER_OUTPUT"
else
    echo -e "${RED}❌ Qualcosa è andato storto nella trascrizione.${NC}"
    echo "Prova con un formato audio diverso o controlla che Whisper sia installato."
    exit 1
fi
