#!/usr/bin/make -f

DOCKER_COMPOSE_DEV = docker compose
DOCKER_COMPOSE_CI = docker compose -f docker-compose.yml
DOCKER_COMPOSE = $(DOCKER_COMPOSE_DEV)


build:
	$(DOCKER_COMPOSE) build spacy-keyword-extraction-api


ci-build:
	$(MAKE) DOCKER_COMPOSE="$(DOCKER_COMPOSE_CI)" build

ci-lint:
	echo "Dummy lint"

ci-unittest:
	echo "Dummy unittest"
