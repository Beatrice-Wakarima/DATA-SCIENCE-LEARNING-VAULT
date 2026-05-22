---
title: End-to-End Pipeline Project — Bank Marketing
tags: [data-engineering, project, pipeline, bank-marketing]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# 🚀 End-to-End Pipeline Project — Bank Marketing

> This note builds a complete, production-grade data pipeline for the Bank Marketing dataset using everything from the series: Python + PostgreSQL + dbt + Airflow + Docker. This is the flagship project for your portfolio.

---

## Project Architecture

```
┌──────────────────────────────────────────────────────────────┐
│              Bank Marketing Data Platform                    │
├────────────┬───────────────┬──────────────┬─────────────────┤
│  INGEST    │   STORE       │  TRANSFORM   │     SERVE       │
│            │               │              │                 │
│  Python    │  PostgreSQL   │    dbt       │  Power BI       │
│  CSV/API   │  Bronze Layer │  Silver Layer│  FastAPI        │
│  Airflow   │  Silver Layer │  Gold Layer  │  Quartz Site    │
│  Docker    │  Gold Layer   │  Star Schema │                 │
└────────────┴───────────────┴──────────────┴─────────────────┘
```

---

## Project Structure

```
bank_marketing_platform/
│
├── 📁 pipeline/                    ← Python ETL
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   └── src/
│       ├── extract.py
│       ├── transform.py
│       ├── load.py
│       ├── quality.py
│       └── utils.py
│
├── 📁 dbt/                         ← dbt transformations
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── packages.yml
│   └── models/
│       ├── staging/
│       │   ├── stg_bank_marketing.sql
│       │   └── _sources.yml
│       ├── intermediate/
│       │   └── int_customer_segments.sql
│       └── marts/
│           ├── dim_customers.sql
│           ├── fct_campaign_contacts.sql
│           └── fct_campaign_performance.sql
│
├── 📁 dags/                        ← Airflow DAGs
│   └── bank_marketing_pipeline.py
│
├── 📁 sql/                         ← Database setup
│   └── init.sql
│
├── 📁 api/                         ← FastAPI service
│   ├── Dockerfile
│   └── main.py
│
├── 📁 data/                        ← Raw data
│   └── bank_marketing.csv
│
├── docker-compose.yml
├── .env
└── Makefile
```

---

## Step 1 — Database Initialisation

```sql
-- sql/init.sql
-- Run automatically on first Docker start

-- Create schemas
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE SCHEMA IF NOT EXISTS staging;

-- Bronze: raw data
CREATE TABLE IF NOT EXISTS bronze.raw_bank_marketing (
    id          BIGSERIAL PRIMARY KEY,
    age         TEXT,
    job         TEXT,
    marital     TEXT,
    education   TEXT,
    default_    TEXT,
    balance     TEXT,
    housing     TEXT,
    loan        TEXT,
    contact     TEXT,
    day         TEXT,
    month       TEXT,
    duration    TEXT,
    campaign    TEXT,
    pdays       TEXT,
    previous    TEXT,
    poutcome    TEXT,
    y           TEXT,
    _source_file TEXT,
    _loaded_at  TIMESTAMP DEFAULT NOW(),
    _run_date   DATE
);

-- Pipeline audit log
CREATE TABLE IF NOT EXISTS pipeline_audit (
    id              BIGSERIAL PRIMARY KEY,
    run_date        DATE,
    pipeline_name   VARCHAR(100),
    stage           VARCHAR(50),
    rows_in         INTEGER DEFAULT 0,
    rows_out        INTEGER DEFAULT 0,
    status          VARCHAR(20) DEFAULT 'running',
    started_at      TIMESTAMP DEFAULT NOW(),
    completed_at    TIMESTAMP,
    error_message   TEXT
);

-- Grant permissions
GRANT ALL ON ALL TABLES IN SCHEMA bronze TO beatrice;
GRANT ALL ON ALL TABLES IN SCHEMA silver TO beatrice;
GRANT ALL ON ALL TABLES IN SCHEMA gold TO beatrice;
```

---

## Step 2 — Python ETL Pipeline

```python
# pipeline/main.py
"""
Bank Marketing ETL Pipeline
Implements Medallion Architecture: CSV → Bronze → Silver (via dbt)
"""
import pandas as pd
import logging
import os
from datetime import date
from sqlalchemy import create_engine, text
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("bank_pipeline")


def get_engine():
    url = (
        f"postgresql://{os.getenv('DB_USER', 'beatrice')}:"
        f"{os.getenv('DB_PASSWORD', 'secret123')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME', 'data_vault')}"
    )
    return create_engine(url, pool_pre_ping=True)


def extract(filepath: str) -> pd.DataFrame:
    """Extract raw data from CSV"""
    logger.info(f"📥 Extracting: {filepath}")
    df = pd.read_csv(filepath, sep=";")
    logger.info(f"   Extracted {len(df):,} rows, {len(df.columns)} columns")
    return df


def validate(df: pd.DataFrame) -> pd.DataFrame:
    """Validate raw data quality"""
    logger.info("🔍 Validating source data...")

    checks = {
        "has_rows": len(df) > 0,
        "required_cols": all(c in df.columns
            for c in ["age", "job", "balance", "y"]),
        "no_empty_df": not df.empty,
        "target_values": set(df["y"].unique()).issubset({"yes", "no"}),
    }

    failed = [k for k, v in checks.items() if not v]
    if failed:
        raise ValueError(f"Validation failed: {failed}")

    # Log stats
    sub_rate = (df["y"] == "yes").mean() * 100
    logger.info(f"   ✅ {len(df):,} rows validated")
    logger.info(f"   Subscription rate: {sub_rate:.1f}%")
    logger.info(f"   Age range: {df['age'].min()}–{df['age'].max()}")
    logger.info(f"   Balance range: {df['balance'].min():,.0f}–"
               f"{df['balance'].max():,.0f}")
    return df


def load_bronze(df: pd.DataFrame, engine,
                run_date: str) -> int:
    """Load raw data to Bronze layer"""
    logger.info("🟤 Loading to Bronze...")

    # Add metadata
    df = df.copy()
    df["_source_file"] = os.getenv("DATA_PATH", "bank_marketing.csv")
    df["_loaded_at"] = pd.Timestamp.now()
    df["_run_date"] = run_date
    df.columns = [c.replace(".", "_") for c in df.columns]

    # Idempotent: delete then reload
    with engine.connect() as conn:
        conn.execute(text(
            "DELETE FROM bronze.raw_bank_marketing "
            "WHERE _run_date = :run_date"
        ), {"run_date": run_date})
        conn.commit()

    df.to_sql(
        "raw_bank_marketing", engine,
        schema="bronze", if_exists="append",
        index=False, chunksize=5000
    )

    logger.info(f"   ✅ {len(df):,} rows in bronze.raw_bank_marketing")
    return len(df)


def log_audit(engine, stage: str, rows_in: int,
              rows_out: int, status: str,
              error: str = None, run_date: str = None):
    """Log pipeline execution to audit table"""
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO pipeline_audit
                (run_date, pipeline_name, stage,
                 rows_in, rows_out, status, completed_at, error_message)
            VALUES
                (:date, 'bank_marketing', :stage,
                 :rows_in, :rows_out, :status, NOW(), :error)
        """), {
            "date": run_date or str(date.today()),
            "stage": stage,
            "rows_in": rows_in,
            "rows_out": rows_out,
            "status": status,
            "error": error
        })
        conn.commit()


def run_pipeline(data_path: str = None,
                 run_date: str = None) -> dict:
    """Run complete ETL pipeline"""

    run_date = run_date or str(date.today())
    data_path = data_path or os.getenv("DATA_PATH", "data/bank_marketing.csv")

    logger.info("=" * 60)
    logger.info(f"🚀 Bank Marketing Pipeline — {run_date}")
    logger.info("=" * 60)

    engine = get_engine()
    stats = {"run_date": run_date, "status": "failed"}

    try:
        # Extract
        df = extract(data_path)
        log_audit(engine, "extract", 0, len(df), "success", run_date=run_date)

        # Validate
        df = validate(df)
        log_audit(engine, "validate", len(df), len(df), "success",
                  run_date=run_date)

        # Load Bronze
        rows_loaded = load_bronze(df, engine, run_date)
        log_audit(engine, "load_bronze", len(df), rows_loaded, "success",
                  run_date=run_date)

        stats.update({
            "status": "success",
            "rows_extracted": len(df),
            "rows_loaded": rows_loaded
        })

        logger.info("=" * 60)
        logger.info(f"✅ Pipeline complete! {rows_loaded:,} rows in Bronze")
        logger.info("   Run dbt next: dbt build --target prod")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"❌ Pipeline failed: {e}")
        log_audit(engine, "pipeline", 0, 0, "failed",
                  error=str(e), run_date=run_date)
        raise

    return stats


if __name__ == "__main__":
    result = run_pipeline()
    print(result)
```

---

## Step 3 — dbt Models

```sql
-- dbt/models/staging/stg_bank_marketing.sql
{{ config(materialized='view', schema='staging') }}

SELECT
    CAST(age AS INTEGER)                                    AS age,
    TRIM(LOWER(job))                                        AS job,
    TRIM(LOWER(marital))                                    AS marital,
    TRIM(LOWER(education))                                  AS education,
    TRIM(LOWER(contact))                                    AS contact,
    TRIM(LOWER(month))                                      AS month,
    CAST(balance AS DECIMAL(12,2))                          AS balance,
    CAST(duration AS INTEGER)                               AS call_duration_secs,
    CAST(campaign AS INTEGER)                               AS campaign_contacts,
    CASE WHEN LOWER(TRIM(y)) = 'yes' THEN TRUE ELSE FALSE END AS subscribed,
    CASE
        WHEN CAST(balance AS DECIMAL) > 10000  THEN 'high'
        WHEN CAST(balance AS DECIMAL) > 1000   THEN 'medium'
        WHEN CAST(balance AS DECIMAL) >= 0     THEN 'low'
        ELSE 'negative'
    END                                                     AS balance_segment,
    CASE
        WHEN CAST(age AS INTEGER) < 30 THEN 'young'
        WHEN CAST(age AS INTEGER) < 50 THEN 'middle'
        ELSE 'senior'
    END                                                     AS age_segment,
    _run_date,
    _loaded_at
FROM {{ source('bronze', 'raw_bank_marketing') }}
WHERE age IS NOT NULL
  AND CAST(age AS INTEGER) BETWEEN 18 AND 95
```

```sql
-- dbt/models/marts/fct_campaign_performance.sql
{{ config(materialized='table', schema='gold') }}

SELECT
    job,
    education,
    marital,
    balance_segment,
    age_segment,
    contact,
    month,
    COUNT(*)                                            AS total_contacts,
    SUM(CASE WHEN subscribed THEN 1 ELSE 0 END)        AS subscriptions,
    ROUND(
        100.0 * SUM(CASE WHEN subscribed THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 2
    )                                                   AS conversion_rate,
    ROUND(AVG(balance), 2)                             AS avg_balance,
    ROUND(AVG(call_duration_secs), 0)                  AS avg_call_duration,
    NOW()                                               AS refreshed_at
FROM {{ ref('stg_bank_marketing') }}
GROUP BY 1, 2, 3, 4, 5, 6, 7
```

---

## Step 4 — Docker Compose (Full Stack)

```yaml
# docker-compose.yml
version: "3.8"

services:
  postgres:
    image: postgres:15
    container_name: bank-postgres
    env_file: .env
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./sql/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      retries: 5

  pipeline:
    build: ./pipeline
    container_name: bank-pipeline
    env_file: .env
    environment:
      DB_HOST: postgres
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      postgres:
        condition: service_healthy

  dbt:
    build:
      context: ./dbt
      dockerfile: Dockerfile.dbt
    container_name: bank-dbt
    env_file: .env
    environment:
      DB_HOST: postgres
    depends_on:
      postgres:
        condition: service_healthy

  airflow:
    image: apache/airflow:2.7.0
    container_name: bank-airflow
    env_file: .env
    environment:
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: >
        postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@postgres/${DB_NAME}
      AIRFLOW__CORE__LOAD_EXAMPLES: "false"
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
      - ./dbt:/opt/dbt
    depends_on:
      postgres:
        condition: service_healthy
    command: >
      bash -c "airflow db init &&
               airflow users create --username admin --password admin
                 --firstname Beatrice --lastname Builds
                 --role Admin --email beatiewakarima1@gmail.com &&
               airflow webserver"

  api:
    build: ./api
    container_name: bank-api
    env_file: .env
    environment:
      DB_HOST: postgres
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  pgdata:
```

---

## Step 5 — Makefile (One Command Operations)

```makefile
# Makefile

.PHONY: up down pipeline dbt test api logs clean

# Start full stack
up:
	docker compose up -d
	@echo "Stack running:"
	@echo "  PostgreSQL: localhost:5432"
	@echo "  Airflow:    http://localhost:8080"
	@echo "  API:        http://localhost:8000"
	@echo "  API Docs:   http://localhost:8000/docs"

# Run ETL pipeline
pipeline:
	docker compose run --rm pipeline python main.py

# Run dbt transformations
dbt:
	docker compose run --rm dbt dbt build --target prod

# Run dbt tests only
dbt-test:
	docker compose run --rm dbt dbt test --target prod

# Run full pipeline (extract → bronze → dbt → gold)
run-all:
	make pipeline
	make dbt
	@echo "✅ Full pipeline complete!"

# View logs
logs:
	docker compose logs -f pipeline dbt

# Connect to database
db:
	docker compose exec postgres psql -U beatrice -d data_vault

# Stop everything
down:
	docker compose down

# Clean everything (WARNING: deletes data!)
clean:
	docker compose down -v
	docker system prune -f
```

```bash
# Run the complete pipeline
make up         # Start stack
make run-all    # Extract → Bronze → Silver → Gold
make logs       # View progress
make db         # Check data in PostgreSQL
```

---

## Quick Reference — Pipeline Stages

```
Stage           Command                 Output
──────────────────────────────────────────────────────
1. Start stack  make up                 All containers running
2. Extract      make pipeline           bronze.raw_bank_marketing
3. Transform    make dbt                staging.*, silver.*, gold.*
4. Validate     make dbt-test           All quality checks pass
5. Serve        http://localhost:8000   API with customer data
6. Monitor      http://localhost:8080   Airflow DAG runs
```

---

## Previous | Next
← [[07 - Streaming with Kafka]] | → [[09 - Monitoring and Alerting]]
