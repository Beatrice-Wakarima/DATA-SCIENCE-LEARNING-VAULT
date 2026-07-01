---
title: Airflow Operators and Sensors
tags: [airflow, operators, sensors, data-engineering]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# ⚙️ Airflow Operators & Sensors

> Operators are the building blocks of Airflow — they define what each task does. Sensors are special operators that wait for a condition. Mastering both is essential for building real pipelines.

---

## Operator Categories

```
Action Operators    — Execute something (Python, Bash, SQL, email)
Transfer Operators  — Move data between systems (S3 to Snowflake, etc.)
Sensor Operators    — Wait for a condition (file, time, HTTP, DB)
```

---

## PythonOperator

```python
from airflow.operators.python import PythonOperator

# Simple function
def extract_data():
    import pandas as pd
    df = pd.read_csv("data/bank_marketing.csv", sep=";")
    print(f"Extracted {len(df):,} rows")
    return len(df)

# Function with context (access execution date, XComs, etc.)
def transform_data(**context):
    execution_date = context["ds"]              # '2026-05-20'
    task_instance = context["ti"]               # TaskInstance object
    prev_rows = task_instance.xcom_pull(
        task_ids="extract_data",
        key="return_value"
    )
    print(f"Transforming {prev_rows} rows for {execution_date}")

# With templates (Jinja)
def load_data(run_date, **context):
    print(f"Loading for: {run_date}")

t1 = PythonOperator(
    task_id="extract_data",
    python_callable=extract_data
)

t2 = PythonOperator(
    task_id="transform_data",
    python_callable=transform_data,
    provide_context=True        # Pass **context (Airflow 1.x compat)
)

t3 = PythonOperator(
    task_id="load_data",
    python_callable=load_data,
    op_kwargs={"run_date": "{{ ds }}"}  # Jinja template
)
```

---

## BashOperator

```python
from airflow.operators.bash import BashOperator

# Simple bash command
run_script = BashOperator(
    task_id="run_script",
    bash_command="python /opt/pipeline/main.py"
)

# With Jinja templates
run_dbt = BashOperator(
    task_id="run_dbt",
    bash_command="""
        cd /opt/dbt && \
        dbt build \
            --target prod \
            --select staging+ \
            --vars '{"run_date": "{{ ds }}"}'
    """
)

# With environment variables
run_pipeline = BashOperator(
    task_id="run_pipeline",
    bash_command="python /opt/pipeline/main.py --date {{ ds }}",
    env={
        "DB_HOST": "postgres",
        "DB_PASSWORD": "{{ var.value.db_password }}",
        "RUN_DATE": "{{ ds }}"
    }
)

# Multi-line complex script
complex_task = BashOperator(
    task_id="complex_bash",
    bash_command="""
        set -e  # Exit on any error
        echo "Starting pipeline for {{ ds }}"
        
        # Check if source file exists
        if [ ! -f /data/input_{{ ds_nodash }}.csv ]; then
            echo "ERROR: Source file not found!"
            exit 1
        fi
        
        # Run transformation
        python /scripts/transform.py --date {{ ds }}
        
        echo "Pipeline complete!"
    """
)
```

---

## Database Operators

```python
# ── PostgreSQL ────────────────────────────────────────────
from airflow.providers.postgres.operators.postgres import PostgresOperator

run_sql = PostgresOperator(
    task_id="run_sql",
    postgres_conn_id="postgres_data_vault",
    sql="""
        DELETE FROM bronze.raw_bank_marketing
        WHERE _run_date = '{{ ds }}';
        
        INSERT INTO pipeline_audit (run_date, status)
        VALUES ('{{ ds }}', 'running');
    """
)

# SQL from file
run_sql_file = PostgresOperator(
    task_id="run_sql_file",
    postgres_conn_id="postgres_data_vault",
    sql="sql/transform_silver.sql"  # Relative to dags/ folder
)

# ── Snowflake ─────────────────────────────────────────────
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

snowflake_task = SnowflakeOperator(
    task_id="snowflake_transform",
    snowflake_conn_id="snowflake_data_vault",
    sql="""
        CALL DATA_VAULT.SILVER.TRANSFORM_BANK_MARKETING('{{ ds }}')
    """,
    warehouse="ETL_WH",
    database="DATA_VAULT",
    schema="BRONZE"
)
```

---

## Email Operator

```python
from airflow.operators.email import EmailOperator

send_report = EmailOperator(
    task_id="send_success_report",
    to=["beatiewakarima1@gmail.com", "manager@company.com"],
    subject="✅ Daily Pipeline Complete — {{ ds }}",
    html_content="""
    <h2>Pipeline Complete</h2>
    <p>Run date: <b>{{ ds }}</b></p>
    <p>Status: <b style="color:green;">SUCCESS</b></p>
    <ul>
        <li>Rows extracted: {{ ti.xcom_pull('extract', key='rows') }}</li>
        <li>Duration: check Airflow UI</li>
    </ul>
    <p><a href="http://airflow:8080">View in Airflow</a></p>
    """,
    files=["/outputs/daily_report_{{ ds_nodash }}.xlsx"]
)
```

---

## BranchPythonOperator — Conditional Paths

```python
from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator

def choose_path(**context):
    """Return task_id of the branch to follow"""
    execution_date = context["ds"]
    weekday = context["execution_date"].weekday()  # 0=Mon, 6=Sun

    if weekday == 0:  # Monday
        return "full_refresh"
    else:
        return "incremental_load"

branch = BranchPythonOperator(
    task_id="choose_load_strategy",
    python_callable=choose_path
)

full_refresh = BashOperator(
    task_id="full_refresh",
    bash_command="dbt run --full-refresh --target prod"
)

incremental = BashOperator(
    task_id="incremental_load",
    bash_command="dbt run --target prod"
)

# Both paths converge here
join = EmptyOperator(
    task_id="join",
    trigger_rule="none_failed_min_one_success"
)

send_report = EmailOperator(task_id="send_report", ...)

branch >> [full_refresh, incremental] >> join >> send_report
```

---

## Sensors — Wait for Conditions

### FileSensor
```python
from airflow.sensors.filesystem import FileSensor

wait_for_file = FileSensor(
    task_id="wait_for_source_file",
    filepath="/data/raw/bank_marketing_{{ ds }}.csv",
    poke_interval=60,       # Check every 60 seconds
    timeout=3600,           # Fail after 1 hour
    mode="reschedule",      # Release worker slot while waiting
    soft_fail=False         # Fail task (not skip) on timeout
)
```

### TimeSensor — Wait Until a Time
```python
from airflow.sensors.time_sensor import TimeSensor
from datetime import time

wait_until_morning = TimeSensor(
    task_id="wait_until_6am",
    target_time=time(6, 0),     # Wait until 6:00 AM
    mode="reschedule"
)
```

### HttpSensor — Wait for API Response
```python
from airflow.providers.http.sensors.http import HttpSensor

wait_for_api = HttpSensor(
    task_id="wait_for_api",
    http_conn_id="bank_api",
    endpoint="health",
    request_params={},
    response_check=lambda response: response.json()["status"] == "ok",
    poke_interval=30,
    timeout=300,
    mode="reschedule"
)
```

### ExternalTaskSensor — Wait for Another DAG
```python
from airflow.sensors.external_task import ExternalTaskSensor

wait_for_upstream = ExternalTaskSensor(
    task_id="wait_for_extract_dag",
    external_dag_id="bank_extract_pipeline",
    external_task_id="load_bronze",     # None = wait for whole DAG
    execution_delta=None,               # Same execution date
    timeout=7200,                       # 2 hours max
    mode="reschedule",
    poke_interval=60
)
```

### SQLSensor — Wait for Data
```python
from airflow.providers.common.sql.sensors.sql import SqlSensor

wait_for_data = SqlSensor(
    task_id="wait_for_bronze_data",
    conn_id="postgres_data_vault",
    sql="""
        SELECT COUNT(*) FROM bronze.raw_bank_marketing
        WHERE _run_date = '{{ ds }}'
    """,
    success=lambda count: count > 0,    # Callable — True = success
    poke_interval=120,
    timeout=3600,
    mode="reschedule"
)
```

---

## Sensor Modes

```python
# poke mode (default)
# Worker holds a slot the entire time — wastes resources
mode="poke"

# reschedule mode (recommended for long waits)
# Worker releases slot between checks — much more efficient
mode="reschedule"

# smart sensor (batch poke — advanced)
# Batches multiple sensor checks — most efficient
mode="smart"
```

---

## Hooks — Reusable Connections

```python
# Hooks give you a connection object to use inside PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def query_database(**context):
    # PostgresHook — uses connection stored in Airflow Connections
    hook = PostgresHook(postgres_conn_id="postgres_data_vault")

    # Get results as list of tuples
    records = hook.get_records("SELECT * FROM silver.bank_customers LIMIT 10")

    # Get as pandas DataFrame
    df = hook.get_pandas_df("SELECT * FROM silver.bank_customers")

    # Run SQL
    hook.run("UPDATE pipeline_audit SET status='running' WHERE run_date='{{ ds }}'")

    # Get SQLAlchemy engine (for pandas to_sql)
    engine = hook.get_sqlalchemy_engine()

    return len(df)

def upload_to_s3(**context):
    hook = S3Hook(aws_conn_id="aws_default")
    hook.load_file(
        filename="/outputs/report.csv",
        key=f"reports/{{ ds }}/report.csv",
        bucket_name="beatrice-data-lake",
        replace=True
    )
```

---

## Complete DAG with All Operator Types

```python
# dags/bank_marketing_pipeline_v2.py
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.operators.empty import EmptyOperator
from airflow.sensors.filesystem import FileSensor
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd

default_args = {
    "owner": "beatrice",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["beatiewakarima1@gmail.com"]
}

with DAG(
    dag_id="bank_marketing_v2",
    default_args=default_args,
    schedule_interval="0 5 * * 1-5",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["bank", "production"]
) as dag:

    # 1. Wait for source file
    wait_file = FileSensor(
        task_id="wait_for_source",
        filepath="/data/bank_marketing_{{ ds_nodash }}.csv",
        poke_interval=300,
        timeout=3600,
        mode="reschedule"
    )

    # 2. Extract to bronze
    def extract(**context):
        df = pd.read_csv(
            f"/data/bank_marketing_{context['ds_nodash']}.csv",
            sep=";"
        )
        hook = PostgresHook("postgres_data_vault")
        engine = hook.get_sqlalchemy_engine()
        df["_run_date"] = context["ds"]
        hook.run(f"DELETE FROM bronze.raw_bank_marketing WHERE _run_date='{context['ds']}'")
        df.to_sql("raw_bank_marketing", engine, schema="bronze",
                  if_exists="append", index=False)
        context["ti"].xcom_push(key="rows_extracted", value=len(df))
        return len(df)

    extract_task = PythonOperator(
        task_id="extract_to_bronze",
        python_callable=extract
    )

    # 3. Branch: full refresh Mondays, incremental otherwise
    def choose_strategy(**context):
        return "full_refresh" if context["execution_date"].weekday() == 0 else "incremental"

    branch = BranchPythonOperator(
        task_id="choose_strategy",
        python_callable=choose_strategy
    )

    # 4a. Full refresh
    full_refresh = BashOperator(
        task_id="full_refresh",
        bash_command="cd /opt/dbt && dbt build --full-refresh --target prod"
    )

    # 4b. Incremental
    incremental = BashOperator(
        task_id="incremental",
        bash_command="cd /opt/dbt && dbt build --target prod"
    )

    # 5. Join paths
    join = EmptyOperator(
        task_id="join",
        trigger_rule="none_failed_min_one_success"
    )

    # 6. Validate
    validate = PostgresOperator(
        task_id="validate",
        postgres_conn_id="postgres_data_vault",
        sql="""
            DO $$ BEGIN
                IF (SELECT COUNT(*) FROM gold.campaign_performance
                    WHERE report_date = '{{ ds }}') = 0
                THEN RAISE EXCEPTION 'Gold table empty for {{ ds }}!';
                END IF;
            END $$;
        """
    )

    # 7. Send report
    report = EmailOperator(
        task_id="send_report",
        to=["beatiewakarima1@gmail.com"],
        subject="✅ Bank Pipeline Complete — {{ ds }}",
        html_content="<h2>Pipeline complete for {{ ds }}</h2>"
    )

    # Dependencies
    wait_file >> extract_task >> branch
    branch >> [full_refresh, incremental] >> join >> validate >> report
```

---

## Quick Reference

```python
# Core operators
PythonOperator(task_id, python_callable, op_kwargs={})
BashOperator(task_id, bash_command)
PostgresOperator(task_id, postgres_conn_id, sql)
EmailOperator(task_id, to, subject, html_content)
BranchPythonOperator(task_id, python_callable)
EmptyOperator(task_id)  # Placeholder/join point

# Sensors
FileSensor(task_id, filepath, poke_interval, timeout, mode)
HttpSensor(task_id, http_conn_id, endpoint, response_check)
ExternalTaskSensor(task_id, external_dag_id, external_task_id)
SqlSensor(task_id, conn_id, sql, success)

# Hooks (inside PythonOperator)
PostgresHook(postgres_conn_id).get_pandas_df(sql)
PostgresHook(postgres_conn_id).run(sql)
S3Hook(aws_conn_id).load_file(filename, key, bucket_name)

# XCom
ti.xcom_push(key="name", value=data)
ti.xcom_pull(task_ids="task", key="name")
```

---

## Previous | Next
← [[01 - Introduction to Apache Airflow]] | → [[03 - Airflow Taskflow API and Best Practices]]
