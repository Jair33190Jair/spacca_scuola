PYTHON  := python3
SRC     := src
DPI     ?= 300

# Usage:
#   make preprocess FOLDER=02_semestre/salute_mentale/01_intro/risorse

.PHONY: preprocess

preprocess:
ifndef FOLDER
	$(error FOLDER is required, e.g. make preprocess FOLDER=02_semestre/salute_mentale/01_intro/risorse)
endif
	@echo "── pdf → txt ──────────────────────────────"
	@for pdf in $(FOLDER)/*.pdf; do \
		[ -f "$$pdf" ] || continue; \
		txt="$${pdf%.pdf}.txt"; \
		if [ ! -f "$$txt" ]; then \
			echo "[pdf2txt] $$pdf"; \
			$(PYTHON) $(SRC)/S1_pdf2txt.py "$$pdf" --dpi $(DPI); \
		else \
			echo "[pdf2txt] $$(basename $$pdf) — .txt exists, skipping"; \
		fi; \
	done
	@echo "── normalize ───────────────────────────────"
	@$(PYTHON) $(SRC)/S1_txt_normalizer.py $(FOLDER)
