---
title: Pipeline Orchestration with Airflow
tags: [data-engineering, airflow, orchestration]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# 🌬️ Pipeline Orchestration with Airflow

> Airflow schedules, monitors, and manages your data pipelines as DAGs. It is the industry standard for orchestration — used at Airbnb, Twitter, LinkedIn, and most data-mature companies.

---

## Why Orchestration?

```
Without Airflow:
  ❌ Cron jobs that fail silently
  ❌ No visibility into what ran and when
  ❌ No retry logic
  ❌ No dependency management
  ❌ Can't run tasks in parallel
  ❌ No alerting on failure

With Airflow:
  ✅ Visual DAG editor and monitor
  ✅ Automatic retries with backoff
  ✅ Task dependencies enforced
  ✅ Parallel execution
  ✅ Email/Slack alerts on failure
  ✅ Historical run logs
  ✅ SLA monitoring
```

---

## Airflow Core Concepts

```
DAG         = Directed Acyclic Graph — your pipeline
Task        = One unit of work
Operator    = Template for a task type
Sensor      = Waits for a condition
Hook        = Connection to external system
Connection  = Stored credentials (UI → Admin → Connections)
Variable    = Stored config values (UI → Admin → Variables)
XCom        = Pass data between tasks
Pool        = Limit concurrent task slots
SLA         = Expected completion time
```

---

## Full ETL DAG — Bank Marketing Pipeline

```python
# dags/bank_marketing_etl.py
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.email import send_email
from datetime import datetime, timedelta
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# ── DEFAULT ARGS ──────────────────────────────────────────────
default_args = {
    "owner": "beatrice",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=30),
    "email": ["beatiewakarima1@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "execution_timeout": timedelta(hours=2)
}

# ── DAG DEFINITION ────────────────────────────────────────────
with DAG(
    dag_id="bank_marketing_etl",
    default_args=default_args,
    description="Daily Bank Marketing ETL Pipeline",
    schedule_interval="0 5 * * 1-5",       # Weekdays at 5 AM EAT
    catchup=False,
    max_active_runs=1,                       # No concurrent runs
    tags=["bank", "etl", "daily", "production"]
) as dag:

    # ── TASK 1: CHECK DATA AVAILABILITY ───────────────────────
    wait_for_data = FileSensor(
        task_id="wait_for_source_data",
        filepath="/data/raw/bank_marketing_{{ ds }}.csv",
        poke_interval=300,              # Check every 5 minutes
        timeout=3600,                   # Fail after 1 hour
        mode="reschedule"               # Release worker while waiting
    )

    # ── TASK 2: VALIDATE SOURCE ───────────────────────────────
    @task(task_id="validate_source")
    def validate_source(**context):
        run_date = context["ds"]
        filepath = f"/data/raw/bank_marketing_{run_date}.csv"

        df = pd.read_csv(filepath, sep=";")
        row_count = len(df)

        checks = {
            "has_rows": row_count > 0,
            "has_required_columns": all(c in df.columns
                for c in ["age", "job", "balance", "y"]),
            "no_all_nulls": df.isnull().all(axis=1).sum() == 0,
        }

        failed = [k for k, v in checks.items() if not v]
        if failed:
            raise ValueError(f"Source validation failed: {failed}")

        logger.info(f"✅ Source validated: {row_count:,} rows")

        # Push stats to XCom
        context["ti"].xcom_push(key="source_row_count", value=row_count)
        context["ti"].xcom_push(key="source_filepath", value=filepath)
        return {"rows": row_count, "filepath": filepath}

    # ── TASK 3: EXTRACT TO BRONZE ─────────────────────────────
    @task(task_id="extract_to_bronze")
    def extract_to_bronze(**context):
        ti = context["ti"]
        stats = ti.xcom_pull(task_ids="validate_source")

        df = pd.read_csv(stats["filepath"], sep=";")

        # Add metadata
        df["_source_file"] = stats["filepath"]
        df["_loaded_at"] = datetime.now()
        df["_run_date"] = context["ds"]

        # Load to PostgreSQL bronze
        hook = PostgresHook(postgres_conn_id="postgres_data_vault")
        engine = hook.get_sqlalchemy_engine()

        # Delete existing data for this run date (idempotent)
        hook.run(f"""
            DELETE FROM bronze.raw_bank_marketing
            WHERE _run_date = '{context["ds"]}'
        """)

        df.to_sql("raw_bank_marketing", engine,
                  schema="bronze", if_exists="append",
                  index=False, chunksize=5000)

        logger.info(f"🟤 Bronze loaded: {len(df):,} rows")
        ti.xcom_push(key="bronze_rows", value=len(df))
        return len(df)

    # ── TASK 4: BRANCH — DECIDE TRANSFORM STRATEGY ───────────
    def choose_transform_strategy(**context):
        """Choose full or incremental transform"""
        run_date = context["ds"]
        # Full refresh on Mondays
        if datetime.strptime(run_date, "%Y-%m-%d").weekday() == 0:
            return "full_transform"
        return "incremental_transform"

    branch_strategy = BranchPythonOperator(
        task_id="choose_strategy",
        python_callable=choose_transform_strategy
    )

    # ── TASK 5A: FULL TRANSFORM ───────────────────────────────
    full_transform = BashOperator(
        task_id="full_transform",
        bash_command=(
            "cd /opt/dbt && dbt build --full-refresh "
            "--select staging+ --target prod"
        )
    )

    # ── TASK 5B: INCREMENTAL TRANSFORM ───────────────────────
    incremental_transform = BashOperator(
        task_id="incremental_transform",
        bash_command=(
            "cd /opt/dbt && dbt build "
            "--select staging+ --target prod"
        )
    )

    # ── TASK 6: RUN DBT MARTS ────────────────────────────────
    dbt_marts = BashOperator(
        task_id="dbt_marts",
        bash_command=(
            "cd /opt/dbt && dbt build "
            "--select marts --target prod"
        ),
        trigger_rule="none_failed_min_one_success"  # Run after either branch
    )

    # ── TASK 7: DATA QUALITY CHECKS ──────────────────────────
    @task(task_id="data_quality_checks",
          trigger_rule="none_failed_min_one_success")
    def run_quality_checks(**context):
        hook = PostgresHook(postgres_conn_id="postgres_data_vault")

        checks = {}

        # Check 1: Row count
        count = hook.get_first(
            "SELECT COUNT(*) FROM silver.bank_customers"
        )[0]
        checks["row_count"] = count > 0

        # Check 2: No nulls in key columns
        nulls = hook.get_first("""
            SELECT COUNT(*) FROM silver.bank_customers
            WHERE job IS NULL OR balance IS NULL
        """)[0]
        checks["no_critical_nulls"] = nulls == 0

        # Check 3: Subscription rate sanity check
        rate = hook.get_first("""
            SELECT ROUND(100.0 * SUM(CASE WHEN subscribed THEN 1 ELSE 0 END)
                   / COUNT(*), 2)
            FROM silver.bank_customers
        """)[0]
        checks["subscription_rate_reasonable"] = 1 <= float(rate) <= 50

        # Check 4: Data freshness
        last_load = hook.get_first("""
            SELECT MAX(processed_at) FROM silver.bank_customers
        """)[0]
        checks["data_is_fresh"] = last_load is not None

        failed = [k for k, v in checks.items() if not v]

        if failed:
            raise ValueError(f"Quality checks failed: {failed}")

        logger.info(f"✅ All quality checks passed: {checks}")
        return checks

    # ── TASK 8: SEND SUCCESS REPORT ──────────────────────────
    @task(task_id="send_success_report")
    def send_report(**context):
        ti = context["ti"]
        run_date = context["ds"]
        source_rows = ti.xcom_pull(task_ids="validate_source",
                                   key="source_row_count")
        bronze_rows = ti.xcom_pull(task_ids="extract_to_bronze")

        body = f"""
        <h2>✅ Bank Marketing Pipeline — SUCCESS</h2>
        <p><b>Run Date:</b> {run_date}</p>
        <p><b>Source Rows:</b> {source_rows:,}</p>
        <p><b>Bronze Rows:</b> {bronze_rows:,}</p>
        <p>All dbt models and quality checks passed.</p>
        <p>Dashboard updated: 
           <a href="https://data-science-learning-vault.vercel.app">
           View Site</a>
        </p>
        """

        send_email(
            to=["beatiewakarima1@gmail.com"],
            subject=f"✅ Pipeline Complete — {run_date}",
            html_content=body
        )
        logger.info("📧 Success report sent")

    # ── TASK DEPENDENCIES ────────────────────────────────────
    validate = validate_source()
    bronze = extract_to_bronze()
    quality = run_quality_checks()
    report = send_report()

    (
        wait_for_data
        >> validate
        >> bronze
        >> branch_strategy
        >> [full_transform, incremental_transform]
        >> dbt_marts
        >> quality
        >> report
    )
```

---

## Connections — Store Credentials Safely

```python
# Set up via Airflow UI → Admin → Connections
# OR via environment variables:

# PostgreSQL connection
# AIRFLOW_CONN_POSTGRES_DATA_VAULT=postgresql://beatrice:secret@localhost:5432/data_vault

# Using in DAGs
from airflow.providers.postgres.hooks.postgres import PostgresHook

hook = PostgresHook(postgres_conn_id="postgres_data_vault")
df = hook.get_pandas_df("SELECT * FROM silver.bank_customers")
hook.run("UPDATE ...")
engine = hook.get_sqlalchemy_engine()
```

---

## Variables — Store Configuration

```python
# Set via UI: Admin → Variables
# Key: batch_size, Value: 5000
# Key: notification_email, Value: beatrice@gmail.com

from airflow.models import Variable

batch_size = Variable.get("batch_size", default_var=5000, deserialize_json=False)
email = Variable.get("notification_email")
config = Variable.get("pipeline_config", deserialize_json=True)
```

---

## SLA Monitoring

```python
def sla_miss_callback(dag, task_list, blocking_task_list,
                      slas, blocking_tis):
    """Called when SLA is missed"""
    logger.error(f"SLA MISSED for tasks: {task_list}")
    send_email(
        to=["beatiewakarima1@gmail.com"],
        subject="⚠️ SLA MISSED — Bank Marketing Pipeline",
        html_content=f"Tasks missed SLA: {task_list}"
    )

with DAG(
    dag_id="bank_marketing_etl",
    sla_miss_callback=sla_miss_callback,
    default_args={
        "sla": timedelta(hours=2)    # Each task must complete within 2 hours
    }
) as dag:
    pass
```

---

## Pools — Control Concurrency

```bash
# Create pool via CLI
airflow pools set database_pool 3 "Max 3 concurrent DB tasks"

# Or via UI: Admin → Pools
```

```python
# Use pool in task
load_task = PythonOperator(
    task_id="load_to_database",
    python_callable=load_data,
    pool="database_pool",           # Limits to 3 concurrent
    pool_slots=1
)
```

---

## Trigger Rules

```python
# Default: all_success — runs only if all upstreams succeed
task = PythonOperator(task_id="t", python_callable=fn)

# none_failed — runs if at least one upstream succeeded
cleanup = PythonOperator(
    task_id="cleanup",
    python_callable=cleanup_fn,
    trigger_rule="none_failed_min_one_success"
)

# all_done — runs regardless of upstream success/failure
notify = PythonOperator(
    task_id="always_notify",
    python_callable=send_notification,
    trigger_rule="all_done"
)

# one_success — runs if any one upstream succeeds
```

---

## Quick Reference

```python
# DAG skeleton
with DAG(
    dag_id="my_dag",
    schedule_interval="0 6 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args={"retries": 3, "retry_delay": timedelta(minutes=5)}
) as dag:

    # Operators
    PythonOperator(task_id="t", python_callable=fn)
    BashOperator(task_id="t", bash_command="cmd")
    FileSensor(task_id="t", filepath="/path/to/file")

    # Taskflow API
    @task
    def my_task(**context): ...

    # Dependencies
    t1 >> t2 >> [t3, t4] >> t5

# XCom
context["ti"].xcom_push(key="key", value=data)
context["ti"].xcom_pull(task_ids="task", key="key")

# Hooks
PostgresHook(postgres_conn_id="conn_id").get_pandas_df("SQL")

# Variables
Variable.get("key", default_var="default")
```

---

## Previous | Next
← [[03 - Loading Data (Batch)]] | → [[05 - Data Warehouse Design]]
