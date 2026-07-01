---
title: Airflow Production Deployment
tags: [airflow, docker, production, deployment]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# 🚀 Airflow Production Deployment

> Running Airflow in production requires a robust setup: proper Docker Compose configuration, external PostgreSQL, CeleryExecutor for parallelism, health checks, and monitoring. This note covers everything to go from dev to production.

---

## Production Architecture

```
┌──────────────────────────────────────────────────────┐
│                 Production Airflow                   │
├──────────────┬────────────┬────────────┬─────────────┤
│  Webserver   │ Scheduler  │  Worker 1  │  Worker 2   │
│  (port 8080) │            │  (Celery)  │  (Celery)   │
├──────────────┴────────────┴────────────┴─────────────┤
│           Message Broker (Redis)                     │
├──────────────────────────────────────────────────────┤
│           Metadata DB (PostgreSQL)                   │
└──────────────────────────────────────────────────────┘
```

---

## Production Docker Compose

```yaml
# docker-compose.prod.yml
version: "3.8"

x-airflow-common: &airflow-common
  image: apache/airflow:2.9.0
  environment: &airflow-common-env
    AIRFLOW__CORE__EXECUTOR: CeleryExecutor
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres/${POSTGRES_DB}
    AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres/${POSTGRES_DB}
    AIRFLOW__CELERY__BROKER_URL: redis://redis:6379/0
    AIRFLOW__CORE__FERNET_KEY: ${AIRFLOW_FERNET_KEY}
    AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: "true"
    AIRFLOW__CORE__LOAD_EXAMPLES: "false"
    AIRFLOW__CORE__DEFAULT_TIMEZONE: Africa/Nairobi
    AIRFLOW__WEBSERVER__SECRET_KEY: ${AIRFLOW_SECRET_KEY}
    AIRFLOW__WEBSERVER__EXPOSE_CONFIG: "false"
    AIRFLOW__SMTP__SMTP_HOST: smtp.gmail.com
    AIRFLOW__SMTP__SMTP_PORT: 587
    AIRFLOW__SMTP__SMTP_USER: ${SMTP_USER}
    AIRFLOW__SMTP__SMTP_PASSWORD: ${SMTP_PASSWORD}
    AIRFLOW__SMTP__SMTP_MAIL_FROM: ${SMTP_USER}
    AIRFLOW__SMTP__SMTP_SSL: "false"
    AIRFLOW__SMTP__SMTP_STARTTLS: "true"
    AIRFLOW__LOGGING__REMOTE_LOGGING: "true"
    AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER: s3://beatrice-data-lake/airflow-logs/
    AIRFLOW__LOGGING__REMOTE_LOG_CONN_ID: aws_default
    # Connections
    AIRFLOW_CONN_POSTGRES_DATA_VAULT: postgresql://${DB_USER}:${DB_PASSWORD}@db-host:5432/data_vault
    AIRFLOW_CONN_SNOWFLAKE_DATA_VAULT: snowflake://${SNOW_USER}:${SNOW_PASSWORD}@${SNOW_ACCOUNT}/DATA_VAULT/SILVER?warehouse=ETL_WH
    # Variables
    AIRFLOW_VAR_DATA_PATH: /data/bank_marketing.csv
    AIRFLOW_VAR_BATCH_SIZE: "5000"
    AIRFLOW_VAR_NOTIFY_EMAIL: ${NOTIFY_EMAIL}
  volumes:
    - ${AIRFLOW_PROJ_DIR}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR}/plugins:/opt/airflow/plugins
    - ${AIRFLOW_PROJ_DIR}/data:/opt/airflow/data
    - ${AIRFLOW_PROJ_DIR}/dbt:/opt/dbt
  user: "${AIRFLOW_UID:-50000}:0"
  depends_on: &airflow-depends
    postgres:
      condition: service_healthy
    redis:
      condition: service_healthy

services:

  # ── Metadata Database ───────────────────────────────────
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "${POSTGRES_USER}"]
      interval: 10s
      retries: 5
      start_period: 5s
    restart: always

  # ── Message Broker ──────────────────────────────────────
  redis:
    image: redis:7-alpine
    expose:
      - 6379
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 30s
      retries: 50
    restart: always

  # ── Airflow Web Server ──────────────────────────────────
  airflow-webserver:
    <<: *airflow-common
    command: webserver
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always

  # ── Airflow Scheduler ────────────────────────────────────
  airflow-scheduler:
    <<: *airflow-common
    command: scheduler
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8974/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always

  # ── Celery Workers ───────────────────────────────────────
  airflow-worker:
    <<: *airflow-common
    command: celery worker
    healthcheck:
      test:
        - "CMD-SHELL"
        - 'celery --app airflow.providers.celery.executors.celery_executor.app inspect ping -d "celery@$${HOSTNAME}" || exit 1'
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    environment:
      <<: *airflow-common-env
      DUMB_INIT_SETSID: "0"
    restart: always
    deploy:
      replicas: 2          # Run 2 workers by default

  # ── Celery Flower (Worker Monitor) ───────────────────────
  flower:
    <<: *airflow-common
    command: celery flower
    profiles:
      - flower
    ports:
      - "5555:5555"
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:5555/"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always

  # ── Airflow Init ─────────────────────────────────────────
  airflow-init:
    <<: *airflow-common
    entrypoint: /bin/bash
    command:
      - -c
      - |
        mkdir -p /sources/logs /sources/dags /sources/plugins
        chown -R "${AIRFLOW_UID}:0" /sources/{logs,dags,plugins}
        exec /entrypoint airflow version
    environment:
      <<: *airflow-common-env
      _AIRFLOW_DB_MIGRATE: "true"
      _AIRFLOW_WWW_USER_CREATE: "true"
      _AIRFLOW_WWW_USER_USERNAME: ${_AIRFLOW_WWW_USER_USERNAME:-airflow}
      _AIRFLOW_WWW_USER_PASSWORD: ${_AIRFLOW_WWW_USER_PASSWORD:-airflow}
    user: "0:0"
    volumes:
      - ${AIRFLOW_PROJ_DIR}:/sources

volumes:
  postgres_data:
```

---

## Environment Variables (.env)

```bash
# .env — never commit this!

# PostgreSQL (Airflow metadata DB)
POSTGRES_USER=airflow
POSTGRES_PASSWORD=secure_airflow_password_123
POSTGRES_DB=airflow

# Airflow security
AIRFLOW_UID=50000
AIRFLOW_FERNET_KEY=81HqDtbfqnzXso2e9bRIQzdiXSiJSSkXjA5MpSNBFss=
AIRFLOW_SECRET_KEY=a25mQ1FHTUh3MnFRSk5KMEIyVVU2YmN0VGRyYTVXY08=

# SMTP (Gmail)
SMTP_USER=beatiewakarima1@gmail.com
SMTP_PASSWORD=your_app_password

# Data platform connections
DB_USER=beatrice
DB_PASSWORD=data_vault_password
SNOW_USER=beatrice
SNOW_PASSWORD=snowflake_password
SNOW_ACCOUNT=xy12345.eu-west-1

# Notifications
NOTIFY_EMAIL=beatiewakarima1@gmail.com

# Project directory
AIRFLOW_PROJ_DIR=.
```

---

## Custom Airflow Image (With Dependencies)

```dockerfile
# Dockerfile.airflow
FROM apache/airflow:2.9.0

USER root

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Python packages
COPY requirements-airflow.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt
```

```text
# requirements-airflow.txt
apache-airflow-providers-postgres==5.10.0
apache-airflow-providers-snowflake==5.3.0
apache-airflow-providers-amazon==8.18.0
apache-airflow-providers-celery==3.6.0
apache-airflow-providers-redis==3.7.0
apache-airflow-providers-http==4.10.0
apache-airflow-providers-common-sql==1.12.0

pandas==2.2.0
sqlalchemy==1.4.52
psycopg2-binary==2.9.9
snowflake-connector-python==3.6.0
snowflake-sqlalchemy==1.5.1
requests==2.31.0
python-dotenv==1.0.0
dbt-postgres==1.7.0
dbt-snowflake==1.7.0
```

---

## Starting the Stack

```bash
# Generate Fernet key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Initialise
docker compose -f docker-compose.prod.yml up airflow-init

# Start everything
docker compose -f docker-compose.prod.yml up -d

# Check health
docker compose -f docker-compose.prod.yml ps

# Scale workers
docker compose -f docker-compose.prod.yml up -d --scale airflow-worker=4

# View logs
docker compose -f docker-compose.prod.yml logs -f airflow-scheduler
docker compose -f docker-compose.prod.yml logs -f airflow-worker

# Restart a service
docker compose -f docker-compose.prod.yml restart airflow-scheduler
```

---

## Makefile for Airflow Operations

```makefile
# Makefile

.PHONY: up down init restart logs trigger test

# Start full stack
up:
	docker compose -f docker-compose.prod.yml up -d
	@echo "Airflow running at: http://localhost:8080"

# Stop
down:
	docker compose -f docker-compose.prod.yml down

# Initialise DB and admin user
init:
	docker compose -f docker-compose.prod.yml up airflow-init

# Restart scheduler (after DAG changes)
restart-scheduler:
	docker compose -f docker-compose.prod.yml restart airflow-scheduler

# View scheduler logs
logs:
	docker compose -f docker-compose.prod.yml logs -f airflow-scheduler airflow-worker

# Trigger a DAG manually
trigger:
	docker compose -f docker-compose.prod.yml exec airflow-scheduler \
		airflow dags trigger bank_marketing_taskflow

# Test a specific task
test-task:
	docker compose -f docker-compose.prod.yml exec airflow-scheduler \
		airflow tasks test bank_marketing_taskflow extract_source_data 2026-05-20

# List DAGs
list-dags:
	docker compose -f docker-compose.prod.yml exec airflow-scheduler \
		airflow dags list

# Backfill missed runs
backfill:
	docker compose -f docker-compose.prod.yml exec airflow-scheduler \
		airflow dags backfill bank_marketing_taskflow \
		--start-date 2026-05-01 --end-date 2026-05-20

# Scale workers
scale-workers:
	docker compose -f docker-compose.prod.yml up -d --scale airflow-worker=4
```

---

## Health Monitoring Queries

```sql
-- Check failed DAG runs in last 7 days
SELECT
    dag_id,
    run_id,
    state,
    execution_date,
    start_date,
    end_date,
    EXTRACT(EPOCH FROM (end_date - start_date)) AS duration_secs
FROM dag_run
WHERE state = 'failed'
  AND execution_date >= NOW() - INTERVAL '7 days'
ORDER BY execution_date DESC;

-- Failed tasks in last 24h
SELECT
    dag_id,
    task_id,
    run_id,
    state,
    start_date,
    end_date,
    try_number
FROM task_instance
WHERE state = 'failed'
  AND start_date >= NOW() - INTERVAL '24 hours'
ORDER BY start_date DESC;

-- Average run duration per DAG
SELECT
    dag_id,
    COUNT(*) AS total_runs,
    COUNT(*) FILTER (WHERE state = 'success') AS successes,
    COUNT(*) FILTER (WHERE state = 'failed') AS failures,
    ROUND(AVG(EXTRACT(EPOCH FROM (end_date - start_date))) / 60, 1) AS avg_minutes
FROM dag_run
WHERE execution_date >= NOW() - INTERVAL '30 days'
  AND state IN ('success', 'failed')
GROUP BY dag_id
ORDER BY avg_minutes DESC;

-- Long-running tasks
SELECT
    ti.dag_id,
    ti.task_id,
    ti.execution_date,
    EXTRACT(EPOCH FROM (NOW() - ti.start_date)) / 60 AS running_minutes
FROM task_instance ti
WHERE ti.state = 'running'
  AND ti.start_date < NOW() - INTERVAL '1 hour'
ORDER BY running_minutes DESC;
```

---

## Quick Reference

```bash
# Start/stop
docker compose up -d
docker compose down
docker compose ps

# Airflow CLI inside container
docker compose exec airflow-scheduler airflow ...

# DAG management
airflow dags list
airflow dags trigger dag_id
airflow dags pause dag_id
airflow dags unpause dag_id
airflow dags delete dag_id

# Task management
airflow tasks list dag_id
airflow tasks test dag_id task_id execution_date
airflow tasks clear dag_id --start-date ... --end-date ...

# Backfill
airflow dags backfill dag_id --start-date YYYY-MM-DD --end-date YYYY-MM-DD

# Connections
airflow connections list
airflow connections add conn_id --conn-uri uri
airflow connections delete conn_id

# Variables
airflow variables list
airflow variables set key value
airflow variables get key
airflow variables delete key
```

---

## Previous | Next
← [[04 - Airflow Connections Variables and XCom]] | → [[06 - Airflow Interview Cheat Sheet]]
