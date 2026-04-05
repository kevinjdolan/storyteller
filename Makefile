SHELL := /usr/bin/env bash

.DEFAULT_GOAL := help

COMPOSE := ./scripts/dev-compose.sh

.PHONY: help bootstrap up down logs ps reset format format-check lint test build check ci frontend-format frontend-format-check frontend-lint frontend-test frontend-build backend-format backend-format-check backend-lint backend-test backend-integration-test backend-seed-catalog backend-storage-smoke backend-artifact-cleanup-dry-run backend-artifact-cleanup-apply

help: ## Show the common developer commands
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_.-]+:.*## / {printf "  %-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

bootstrap: ## Prepare local dependencies, install hooks, and create secrets.yaml if missing
	@./scripts/bootstrap-dev.sh

up: ## Start or rebuild the local Docker Compose stack in detached mode
	@$(COMPOSE) up --build -d

down: ## Stop the local stack and preserve persistent data
	@$(COMPOSE) down --remove-orphans

logs: ## Follow logs from the local Docker Compose stack
	@$(COMPOSE) logs -f --tail=200

ps: ## Show the current local Docker Compose service state
	@$(COMPOSE) ps

reset: ## Stop the stack and remove only Postgres and fake GCS persistent data
	@./scripts/reset-local-data.sh

frontend-format: ## Format frontend files with Prettier
	@npm --prefix frontend run format

frontend-format-check: ## Check frontend formatting with Prettier
	@npm --prefix frontend run format:check

frontend-lint: ## Run the frontend ESLint checks
	@npm --prefix frontend run lint

frontend-test: ## Run the frontend unit test suite
	@npm --prefix frontend run test

frontend-build: ## Run the frontend production build
	@npm --prefix frontend run build

backend-format: ## Format backend Python files with Ruff
	@cd backend && if [[ -x .venv/bin/python ]]; then .venv/bin/python -m ruff format app tests; elif command -v python3 >/dev/null 2>&1; then python3 -m ruff format app tests; else python -m ruff format app tests; fi

backend-format-check: ## Check backend Python formatting with Ruff
	@cd backend && if [[ -x .venv/bin/python ]]; then .venv/bin/python -m ruff format --check app tests; elif command -v python3 >/dev/null 2>&1; then python3 -m ruff format --check app tests; else python -m ruff format --check app tests; fi

backend-lint: ## Run backend Ruff lint checks
	@cd backend && if [[ -x .venv/bin/python ]]; then .venv/bin/python -m ruff check app tests; elif command -v python3 >/dev/null 2>&1; then python3 -m ruff check app tests; else python -m ruff check app tests; fi

backend-test: ## Run the backend pytest suite
	@cd backend && if [[ -x .venv/bin/python ]]; then .venv/bin/python -m pytest; elif command -v python3 >/dev/null 2>&1; then python3 -m pytest; else python -m pytest; fi

backend-integration-test: ## Run backend integration tests against local Postgres and fake GCS
	@$(COMPOSE) up -d postgres gcs
	@./scripts/wait-for-compose-services.sh postgres gcs
	@cd backend && \
	export STORYTELLER_RUN_INTEGRATION_TESTS=1; \
	export STORYTELLER_SECRETS_FILE="$${STORYTELLER_SECRETS_FILE:-}"; \
	export STORYTELLER_INTEGRATION_POSTGRES_ADMIN_URL="$${STORYTELLER_INTEGRATION_POSTGRES_ADMIN_URL:-postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/postgres}"; \
	export STORYTELLER_INTEGRATION_GCS_ENDPOINT="$${STORYTELLER_INTEGRATION_GCS_ENDPOINT:-http://127.0.0.1:8568}"; \
	export STORYTELLER_INTEGRATION_GCS_PUBLIC_URL="$${STORYTELLER_INTEGRATION_GCS_PUBLIC_URL:-http://127.0.0.1:8568}"; \
	export STORYTELLER_INTEGRATION_GCS_PROJECT_ID="$${STORYTELLER_INTEGRATION_GCS_PROJECT_ID:-storyteller-local}"; \
	export STORYTELLER_INTEGRATION_GCS_SESSIONS_BUCKET_NAME="$${STORYTELLER_INTEGRATION_GCS_SESSIONS_BUCKET_NAME:-storyteller-sessions}"; \
	export STORYTELLER_INTEGRATION_GCS_AUDIO_BUCKET_NAME="$${STORYTELLER_INTEGRATION_GCS_AUDIO_BUCKET_NAME:-storyteller-audio}"; \
	export STORYTELLER_INTEGRATION_GCS_EXPORTS_BUCKET_NAME="$${STORYTELLER_INTEGRATION_GCS_EXPORTS_BUCKET_NAME:-storyteller-exports}"; \
	if [[ -x .venv/bin/python ]]; then .venv/bin/python -m pytest --run-integration -m integration tests/integration; elif command -v python3 >/dev/null 2>&1; then python3 -m pytest --run-integration -m integration tests/integration; else python -m pytest --run-integration -m integration tests/integration; fi

backend-seed-catalog: ## Seed the backend-owned genre and tone catalog
	@cd backend && if [[ -x .venv/bin/python ]]; then .venv/bin/python -m app.seed_catalog; elif command -v python3 >/dev/null 2>&1; then python3 -m app.seed_catalog; else python -m app.seed_catalog; fi

backend-storage-smoke: ## Round-trip a sample object through the configured storage backend
	@cd backend && \
	export STORYTELLER_SECRETS_FILE="$${STORYTELLER_SECRETS_FILE:-}"; \
	export STORYTELLER_DATABASE_URL="$${STORYTELLER_DATABASE_URL:-postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller}"; \
	export STORYTELLER_GEMINI_API_KEY="$${STORYTELLER_GEMINI_API_KEY:-test-key}"; \
	export STORYTELLER_GCS_ENDPOINT="$${STORYTELLER_GCS_ENDPOINT:-http://127.0.0.1:8568}"; \
	export STORYTELLER_GCS_PROJECT_ID="$${STORYTELLER_GCS_PROJECT_ID:-storyteller-local}"; \
	export STORYTELLER_GCS_PUBLIC_URL="$${STORYTELLER_GCS_PUBLIC_URL:-http://127.0.0.1:8568}"; \
	export STORYTELLER_GCS_SESSIONS_BUCKET_NAME="$${STORYTELLER_GCS_SESSIONS_BUCKET_NAME:-storyteller-sessions}"; \
	export STORYTELLER_GCS_AUDIO_BUCKET_NAME="$${STORYTELLER_GCS_AUDIO_BUCKET_NAME:-storyteller-audio}"; \
	export STORYTELLER_GCS_EXPORTS_BUCKET_NAME="$${STORYTELLER_GCS_EXPORTS_BUCKET_NAME:-storyteller-exports}"; \
	if [[ -x .venv/bin/python ]]; then .venv/bin/python -m app.storage.smoke_test; elif command -v python3 >/dev/null 2>&1; then python3 -m app.storage.smoke_test; else python -m app.storage.smoke_test; fi

backend-artifact-cleanup-dry-run: ## Preview expired temporary artifacts without deleting anything
	@cd backend && \
	export STORYTELLER_SECRETS_FILE="$${STORYTELLER_SECRETS_FILE:-}"; \
	export STORYTELLER_DATABASE_URL="$${STORYTELLER_DATABASE_URL:-postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller}"; \
	export STORYTELLER_GEMINI_API_KEY="$${STORYTELLER_GEMINI_API_KEY:-test-key}"; \
	export STORYTELLER_GCS_ENDPOINT="$${STORYTELLER_GCS_ENDPOINT:-http://127.0.0.1:8568}"; \
	export STORYTELLER_GCS_PROJECT_ID="$${STORYTELLER_GCS_PROJECT_ID:-storyteller-local}"; \
	export STORYTELLER_GCS_PUBLIC_URL="$${STORYTELLER_GCS_PUBLIC_URL:-http://127.0.0.1:8568}"; \
	export STORYTELLER_GCS_SESSIONS_BUCKET_NAME="$${STORYTELLER_GCS_SESSIONS_BUCKET_NAME:-storyteller-sessions}"; \
	export STORYTELLER_GCS_AUDIO_BUCKET_NAME="$${STORYTELLER_GCS_AUDIO_BUCKET_NAME:-storyteller-audio}"; \
	export STORYTELLER_GCS_EXPORTS_BUCKET_NAME="$${STORYTELLER_GCS_EXPORTS_BUCKET_NAME:-storyteller-exports}"; \
	if [[ -x .venv/bin/python ]]; then .venv/bin/python -m app.maintenance.artifact_cleanup; elif command -v python3 >/dev/null 2>&1; then python3 -m app.maintenance.artifact_cleanup; else python -m app.maintenance.artifact_cleanup; fi

backend-artifact-cleanup-apply: ## Delete expired temporary artifacts after reviewing the dry run
	@cd backend && \
	export STORYTELLER_SECRETS_FILE="$${STORYTELLER_SECRETS_FILE:-}"; \
	export STORYTELLER_DATABASE_URL="$${STORYTELLER_DATABASE_URL:-postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller}"; \
	export STORYTELLER_GEMINI_API_KEY="$${STORYTELLER_GEMINI_API_KEY:-test-key}"; \
	export STORYTELLER_GCS_ENDPOINT="$${STORYTELLER_GCS_ENDPOINT:-http://127.0.0.1:8568}"; \
	export STORYTELLER_GCS_PROJECT_ID="$${STORYTELLER_GCS_PROJECT_ID:-storyteller-local}"; \
	export STORYTELLER_GCS_PUBLIC_URL="$${STORYTELLER_GCS_PUBLIC_URL:-http://127.0.0.1:8568}"; \
	export STORYTELLER_GCS_SESSIONS_BUCKET_NAME="$${STORYTELLER_GCS_SESSIONS_BUCKET_NAME:-storyteller-sessions}"; \
	export STORYTELLER_GCS_AUDIO_BUCKET_NAME="$${STORYTELLER_GCS_AUDIO_BUCKET_NAME:-storyteller-audio}"; \
	export STORYTELLER_GCS_EXPORTS_BUCKET_NAME="$${STORYTELLER_GCS_EXPORTS_BUCKET_NAME:-storyteller-exports}"; \
	if [[ -x .venv/bin/python ]]; then .venv/bin/python -m app.maintenance.artifact_cleanup --apply; elif command -v python3 >/dev/null 2>&1; then python3 -m app.maintenance.artifact_cleanup --apply; else python -m app.maintenance.artifact_cleanup --apply; fi

format: ## Format frontend and backend source files
	@$(MAKE) frontend-format
	@$(MAKE) backend-format

format-check: ## Check frontend and backend formatting without changing files
	@$(MAKE) frontend-format-check
	@$(MAKE) backend-format-check

lint: ## Run frontend and backend lint checks
	@$(MAKE) frontend-lint
	@$(MAKE) backend-lint

test: ## Run the backend and frontend automated tests
	@$(MAKE) backend-test
	@$(MAKE) frontend-test

build: ## Run the frontend production build
	@$(MAKE) frontend-build

check: ## Run formatting checks, lint, tests, and the frontend production build
	@$(MAKE) format-check
	@$(MAKE) lint
	@$(MAKE) test
	@$(MAKE) build

ci: ## Run the full CI validation path, including backend integration coverage
	@$(MAKE) check
	@$(MAKE) backend-integration-test
