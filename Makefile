PYTHON  := .venv/bin/python
SRC     := src
DPI     ?= 300

# Usage:
#   make preprocess FOLDER=02_semestre/salute_mentale/01_intro/risorse
#   make preprocess FOLDER=02_semestre/salute_mentale
#   make preprocess FOLDER=path/to/file.pdf

.PHONY: preprocess export_pdf

# Usage:
#   make export_pdf FOLDER=02_semestre/salute_mentale
#   make export_pdf FOLDER=02_semestre/salute_mentale/01_intro

export_pdf:
ifndef FOLDER
	$(error FOLDER is required, e.g. make export_pdf FOLDER=02_semestre/salute_mentale)
endif
	DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib $(PYTHON) $(SRC)/md_to_pdf.py "$(FOLDER)"

preprocess:
ifndef FOLDER
	$(error FOLDER is required, e.g. make preprocess FOLDER=02_semestre/salute_mentale or .../risorse or .../file.pdf)
endif
	@set -e; \
	root="$(FOLDER)"; \
	if [ -f "$$root" ]; then \
		case "$$root" in \
			*.pdf) \
				dir="$$(dirname "$$root")"; \
				txt="$${root%.pdf}.txt"; \
				echo ""; \
				echo "==> $$root"; \
				echo "── pdf → txt ──────────────────────────────"; \
				if [ ! -f "$$txt" ]; then \
					echo "[pdf2txt] $$root"; \
					$(PYTHON) $(SRC)/pdf_to_txt.py "$$root" --dpi $(DPI); \
				else \
					echo "[pdf2txt] $$(basename "$$root") — .txt exists, skipping"; \
				fi; \
				echo "── normalize ───────────────────────────────"; \
				$(PYTHON) $(SRC)/txt_normalizer.py "$$dir"; \
				exit 0; \
				;; \
			*) \
				echo "Error: file is not a PDF: $$root"; \
				exit 1; \
				;; \
		esac; \
	fi; \
	if [ ! -d "$$root" ]; then \
		echo "Error: path does not exist or is not a directory/PDF: $$root"; \
		exit 1; \
	fi; \
	if [ "$$(basename "$$root")" = "risorse" ]; then \
		risorse_dirs="$$root"; \
	else \
		risorse_dirs="$$(find "$$root" -type d -name risorse | sort)"; \
	fi; \
	if [ -z "$$risorse_dirs" ]; then \
		echo "Error: no risorse folders found under $$root"; \
		exit 1; \
	fi; \
	for dir in $$risorse_dirs; do \
		echo ""; \
		echo "==> $$dir"; \
		echo "── pdf → txt ──────────────────────────────"; \
		for pdf in "$$dir"/*.pdf; do \
			[ -f "$$pdf" ] || continue; \
			txt="$${pdf%.pdf}.txt"; \
			if [ ! -f "$$txt" ]; then \
				echo "[pdf2txt] $$pdf"; \
				$(PYTHON) $(SRC)/pdf_to_txt.py "$$pdf" --dpi $(DPI); \
			else \
				echo "[pdf2txt] $$(basename "$$pdf") — .txt exists, skipping"; \
			fi; \
		done; \
		echo "── normalize ───────────────────────────────"; \
		$(PYTHON) $(SRC)/txt_normalizer.py "$$dir"; \
	done
