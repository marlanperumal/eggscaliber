.PHONY: setup dev api web lint test docker-up docker-down check

setup:
	uv sync --project apps/api
	pnpm install

dev: docker-up
	@echo "Run 'make api' and 'make web' in separate terminals."

api:
	uv run --project apps/api uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000

web:
	pnpm --filter @eggscaliber/web dev

lint:
	pnpm lint
	uv run --project apps/api ruff check apps/api

test:
	pnpm test
	PYTHONPATH=. uv run --project apps/api pytest

docker-up:
	docker compose up -d

docker-down:
	docker compose down

check: lint test
