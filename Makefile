#!/usr/bin/make

PYTHON := python3
PANDOC := pandoc
RM := rm

default: quickcheck.html quickcheck.pdf

.SUFFIXES:
.SUFFIXES: .md .html .pdf

.md.html:
	@mkdir -p public
	@$(PANDOC) --css article.css --to html4 --output public/$@ --embed-resources --standalone --section-divs $<
	@mv public/$@ public/index.html

.md.pdf:
	@mkdir -p public
	@$(PANDOC) --css article.css --to latex --output public/$@ --embed-resources --standalone --section-divs $<

.PHONY: check
check:
	@uv run ruff check --fix src/
	@uv run ruff format src/

.PHONY: lint
lint:
	@uv run ruff check src/
	@uv run ruff format --check src/

.PHONY: test
test:
	@uv run pytest src/ -v

.PHONY: sync
sync:
	@uv sync --extra dev

.PHONY: clean
clean:
	@$(RM) -rf public
	@$(RM) -rf .pytest_cache
	@$(RM) -rf .ruff_cache
	@$(RM) -rf __pycache__
	@find . -name "__pycache__" -type d -exec $(RM) -rf {} +
