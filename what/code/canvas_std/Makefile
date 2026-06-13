.PHONY: install test lint all
# Local "CI" for canvas_std (E0.1). A repo-level CI hook is wired at E2.3 (publish).

install:
	pip install -e ".[dev]"

test:
	pytest -q

lint:
	ruff check src tests

all: lint test
