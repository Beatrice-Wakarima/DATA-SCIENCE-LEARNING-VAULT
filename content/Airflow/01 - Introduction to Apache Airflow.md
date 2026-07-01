---
title: Introduction to Apache Airflow
tags: [airflow, orchestration, data-engineering, basics]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# Introduction to Apache Airflow

> Apache Airflow is the industry-standard platform for programmatically authoring, scheduling, and monitoring data pipelines. It replaces fragile cron jobs with a fully observable, retry-capable, dependency-managed workflow system.

---

## Why Airflow?

```
Without Airflow (cron jobs):
  ❌ Task B runs even if Task A failed
  ❌ No visibility into what's running
  ❌ Failed jobs go unnoticed
  ❌ No retry logic
  ❌ No parallel execution
  ❌ No alerting
  ❌ Hard to test or version control

With Airflow:
  ✅ Dependencies enforced — Task B waits for Task A
  ✅ Beautiful UI showing every run
  ✅ Automatic retries with configurable backoff
  ✅ Email/Slack alerts on failure
  ✅ Parallel task execution
  ✅ DAGs are Python code — version controlled in Git
  ✅ SLA monitoring
  ✅ Backfill historical runs
```

---

## Airflow Core Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Airflow Components                   │
├──────────────┬──────────────┬───────────┬──────────────┤
│   Web Server │   Scheduler  │  Executor │   Metadata   │
│   (Flower UI)│  (DAG parser,│  (runs    │   Database   │
│   Port 8080  │   triggers)  │   tasks)  │  (PostgreSQL)│
└──────────────┴──────────────┴───────────┴──────────────┘
                                    ↓
                            Worker Nodes
                        (execute actual tasks)
```

**Components:**
- **Web Server** — Airflow UI at port 8080
- **Scheduler** — parses DAGs, triggers tasks based on schedule
- **Executor** — determines how tasks run (Local, Celery, Kubernetes)
- **Metadata DB** — stores DAG definitions, run history, task state (PostgreSQL recommended)
- **Workers** — processes that actually execute task code

---

## Key Concepts

```
DAG         Directed Acyclic Graph — your pipeline blueprint
            A Python file defining tasks and dependencies

Task        A single unit of work in a DAG
            Created by instantiating an Operator

Operator    A template for a task type
            PythonOperator, BashOperator, SQLOperator, etc.

Sensor      A special operator that waits for a condition
            FileSensor, HttpSensor, ExternalTaskSensor

Hook        Abstraction for external system connections
            PostgresHook, SnowflakeHook, S3Hook

Connection  Stored credentials for external systems
            Configured in UI: Admin → Connections

Variable    Key-value config stored in Airflow
            Configured in UI: Admin → Variables

XCom        Cross-communication between tasks
            Push/pull data between task instances

Pool        Limits concurrent task slots
            Created in UI: Admin → Pools

DAG Run     One execution of a DAG
            Identified by run_id and execution_date

Task Instance One execution of a task in a DAG Run
              Has state: queued, running, success, failed, skipped

Execution Date The logical date of the DAG run (not wall-clock time)
               Critical for backfilling and idempotent pipelines
```

---

## Executors

```
LocalExecutor       — Tasks run as subprocess on scheduler machine
                      Good for single-machine setups, development

CeleryExecutor      — Tasks distributed across worker machines
                      Good for production, many concurrent tasks

KubernetesExecutor  — Each task gets its own Kubernetes pod
                      Best for dynamic scaling, cloud-native

SequentialExecutor  — One task at a time (default, development only)
                      Never use in production
```

---

## Installation — Docker Compose (Recommended)

```bash
# Download official docker-compose.yaml
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'

# Create required directories
mkdir -p ./dags ./logs ./plugins ./config

# Set Airflow UID
echo -e "AIRFLOW_UID=$(id -u)" > .env

# Initialise the database
docker compose up airflow-init

# Start all services
docker compose up -d

# Access: http://localhost:8080
# Username: airflow
# Password: airflow
```

---

## Your First DAG

```python
# dags/my_first_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# ── Step 1: Default arguments ────────────────────────────
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

# ── Step 2: Define the DAG ───────────────────────────────
with DAG(
    dag_id="my_first_dag",
    default_args=default_args,
    description="My first Airflow pipeline",
    schedule_interval="@daily",
    catchup=False,
    tags=["tutorial"]
) as dag:

    # ── Step 3: Define tasks ─────────────────────────────

    def say_hello():
        print("Hello from Airflow!")
        return "success"

    def process_data(**context):
        # Access execution date
        execution_date = context["ds"]
        print(f"Processing data for: {execution_date}")

    # Python task
    task_hello = PythonOperator(
        task_id="say_hello",
        python_callable=say_hello
    )

    # Bash task
    task_bash = BashOperator(
        task_id="run_bash",
        bash_command="echo 'Running bash command on {{ ds }}'"
    )

    # Task with context
    task_process = PythonOperator(
        task_id="process_data",
        python_callable=process_data
    )

    # ── Step 4: Set dependencies ─────────────────────────
    task_hello >> task_bash >> task_process
```

---

## Schedule Intervals

```python
# Preset schedules
schedule_interval="@once"           # Run once only
schedule_interval="@hourly"         # Every hour
schedule_interval="@daily"          # Daily at midnight
schedule_interval="@weekly"         # Weekly on Sunday
schedule_interval="@monthly"        # First day of month

# Cron expressions
schedule_interval="0 5 * * *"       # Daily at 5 AM
schedule_interval="0 5 * * 1-5"     # Weekdays at 5 AM
schedule_interval="0 */4 * * *"     # Every 4 hours
schedule_interval="30 6 1 * *"      # Monthly on 1st at 6:30 AM
schedule_interval="0 6 * * 1"       # Every Monday at 6 AM

# Cron with timezone (Airflow 2.2+)
from pendulum import timezone
with DAG(
    dag_id="nairobi_pipeline",
    schedule_interval="0 5 * * *",
    start_date=datetime(2026, 1, 1, tzinfo=timezone("Africa/Nairobi"))
) as dag:
    pass

# Disable scheduling (manual trigger only)
schedule_interval=None
```

---

## Task States

```
queued    → Waiting for a worker slot
running   → Currently executing
success   → Completed successfully ✅
failed    → Raised an exception ❌
skipped   → Skipped due to branching
up_for_retry → Failed, waiting to retry
up_for_reschedule → Sensor waiting to poke again
removed   → Task definition changed
upstream_failed → Upstream task failed (trigger rule)
```

---

## Key DAG Parameters

```python
with DAG(
    dag_id="production_dag",            # Unique identifier
    description="What this DAG does",
    schedule_interval="0 5 * * *",      # When to run
    start_date=datetime(2026, 1, 1),    # When to start scheduling
    end_date=None,                      # When to stop (optional)
    catchup=False,                      # Don't backfill missed runs
    max_active_runs=1,                  # Only 1 concurrent run
    max_active_tasks=16,                # Max concurrent tasks
    dagrun_timeout=timedelta(hours=2),  # Fail run if takes too long
    tags=["production", "etl"],         # For filtering in UI
    doc_md="""                          # Documentation
    ## My Pipeline
    This pipeline does XYZ.
    """,
    default_args={
        "owner": "beatrice",
        "retries": 3,
        "retry_delay": timedelta(minutes=5),
        "retry_exponential_backoff": True,
        "max_retry_delay": timedelta(hours=1),
        "execution_timeout": timedelta(hours=2),
        "sla": timedelta(hours=3),
        "email_on_failure": True
    }
) as dag:
    pass
```

---

## Airflow UI — Key Pages

```
DAGs page          → List of all DAGs, toggle on/off, trigger manually
Graph view         → Visual representation of DAG and task dependencies
Grid view          → Calendar-style view of all runs
Gantt chart        → Timeline of task durations
Task logs          → Full stdout/stderr of each task execution
Admin → Connections → Store database credentials, API keys
Admin → Variables   → Store config values
Admin → Pools       → Manage task concurrency limits
```

---

## Quick Reference

```python
# DAG skeleton
with DAG(
    dag_id="name",
    schedule_interval="0 5 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)}
) as dag:
    t1 = PythonOperator(task_id="t1", python_callable=fn)
    t2 = BashOperator(task_id="t2", bash_command="echo hi")
    t1 >> t2

# Dependencies
t1 >> t2                    # t1 then t2
t1 >> [t2, t3]              # t2 and t3 in parallel after t1
[t1, t2] >> t3              # t3 after both t1 and t2
t1.set_downstream(t2)       # Same as t1 >> t2
t2.set_upstream(t1)         # Same as t1 >> t2

# CLI commands
airflow dags list
airflow dags trigger dag_id
airflow tasks test dag_id task_id 2026-05-20
airflow dags backfill dag_id --start-date 2026-01-01 --end-date 2026-05-01
```

---

## Previous | Next
← Start | → [[02 - Airflow Operators and Sensors]]
