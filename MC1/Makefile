
.PHONY: all

-include .env

SHELL=/bin/bash -e

.DEFAULT_GOAL := help


migration:
	@poetry run alembic upgrade head

run_app:
	@poetry run uvicorn --host 0.0.0.0 main:app
