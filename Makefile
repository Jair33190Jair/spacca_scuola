PYTHON  := .venv/bin/python
SRC     := src
DPI     ?= 300

# Usage:
#   make preprocess FOLDER=02_semestre/salute_mentale/01_intro/risorse
#   make preprocess FOLDER=02_semestre/salute_mentale

.PHONY: preprocess export_pdf

# Usage:
#   make export_pdf FOLDER=02_semestre/salute_mentale
#   make export_pdf FOLDER=02_semestre/salute_mentale/01_intro

export_pdf:
ifndef FOLDER
	$(error FOLDER is required, e.g. make export_pdf FOLDER=02_semestre/salute_mentale)
endif
	$(PYTHON) $(SRC)/md_to_pdf.py "$(FOLDER)"

preprocess:
ifndef FOLDER
	$(error FOLDER is required, e.g. make preprocess FOLDER=02_semestre/salute_mentale or .../risorse)
endif
	@set -e; \
	root="$(FOLDER)"; \
	if [ ! -d "$$root" ]; then \
		echo "Error: folder does not exist: $$root"; \
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
