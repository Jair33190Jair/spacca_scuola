#!/usr/bin/env python3
"""
Convert generated Markdown summaries to PDF and zip them.

Accepts a lesson folder or a subject folder:
  - Lesson:  02_semestre/<subject>/<NN>_<lesson>/
  - Subject: 02_semestre/<subject>/

In lesson mode, converts gen/*.md to PDF and produces a zip
next to the lesson folder.

In subject mode, produces a single zip for the whole subject:
  <subject>.zip
  ├── gen_ampia_panoramica.pdf   (if present)
  ├── 01_<lesson>/
  │   ├── 01_riassunto_dettagliato.pdf
  │   └── ...
  └── 02_<lesson>/
      └── ...

Usage:
  python src/md_to_pdf.py 02_semestre/sociologia/01_introduzione
  python src/md_to_pdf.py 02_semestre/sociologia
"""

import argparse
import sys
import zipfile
from pathlib import Path

import markdown2
from weasyprint import HTML


def _md_to_pdf(md_path: Path, out_path: Path) -> None:
    html = markdown2.markdown(
        md_path.read_text(encoding="utf-8"),
        extras=["tables", "fenced-code-blocks"],
    )
    # Minimal CSS: readable font, constrained width, page margins
    styled = f"""
    <style>
      body {{ font-family: Georgia, serif; max-width: 720px;
              margin: auto; font-size: 13pt; line-height: 1.6; }}
      h1, h2, h3 {{ font-family: Helvetica, sans-serif; }}
      table {{ border-collapse: collapse; width: 100%; }}
      td, th {{ border: 1px solid #ccc; padding: 6px 10px; }}
      th {{ background: #f4f4f4; }}
      code {{ background: #f0f0f0; padding: 2px 4px; }}
    </style>
    {html}
    """
    HTML(string=styled).write_pdf(out_path)


def _collect_lesson_pdfs(
    lesson_dir: Path,
    zf: zipfile.ZipFile,
    zip_prefix: str,
) -> list[Path]:
    """Render gen/*.md → PDF, add to open zip, return tmp paths."""
    gen_dir = lesson_dir / "gen"
    if not gen_dir.is_dir():
        return []

    tmp: list[Path] = []
    for md in sorted(gen_dir.glob("*.md")):
        pdf_path = gen_dir / md.with_suffix(".pdf").name
        print(f"  {md.name} → {pdf_path.name}")
        _md_to_pdf(md, pdf_path)
        zf.write(pdf_path, f"{zip_prefix}/{pdf_path.name}")
        tmp.append(pdf_path)
    return tmp


def export_lesson(lesson_dir: Path) -> Path:
    """Single lesson → zip next to the lesson folder."""
    if not (lesson_dir / "gen").is_dir():
        raise FileNotFoundError(f"No gen/ folder in {lesson_dir}")

    zip_path = lesson_dir.parent / f"{lesson_dir.name}.zip"
    tmp_pdfs: list[Path] = []

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        tmp_pdfs = _collect_lesson_pdfs(lesson_dir, zf, lesson_dir.name)

    for pdf in tmp_pdfs:
        pdf.unlink()

    return zip_path


def export_subject(subject_dir: Path) -> Path:
    """Whole subject → one zip with all lessons + ampia panoramica."""
    lessons = sorted(
        d for d in subject_dir.iterdir()
        if d.is_dir() and (d / "gen").is_dir()
    )
    if not lessons:
        raise FileNotFoundError(
            f"No lesson folders with gen/ found in {subject_dir}"
        )

    zip_path = subject_dir.parent / f"{subject_dir.name}.zip"
    tmp_pdfs: list[Path] = []

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # ampia panoramica at subject root (if present)
        panoramica = subject_dir / "gen_ampia_panoramica.md"
        if panoramica.exists():
            pdf_path = subject_dir / "gen_ampia_panoramica.pdf"
            print(f"  gen_ampia_panoramica.md → gen_ampia_panoramica.pdf")
            _md_to_pdf(panoramica, pdf_path)
            zf.write(pdf_path, "gen_ampia_panoramica.pdf")
            tmp_pdfs.append(pdf_path)

        for lesson in lessons:
            print(f"[lesson] {lesson.name}")
            tmp_pdfs += _collect_lesson_pdfs(lesson, zf, lesson.name)

    for pdf in tmp_pdfs:
        pdf.unlink()

    return zip_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export gen/*.md summaries to PDF zip."
    )
    parser.add_argument(
        "path",
        help="Lesson folder or subject folder",
    )
    args = parser.parse_args()

    target = Path(args.path)
    if not target.is_dir():
        print(f"Error: not a directory: {target}")
        sys.exit(1)

    if (target / "gen").is_dir():
        # Lesson mode
        print(f"[export lesson] {target.name}")
        zip_path = export_lesson(target)
        print(f"→ {zip_path}")
    else:
        # Subject mode
        print(f"[export subject] {target.name}")
        zip_path = export_subject(target)
        print(f"→ {zip_path}")


if __name__ == "__main__":
    main()
