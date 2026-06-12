#!/usr/bin/env python3
"""
One-off script: prepend [FONTE: filename] to .txt files in risorse/
dirs that don't already have it.

Usage:
  python src/patch_fonte_header.py
  python src/patch_fonte_header.py --dry-run
"""

import argparse
from pathlib import Path


def patch(root: Path, dry_run: bool) -> None:
    txt_files = sorted(root.rglob("risorse/*.txt"))
    patched = 0
    skipped = 0

    for txt in txt_files:
        content = txt.read_text(encoding="utf-8")
        header = f"[FONTE: {txt.name}]"
        if content.startswith("[FONTE:"):
            skipped += 1
            continue
        new_content = f"{header}\n\n{content}"
        if dry_run:
            print(f"  would patch: {txt.relative_to(root)}")
        else:
            txt.write_text(new_content, encoding="utf-8")
            print(f"  patched: {txt.relative_to(root)}")
        patched += 1

    print(f"\n{'(dry run) ' if dry_run else ''}patched: {patched}, already ok: {skipped}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would change without writing",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    print(f"Root: {root}")
    patch(root, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
