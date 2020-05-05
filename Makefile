# Makefile for Ski Recommender

# Build Docker Image
build:
	docker build -t skirec:dev .

# Development
# Mount repo to Docker image
develop:
	docker run --rm -ti \
		--name ski-recsys \
		-v "$PWD":/recsys skirec:dev \
		ipython

# Test all scripts
test:
	docker run --rm -ti \
    	--name ski-recsys \
    	-v "$PWD":/recsys skirec:dev \
    	pytest --cov=src tests/

# Run web app (Development)
web_app_dev:
	docker run --rm -ti \
		--name ski-recsys \
		-p 8080:8080 \
		-v "$PWD":/recsys skirec:dev \
		python web_app/app.py

# Run web app (Production)
web_app_prod:
	docker run --rm -ti \
		--name ski-recsys \
		-p 8080:8080 \
		python web_app/app.py
