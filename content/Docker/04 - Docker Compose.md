---
title: Docker Compose
tags: [docker, compose, devops, data-engineering]
created: 2026-05-20
up:: [[Docker MOC]]
---

# 🎼 Docker Compose

> Docker Compose manages multi-container applications with a single YAML file. One command starts your entire stack — database, API, pipeline, monitoring. Essential for data engineering.

---

## What is Docker Compose?

```
Without Compose:           With Compose:
  docker run postgres...     docker compose up
  docker run redis...
  docker run airflow...
  docker run api...
  (4 commands, easy to forget flags)
```

---

## Basic docker-compose.yml

```yaml
# docker-compose.yml
version: "3.8"

services:
  
  # Service 1: PostgreSQL
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: beatrice
      POSTGRES_PASSWORD: secret123
      POSTGRES_DB: data_vault
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # Service 2: Python API
  api:
    build: .                    # Build from Dockerfile in current dir
    ports:
      - "8000:8000"
    environment:
      DB_HOST: postgres         # Uses service name!
      DB_PASSWORD: secret123
    depends_on:
      - postgres                # Start postgres first

# Named volumes
volumes:
  postgres_data:
```

---

## Full docker-compose.yml Reference

```yaml
version: "3.8"

services:
  
  my-service:
    # Image or Build
    image: python:3.11-slim             # Use existing image
    build:                              # OR build from Dockerfile
      context: .                        # Build context (directory)
      dockerfile: Dockerfile            # Dockerfile name
      args:                             # Build arguments
        VERSION: "1.0.0"
        ENV: "production"
    
    # Container settings
    container_name: my-service          # Custom container name
    hostname: my-service
    restart: always                     # no | always | on-failure | unless-stopped
    
    # Ports: host:container
    ports:
      - "8000:8000"
      - "8443:443"
    
    # Environment variables
    environment:
      DB_HOST: postgres
      DB_PORT: 5432
      APP_ENV: production
    env_file:
      - .env                            # Load from .env file
    
    # Volumes
    volumes:
      - ./data:/app/data                # Bind mount
      - named-volume:/app/uploads       # Named volume
      - ./config:/app/config:ro         # Read-only
    
    # Dependencies
    depends_on:
      postgres:
        condition: service_healthy      # Wait for health check
      redis:
        condition: service_started      # Just wait for start
    
    # Networking
    networks:
      - app-network
    
    # Health check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    
    # Resource limits
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          memory: 256M
    
    # Override CMD
    command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
    
    # Override ENTRYPOINT
    entrypoint: ["python", "-m"]

networks:
  app-network:
    driver: bridge

volumes:
  named-volume:
    driver: local
```

---

## Beatrice Builds — Full Data Stack

```yaml
# docker-compose.yml — Complete data engineering stack
version: "3.8"

services:

  # ── DATABASE ──────────────────────────────────────
  postgres:
    image: postgres:15
    container_name: bb-postgres
    environment:
      POSTGRES_USER: ${DB_USER:-beatrice}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-secret123}
      POSTGRES_DB: ${DB_NAME:-data_vault}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./sql/init.sql:/docker-entrypoint-initdb.d/01_init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-beatrice}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - bb-network

  # ── DATABASE UI ───────────────────────────────────
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: bb-pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_EMAIL:-beatrice@gmail.com}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD:-admin}
    ports:
      - "5050:80"
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - bb-network

  # ── ETL PIPELINE ──────────────────────────────────
  pipeline:
    build:
      context: ./pipeline
      dockerfile: Dockerfile
    container_name: bb-pipeline
    env_file: .env
    environment:
      DB_HOST: postgres           # Uses service name!
      DB_PORT: 5432
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
      - ./logs:/app/logs
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - bb-network

  # ── FASTAPI ───────────────────────────────────────
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    container_name: bb-api
    env_file: .env
    environment:
      DB_HOST: postgres
    ports:
      - "8000:8000"
    volumes:
      - ./logs:/app/logs
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    networks:
      - bb-network

  # ── AIRFLOW ───────────────────────────────────────
  airflow:
    image: apache/airflow:2.7.0
    container_name: bb-airflow
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://beatrice:secret123@postgres/airflow
      AIRFLOW__CORE__LOAD_EXAMPLES: "false"
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs/airflow:/opt/airflow/logs
    depends_on:
      postgres:
        condition: service_healthy
    command: >
      bash -c "airflow db init &&
               airflow users create --username admin --password admin
                 --firstname Beatrice --lastname Builds
                 --role Admin --email beatrice@gmail.com &&
               airflow webserver"
    networks:
      - bb-network

networks:
  bb-network:
    driver: bridge

volumes:
  postgres_data:
  pgadmin_data:
```

---

## Essential Compose Commands

```bash
# Start all services
docker compose up

# Start in background (detached)
docker compose up -d

# Build images then start
docker compose up --build

# Start specific service only
docker compose up postgres

# Stop all services
docker compose down

# Stop and remove volumes (WARNING: deletes data!)
docker compose down -v

# Stop and remove images too
docker compose down --rmi all

# View running services
docker compose ps

# View logs
docker compose logs
docker compose logs postgres        # Specific service
docker compose logs -f api          # Follow live logs
docker compose logs --tail 50 api   # Last 50 lines

# Rebuild specific service
docker compose build api
docker compose build --no-cache api

# Shell into a service
docker compose exec postgres psql -U beatrice -d data_vault
docker compose exec api bash

# Run one-off command
docker compose run --rm pipeline python scripts/seed_data.py

# Scale a service (run multiple instances)
docker compose up --scale api=3

# Restart a service
docker compose restart api

# Pull latest images
docker compose pull
```

---

## Environment Variables in Compose

```yaml
# Method 1: Hardcoded (only for non-secrets)
environment:
  APP_ENV: production

# Method 2: From .env file (auto-loaded!)
# .env file:
# DB_PASSWORD=secret123
# DB_USER=beatrice
services:
  app:
    environment:
      DB_PASSWORD: ${DB_PASSWORD}    # From .env
      DB_USER: ${DB_USER:-beatrice}  # With default

# Method 3: env_file directive
services:
  app:
    env_file:
      - .env
      - .env.production

# Method 4: Pass at runtime
docker compose up -e DB_PASSWORD=override
```

---

## Health Checks & Dependencies

```yaml
services:
  postgres:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U beatrice"]
      interval: 10s       # Check every 10s
      timeout: 5s         # Fail after 5s no response
      retries: 5          # Try 5 times before unhealthy
      start_period: 30s   # Grace period on startup

  api:
    build: .
    depends_on:
      postgres:
        condition: service_healthy    # Wait for healthy!
      redis:
        condition: service_started    # Just started
```

---

## Development vs Production Compose

```yaml
# docker-compose.yml — Base config
services:
  api:
    build: .
    environment:
      DB_HOST: postgres

# docker-compose.override.yml — Dev additions (auto-loaded!)
services:
  api:
    volumes:
      - .:/app              # Live code reload
    command: uvicorn main:app --reload --host 0.0.0.0
    environment:
      APP_ENV: development

# docker-compose.prod.yml — Production
services:
  api:
    restart: always
    environment:
      APP_ENV: production
    deploy:
      replicas: 3
```

```bash
# Development (uses base + override automatically)
docker compose up

# Production (explicit file)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

---

## Quick Reference

```bash
# Start
docker compose up -d              # Background
docker compose up --build         # Rebuild first

# Stop
docker compose down               # Stop + remove containers
docker compose down -v            # Also remove volumes

# Monitor
docker compose ps                 # Service status
docker compose logs -f service    # Live logs
docker compose stats              # Resource usage

# Interact
docker compose exec svc bash      # Shell
docker compose run --rm svc cmd   # One-off command

# Rebuild
docker compose build svc
docker compose up -d --build svc  # Rebuild + restart
```

---

## Previous | Next
← [[03 - Docker Volumes and Networks]] | → [[05 - Docker for Data Engineering]]
