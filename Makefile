# Makefile for Ski Recommender

# Global variables
DOCKER_IMAGE=skirec
DOCKER_TAG=dev

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
		ipython

# Test all scripts
test: build
	docker run --rm \
		-t ${DOCKER_IMAGE}:${DOCKER_TAG} \
		pytest tests/
		# pytest tests/test_webscrape_trails.py
		# pytest tests/test_make_mtn_df.py
		# pytest --cov-report=html --cov=src --cov=web_app tests/test_make_mtn_df.py

# Run web app (Development)
web_app_dev:
	docker run --rm \
		--name ski-recsys \
		-p 8080:8080 \
		-v "$$PWD":/recsys \
		-t ${DOCKER_IMAGE}:${DOCKER_TAG} \
		python web_app/app.py

# Run web app (Production)
web_app_prod: build
	docker run --rm \
		--name ski-recsys \
		-p 8080:8080 \
		-t ${DOCKER_IMAGE}:${DOCKER_TAG} \
		python web_app/app.py
