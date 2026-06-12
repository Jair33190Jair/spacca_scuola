#!/usr/bin/env python3
"""
Extract text from PDFs, both digital and scanned.

Hybrid strategy:
  1. Try direct text extraction (PyMuPDF)
  2. If a page has no text -> OCR with Tesseract

Usage:
  python src/pdf_txt.py path/to/file.pdf
  python src/pdf_txt.py path/to/file.pdf --dpi 400
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

from PIL import Image
import fitz  # PyMuPDF

# High-resolution scanned lesson PDFs
# exceed Pillow's anti-decompression-bomb
# threshold. It is safe to raise it: the files are ours.
Image.MAX_IMAGE_PIXELS = None


# Minimum character threshold to consider
# a page as "containing text". Pages below this threshold
# are treated as scans -> OCR.
MIN_CHARS = 50


def extract_direct_text(page: fitz.Page) -> str:
    """Extract embedded text from the PDF (no OCR)."""
    return page.get_text("text").strip()


def auto_rotate_image(img: Image.Image) -> tuple[Image.Image, int]:
    """Detect and correct image rotation using Tesseract OSD."""
    try:
        import pytesseract
        osd = pytesseract.image_to_osd(img, output_type=pytesseract.Output.DICT)
        angle = osd.get("rotate", 0)
        if angle != 0:
            return img.rotate(-angle, expand=True), angle
    except Exception:
        pass
    return img, 0


def is_low_quality(text: str) -> bool:
    """Return True if extracted text looks garbled."""
    words = text.split()
    if len(words) < 10:
        return True
    total = len(text)
    if total == 0:
        return True
    garbage = sum(
        1 for c in text
        if not (c.isalnum() or c.isspace())
    )
    return (garbage / total) > 0.25


def _mid_case_transitions(word: str) -> int:
    return sum(1 for i in range(1, len(word)) if word[i].isupper() and word[i - 1].islower())


def _garbled_line_score(line: str) -> float:
    words = line.split()
    if not words:
        return 0.0
    alpha_words = [re.sub(r'[^\w]', '', w) for w in words if re.search(r'[a-zA-Z]', w)]
    mixed = sum(1 for w in alpha_words if re.search(r'[a-zA-Z]', w) and re.search(r'\d', w))
    case_flips = sum(_mid_case_transitions(w) for w in alpha_words)
    mid_brackets = len(re.findall(r'(?<!\[FONTE)\]', line))
    digit_count = sum(1 for c in line if c.isdigit())
    n = len(alpha_words) or 1
    return (
        (mixed / n) * 0.4
        + min(case_flips / n / 2, 1.0) * 0.35
        + min(mid_brackets / 3, 1.0) * 0.1
        + min(digit_count / 20, 1.0) * 0.15
    )


def looks_garbled(text: str) -> bool:
    """Return True if direct-extracted text has the scrambled-PDF pattern."""
    lines = [l for l in text.splitlines() if len(l) > 10]
    sample = lines[:80]
    if not sample:
        return False
    scores = [_garbled_line_score(l) for l in sample]
    garbled_fraction = sum(1 for s in scores if s > 0.20) / len(scores)
    if garbled_fraction > 0.25:
        return True
    flip_counts = [
        sum(_mid_case_transitions(re.sub(r'[^\w]', '', w)) for w in l.split() if re.search(r'[a-zA-Z]', w))
        for l in sample
    ]
    if flip_counts and sum(1 for f in flip_counts if f >= 2) / len(flip_counts) > 0.20:
        return True
    return False


def extract_ocr_text(
    pdf_path: str,
    page_number: int,
    dpi: int,
) -> tuple[str, int]:
    """
    Convert a single page to an image and apply Tesseract OCR.
    Returns (text, rotation_angle_applied).
    """
    from pdf2image import convert_from_path
    import pytesseract

    images = convert_from_path(
        pdf_path,
        first_page=page_number,
        last_page=page_number,
        dpi=dpi,
    )
    if not images:
        return "", 0

    img, angle = auto_rotate_image(images[0])
    text = pytesseract.image_to_string(img, lang="ita").strip()
    return text, angle


def check_tesseract() -> bool:
    """Check whether Tesseract is installed."""
    return shutil.which("tesseract") is not None


def extract_pdf(pdf_path: str, dpi: int = 300) -> str:
    """
    Extract all text from a PDF.

    For each page, automatically decide whether to use
    direct extraction or OCR.
    """
    doc = fitz.open(pdf_path)
    result = []
    rotated_pages = []
    low_quality_pages = []

    for i, page in enumerate(doc):
        page_num = i + 1
        text = extract_direct_text(page)

        if len(text) >= MIN_CHARS and page.rotation == 0:
            print(
                f"  Page {page_num}/{len(doc)}: "
                f"direct text ({len(text)} characters)"
            )
            if is_low_quality(text):
                low_quality_pages.append(page_num)
                print(f"  Page {page_num}: ⚠ low quality")
                result.append(
                    f"[⚠ PAGINA ILLEGGIBILE: pagina {page_num}"
                    f" — contenuto non leggibile, revisione manuale necessaria]"
                )
                continue
            if looks_garbled(text):
                print(f"  Page {page_num}: ⚠ garbled direct text — falling back to OCR")
            else:
                result.append(text)
                continue

        if len(text) >= MIN_CHARS and page.rotation != 0:
            # Direct extraction on rotated pages gives wrong reading order —
            # always use OCR so auto-rotation can correct it.
            print(
                f"  Page {page_num}/{len(doc)}: "
                f"direct text skipped (rotation={page.rotation}°) — using OCR"
            )

        # Page without text -> OCR required
        if not check_tesseract():
            print(
                f"  Page {page_num}/{len(doc)}: "
                f"SKIP (scan, Tesseract required)"
            )
            result.append(
                f"[Page {page_num}: scan - "
                f"install tesseract-ocr]"
            )
            continue

        print(
            f"  Page {page_num}/{len(doc)}: "
            f"OCR (Tesseract, {dpi} DPI)..."
        )
        ocr_text, angle = extract_ocr_text(pdf_path, page_num, dpi)
        if angle != 0:
            rotated_pages.append(page_num)
            print(f"  Page {page_num}: rotated {angle}° before OCR")
        if is_low_quality(ocr_text):
            low_quality_pages.append(page_num)
            print(f"  Page {page_num}: ⚠ low quality after OCR")
            result.append(
                f"[⚠ PAGINA ILLEGGIBILE: pagina {page_num}"
                f" — contenuto non leggibile, revisione manuale necessaria]"
            )
        else:
            result.append(ocr_text)

    doc.close()

    if rotated_pages:
        pages = ", ".join(str(p) for p in rotated_pages)
        print(f"\n⚠  {len(rotated_pages)} page(s) auto-rotated (pages: {pages})")
    if low_quality_pages:
        pages = ", ".join(str(p) for p in low_quality_pages)
        print(f"⚠  {len(low_quality_pages)} page(s) low quality after extraction (pages: {pages}) — review manually")

    return "\n\n---\n\n".join(result)


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from PDF "
        "(direct + OCR fallback)."
    )
    parser.add_argument(
        "pdf",
        help="Path to the PDF file",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="DPI for OCR on scanned pages "
        "(default: 300)",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: {pdf_path} not found.")
        sys.exit(1)

    print(f"Processing: {pdf_path}")
    extracted_text = extract_pdf(str(pdf_path), dpi=args.dpi)
    extracted_text = f"[FONTE: {pdf_path.name}]\n\n{extracted_text}"
    output_path = pdf_path.with_suffix(".txt")
    output_path.write_text(extracted_text, encoding="utf-8")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
