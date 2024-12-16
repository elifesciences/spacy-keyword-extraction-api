#!/usr/bin/make -f

DOCKER_COMPOSE_DEV = docker compose
DOCKER_COMPOSE_CI = docker compose -f docker-compose.yml
DOCKER_COMPOSE = $(DOCKER_COMPOSE_DEV)


build:
	$(DOCKER_COMPOSE) build spacy-keyword-extraction-api

build-dev:
	$(DOCKER_COMPOSE) build spacy-keyword-extraction-api-dev

flake8:
	$(DOCKER_COMPOSE) run --rm spacy-keyword-extraction-api-dev \
		python -m flake8 spacy_keyword_extraction_api tests

lint: flake8


start:
	$(DOCKER_COMPOSE) up -d spacy-keyword-extraction-api

stop:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f


ci-build:
	$(MAKE) DOCKER_COMPOSE="$(DOCKER_COMPOSE_CI)" build

ci-lint:
	echo "Dummy lint"

ci-unittest:
	echo "Dummy unittest"
