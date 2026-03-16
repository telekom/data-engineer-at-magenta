.PHONY: help install start lint format typecheck test dbt-run dbt-test dbt-docs clean

help:
	@echo "Available commands:"
	@echo "  install      Install all dependencies via pixi (dev environment)"
	@echo "  start        Start Dagster dev server"
	@echo "  notebook     Launch Jupyter Lab"
	@echo "  lint         Run ruff linter"
	@echo "  format       Run ruff formatter"
	@echo "  typecheck    Run pyright type checker"
	@echo "  test         Run pytest with coverage"
	@echo "  dbt-run      Run all dbt models"
	@echo "  dbt-test     Run all dbt tests"
	@echo "  dbt-docs     Generate and serve dbt documentation"
	@echo "  clean        Remove generated artifacts"

install:
	pixi install -e dev

start:
	pixi run start-dev

notebook:
	pixi run -e dev notebook

lint:
	pixi run -e dev lint

format:
	pixi run -e dev format

typecheck:
	pixi run -e dev typecheck

test:
	pixi run -e dev test

dbt-run:
	pixi run dbt-run

dbt-test:
	pixi run dbt-test

dbt-docs:
	pixi run dbt-docs-generate && pixi run dbt-docs-serve

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null; true
	find . -name "*.duckdb" -not -path "*/code_location_de_dbt/*" -delete 2>/dev/null; true
	rm -rf .dagster/storage 2>/dev/null; true
	rm -rf src/code_location_de_dbt/target 2>/dev/null; true
