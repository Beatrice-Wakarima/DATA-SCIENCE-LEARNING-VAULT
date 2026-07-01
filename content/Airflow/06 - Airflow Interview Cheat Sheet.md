---
title: Airflow Interview Cheat Sheet
tags: [airflow, interview, cheatsheet, orchestration]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# 🎯 Airflow Interview Cheat Sheet

> Everything you need for Airflow interviews — concepts, architecture, scenario questions, common patterns, and a full command reference.

---

## Core Concept Q&A

**Q: What is Apache Airflow and why use it?**
A: Airflow is an open-source workflow orchestration platform that lets you programmatically author, schedule, and monitor pipelines as DAGs (Directed Acyclic Graphs). Advantages over cron: dependency management, retry logic, visual monitoring, alerting, backfilling, and version control in Git.

**Q: What is a DAG?**
A: A Directed Acyclic Graph — a collection of tasks with directional dependencies and no cycles. In Airflow, DAGs are Python files that define tasks and their execution order.

**Q: What is the difference between schedule_interval and execution_date?**
A: `schedule_interval` defines how often a DAG runs. `execution_date` is the logical date of a run — the start of the schedule interval, not the wall-clock time the run actually starts. For `@daily`, a run with `execution_date=2026-05-20` runs after midnight on May 21st, covering May 20th's data.

**Q: What does catchup=False do?**
A: Prevents Airflow from backfilling all missed runs between `start_date` and today when a DAG is first deployed. With `catchup=True` (default), Airflow creates a run for every missed interval — useful for historical data loads but dangerous for production ETL.

**Q: What is the Executor?**
A: The component that decides how tasks are run:
- `SequentialExecutor` — one task at a time, development only
- `LocalExecutor` — parallel tasks as subprocesses on the scheduler machine
- `CeleryExecutor` — distributes tasks across multiple worker machines
- `KubernetesExecutor` — each task gets its own Kubernetes pod

**Q: What is XCom?**
A: Cross-Communication — a mechanism for tasks to share small amounts of data (row counts, file paths, status). Stored in Airflow's metadata DB. Not for large DataFrames — use files, S3, or databases for that.

**Q: What is a Hook?**
A: An abstraction over a connection to an external system. `PostgresHook`, `SnowflakeHook`, `S3Hook` provide methods like `get_pandas_df()`, `run()`, `load_file()`. They use credentials stored in Airflow Connections.

**Q: What is the difference between a Sensor and an Operator?**
A: An Operator executes an action immediately. A Sensor polls a condition repeatedly until it's true (file exists, API returns 200, time reached), then succeeds. Sensors support `poke` (hold worker slot) and `reschedule` (release slot between checks) modes.

**Q: What is a trigger rule?**
A: Defines when a task runs based on its upstream tasks:
- `all_success` — default, runs if ALL upstreams succeeded
- `all_failed` — runs only if ALL failed
- `all_done` — runs regardless of outcome
- `one_success` — runs if ANY upstream succeeded
- `none_failed` — runs if no upstream failed (some may be skipped)
- `none_failed_min_one_success` — runs if no failures and at least one success (for branching)

**Q: What is the Taskflow API?**
A: The modern, decorator-based way to write DAGs (Airflow 2.0+). Uses `@dag` and `@task` decorators. XCom is automatic — return values are pushed, function arguments pull from previous task returns. Much less boilerplate than the classic API.

**Q: How does Airflow handle retries?**
A: Configured via `retries` and `retry_delay`. With `retry_exponential_backoff=True`, delay doubles each attempt. `max_retry_delay` caps the maximum wait. Tasks move to `up_for_retry` state between attempts.

---

## Architecture Questions

**Q: Describe the Airflow component lifecycle for a task execution.**
A:
1. Scheduler parses DAG files (every 30s by default)
2. Scheduler creates a DagRun when schedule triggers
3. Scheduler identifies tasks ready to run (dependencies met)
4. Scheduler sends task to Executor
5. Executor queues task (Celery: sends to Redis broker)
6. Worker picks up task from queue
7. Worker executes task code
8. Worker reports result to metadata DB
9. Scheduler reads state, triggers next eligible tasks

**Q: Where are DAG definitions stored?**
A: In Python files in the `dags/` folder. The Scheduler scans this folder on a configurable interval, parses Python files, and registers DAGs. Best practice: mount this folder via Docker volume, synced from Git.

**Q: How do you scale Airflow?**
A:
- More workers: `docker compose up --scale airflow-worker=N` or add Kubernetes nodes
- Larger workers: more CPUs/RAM per worker
- More Schedulers: Airflow 2.0+ supports multiple schedulers for HA
- Pool sizing: create pools to limit concurrent resource-intensive tasks

---

## Scenario Questions

**Q: A DAG has been running for 2 hours but usually completes in 20 minutes. How do you investigate?**
A:
1. Open Airflow UI → DAG → Graph view → find the stuck task (orange/running)
2. Click task → View Log — look for errors, infinite loops, or blocking I/O
3. Check if worker is still alive: `airflow tasks state dag_id task_id execution_date`
4. Check database/API the task is calling for slow queries or timeouts
5. If task is hung: clear the task instance and re-run with `airflow tasks clear`
6. Add `execution_timeout=timedelta(hours=1)` to prevent future hangs

**Q: How do you run a backfill for a new pipeline over 6 months of historical data?**
A:
```bash
airflow dags backfill bank_marketing_pipeline \
    --start-date 2025-11-01 \
    --end-date 2026-05-01 \
    --reset-dagruns   # Re-run even if previously succeeded
```
Ensure the DAG is idempotent first (safe to run multiple times for same date). Consider using `--max-active-runs` to limit concurrent backfill runs.

**Q: A task fails intermittently on network timeouts. How do you handle it?**
A:
```python
@task(
    retries=5,
    retry_delay=timedelta(minutes=1),
    retry_exponential_backoff=True,    # 1min, 2min, 4min, 8min, 16min
    max_retry_delay=timedelta(minutes=30)
)
def fetch_from_api():
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        raise AirflowException("Timeout — will retry")
```

**Q: How do you share a large DataFrame between tasks?**
A: Don't use XCom for DataFrames. Instead:
```python
@task()
def extract() -> str:           # Return file PATH, not data
    df = pd.read_csv("source.csv")
    path = "/tmp/extract_{{ ds }}.parquet"
    df.to_parquet(path)
    return path                 # XCom carries path (~100 bytes)

@task()
def transform(input_path: str) -> str:
    df = pd.read_parquet(input_path)   # Read from disk
    df_clean = clean(df)
    output_path = "/tmp/transform_{{ ds }}.parquet"
    df_clean.to_parquet(output_path)
    return output_path
```

**Q: Two DAGs need to share data. How do you do it?**
A: Three options:
1. `ExternalTaskSensor` — wait for the other DAG to complete, then read from shared storage (DB/S3)
2. Cross-DAG XCom pull: `ti.xcom_pull(dag_id="other_dag", task_ids="task", key="key")`
3. Dataset-driven scheduling (Airflow 2.4+): DAG B triggers when DAG A updates a Dataset

---

## Common Patterns

### Idempotent Pipeline
```python
@task()
def load_bronze(run_date: str) -> int:
    # Delete today's data first → insert → idempotent
    hook.run(f"DELETE FROM bronze.table WHERE date = '{run_date}'")
    df.to_sql("table", engine, schema="bronze", if_exists="append")
    return len(df)
```

### Conditional Branching
```python
def choose_branch(**context):
    return "full_refresh" if context["execution_date"].weekday() == 0 else "incremental"

branch = BranchPythonOperator(task_id="branch", python_callable=choose_branch)
full  = BashOperator(task_id="full_refresh", ...)
incr  = BashOperator(task_id="incremental", ...)
join  = EmptyOperator(task_id="join", trigger_rule="none_failed_min_one_success")
branch >> [full, incr] >> join
```

### Dynamic Tasks
```python
@task()
def get_tables() -> list:
    return ["customers", "transactions", "products"]

@task()
def process_table(table: str) -> str:
    return f"Processed {table}"

tables = get_tables()
process_table.expand(table_name=tables)  # One task per table, parallel!
```

### SLA Monitoring
```python
def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    logger.error(f"SLA missed for: {task_list}")
    # Send alert

with DAG(
    sla_miss_callback=sla_miss_callback,
    default_args={"sla": timedelta(hours=2)}
) as dag:
    pass
```

### Task Dependencies Patterns
```python
# Sequential
t1 >> t2 >> t3 >> t4

# Fan out
t1 >> [t2, t3, t4]

# Fan in
[t2, t3, t4] >> t5

# Complex
t1 >> [t2, t3]
t2 >> t4
t3 >> t4
t4 >> t5

# All at once
t1.set_downstream([t2, t3])
t5.set_upstream([t3, t4])
```

---

## Complete Command Reference

```bash
# ── DAG Management ────────────────────────────────────
airflow dags list                          # List all DAGs
airflow dags list-jobs --dag-id dag_id     # List jobs for a DAG
airflow dags show dag_id                   # Show DAG structure
airflow dags trigger dag_id                # Trigger manually
airflow dags trigger dag_id --conf '{"key":"val"}'  # With config
airflow dags pause dag_id                  # Pause scheduling
airflow dags unpause dag_id               # Resume scheduling
airflow dags delete dag_id                # Delete DAG metadata
airflow dags backfill dag_id \
    --start-date YYYY-MM-DD \
    --end-date YYYY-MM-DD                 # Backfill historical

# ── Task Management ───────────────────────────────────
airflow tasks list dag_id                 # List tasks in DAG
airflow tasks test dag_id task_id YYYY-MM-DD  # Test task locally
airflow tasks run dag_id task_id run_id   # Run specific task
airflow tasks clear dag_id \
    --start-date YYYY-MM-DD \
    --end-date YYYY-MM-DD                 # Clear task instances
airflow tasks state dag_id task_id execution_date  # Get task state
airflow tasks log dag_id task_id execution_date 1  # Get task log

# ── Connections ───────────────────────────────────────
airflow connections list                  # List all connections
airflow connections get conn_id           # Get connection details
airflow connections add conn_id \
    --conn-uri "postgresql://user:pass@host/db"
airflow connections delete conn_id

# ── Variables ─────────────────────────────────────────
airflow variables list                    # List all variables
airflow variables get key                 # Get variable value
airflow variables set key value           # Set variable
airflow variables delete key              # Delete variable
airflow variables import variables.json   # Import from file
airflow variables export variables.json   # Export to file

# ── Users ─────────────────────────────────────────────
airflow users list
airflow users create \
    --username admin --password admin \
    --firstname Beatrice --lastname Builds \
    --role Admin --email beatrice@gmail.com
airflow users delete --username username

# ── Pools ─────────────────────────────────────────────
airflow pools list
airflow pools set pool_name 3 "Description"
airflow pools delete pool_name

# ── Celery (Production) ───────────────────────────────
airflow celery worker                     # Start a worker
airflow celery flower                     # Start flower monitor
airflow celery stop                       # Stop worker

# ── DB ────────────────────────────────────────────────
airflow db init                           # Initialise DB
airflow db migrate                        # Apply migrations
airflow db clean --clean-before-timestamp "2026-01-01"  # Clean old records
```

---

## Key Configuration Reference

```ini
# airflow.cfg (key settings)

[core]
executor = CeleryExecutor
default_timezone = Africa/Nairobi
load_examples = False
dags_are_paused_at_creation = True
max_active_tasks_per_dag = 16
max_active_runs_per_dag = 1
dagbag_import_timeout = 30
dag_file_processor_timeout = 50

[database]
sql_alchemy_conn = postgresql+psycopg2://user:pass@host/db
sql_alchemy_pool_size = 5
sql_alchemy_max_overflow = 10

[scheduler]
dag_dir_list_interval = 30       # Scan dags/ every 30s
min_file_process_interval = 30   # Reprocess DAG file every 30s
catchup_by_default = False
max_dagruns_to_create_per_loop = 10

[celery]
broker_url = redis://redis:6379/0
result_backend = db+postgresql://user:pass@host/db
worker_concurrency = 16          # Tasks per worker

[webserver]
workers = 4                      # Gunicorn workers
secret_key = your-secret-key
expose_config = False
rbac = True

[smtp]
smtp_host = smtp.gmail.com
smtp_port = 587
smtp_user = beatrice@gmail.com
smtp_password = app_password
smtp_mail_from = beatrice@gmail.com
```

---

## Previous | Next
← [[05 - Airflow Production Deployment]] | → [[Airflow MOC]]
