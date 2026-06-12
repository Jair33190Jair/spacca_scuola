#!/usr/bin/env python3
"""
Detect failed extractions in risorse/ .txt files.

Two failure modes:
  EMPTY   — file body is blank after the [FONTE:] header
  GARBLED — file has content but OCR produced scrambled text

Usage:
  python3 find_failed_extractions.py [--root <path>]

Output: failed_extractions.txt  (tab-separated: TYPE <tab> PATH)
"""

import re
import sys
from pathlib import Path

ROOT_DEFAULT = Path(__file__).parent.parent


def is_mixed_alnum(word: str) -> bool:
    """True if word mixes letters and digits — sign of garbled OCR."""
    return bool(re.search(r'[a-zA-Z]', word) and re.search(r'\d', word))


def mid_case_transitions(word: str) -> int:
    """Count lowercase→uppercase transitions after position 0 (e.g. aTOSIAd → 1)."""
    return sum(1 for i in range(1, len(word)) if word[i].isupper() and word[i - 1].islower())


def garbled_line_score(line: str) -> float:
    """
    Returns 0.0–1.0. High value = likely garbled.
    Signals: mixed alnum tokens, random mid-word case flips, mid-line brackets, high digit density.
    """
    words = line.split()
    if not words:
        return 0.0

    alpha_words = [re.sub(r'[^\w]', '', w) for w in words if re.search(r'[a-zA-Z]', w)]

    mixed = sum(1 for w in alpha_words if is_mixed_alnum(w))
    case_flips = sum(mid_case_transitions(w) for w in alpha_words)
    mid_brackets = len(re.findall(r'(?<!\[FONTE)\]', line))
    digit_count = sum(1 for c in line if c.isdigit())

    n = len(alpha_words) or 1
    score = (
        (mixed / n) * 0.4
        + min(case_flips / n / 2, 1.0) * 0.35
        + min(mid_brackets / 3, 1.0) * 0.1
        + min(digit_count / 20, 1.0) * 0.15
    )
    return score


def classify(path: Path) -> str | None:
    """Return 'EMPTY', 'GARBLED', or None if file looks fine."""
    try:
        text = path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return None

    lines = text.splitlines()

    # Strip leading [FONTE:] header and blank lines
    body_lines = [l for l in lines[1:] if l.strip()]

    if not body_lines:
        return 'EMPTY'

    # Score garbled: check first 80 lines of body (covers most PDFs)
    sample = body_lines[:80]
    scores = [garbled_line_score(l) for l in sample if len(l) > 10]
    if not scores:
        return None

    garbled_fraction = sum(1 for s in scores if s > 0.20) / len(scores)
    if garbled_fraction > 0.25:
        return 'GARBLED'

    # Second pass: catch files with persistent random case-flipping
    # even if the mixed-alnum signal is weak
    flip_counts = [
        sum(mid_case_transitions(re.sub(r'[^\w]', '', w)) for w in l.split() if re.search(r'[a-zA-Z]', w))
        for l in sample if len(l) > 10
    ]
    flippy_lines = sum(1 for f in flip_counts if f >= 2)
    if flippy_lines / len(flip_counts) > 0.20:
        return 'GARBLED'

    return None


def main():
    root = ROOT_DEFAULT
    if '--root' in sys.argv:
        idx = sys.argv.index('--root')
        root = Path(sys.argv[idx + 1])

    txt_files = sorted(root.rglob('risorse/*.txt'))
    results = []

    for path in txt_files:
        kind = classify(path)
        if kind:
            results.append((kind, path))

    out_path = Path(__file__).parent / 'failed_extractions.txt'
    with out_path.open('w', encoding='utf-8') as f:
        for kind, path in results:
            f.write(f'{kind}\t{path}\n')

    empty = sum(1 for k, _ in results if k == 'EMPTY')
    garbled = sum(1 for k, _ in results if k == 'GARBLED')
    print(f'Scanned {len(txt_files)} files → {empty} EMPTY, {garbled} GARBLED')
    print(f'Results written to: {out_path}')


if __name__ == '__main__':
    main()
