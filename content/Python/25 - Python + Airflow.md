---
title: Python + Airflow (Deep Dive)
tags: [python, airflow, data-engineering, orchestration]
created: 2026-05-20
up:: [[Python MOC]]
---

# 🌬️ Python + Airflow (Deep Dive)

> Apache Airflow is the industry standard for orchestrating data pipelines. It schedules, monitors, and manages complex workflows as DAGs. Used at Airbnb, Twitter, LinkedIn, and most data-mature companies.

---

## Core Concepts

```
DAG         = Directed Acyclic Graph — your pipeline blueprint
Task        = A single unit of work (extract, transform, load)
Operator    = Template for a task type (Python, Bash, SQL, etc.)
Sensor      = Waits for a condition before proceeding
Hook        = Connection to external systems (Postgres, S3, etc.)
Schedule    = When the DAG runs (cron expression)
Run         = One execution of a DAG
XCom        = Cross-communication between tasks
```

---

## Installation with Docker (Recommended)

```bash
# Download Airflow docker-compose
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'

# Create required directories
mkdir -p ./dags ./logs ./plugins ./config

# Start Airflow
docker compose up airflow-init
docker compose up -d

# Access UI: http://localhost:8080
# Username: airflow | Password: airflow
```

---

## Your First DAG

```python
# dags/first_pipeline.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default settings for all tasks
default_args = {
    "owner": "beatrice",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "email": ["beatiewakarima1@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5)
}

# Define DAG
with DAG(
    dag_id="first_pipeline",
    default_args=default_args,
    description="My first Airflow pipeline",
    schedule_interval="0 6 * * *",      # Daily at 6 AM
    catchup=False,                       # Don't backfill missed runs
    tags=["beginner", "demo"]
) as dag:
    
    def extract():
        print("📥 Extracting data...")
        return {"rows": 1000, "source": "bank_marketing.csv"}
    
    def transform():
        print("🔄 Transforming data...")
        return {"rows_clean": 950}
    
    def load():
        print("📤 Loading to database...")
    
    # Define tasks
    task_extract = PythonOperator(
        task_id="extract",
        python_callable=extract
    )
    
    task_transform = PythonOperator(
        task_id="transform",
        python_callable=transform
    )
    
    task_load = PythonOperator(
        task_id="load",
        python_callable=load
    )
    
    task_notify = BashOperator(
        task_id="notify",
        bash_command='echo "Pipeline complete at $(date)"'
    )
    
    # Set task order (dependencies)
    task_extract >> task_transform >> task_load >> task_notify
```

---

## Task Dependencies — Setting Order

```python
# Linear chain
t1 >> t2 >> t3 >> t4

# Parallel tasks
t1 >> [t2, t3] >> t4      # t2 and t3 run in parallel after t1

# Fan out then merge
extract >> [transform_sales, transform_customers, transform_products] >> load

# Complex dependencies
start >> check_data
check_data >> [process_new, process_updates]
process_new >> merge
process_updates >> merge
merge >> validate >> send_report

# Set upstream/downstream explicitly
t2.set_upstream(t1)
t3.set_downstream(t4)
```

---

## XCom — Passing Data Between Tasks

```python
from airflow.operators.python import PythonOperator

def extract(**context):
    """Extract and push data to XCom"""
    data = {"rows": 45211, "source": "bank_marketing"}
    
    # Push to XCom
    context["ti"].xcom_push(key="extract_stats", value=data)
    return data      # Return value is also automatically pushed

def transform(**context):
    """Pull data from previous task"""
    # Pull from XCom
    stats = context["ti"].xcom_pull(task_ids="extract", key="extract_stats")
    print(f"Processing {stats['rows']:,} rows from {stats['source']}")
    
    clean_rows = stats["rows"] - 261     # Remove invalid
    context["ti"].xcom_push(key="transform_stats", value={"clean_rows": clean_rows})

def load(**context):
    stats = context["ti"].xcom_pull(task_ids="transform", key="transform_stats")
    print(f"Loading {stats['clean_rows']:,} clean rows")

with DAG("xcom_demo", start_date=datetime(2026,1,1), schedule_interval="@daily") as dag:
    
    t1 = PythonOperator(task_id="extract", python_callable=extract)
    t2 = PythonOperator(task_id="transform", python_callable=transform)
    t3 = PythonOperator(task_id="load", python_callable=load)
    
    t1 >> t2 >> t3
```

---

## Sensors — Wait for Conditions

```python
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.time_delta import TimeDeltaSensor
from airflow.operators.python import PythonOperator
from datetime import timedelta

with DAG("sensor_demo", start_date=datetime(2026,1,1),
         schedule_interval="0 7 * * *") as dag:
    
    # Wait for file to exist before processing
    wait_for_file = FileSensor(
        task_id="wait_for_data_file",
        filepath="/data/raw/daily_sales_{{ ds }}.csv",
        poke_interval=60,       # Check every 60 seconds
        timeout=3600,           # Fail after 1 hour
        mode="reschedule"       # Release worker while waiting
    )
    
    process_file = PythonOperator(
        task_id="process_file",
        python_callable=lambda: print("File found! Processing...")
    )
    
    wait_for_file >> process_file
```

---

## Hooks — Connect to External Systems

```python
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def query_database(**context):
    """Use PostgresHook to query database"""
    # Connection configured in Airflow UI → Admin → Connections
    hook = PostgresHook(postgres_conn_id="my_postgres_conn")
    
    # Get DataFrame
    df = hook.get_pandas_df("""
        SELECT customer_id, name, balance, tier
        FROM customers
        WHERE is_active = TRUE
        ORDER BY balance DESC
        LIMIT 100
    """)
    
    print(f"Fetched {len(df)} customers")
    return df.to_json()

def run_sql(**context):
    """Execute SQL with PostgresHook"""
    hook = PostgresHook(postgres_conn_id="my_postgres_conn")
    
    hook.run("""
        INSERT INTO pipeline_logs (run_date, status, rows_processed)
        VALUES (NOW(), 'success', 45000)
    """)
```

---

## Taskflow API — Modern Way (Airflow 2+)

```python
from airflow.decorators import dag, task
from datetime import datetime
import pandas as pd

@dag(
    dag_id="bank_marketing_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule_interval="0 6 * * *",
    catchup=False,
    tags=["bank", "etl"]
)
def bank_marketing_pipeline():
    
    @task()
    def extract() -> dict:
        """Extract bank marketing data"""
        df = pd.read_csv("data/bank_marketing.csv")
        print(f"Extracted {len(df):,} rows")
        return {"rows": len(df), "columns": list(df.columns)}
    
    @task()
    def validate(extract_result: dict) -> dict:
        """Validate extracted data"""
        print(f"Validating {extract_result['rows']:,} rows")
        required_cols = ["age", "job", "balance", "y"]
        missing = [c for c in required_cols if c not in extract_result["columns"]]
        if missing:
            raise ValueError(f"Missing columns: {missing}")
        return {"valid": True, "rows": extract_result["rows"]}
    
    @task()
    def transform(validate_result: dict) -> dict:
        """Clean and transform data"""
        df = pd.read_csv("data/bank_marketing.csv")
        df = df.drop_duplicates()
        df = df.dropna(subset=["age", "job", "balance"])
        df.to_parquet("data/processed/bank_clean.parquet")
        return {"clean_rows": len(df)}
    
    @task()
    def load(transform_result: dict) -> str:
        """Load to data warehouse"""
        from sqlalchemy import create_engine
        import os
        engine = create_engine(os.getenv("DB_URL"))
        df = pd.read_parquet("data/processed/bank_clean.parquet")
        df.to_sql("bank_marketing", engine, if_exists="replace", index=False)
        return f"Loaded {transform_result['clean_rows']:,} rows to warehouse"
    
    @task()
    def notify(load_result: str):
        """Send completion notification"""
        print(f"✅ Pipeline complete: {load_result}")
        # send_email(load_result)
    
    # Wire tasks together
    extracted = extract()
    validated = validate(extracted)
    transformed = transform(validated)
    loaded = load(transformed)
    notify(loaded)

# Instantiate the DAG
pipeline = bank_marketing_pipeline()
```

---

## Connections & Variables

```python
# In Airflow UI → Admin → Connections
# Add connection:
#   Conn ID: my_postgres
#   Conn Type: Postgres
#   Host: localhost
#   Login: beatrice
#   Password: secret
#   Port: 5432
#   Schema: sales_db

# In code:
from airflow.hooks.base import BaseHook

conn = BaseHook.get_connection("my_postgres")
print(conn.host, conn.login, conn.schema)

# Variables (Airflow UI → Admin → Variables)
from airflow.models import Variable

batch_size = Variable.get("batch_size", default_var=1000)
env = Variable.get("environment", default_var="dev")
config = Variable.get("pipeline_config", deserialize_json=True)
```

---

## Real World Production DAG

```python
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable
from datetime import datetime, timedelta
import pandas as pd
import logging

logger = logging.getLogger(__name__)

@dag(
    dag_id="production_bank_etl",
    schedule_interval="0 5 * * 1-5",       # Weekdays at 5 AM
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,                      # Only one run at a time
    default_args={
        "owner": "beatrice",
        "retries": 3,
        "retry_delay": timedelta(minutes=5),
        "email_on_failure": True,
        "email": ["beatiewakarima1@gmail.com"]
    },
    tags=["production", "bank", "daily"]
)
def production_bank_etl():
    
    @task()
    def extract_source_data(**context):
        run_date = context["ds"]            # Execution date: 2026-05-20
        hook = PostgresHook("source_db")
        df = hook.get_pandas_df(f"""
            SELECT * FROM transactions
            WHERE DATE(created_at) = '{run_date}'
        """)
        logger.info(f"Extracted {len(df):,} transactions for {run_date}")
        df.to_parquet(f"/tmp/raw_{run_date}.parquet")
        return {"rows": len(df), "date": run_date}
    
    @task()
    def run_quality_checks(stats: dict):
        df = pd.read_parquet(f"/tmp/raw_{stats['date']}.parquet")
        
        checks = {
            "no_nulls_in_amount": df["amount"].isnull().sum() == 0,
            "no_negative_amounts": (df["amount"] < 0).sum() == 0,
            "row_count_reasonable": len(df) > 0
        }
        
        failed = [k for k, v in checks.items() if not v]
        if failed:
            raise ValueError(f"Quality checks failed: {failed}")
        
        logger.info(f"✅ All quality checks passed for {stats['date']}")
        return stats
    
    @task()
    def transform_and_enrich(stats: dict):
        df = pd.read_parquet(f"/tmp/raw_{stats['date']}.parquet")
        
        df["transaction_size"] = pd.cut(
            df["amount"],
            bins=[0, 1000, 10000, 100000, float("inf")],
            labels=["Small", "Medium", "Large", "Major"]
        )
        df["processing_date"] = stats["date"]
        
        df.to_parquet(f"/tmp/clean_{stats['date']}.parquet")
        logger.info(f"Transformed {len(df):,} rows")
        return stats
    
    @task()
    def load_to_warehouse(stats: dict):
        from sqlalchemy import create_engine
        import os
        df = pd.read_parquet(f"/tmp/clean_{stats['date']}.parquet")
        engine = create_engine(os.getenv("WAREHOUSE_URL"))
        df.to_sql("fact_transactions", engine, if_exists="append", index=False)
        logger.info(f"✅ Loaded {len(df):,} rows for {stats['date']}")
    
    # Wire up pipeline
    extracted = extract_source_data()
    validated = run_quality_checks(extracted)
    transformed = transform_and_enrich(validated)
    load_to_warehouse(transformed)

dag_instance = production_bank_etl()
```

---

## Airflow Quick Reference

```python
# Schedule expressions
"@hourly"               # Every hour
"@daily"                # Daily at midnight
"@weekly"               # Weekly on Sunday
"@monthly"              # Monthly on 1st
"0 6 * * *"             # Daily at 6 AM
"0 6 * * 1-5"           # Weekdays at 6 AM
"0 */4 * * *"           # Every 4 hours

# Key parameters
catchup=False           # Don't backfill
max_active_runs=1       # One run at a time
depends_on_past=True    # Wait for yesterday's run

# Task dependencies
t1 >> t2                # t1 then t2
t1 >> [t2, t3]          # t2 and t3 in parallel
[t1, t2] >> t3          # Both must finish before t3

# Operators
PythonOperator          # Run Python function
BashOperator            # Run bash command
PostgresOperator        # Run SQL on Postgres
EmailOperator           # Send email
DummyOperator           # Placeholder task
BranchPythonOperator    # Conditional branching
```

---

## Previous | Next
← [[24 - Python + Docker]] | → [[Python MOC]]
