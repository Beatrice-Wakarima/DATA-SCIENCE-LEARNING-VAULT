---
title: Python + Docker
tags: [python, docker, data-engineering, devops]
created: 2026-05-20
up:: [[Python MOC]]
---

# 🐳 Python + Docker

> Docker packages your Python app and all its dependencies into a container that runs identically everywhere — your laptop, a server, or the cloud. Eliminates "works on my machine" forever.

---

## Why Docker for Python?

```
Without Docker:
  Dev machine:    Python 3.11, pandas 2.0  ✅
  Server:         Python 3.8, pandas 1.3   ❌ Different!
  Colleague:      Python 3.10, pandas 1.5  ❌ Different!

With Docker:
  Everywhere:     Python 3.11, pandas 2.0  ✅ Always same!
```

---

## Dockerfile — Packaging a Python App

```dockerfile
# Dockerfile

# Base image — Python 3.11 slim (lightweight)
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (Docker layer caching optimization)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Create non-root user (security best practice)
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose port (for APIs)
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Dockerfile for Data Pipeline

```dockerfile
# Dockerfile for ETL pipeline
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY main.py .
COPY config/ ./config/

# Create data directories
RUN mkdir -p data/raw data/processed outputs logs

# Run pipeline
CMD ["python", "main.py"]
```

---

## Building & Running

```bash
# Build image
docker build -t beatrice-pipeline .
docker build -t beatrice-pipeline:v1.0 .      # With version tag

# Run container
docker run beatrice-pipeline
docker run -d beatrice-pipeline                # Detached (background)
docker run --name my-pipeline beatrice-pipeline  # Named container

# Run with environment variables
docker run -e DB_HOST=localhost -e DB_PASSWORD=secret beatrice-pipeline

# Run with .env file
docker run --env-file .env beatrice-pipeline

# Mount local folder (so container can read/write files)
docker run -v $(pwd)/data:/app/data beatrice-pipeline

# Run FastAPI with port mapping
docker run -p 8000:8000 beatrice-api
# localhost:8000 → container:8000
```

---

## Essential Docker Commands

```bash
# Images
docker images                       # List all images
docker pull python:3.11-slim        # Pull from Docker Hub
docker rmi beatrice-pipeline        # Remove image
docker image prune                  # Remove unused images

# Containers
docker ps                           # Running containers
docker ps -a                        # All containers (including stopped)
docker stop my-pipeline             # Stop container
docker start my-pipeline            # Start stopped container
docker rm my-pipeline               # Remove container
docker logs my-pipeline             # View logs
docker logs -f my-pipeline          # Follow logs (live)
docker exec -it my-pipeline bash    # Shell into running container

# Build & run shortcut
docker build -t myapp . && docker run myapp
```

---

## Docker Compose — Multi-Container Apps

```yaml
# docker-compose.yml
version: "3.8"

services:
  
  # PostgreSQL database
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: beatrice
      POSTGRES_PASSWORD: secret123
      POSTGRES_DB: sales_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U beatrice"]
      interval: 10s
      timeout: 5s
      retries: 5
  
  # Python ETL pipeline
  pipeline:
    build: .
    environment:
      DB_HOST: postgres
      DB_PORT: 5432
      DB_NAME: sales_db
      DB_USER: beatrice
      DB_PASSWORD: secret123
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
      - ./logs:/app/logs
    depends_on:
      postgres:
        condition: service_healthy
  
  # FastAPI service
  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "8000:8000"
    environment:
      DB_HOST: postgres
    depends_on:
      - postgres
    restart: always

volumes:
  postgres_data:
```

```bash
# Docker Compose commands
docker compose up                   # Start all services
docker compose up -d                # Start in background
docker compose down                 # Stop and remove
docker compose down -v              # Also remove volumes
docker compose logs pipeline        # Logs for specific service
docker compose exec api bash        # Shell into service
docker compose build                # Rebuild images
```

---

## .dockerignore — Exclude Files

```dockerignore
# .dockerignore
venv/
__pycache__/
*.pyc
.env
.git/
*.md
data/raw/
notebooks/
tests/
.pytest_cache/
logs/
```

---

## Multi-Stage Build — Smaller Images

```dockerfile
# Stage 1 — Build
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2 — Runtime (much smaller!)
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy only installed packages from builder
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
COPY main.py .

ENV PATH=/root/.local/bin:$PATH

CMD ["python", "main.py"]
```

---

## Real World Example — Full Stack Pipeline

```yaml
# docker-compose.yml — Beatrice Builds Data Stack
version: "3.8"

services:
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./sql/init.sql:/docker-entrypoint-initdb.d/init.sql
  
  etl_pipeline:
    build: ./pipeline
    env_file: .env
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
    depends_on:
      - postgres
    command: python main.py
  
  api:
    build: ./api
    env_file: .env
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
  
  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: beatrice@gmail.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - postgres

volumes:
  pgdata:
```

```bash
# Start the full stack
docker compose up -d

# Your services:
# API:      http://localhost:8000
# API Docs: http://localhost:8000/docs  
# PgAdmin:  http://localhost:5050
# Postgres: localhost:5432
```

---

## Dockerfile Best Practices

```dockerfile
# ✅ DO
FROM python:3.11-slim              # Use slim images
COPY requirements.txt .            # Copy requirements FIRST (caching)
RUN pip install -r requirements.txt
COPY . .                           # Then copy source code
USER appuser                       # Don't run as root

# ❌ DON'T
FROM python:3.11                   # Full image is huge
COPY . .                           # Don't copy everything first
RUN pip install pandas numpy ...   # Don't install without requirements.txt
```

---

## Python Code to Interact with Docker

```python
import docker

# Connect to Docker daemon
client = docker.from_env()

# List running containers
for container in client.containers.list():
    print(f"{container.name}: {container.status}")

# Run a container from Python
container = client.containers.run(
    "python:3.11-slim",
    command="python -c \"print('Hello from Docker!')\"",
    remove=True
)
print(container.decode())

# Build an image from Python
image, logs = client.images.build(path=".", tag="my-pipeline:latest")
for log in logs:
    if "stream" in log:
        print(log["stream"].strip())
```

---

## Quick Reference

```bash
# Build
docker build -t name:tag .

# Run
docker run name                     # Basic
docker run -d -p 8000:8000 name     # Detached + port
docker run --env-file .env name     # With env file
docker run -v ./data:/app/data name # With volume mount

# Compose
docker compose up -d
docker compose down
docker compose logs -f service_name
docker compose exec service bash

# Cleanup
docker system prune                 # Remove unused everything
docker volume prune                 # Remove unused volumes
```

---

## Previous | Next
← [[23 - PySpark Basics]] | → [[25 - Python + Airflow]]
