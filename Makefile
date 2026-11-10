# =============================================================================
# Taller 1 — Dry Bean ML · automatización de tareas
# =============================================================================

SHELL := /bin/bash

.DEFAULT_GOAL := help
.PHONY: help install dev pre-commit-install pre-commit lint format format-check test check data pipeline notebook clean

help: ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

install: ## Sincroniza el entorno virtual e instala dependencias
	uv sync

dev: install pre-commit-install ## Prepara el entorno de desarrollo (sync + hooks)

pre-commit-install: ## Instala los hooks de pre-commit en el repositorio local
	uv run pre-commit install

pre-commit: ## Ejecuta todos los hooks de pre-commit sobre el repositorio
	uv run pre-commit run --all-files

lint: ## Ejecuta Ruff (lint)
	uv run ruff check .

format: ## Formatea el código con Ruff
	uv run ruff format .

format-check: ## Verifica el formato sin modificarlo
	uv run ruff format --check .

test: ## Ejecuta las pruebas
	uv run pytest

check: lint format-check test ## Verificación completa (lint + formato + pruebas)

data: ## Descarga el dataset crudo de UCI en data/bronze
	uv run taller1 pipeline --quiet

pipeline: ## Ejecuta el flujo CRISP-DM completo y genera los artefactos
	uv run taller1 pipeline

notebook: ## Ejecuta el notebook del laboratorio de inicio a fin
	uv run jupyter nbconvert --to notebook --execute --inplace "notebooks/01_laboratorio_drybean.ipynb"

clean: ## Limpia cachés y artefactos temporales
	rm -rf .pytest_cache .ruff_cache dist build htmlcov .coverage
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .ipynb_checkpoints -prune -exec rm -rf {} +
