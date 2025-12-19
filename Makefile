.PHONY: up down migrate test help

TEST_PATH ?= tests/

help:
	@echo "Available commands:"
	@echo "  make up        Start all services"
	@echo "  make down      Stop all services"
	@echo "  make migrate   Run Flask-Migrate upgrade"
	@echo "  make test      Run tests (default: tests/)"
	@echo "  make test TEST_PATH=path/to/tests"

up:
	docker compose up -d postgres flask-app

down:
	docker compose down

migrate:
	docker compose run --rm flask-app flask db upgrade

test:
	docker compose run --rm tests pytest $(TEST_PATH) -q
