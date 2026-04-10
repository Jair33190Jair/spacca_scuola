#!/usr/bin/env python3
"""
Normalize messy .txt files in a risorse/ folder.

A file is "messy" when it looks like a single-line audio
dump (average line length > threshold). Normalization
splits it at conservative sentence boundaries and groups
sentences into paragraph-sized blocks for easier LLM
consumption.

Usage:
  python src/S1_txt_normalizer.py path/to/risorse/
"""

import argparse
import re
import sys
import textwrap
from pathlib import Path


# A .txt is considered "messy" when its average line
# length exceeds this threshold. Single-line audio
# transcriptions typically land in the thousands.
_MESSY_THRESHOLD = 300
_TARGET_PARAGRAPH_LEN = 700
_MAX_SENTENCE_LEN = 450
_WRAP_WIDTH = 110


def _normalize_whitespace(text: str) -> str:
    """Apply low-risk whitespace and punctuation cleanup."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *([,;:.?!])", r"\1", text)
    text = re.sub(r"([,;:.?!])(?=\S)", r"\1 ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _split_long_fragment(fragment: str, limit: int = _MAX_SENTENCE_LEN) -> list[str]:
    """
    Split an oversized fragment conservatively.

    We try stronger punctuation first and only fall back to word-boundary
    wrapping when the transcript gives us no reliable sentence markers.
    """
    fragment = fragment.strip()
    if not fragment:
        return []
    if len(fragment) <= limit:
        return [fragment]

    parts = re.split(r'(?<=[;:])\s+', fragment)
    if len(parts) > 1:
        out: list[str] = []
        for part in parts:
            out.extend(_split_long_fragment(part, limit=limit))
        return out

    words = fragment.split()
    out = []
    buf: list[str] = []
    buf_len = 0
    for word in words:
        extra = len(word) if not buf else len(word) + 1
        if buf and buf_len + extra > limit:
            out.append(" ".join(buf))
            buf = [word]
            buf_len = len(word)
        else:
            buf.append(word)
            buf_len += extra
    if buf:
        out.append(" ".join(buf))
    return out


def _split_sentences(text: str) -> list[str]:
    """
    Split text on conservative sentence boundaries.

    We intentionally avoid semantic or discourse-marker splitting to reduce
    the risk of breaking a single concept across multiple units.
    """
    fragments = re.split(r'(?<=[.?!])\s+(?=[A-ZÁÉÍÓÚÀÈÌÒÙ])', text)
    sentences: list[str] = []
    for frag in fragments:
        frag = frag.strip()
        if not frag:
            continue
        sentences.extend(_split_long_fragment(frag))
    return sentences


def _group_paragraphs(sentences: list[str], target_len: int = _TARGET_PARAGRAPH_LEN) -> list[str]:
    """Group sentence units into paragraph-sized blocks without re-splitting them."""
    paragraphs: list[str] = []
    current: list[str] = []
    current_len = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        extra = len(sentence) if not current else len(sentence) + 1
        if current and current_len + extra > target_len:
            paragraphs.append(" ".join(current))
            current = [sentence]
            current_len = len(sentence)
        else:
            current.append(sentence)
            current_len += extra

    if current:
        paragraphs.append(" ".join(current))

    return paragraphs


def _format_paragraphs(paragraphs: list[str], width: int = _WRAP_WIDTH) -> str:
    """
    Wrap paragraphs for human readability while preserving paragraph boundaries.

    This keeps concept-level grouping for LLMs, but avoids very long visual lines
    in editors and terminals.
    """
    formatted: list[str] = []
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        formatted.append(
            textwrap.fill(
                paragraph,
                width=width,
                break_long_words=False,
                break_on_hyphens=False,
            )
        )
    return "\n\n".join(formatted)


def _is_messy(path: Path) -> bool:
    """Return True if the file has very few lines relative to its size."""
    text = path.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        return False
    return (len(text) / len(lines)) > _MESSY_THRESHOLD


def normalize(path: Path) -> None:
    """
    Normalize a messy transcription into paragraph-sized blocks.

    Splits on conservative sentence boundaries and only falls back to
    word-boundary wrapping when a fragment is extremely long.
    """
    text = path.read_text(encoding="utf-8")
    text = _normalize_whitespace(text)
    sentences = _split_sentences(text)
    paragraphs = _group_paragraphs(sentences)
    formatted = _format_paragraphs(paragraphs)
    path.write_text(formatted, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalize messy transcription .txt files in a folder."
    )
    parser.add_argument("folder", help="Path to the risorse/ folder")
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.is_dir():
        print(f"Error: not a directory: {folder}")
        sys.exit(1)

    for txt in sorted(folder.glob("*.txt")):
        if _is_messy(txt):
            print(f"[normalize] {txt.name} — normalizing...")
            normalize(txt)
            print(f"  done")
        else:
            print(f"[normalize] {txt.name} — clean, skipping")


if __name__ == "__main__":
    main()
