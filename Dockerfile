FROM python:3.6.8-slim

# Install libraries
COPY docker_requirements.txt ./
RUN pip install --no-cache-dir -r docker_requirements.txt


# Copy files to image
COPY . .