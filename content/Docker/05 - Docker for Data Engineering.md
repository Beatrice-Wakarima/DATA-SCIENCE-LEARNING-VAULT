---
title: Docker for Data Engineering
tags: [docker, data-engineering, pipelines]
created: 2026-05-20
up:: [[Docker MOC]]
---

# ⚙️ Docker for Data Engineering

> This note shows how Docker powers real data engineering workflows — containerising pipelines, running databases, orchestrating with Airflow, and building reproducible data stacks.

---

## Why Docker for Data Engineering?

```
Problem Without Docker:
  "The pipeline runs on my machine but fails in production"
  "I need Python 3.8 for project A and 3.11 for project B"
  "Setting up Airflow took 3 days and broke my system"

Solution With Docker:
  Every pipeline runs in identical environments
  Multiple Python versions in separate containers
  Airflow running in 5 minutes with one command
```

---

## Pattern 1 — Containerised ETL Pipeline

```
Project Structure:
pipeline/
├── Dockerfile
├── requirements.txt
├── main.py
├── src/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── data/
└── outputs/
```

```dockerfile
# pipeline/Dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY main.py .

RUN mkdir -p data outputs logs

RUN useradd -m appuser && chown -R appuser /app
USER appuser

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
```

```python
# main.py — pipeline entry point
import logging
import os
from src.extract import extract_bank_data
from src.transform import clean_and_transform
from src.load import load_to_postgres

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

def run():
    logger.info("🚀 Bank Marketing Pipeline starting")

    # Extract
    df = extract_bank_data(
        filepath=os.getenv("DATA_PATH", "data/bank_marketing.csv")
    )

    # Transform
    df_clean = clean_and_transform(df)

    # Load
    load_to_postgres(
        df=df_clean,
        table="bank_customers",
        db_url=os.getenv("DATABASE_URL")
    )

    logger.info("✅ Pipeline complete!")

if __name__ == "__main__":
    run()
```

```bash
# Build and run the pipeline
docker build -t bank-pipeline ./pipeline

docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/outputs:/app/outputs \
  -e DATABASE_URL=postgresql://beatrice:secret@postgres:5432/data_vault \
  -e DATA_PATH=data/bank_marketing.csv \
  --network pipeline-net \
  bank-pipeline
```

---

## Pattern 2 — PostgreSQL + pgAdmin Stack

```yaml
# docker-compose.yml
version: "3.8"

services:
  postgres:
    image: postgres:15
    container_name: bb-postgres
    environment:
      POSTGRES_USER: beatrice
      POSTGRES_PASSWORD: secret123
      POSTGRES_DB: data_vault
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./sql/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U beatrice"]
      interval: 10s
      retries: 5

  pgadmin:
    image: dpage/pgadmin4
    container_name: bb-pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: beatrice@gmail.com
      PGADMIN_DEFAULT_PASSWORD: admin123
    ports:
      - "5050:80"
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  postgres_data:
```

```sql
-- sql/init.sql — runs automatically on first start
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

CREATE TABLE IF NOT EXISTS bronze.raw_bank_marketing (
    id          SERIAL PRIMARY KEY,
    age         TEXT,
    job         TEXT,
    balance     TEXT,
    y           TEXT,
    loaded_at   TIMESTAMP DEFAULT NOW()
);

GRANT ALL ON ALL TABLES IN SCHEMA bronze TO beatrice;
GRANT ALL ON ALL TABLES IN SCHEMA silver TO beatrice;
GRANT ALL ON ALL TABLES IN SCHEMA gold TO beatrice;
```

```bash
docker compose up -d
# PostgreSQL: localhost:5432
# pgAdmin:    http://localhost:5050
```

---

## Pattern 3 — Airflow in Docker

```yaml
# docker-compose.airflow.yml
version: "3.8"

x-airflow-common: &airflow-common
  image: apache/airflow:2.7.0
  environment:
    AIRFLOW__CORE__EXECUTOR: LocalExecutor
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    AIRFLOW__CORE__FERNET_KEY: ''
    AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
    AIRFLOW__WEBSERVER__EXPOSE_CONFIG: 'true'
  volumes:
    - ./dags:/opt/airflow/dags
    - ./logs/airflow:/opt/airflow/logs
    - ./plugins:/opt/airflow/plugins
  depends_on:
    postgres:
      condition: service_healthy

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - airflow_postgres:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airflow"]
      interval: 10s
      retries: 5

  airflow-init:
    <<: *airflow-common
    command: >
      bash -c "
        airflow db init &&
        airflow users create
          --username admin --password admin
          --firstname Beatrice --lastname Builds
          --role Admin --email beatrice@gmail.com
      "

  airflow-webserver:
    <<: *airflow-common
    ports:
      - "8080:8080"
    command: webserver
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8080/health"]
      interval: 30s

  airflow-scheduler:
    <<: *airflow-common
    command: scheduler

volumes:
  airflow_postgres:
```

```bash
# Start Airflow
docker compose -f docker-compose.airflow.yml up airflow-init
docker compose -f docker-compose.airflow.yml up -d

# Access: http://localhost:8080
# Login: admin / admin
```

---

## Pattern 4 — dbt in Docker

```dockerfile
# dbt/Dockerfile
FROM ghcr.io/dbt-labs/dbt-postgres:1.7.0

WORKDIR /usr/app

COPY profiles.yml /root/.dbt/profiles.yml
COPY . .

CMD ["dbt", "run"]
```

```yaml
# profiles.yml
default:
  target: prod
  outputs:
    prod:
      type: postgres
      host: "{{ env_var('DB_HOST') }}"
      user: "{{ env_var('DB_USER') }}"
      password: "{{ env_var('DB_PASSWORD') }}"
      port: 5432
      dbname: data_vault
      schema: silver
      threads: 4
```

```bash
# Run dbt transformations
docker run --rm \
  --network pipeline-net \
  -e DB_HOST=postgres \
  -e DB_USER=beatrice \
  -e DB_PASSWORD=secret123 \
  dbt-pipeline \
  dbt run --select bank_customers+

# Run dbt tests
docker run --rm \
  --network pipeline-net \
  -e DB_HOST=postgres \
  dbt-pipeline \
  dbt test
```

---

## Pattern 5 — Full Data Stack

```yaml
# docker-compose.full-stack.yml
version: "3.8"

services:

  # Storage
  postgres:
    image: postgres:15
    container_name: stack-postgres
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./sql/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      retries: 5
    networks:
      - stack-net

  # Database UI
  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: beatrice@gmail.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - stack-net

  # ETL Pipeline
  pipeline:
    build: ./pipeline
    env_file: .env
    environment:
      DB_HOST: postgres
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - stack-net

  # REST API
  api:
    build: ./api
    env_file: .env
    environment:
      DB_HOST: postgres
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
    restart: unless-stopped
    networks:
      - stack-net

  # Orchestration
  airflow:
    image: apache/airflow:2.7.0
    environment:
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@postgres/${DB_NAME}
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__CORE__LOAD_EXAMPLES: "false"
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - stack-net

networks:
  stack-net:
    driver: bridge

volumes:
  pgdata:
```

```bash
# .env file
DB_USER=beatrice
DB_PASSWORD=secret123
DB_NAME=data_vault

# Start everything
docker compose -f docker-compose.full-stack.yml up -d

echo "Services running:"
echo "  PostgreSQL: localhost:5432"
echo "  pgAdmin:    http://localhost:5050"
echo "  API:        http://localhost:8000"
echo "  API Docs:   http://localhost:8000/docs"
echo "  Airflow:    http://localhost:8080"
```

---

## Makefile — One-Command Operations

```makefile
# Makefile — shortcuts for common Docker operations

.PHONY: up down build logs shell clean pipeline

# Start full stack
up:
	docker compose up -d
	@echo "Stack running!"
	@echo "API: http://localhost:8000"
	@echo "Airflow: http://localhost:8080"

# Stop everything
down:
	docker compose down

# Rebuild and restart
build:
	docker compose build --no-cache
	docker compose up -d

# View logs
logs:
	docker compose logs -f

# Shell into database
db:
	docker compose exec postgres psql -U beatrice -d data_vault

# Shell into API container
shell:
	docker compose exec api bash

# Run pipeline manually
pipeline:
	docker compose run --rm pipeline python main.py

# Remove everything including volumes
clean:
	docker compose down -v
	docker system prune -f

# Run dbt
dbt-run:
	docker compose run --rm pipeline dbt run

dbt-test:
	docker compose run --rm pipeline dbt test
```

```bash
# Now use simple commands:
make up         # Start stack
make down       # Stop stack
make pipeline   # Run ETL
make db         # Connect to database
make logs       # View logs
```

---

## Common Issues & Fixes

```bash
# Issue: Port already in use
# Fix: Change host port
ports:
  - "5433:5432"   # Use 5433 instead of 5432

# Issue: Container exits immediately
# Fix: Check logs
docker compose logs service-name

# Issue: Can't connect between containers
# Fix: Use service name not localhost
DB_HOST: postgres    # ✅ Not localhost or 127.0.0.1

# Issue: Volume permissions
# Fix: Set user in Dockerfile
RUN chown -R appuser:appuser /app/data
USER appuser

# Issue: Env variables not loading
# Fix: Check .env file is in same directory as docker-compose.yml
ls -la .env

# Issue: Build cache causing stale code
# Fix: Force rebuild
docker compose build --no-cache
```

---

## Previous | Next
← [[04 - Docker Compose]] | → [[06 - Docker for PostgreSQL]]
