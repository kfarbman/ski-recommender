FROM python:3.7.6-slim

# Set display port to avoid crash
ENV DISPLAY=:99

# Set Poetry environment variables
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.10

RUN apt-get -y update && \
    apt-get install -y gnupg wget curl

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get -y update && \
    apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN apt-get install -yqq unzip && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Create working directory
WORKDIR /recsys

# System dependencies
RUN pip install "poetry==$POETRY_VERSION"

# Copy Poetry requirements to cache them in Docker layer
COPY poetry.lock pyproject.toml /recsys/

# Project initialization
RUN poetry config virtualenvs.create false \
    && poetry install

# Copy files to image
COPY . .

# Expose Flask
EXPOSE 8080
