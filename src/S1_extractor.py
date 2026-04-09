#!/usr/bin/env python3
"""
Extract text from PDFs, both digital and scanned.

Hybrid strategy:
  1. Try direct text extraction (PyMuPDF)
  2. If a page has no text -> OCR with Tesseract

Usage:
  python src/S1_extractor.py path/to/file.pdf
  python src/S1_extractor.py path/to/file.pdf --dpi 400
"""

import argparse
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


def extract_ocr_text(
    pdf_path: str,
    page_number: int,
    dpi: int,
) -> str:
    """
    Convert a single page to an image
    and apply Tesseract OCR.
    """
    # Lazy import: avoids a crash if Tesseract
    # is not installed and is not needed.
    from pdf2image import convert_from_path
    import pytesseract

    images = convert_from_path(
        pdf_path,
        first_page=page_number,
        last_page=page_number,
        dpi=dpi,
    )
    if not images:
        return ""

    return pytesseract.image_to_string(
        images[0],
        lang="ita",
    ).strip()


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

    for i, page in enumerate(doc):
        page_num = i + 1
        text = extract_direct_text(page)

        if len(text) >= MIN_CHARS:
            print(
                f"  Page {page_num}/{len(doc)}: "
                f"direct text ({len(text)} characters)"
            )
            result.append(text)
            continue

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
        ocr_text = extract_ocr_text(pdf_path, page_num, dpi)
        result.append(ocr_text)

    doc.close()
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
    output_path = pdf_path.with_suffix(".txt")
    output_path.write_text(extracted_text, encoding="utf-8")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
