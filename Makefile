.PHONY: setup dev api web lint test docker-up docker-down docker-validate check verify hooks-install hooks-run hooks-run-push

setup:
	uv sync --project apps/api
	pnpm install

dev: docker-up
	@echo "Starting API and web servers (Ctrl+C to stop both)..."
	@trap 'kill 0' INT TERM EXIT; $(MAKE) api & $(MAKE) web & wait

api:
	PYTHONPATH=. uv run --project apps/api uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000

web:
	pnpm --filter @eggscaliber/web dev

lint:
	pnpm lint
	uv run --project apps/api ruff check apps/api

test:
	pnpm test
	PYTHONPATH=. uv run --project apps/api pytest apps/api

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-validate:
	docker compose config > /dev/null

check: lint test

verify: check hooks-run-push docker-validate

hooks-install:
	uvx pre-commit install --hook-type pre-commit --hook-type pre-push

hooks-run:
	uvx pre-commit run --all-files

hooks-run-push:
	uvx pre-commit run --all-files --hook-stage pre-push
