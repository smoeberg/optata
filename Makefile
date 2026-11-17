.PHONY: dev db-up migrate seed ci lint imports test

DATABASE_URL ?= postgresql://postgres:postgres@127.0.0.1:5432/optata_dev
export DATABASE_URL
export OPTATA_ENV ?= dev

# Full local database with synthetic data only. Never points at production.
dev: db-up migrate seed

db-up:
	docker compose up -d --wait db

migrate:
	python -m tools.migrate

seed:
	python -m tools.fixtures.cli load --seed 42 --dwellings 10000 --orders 1000 --verified-ratio 0.25

# Everything CI runs, runnable locally.
ci: lint imports test

lint:
	ruff check .

imports:
	lint-imports

test:
	pytest -q
