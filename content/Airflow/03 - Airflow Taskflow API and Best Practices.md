---
title: Airflow Taskflow API and Best Practices
tags: [airflow, taskflow, python, best-practices]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# 🎯 Airflow Taskflow API & Best Practices

> The Taskflow API (Airflow 2.0+) is the modern, Pythonic way to write DAGs. It reduces boilerplate dramatically, makes XCom automatic, and produces much cleaner code. This is how production DAGs should be written.

---

## Taskflow API — The Modern Way

```python
# Old way — verbose, manual XCom
from airflow.operators.python import PythonOperator

def extract(**context):
    data = {"rows": 1000}
    context["ti"].xcom_push(key="data", value=data)

def transform(**context):
    data = context["ti"].xcom_pull(task_ids="extract", key="data")
    result = {"clean_rows": data["rows"] - 50}
    context["ti"].xcom_push(key="result", value=result)

t1 = PythonOperator(task_id="extract", python_callable=extract)
t2 = PythonOperator(task_id="transform", python_callable=transform)
t1 >> t2

# ─────────────────────────────────────────────────────────

# New way — Taskflow API (Airflow 2.0+)
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["modern"]
)
def modern_pipeline():

    @task()
    def extract() -> dict:
        return {"rows": 1000, "source": "bank_marketing.csv"}

    @task()
    def transform(data: dict) -> dict:
        # XCom is AUTOMATIC — just return and accept values!
        clean_rows = data["rows"] - 50
        return {"clean_rows": clean_rows}

    @task()
    def load(result: dict) -> str:
        print(f"Loading {result['clean_rows']} rows")
        return "success"

    # Wire up — clean and Pythonic
    raw = extract()
    cleaned = transform(raw)
    load(cleaned)

pipeline = modern_pipeline()
```

---

## Complete Taskflow Bank Marketing Pipeline

```python
# dags/bank_marketing_taskflow.py
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.email import send_email
from datetime import datetime, timedelta
import pandas as pd
import logging

logger = logging.getLogger(__name__)

@dag(
    dag_id="bank_marketing_taskflow",
    schedule_interval="0 5 * * 1-5",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    default_args={
        "owner": "beatrice",
        "retries": 3,
        "retry_delay": timedelta(minutes=5),
        "retry_exponential_backoff": True,
        "max_retry_delay": timedelta(minutes=30),
        "email_on_failure": True,
        "email": ["beatiewakarima1@gmail.com"],
        "execution_timeout": timedelta(hours=2)
    },
    tags=["bank", "taskflow", "production"]
)
def bank_marketing_pipeline():

    @task(task_id="extract_source_data")
    def extract(run_date: str) -> dict:
        """Extract raw data from CSV source"""
        filepath = f"/data/bank_marketing.csv"
        df = pd.read_csv(filepath, sep=";")

        logger.info(f"Extracted {len(df):,} rows for {run_date}")

        # Basic validation
        assert len(df) > 0, "Empty dataset!"
        assert "y" in df.columns, "Missing target column!"

        return {
            "rows": len(df),
            "columns": list(df.columns),
            "filepath": filepath
        }

    @task(task_id="validate_source")
    def validate(extract_result: dict) -> dict:
        """Validate source data quality"""
        df = pd.read_csv(extract_result["filepath"], sep=";")

        checks = {
            "has_rows": len(df) > 0,
            "has_target": "y" in df.columns,
            "valid_target_values": set(df["y"].unique()).issubset({"yes", "no"}),
            "age_in_range": df["age"].between(10, 100).all(),
            "no_empty_df": not df.empty
        }

        failed = [k for k, v in checks.items() if not v]
        if failed:
            raise ValueError(f"Validation failed: {failed}")

        sub_rate = (df["y"] == "yes").mean() * 100
        logger.info(f"✅ Validated: {len(df):,} rows, {sub_rate:.1f}% subscription rate")

        return {**extract_result, "subscription_rate": round(sub_rate, 2)}

    @task(task_id="load_bronze")
    def load_bronze(validated: dict, run_date: str) -> dict:
        """Load raw data to Bronze layer"""
        df = pd.read_csv(validated["filepath"], sep=";")
        df["_run_date"] = run_date
        df["_loaded_at"] = pd.Timestamp.now()

        hook = PostgresHook(postgres_conn_id="postgres_data_vault")
        engine = hook.get_sqlalchemy_engine()

        # Idempotent load
        hook.run(f"""
            DELETE FROM bronze.raw_bank_marketing
            WHERE _run_date = '{run_date}'
        """)

        df.to_sql("raw_bank_marketing", engine,
                  schema="bronze", if_exists="append",
                  index=False, chunksize=5000)

        logger.info(f"🟤 Bronze: {len(df):,} rows loaded")
        return {**validated, "bronze_rows": len(df)}

    @task.bash(task_id="run_dbt_staging")
    def run_dbt_staging() -> str:
        return "cd /opt/dbt && dbt build --select staging --target prod"

    @task.bash(task_id="run_dbt_marts")
    def run_dbt_marts() -> str:
        return "cd /opt/dbt && dbt build --select marts --target prod"

    @task(task_id="validate_gold")
    def validate_gold(run_date: str) -> dict:
        """Validate gold layer after dbt run"""
        hook = PostgresHook(postgres_conn_id="postgres_data_vault")

        count = hook.get_first("""
            SELECT COUNT(*) FROM gold.campaign_performance
            WHERE report_date = CURRENT_DATE()
        """)[0]

        if count == 0:
            raise ValueError("Gold table empty after dbt run!")

        stats = hook.get_first("""
            SELECT
                SUM(total_contacts) AS contacts,
                ROUND(AVG(conversion_rate)::numeric, 2) AS avg_conversion
            FROM gold.campaign_performance
            WHERE report_date = CURRENT_DATE()
        """)

        logger.info(f"✅ Gold validated: {stats[0]:,} contacts, {stats[1]}% avg conversion")
        return {
            "gold_rows": count,
            "total_contacts": stats[0],
            "avg_conversion": float(stats[1])
        }

    @task(task_id="send_success_report", trigger_rule="all_success")
    def send_report(
        bronze_stats: dict,
        gold_stats: dict,
        run_date: str
    ) -> None:
        """Send success notification"""
        html = f"""
        <div style="font-family: Arial; color: #333;">
            <h2 style="color: #27ae60;">✅ Bank Marketing Pipeline Complete</h2>
            <table style="border-collapse: collapse; width: 400px;">
                <tr><td><b>Run Date:</b></td><td>{run_date}</td></tr>
                <tr><td><b>Source Rows:</b></td>
                    <td>{bronze_stats.get('rows', 0):,}</td></tr>
                <tr><td><b>Bronze Rows:</b></td>
                    <td>{bronze_stats.get('bronze_rows', 0):,}</td></tr>
                <tr><td><b>Gold Rows:</b></td>
                    <td>{gold_stats.get('gold_rows', 0):,}</td></tr>
                <tr><td><b>Avg Conversion:</b></td>
                    <td>{gold_stats.get('avg_conversion', 0):.1f}%</td></tr>
                <tr><td><b>Subscription Rate:</b></td>
                    <td>{bronze_stats.get('subscription_rate', 0):.1f}%</td></tr>
            </table>
        </div>
        """
        send_email(
            to=["beatiewakarima1@gmail.com"],
            subject=f"✅ Pipeline Complete — {run_date}",
            html_content=html
        )

    # ── Wire up the pipeline ──────────────────────────────
    from airflow.models.param import Param

    # Context templates via params or execution_date
    run_date = "{{ ds }}"

    extracted   = extract(run_date)
    validated   = validate(extracted)
    bronzed     = load_bronze(validated, run_date)
    _staging    = run_dbt_staging()
    _marts      = run_dbt_marts()
    gold_stats  = validate_gold(run_date)
    send_report(bronzed, gold_stats, run_date)

    # Set explicit dependencies for dbt ordering
    bronzed >> _staging >> _marts >> gold_stats

pipeline_instance = bank_marketing_pipeline()
```

---

## Taskflow Best Practices

```python
# ✅ 1. Use type hints — documents expected data shapes
@task()
def extract() -> dict:
    return {"rows": 1000}

# ✅ 2. Keep tasks small and focused (single responsibility)
# One task = one logical step (extract / validate / load / transform)

# ✅ 3. Make tasks idempotent — same result if run twice
@task()
def load_bronze(run_date: str) -> int:
    hook.run(f"DELETE FROM bronze.table WHERE date = '{run_date}'")
    # Then insert — safe to run multiple times
    return rows_loaded

# ✅ 4. Use variables for sensitive config
from airflow.models import Variable

@task()
def connect_to_db():
    db_url = Variable.get("db_url", deserialize_json=False)
    # Never hardcode credentials!

# ✅ 5. Log meaningful messages
@task()
def transform(data: dict) -> dict:
    logger.info(f"Starting transform: {data['rows']:,} rows")
    # ... transform ...
    logger.info(f"Transform complete: {result['clean_rows']:,} rows retained")
    return result

# ✅ 6. Handle failures gracefully
@task(retries=3, retry_delay=timedelta(minutes=5))
def fetch_from_api(date: str) -> dict:
    try:
        response = requests.get(f"{API_URL}?date={date}", timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        raise AirflowException("API timeout — will retry")
    except requests.HTTPError as e:
        raise AirflowException(f"API error: {e}")

# ✅ 7. Use task groups for visual clarity
from airflow.utils.task_group import TaskGroup

with TaskGroup("dbt_transformations") as dbt_group:
    run_staging = BashOperator(...)
    run_marts = BashOperator(...)
    run_staging >> run_marts

# ✅ 8. Always set execution_timeout
@task(execution_timeout=timedelta(hours=1))
def long_running_task():
    pass
```

---

## Task Groups — Visual Organisation

```python
from airflow.utils.task_group import TaskGroup

@dag(dag_id="grouped_pipeline", ...)
def grouped_pipeline():

    with TaskGroup("extraction") as extract_group:
        extract_customers = PythonOperator(...)
        extract_transactions = PythonOperator(...)
        extract_products = PythonOperator(...)

    with TaskGroup("transformations") as transform_group:
        run_staging = BashOperator(...)
        run_marts = BashOperator(...)
        run_staging >> run_marts

    with TaskGroup("validation") as validate_group:
        validate_bronze = PythonOperator(...)
        validate_gold = PythonOperator(...)

    with TaskGroup("notification") as notify_group:
        send_email = EmailOperator(...)
        update_audit = PostgresOperator(...)

    extract_group >> transform_group >> validate_group >> notify_group
```

---

## Dynamic Task Mapping (Airflow 2.3+)

```python
# Run the same task for multiple inputs in parallel

@dag(dag_id="dynamic_tasks", ...)
def dynamic_pipeline():

    @task()
    def get_tables_to_process() -> list:
        return ["customers", "transactions", "products", "orders"]

    @task()
    def process_table(table_name: str) -> str:
        hook = PostgresHook("postgres_data_vault")
        count = hook.get_first(f"SELECT COUNT(*) FROM silver.{table_name}")[0]
        logger.info(f"Processed {table_name}: {count:,} rows")
        return f"{table_name}: {count}"

    # expand() creates one task instance per list item — all run in parallel!
    tables = get_tables_to_process()
    process_table.expand(table_name=tables)

# In the UI you'll see:
# process_table[0] → customers
# process_table[1] → transactions
# process_table[2] → products
# process_table[3] → orders
# All running in parallel!
```

---

## Callbacks — Custom Failure Handling

```python
def on_failure_callback(context):
    """Called when any task fails"""
    dag_id = context["dag"].dag_id
    task_id = context["task_instance"].task_id
    execution_date = context["ds"]
    exception = context.get("exception")

    # Send Slack/email alert
    send_email(
        to=["beatiewakarima1@gmail.com"],
        subject=f"🚨 FAILURE: {dag_id}.{task_id} on {execution_date}",
        html_content=f"""
        <h2>🚨 Task Failed</h2>
        <p>DAG: {dag_id}</p>
        <p>Task: {task_id}</p>
        <p>Date: {execution_date}</p>
        <p>Error: {str(exception)[:500]}</p>
        """
    )

def on_success_callback(context):
    """Called when task succeeds"""
    logger.info(f"Task {context['task_instance'].task_id} succeeded!")

def on_retry_callback(context):
    """Called when task is retried"""
    logger.warning(
        f"Retrying {context['task_instance'].task_id} "
        f"(attempt {context['task_instance'].try_number})"
    )

# Apply at DAG level
with DAG(
    dag_id="monitored_pipeline",
    on_failure_callback=on_failure_callback,
    on_success_callback=on_success_callback,
    default_args={
        "on_failure_callback": on_failure_callback,
        "on_retry_callback": on_retry_callback
    }
) as dag:
    pass
```

---

## Quick Reference

```python
# Taskflow decorator
@dag(schedule_interval, start_date, catchup, default_args, tags)
def my_dag():
    @task()
    def my_task(input: dict) -> dict:
        return result

    t1 = my_task()

instance = my_dag()

# Task options
@task(
    task_id="custom_id",
    retries=3,
    retry_delay=timedelta(minutes=5),
    retry_exponential_backoff=True,
    execution_timeout=timedelta(hours=1),
    pool="database_pool",
    pool_slots=1,
    priority_weight=10,
    trigger_rule="all_success",
    on_failure_callback=fn
)

# Task groups
with TaskGroup("group_name") as group:
    t1 = ...
    t2 = ...
    t1 >> t2

# Dynamic mapping
task.expand(param=list_of_values)

# Bash shorthand
@task.bash
def run_command() -> str:
    return "echo hello"
```

---

## Previous | Next
← [[02 - Airflow Operators and Sensors]] | → [[04 - Airflow Connections Variables and XCom]]
