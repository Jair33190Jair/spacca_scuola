#!/usr/bin/env python3
"""
Normalize messy .txt files in a risorse/ folder.

A file is "messy" when it looks like a single-line audio
dump (average line length > threshold). Normalization
splits it at sentence boundaries and wraps long lines.

Usage:
  python src/S1_txt_normalizer.py path/to/risorse/
"""

import argparse
import re
import sys
from pathlib import Path


# A .txt is considered "messy" when its average line
# length exceeds this threshold. Single-line audio
# transcriptions typically land in the thousands.
_MESSY_THRESHOLD = 300


def _is_messy(path: Path) -> bool:
    """Return True if the file has very few lines relative to its size."""
    text = path.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        return False
    return (len(text) / len(lines)) > _MESSY_THRESHOLD


def normalize(path: Path) -> None:
    """
    Split a messy transcription at sentence boundaries and
    wrap long sentences at ~120 chars.

    Splits on: .  ?  !  followed by whitespace + uppercase letter.
    """
    text = path.read_text(encoding="utf-8")

    # Primary split: sentence-ending punctuation before a capital
    fragments = re.split(r'(?<=[.?!])\s+(?=[A-ZÁÉÍÓÚÀÈÌÒÙ])', text)

    lines: list[str] = []
    for frag in fragments:
        frag = frag.strip()
        if not frag:
            continue
        if len(frag) <= 120:
            lines.append(frag)
            continue
        # Wrap at word boundaries for very long fragments
        words = frag.split()
        buf: list[str] = []
        buf_len = 0
        for word in words:
            if buf_len + len(word) + 1 > 120 and buf:
                lines.append(" ".join(buf))
                buf = [word]
                buf_len = len(word)
            else:
                buf.append(word)
                buf_len += len(word) + 1
        if buf:
            lines.append(" ".join(buf))

    path.write_text("\n".join(lines), encoding="utf-8")


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
