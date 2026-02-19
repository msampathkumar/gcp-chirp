.PHONY: install uninstall test build clean setup help

help:
	@echo "Available commands:"
	@echo "  make install    - Install the tool globally using uv tool install"
	@echo "  make uninstall  - Uninstall the tool globally"
	@echo "  make test       - Run all tests using pytest"
	@echo "  make build      - Build source and wheel distributions"
	@echo "  make clean      - Remove build artifacts and cache"
	@echo "  make setup      - Run the internal setup wizard"

install:
	uv tool install . --force

uninstall:
	uv tool uninstall gcp-chirp

test:
	uv run pytest

build:
	uv build

clean:
	rm -rf dist/ .pytest_cache/ .venv/
	find . -type d -name "__pycache__" -exec rm -rf {} +

setup:
	uv run gcp-chirp setup
