# Makefile for Ski Recommender

# Global variables
DOCKER_IMAGE=ski-recommender
GIT_COMMIT_ID=$$(git log --format="%H" -n 1 | head -c 7)
DOCKER_TAG=latest

# Build Docker Image
build:
	docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .

# Development
# Mount repo to Docker image
develop:
	docker run --rm -i \
		--name ski-recsys \
		-v "$$PWD":/recsys \
		-t ${DOCKER_IMAGE}:${DOCKER_TAG} \
		/bin/bash

# Test all scripts
test: build
	docker run \
		-t ${DOCKER_IMAGE}:${DOCKER_TAG} \
		pytest \
			--cov=src \
			--cov=web_app \
			tests/

# Run web app (Development)
# Option to change DOCKER_TAG
web_app_dev:
	docker run --rm \
		--name ski-recsys \
		-p 8080:8080 \
		-v "$$PWD":/recsys \
		-t ${DOCKER_IMAGE}:${DOCKER_TAG} \
		python web_app/app.py

# Run web app (Production)
# Option to change DOCKER_TAG
web_app_prod: build
	docker run --rm \
		--name ski-recsys \
		-p 8080:8080 \
		-t ${DOCKER_IMAGE}:${DOCKER_TAG} \
		python web_app/app.py
