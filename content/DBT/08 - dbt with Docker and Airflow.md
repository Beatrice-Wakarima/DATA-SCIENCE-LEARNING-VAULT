---
title: dbt with Docker and Airflow
tags: [dbt, docker, airflow, data-engineering, production]
created: 2026-05-20
up:: [[DBT MOC]]
---

# 🚀 dbt with Docker & Airflow

> Running dbt in Docker ensures reproducible environments. Orchestrating dbt with Airflow schedules, monitors, and chains dbt runs with the rest of your data pipeline. This is production-grade dbt.

---

## dbt in Docker

```dockerfile
# Dockerfile.dbt
FROM ghcr.io/dbt-labs/dbt-postgres:1.7.0

WORKDIR /usr/app/dbt

# Copy dbt project
COPY . .

# Install additional packages
RUN dbt deps

# Default command
CMD ["dbt", "run"]
```

---

## Docker Compose — dbt + PostgreSQL

```yaml
# docker-compose.yml
version: "3.8"

services:

  postgres:
    image: postgres:15
    container_name: dbt-postgres
    environment:
      POSTGRES_USER: beatrice
      POSTGRES_PASSWORD: secret123
      POSTGRES_DB: data_vault
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./sql/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U beatrice"]
      interval: 10s
      retries: 5

  dbt:
    build:
      context: .
      dockerfile: Dockerfile.dbt
    container_name: dbt-runner
    volumes:
      - ./dbt_project:/usr/app/dbt        # Mount project for dev
      - ./logs/dbt:/usr/app/dbt/logs
    environment:
      DB_HOST: postgres
      DB_USER: beatrice
      DB_PASSWORD: secret123
      DB_NAME: data_vault
      DB_PORT: 5432
    depends_on:
      postgres:
        condition: service_healthy
    profiles:
      - dbt                               # Only starts with: docker compose --profile dbt up

volumes:
  pgdata:
```

---

## profiles.yml for Docker

```yaml
# ~/.dbt/profiles.yml OR dbt_project/profiles.yml
bank_marketing:
  target: dev
  outputs:
    dev:
      type: postgres
      host: "{{ env_var('DB_HOST', 'localhost') }}"
      user: "{{ env_var('DB_USER', 'beatrice') }}"
      password: "{{ env_var('DB_PASSWORD') }}"
      port: "{{ env_var('DB_PORT', '5432') | int }}"
      dbname: "{{ env_var('DB_NAME', 'data_vault') }}"
      schema: dbt_dev
      threads: 4
    
    prod:
      type: postgres
      host: "{{ env_var('PROD_DB_HOST') }}"
      user: "{{ env_var('PROD_DB_USER') }}"
      password: "{{ env_var('PROD_DB_PASSWORD') }}"
      port: 5432
      dbname: "{{ env_var('PROD_DB_NAME') }}"
      schema: dbt_prod
      threads: 8
```

---

## Running dbt Commands in Docker

```bash
# Run all models
docker compose run --rm dbt dbt run

# Run with full refresh
docker compose run --rm dbt dbt run --full-refresh

# Run specific models
docker compose run --rm dbt dbt run --select staging

# Run tests
docker compose run --rm dbt dbt test

# Build (run + test)
docker compose run --rm dbt dbt build

# Generate docs
docker compose run --rm dbt dbt docs generate

# Snapshots
docker compose run --rm dbt dbt snapshot

# Debug connection
docker compose run --rm dbt dbt debug

# Check source freshness
docker compose run --rm dbt dbt source freshness

# Run against production
docker compose run --rm \
  -e DB_HOST=${PROD_DB_HOST} \
  -e DB_PASSWORD=${PROD_DB_PASSWORD} \
  dbt dbt run --target prod
```

---

## Orchestrating dbt with Airflow

### Simple Bash Operator

```python
# dags/dbt_pipeline.py
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "beatrice",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["beatiewakarima1@gmail.com"]
}

with DAG(
    dag_id="dbt_bank_marketing",
    default_args=default_args,
    schedule_interval="0 6 * * 1-5",   # Weekdays at 6 AM
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["dbt", "bank", "daily"]
) as dag:

    # Debug connection
    dbt_debug = BashOperator(
        task_id="dbt_debug",
        bash_command="cd /opt/dbt && dbt debug --target prod"
    )

    # Check source freshness
    dbt_source_freshness = BashOperator(
        task_id="dbt_source_freshness",
        bash_command="cd /opt/dbt && dbt source freshness --target prod"
    )

    # Run staging models
    dbt_staging = BashOperator(
        task_id="dbt_run_staging",
        bash_command="cd /opt/dbt && dbt run --select staging --target prod"
    )

    # Test staging
    dbt_test_staging = BashOperator(
        task_id="dbt_test_staging",
        bash_command="cd /opt/dbt && dbt test --select staging --target prod"
    )

    # Run snapshots
    dbt_snapshots = BashOperator(
        task_id="dbt_snapshots",
        bash_command="cd /opt/dbt && dbt snapshot --target prod"
    )

    # Run intermediate + marts
    dbt_marts = BashOperator(
        task_id="dbt_run_marts",
        bash_command="cd /opt/dbt && dbt run --select marts --target prod"
    )

    # Test marts
    dbt_test_marts = BashOperator(
        task_id="dbt_test_marts",
        bash_command="cd /opt/dbt && dbt test --select marts --target prod"
    )

    # Generate docs
    dbt_docs = BashOperator(
        task_id="dbt_generate_docs",
        bash_command="cd /opt/dbt && dbt docs generate --target prod"
    )

    # Pipeline order
    dbt_debug >> dbt_source_freshness >> dbt_staging >> dbt_test_staging
    dbt_test_staging >> dbt_snapshots >> dbt_marts >> dbt_test_marts >> dbt_docs
```

---

### Using astronomer-cosmos (Best Practice)

```bash
# Install cosmos — Airflow-native dbt integration
pip install astronomer-cosmos
```

```python
# dags/dbt_cosmos_pipeline.py
from airflow import DAG
from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
from datetime import datetime

# Configure dbt connection
profile_config = ProfileConfig(
    profile_name="bank_marketing",
    target_name="prod",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="postgres_data_vault",      # Airflow connection
        profile_args={"schema": "dbt_prod"}
    )
)

# Create DAG automatically from dbt project!
dbt_dag = DbtDag(
    dag_id="dbt_bank_marketing_cosmos",
    project_config=ProjectConfig(
        dbt_project_path="/opt/dbt/bank_marketing",
    ),
    profile_config=profile_config,
    execution_config=ExecutionConfig(
        dbt_executable_path="/home/astro/.venv/dbt/bin/dbt",
    ),
    schedule_interval="0 6 * * 1-5",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["dbt", "cosmos"]
)
```

---

## Full Production Stack

```yaml
# docker-compose.prod.yml
version: "3.8"

services:

  postgres:
    image: postgres:15
    env_file: .env
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./sql:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      retries: 5
    networks:
      - data-network

  # ETL Pipeline (Python)
  pipeline:
    build: ./pipeline
    env_file: .env
    volumes:
      - ./data:/app/data
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - data-network

  # dbt Transformations
  dbt:
    build:
      context: ./dbt
      dockerfile: Dockerfile.dbt
    env_file: .env
    environment:
      DB_HOST: postgres
    volumes:
      - ./dbt:/usr/app/dbt
      - ./logs/dbt:/usr/app/dbt/logs
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - data-network

  # Airflow Scheduler
  airflow-scheduler:
    image: apache/airflow:2.7.0
    env_file: .env
    volumes:
      - ./dags:/opt/airflow/dags
      - ./dbt:/opt/dbt
      - ./logs/airflow:/opt/airflow/logs
    environment:
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@postgres/${DB_NAME}
    depends_on:
      postgres:
        condition: service_healthy
    command: scheduler
    networks:
      - data-network

  # Airflow Web UI
  airflow-webserver:
    image: apache/airflow:2.7.0
    env_file: .env
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs/airflow:/opt/airflow/logs
    ports:
      - "8080:8080"
    depends_on:
      postgres:
        condition: service_healthy
    command: webserver
    networks:
      - data-network

networks:
  data-network:

volumes:
  pgdata:
```

---

## CI/CD Pipeline for dbt

```yaml
# .github/workflows/dbt_ci.yml
name: dbt CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    paths:
      - 'dbt/**'

jobs:
  dbt-ci:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dbt
        run: pip install dbt-postgres

      - name: Install dbt packages
        run: cd dbt && dbt deps

      - name: dbt debug
        run: cd dbt && dbt debug
        env:
          DB_HOST: localhost
          DB_USER: test_user
          DB_PASSWORD: test_pass
          DB_NAME: test_db

      - name: dbt build (run + test)
        run: cd dbt && dbt build
        env:
          DB_HOST: localhost
          DB_USER: test_user
          DB_PASSWORD: test_pass
          DB_NAME: test_db

      - name: dbt generate docs
        run: cd dbt && dbt docs generate
```

---

## Makefile for dbt Operations

```makefile
# Makefile

DBT=docker compose run --rm dbt dbt

# Development
dev-run:
	$(DBT) run --target dev

dev-test:
	$(DBT) test --target dev

dev-build:
	$(DBT) build --target dev

# Production
prod-run:
	$(DBT) run --target prod

prod-test:
	$(DBT) test --target prod

prod-build:
	$(DBT) build --target prod

# Specific layers
staging:
	$(DBT) build --select staging --target prod

marts:
	$(DBT) build --select marts --target prod

# Snapshots
snapshot:
	$(DBT) snapshot --target prod

# Documentation
docs:
	$(DBT) docs generate --target prod && $(DBT) docs serve

# Full refresh
full-refresh:
	$(DBT) build --full-refresh --target prod

# Debug
debug:
	$(DBT) debug
	$(DBT) source freshness
```

```bash
make staging      # Run + test staging layer
make marts        # Run + test marts layer
make snapshot     # Run snapshots
make docs         # Generate and serve docs
```

---

## Quick Reference

```bash
# Docker commands
docker compose run --rm dbt dbt run
docker compose run --rm dbt dbt test
docker compose run --rm dbt dbt build
docker compose run --rm dbt dbt snapshot
docker compose run --rm dbt dbt docs generate

# Target switching
dbt run --target dev
dbt run --target prod

# Selective runs
dbt build --select staging
dbt build --select +fct_revenue    # Model + all upstream
dbt build --select fct_revenue+    # Model + all downstream

# Full refresh
dbt build --full-refresh

# CI pattern
dbt deps && dbt debug && dbt build
```

---

## Previous | Next
← [[07 - dbt Incremental Models]] | → [[DBT MOC 1]]
