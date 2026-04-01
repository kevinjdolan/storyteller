SHELL := /usr/bin/env bash

.DEFAULT_GOAL := help

COMPOSE := ./scripts/dev-compose.sh

.PHONY: help bootstrap up down logs ps reset lint test build check frontend-lint frontend-test frontend-build backend-test

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

frontend-lint: ## Run the frontend ESLint checks
	@npm --prefix frontend run lint

frontend-test: ## Run the frontend unit test suite
	@npm --prefix frontend run test

frontend-build: ## Run the frontend production build
	@npm --prefix frontend run build

backend-test: ## Run the backend pytest suite
	@cd backend && if [[ -x .venv/bin/python ]]; then .venv/bin/python -m pytest; elif command -v python3 >/dev/null 2>&1; then python3 -m pytest; else python -m pytest; fi

lint: ## Run the currently available lint checks
	@$(MAKE) frontend-lint

test: ## Run the backend and frontend automated tests
	@$(MAKE) backend-test
	@$(MAKE) frontend-test

build: ## Run the frontend production build
	@$(MAKE) frontend-build

check: ## Run lint, automated tests, and the frontend production build
	@$(MAKE) lint
	@$(MAKE) test
	@$(MAKE) build
