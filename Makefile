#!/usr/bin/make -f

DOCKER_COMPOSE_DEV = docker compose
DOCKER_COMPOSE_CI = docker compose -f docker-compose.yml
DOCKER_COMPOSE = $(DOCKER_COMPOSE_DEV)

VENV = venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python


venv-clean:
	@if [ -d "$(VENV)" ]; then \
		rm -rf "$(VENV)"; \
	fi

venv-create:
	python3 -m venv $(VENV)

dev-install:
	$(PIP) install --disable-pip-version-check -r requirements.build.txt
	$(PIP) install --disable-pip-version-check \
		-r requirements.txt \
		-r requirements.dev.txt


dev-venv: venv-create dev-install


dev-flake8:
	$(PYTHON) -m flake8 spacy_keyword_extraction_api tests

dev-pylint:
	$(PYTHON) -m pylint spacy_keyword_extraction_api tests

dev-mypy:
	$(PYTHON) -m mypy --check-untyped-defs spacy_keyword_extraction_api tests

dev-lint: dev-flake8 dev-pylint dev-mypy

dev-unittest:
	$(PYTHON) -m pytest -p no:cacheprovider $(ARGS) tests/unit_test

dev-test: dev-lint dev-unittest


dev-start:
	$(PYTHON) -m uvicorn \
		spacy_keyword_extraction_api.main:create_app \
		--reload \
		--factory \
		--host 127.0.0.1 \
		--port 8000


build:
	$(DOCKER_COMPOSE) build spacy-keyword-extraction-api

build-dev:
	$(DOCKER_COMPOSE) build spacy-keyword-extraction-api-dev

flake8:
	$(DOCKER_COMPOSE) run --rm spacy-keyword-extraction-api-dev \
		python -m flake8 spacy_keyword_extraction_api tests

pylint:
	$(DOCKER_COMPOSE) run --rm spacy-keyword-extraction-api-dev \
		python -m pylint spacy_keyword_extraction_api tests

mypy:
	$(DOCKER_COMPOSE) run --rm spacy-keyword-extraction-api-dev \
		python -m mypy --check-untyped-defs spacy_keyword_extraction_api tests

lint: flake8 pylint mypy

pytest:
	$(DOCKER_COMPOSE) run --rm spacy-keyword-extraction-api-dev \
		python -m pytest spacy_keyword_extraction_api tests

test: lint pytest


start:
	$(DOCKER_COMPOSE) up -d spacy-keyword-extraction-api

stop:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f


ci-build:
	$(MAKE) DOCKER_COMPOSE="$(DOCKER_COMPOSE_CI)" build

ci-build-dev:
	$(MAKE) DOCKER_COMPOSE="$(DOCKER_COMPOSE_CI)" build-dev

ci-lint:
	$(MAKE) DOCKER_COMPOSE="$(DOCKER_COMPOSE_CI)" lint

ci-unittest:
	$(MAKE) DOCKER_COMPOSE="$(DOCKER_COMPOSE_CI)" pytest
