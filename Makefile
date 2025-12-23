.PHONY: up down migrate migrations test help env setup

TEST_PATH ?= tests/
MSG ?= "auto migration"

help:
	@echo "Available commands:"
	@echo "  make setup    				Set up environment(Run if it is your first time)"
	@echo "  make up                    Start all services"
	@echo "  make down                  Stop all services"
	@echo "  make env                   Create .env from env.example.txt"
	@echo "  make migrate               Run Flask-Migrate upgrade"
	@echo "  make migrations MSG=\"...\" Create a new migration with comment"
	@echo "  make test                  Run tests (default: tests/)"
	@echo "  make test TEST_PATH=path/to/tests"

up:
	docker compose up -d postgres flask-app worker

down:
	docker compose down

env:
	@if [ ! -f .env ]; then \
		cp env.example.txt .env; \
		echo ".env created from env.example.txt"; \
	else \
		echo ".env already exists"; \
	fi

migrate:
	docker compose run --rm flask-app flask db upgrade

migrations:
	docker compose run --rm flask-app flask db migrate -m $(MSG)

test:
	docker compose run --rm tests pytest $(TEST_PATH) -q

setup:
	make env up migrate
