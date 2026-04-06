# Eggscaliber

Eggscaliber is a metadata-first data analysis platform for pilot customers.
It supports ingestion from heterogeneous data sources, grounded analytics, and
natural-language query workflows that are strictly traceable to available data.

## Current Focus

- Tooling and delivery workflow setup.
- Root-run development commands (`uv`, `pnpm`, `docker`).
- Metadata modeling and ingestion editing workflow foundations.
- Grounded AI orchestration and evaluation harness setup.

## Operating Model

- Product truth: Linear.
- Engineering truth: GitHub.
- Design truth: Figma.
- Agent orchestration and coding: Cursor.

See `AGENTS.md` for the full autonomous execution contract.

## Root Commands

Run these from the repository root:

- `pnpm install`
- `uv sync --project apps/api`
- `docker compose up -d`
- `make api` (starts FastAPI on `http://localhost:8000`)
- `make web` (placeholder web command)
- `pnpm check`
- `make docker-down`

## Local Quality Hooks

Install local hooks once per clone:

- `make hooks-install`

Run hook suites manually:

- `make hooks-run` (pre-commit stage)
- `make hooks-run-push` (pre-push stage, includes tests)
