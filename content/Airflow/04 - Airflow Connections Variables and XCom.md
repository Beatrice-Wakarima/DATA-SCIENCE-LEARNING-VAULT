---
title: Airflow Connections, Variables and XCom
tags: [airflow, connections, variables, xcom, configuration]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# 🔌 Airflow Connections, Variables & XCom

> Connections store credentials securely. Variables store configuration. XCom passes data between tasks. Together they make your DAGs configurable, secure, and data-driven.

---

## Connections — Storing Credentials

```
Connections store: host, port, login, password, schema, extra JSON
Used by: Hooks and Operators via conn_id
Storage: Airflow metadata DB (encrypted) or external secret backends
```

### Setting Up Connections in UI

```
Admin → Connections → Add Connection

PostgreSQL:
  Conn Id:    postgres_data_vault
  Conn Type:  Postgres
  Host:       postgres (or localhost)
  Login:      beatrice
  Password:   secret123
  Schema:     data_vault
  Port:       5432

Snowflake:
  Conn Id:    snowflake_data_vault
  Conn Type:  Snowflake
  Account:    xy12345.eu-west-1
  Login:      beatrice
  Password:   secret123
  Schema:     SILVER
  Extra:      {"warehouse": "ETL_WH", "database": "DATA_VAULT"}

AWS S3:
  Conn Id:    aws_default
  Conn Type:  Amazon Web Services
  Login:      AKIAIOSFODNN7EXAMPLE   (Access Key ID)
  Password:   wJalrXUtnFEMI/K7MDENG  (Secret Access Key)
  Extra:      {"region_name": "us-east-1"}

HTTP API:
  Conn Id:    bank_api
  Conn Type:  HTTP
  Host:       https://api.example.com
  Extra:      {"Authorization": "Bearer YOUR_TOKEN"}
```

### Connections via Environment Variables

```bash
# Set connections without the UI — great for Docker/Kubernetes
# Format: AIRFLOW_CONN_{CONN_ID_UPPER}=connection_uri

# PostgreSQL
export AIRFLOW_CONN_POSTGRES_DATA_VAULT='postgresql://beatrice:secret123@postgres:5432/data_vault'

# Snowflake
export AIRFLOW_CONN_SNOWFLAKE_DATA_VAULT='snowflake://beatrice:secret@xy12345.eu-west-1/DATA_VAULT/SILVER?warehouse=ETL_WH'

# AWS
export AIRFLOW_CONN_AWS_DEFAULT='aws://AKIAIO:wJalrX@/?region_name=us-east-1'

# In docker-compose.yml
services:
  airflow-scheduler:
    environment:
      AIRFLOW_CONN_POSTGRES_DATA_VAULT: 'postgresql://beatrice:${DB_PASSWORD}@postgres:5432/data_vault'
      AIRFLOW_CONN_SNOWFLAKE_DATA_VAULT: 'snowflake://beatrice:${SNOW_PASSWORD}@${SNOW_ACCOUNT}/DATA_VAULT/SILVER?warehouse=ETL_WH'
```

### Using Connections in Code

```python
from airflow.hooks.base import BaseHook
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Get connection object
conn = BaseHook.get_connection("postgres_data_vault")
print(conn.host)        # postgres
print(conn.login)       # beatrice
print(conn.password)    # secret123
print(conn.schema)      # data_vault

# Use via Hook (recommended)
hook = PostgresHook(postgres_conn_id="postgres_data_vault")
df = hook.get_pandas_df("SELECT * FROM silver.bank_customers LIMIT 10")

# Build connection string from connection
conn_str = hook.get_uri()
engine = hook.get_sqlalchemy_engine()
```

---

## Variables — Configuration Storage

```
Variables: key-value pairs stored in Airflow metadata DB
Use for: config values, thresholds, feature flags, file paths
NOT for: secrets (use Connections or secret backends for those)
```

### Setting Variables in UI

```
Admin → Variables → Add Variable

Key: batch_size          Value: 5000
Key: notification_emails Value: beatrice@gmail.com,manager@company.com
Key: data_path           Value: /data/bank_marketing.csv
Key: pipeline_config     Value: {"max_retries": 3, "timeout": 3600}
Key: slack_webhook       Value: https://hooks.slack.com/services/...
Key: db_schema           Value: silver
Key: enable_notifications Value: true
```

### Setting Variables via CLI

```bash
# Single variable
airflow variables set batch_size 5000
airflow variables set db_schema silver

# From JSON file
airflow variables import variables.json

# variables.json format:
# {
#   "batch_size": "5000",
#   "pipeline_config": "{\"max_retries\": 3}",
#   "notification_emails": "beatrice@gmail.com"
# }

# Export all variables
airflow variables export variables_backup.json
```

### Environment Variable Overrides

```bash
# Format: AIRFLOW_VAR_{VARIABLE_NAME_UPPER}
export AIRFLOW_VAR_BATCH_SIZE=5000
export AIRFLOW_VAR_DB_SCHEMA=silver
export AIRFLOW_VAR_DATA_PATH=/data/bank_marketing.csv
```

### Using Variables in DAGs

```python
from airflow.models import Variable

# In Python tasks
@task()
def configure_pipeline():
    # Get single variable with default
    batch_size = int(Variable.get("batch_size", default_var=5000))
    db_schema = Variable.get("db_schema", default_var="silver")
    data_path = Variable.get("data_path")

    # Get JSON variable (auto-deserialise)
    config = Variable.get("pipeline_config", deserialize_json=True)
    max_retries = config.get("max_retries", 3)

    # Get with sensitive flag (masks in UI)
    api_key = Variable.get("api_key", default_var=None)

    return {"batch_size": batch_size, "schema": db_schema}

# In Jinja templates (operator arguments)
bash_task = BashOperator(
    task_id="run_script",
    bash_command="python pipeline.py --batch={{ var.value.batch_size }}"
)

sql_task = PostgresOperator(
    task_id="run_sql",
    sql="SELECT * FROM {{ var.value.db_schema }}.bank_customers"
)
```

---

## XCom — Passing Data Between Tasks

```
XCom = Cross-Communication
Stored in Airflow metadata DB
Best for: small data (task status, row counts, file paths, config)
NOT for: large DataFrames (use files/S3/DB instead)
Limit: ~48KB per XCom value (varies by DB)
```

### Automatic XCom (Taskflow API)

```python
@dag(...)
def pipeline():
    @task()
    def extract() -> dict:
        # Return value is AUTOMATICALLY pushed to XCom
        return {"rows": 45211, "source": "bank_marketing.csv"}

    @task()
    def transform(data: dict) -> dict:
        # data is AUTOMATICALLY pulled from extract's XCom
        return {"clean_rows": data["rows"] - 261}

    @task()
    def load(stats: dict):
        print(f"Loading {stats['clean_rows']:,} rows")

    raw = extract()
    clean = transform(raw)
    load(clean)
```

### Manual XCom (Classic API)

```python
def extract(**context):
    rows = 45211
    filepath = "data/bank_marketing.csv"

    # Push multiple values
    ti = context["ti"]
    ti.xcom_push(key="row_count", value=rows)
    ti.xcom_push(key="filepath", value=filepath)
    ti.xcom_push(key="stats", value={"rows": rows, "cols": 17})

    # Return value also pushed as "return_value" key
    return rows

def transform(**context):
    ti = context["ti"]

    # Pull from specific task and key
    rows = ti.xcom_pull(task_ids="extract", key="row_count")
    filepath = ti.xcom_pull(task_ids="extract", key="filepath")
    stats = ti.xcom_pull(task_ids="extract", key="stats")

    # Pull return value (default key)
    return_val = ti.xcom_pull(task_ids="extract")

    # Pull from multiple tasks
    results = ti.xcom_pull(
        task_ids=["extract_customers", "extract_transactions"],
        key="return_value"
    )

    print(f"Got {rows} rows from {filepath}")
```

### XCom in Jinja Templates

```python
# Access XCom values directly in operator args
load_task = BashOperator(
    task_id="load",
    bash_command=(
        "python load.py "
        "--rows={{ ti.xcom_pull(task_ids='extract', key='row_count') }} "
        "--date={{ ds }}"
    )
)

# In SQL
sql_task = PostgresOperator(
    task_id="update_audit",
    sql="""
        INSERT INTO pipeline_audit (run_date, rows_processed)
        VALUES (
            '{{ ds }}',
            {{ ti.xcom_pull(task_ids='extract', key='row_count') }}
        )
    """
)
```

---

## Secret Backends — Production Credential Management

```python
# Instead of storing secrets in Airflow DB,
# use external secret managers

# ── AWS Secrets Manager ────────────────────────────────
# airflow.cfg:
[secrets]
backend = airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
backend_kwargs = {"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables"}

# Store in AWS Secrets Manager:
# airflow/connections/postgres_data_vault → connection URI
# airflow/variables/db_password → secret value

# ── HashiCorp Vault ────────────────────────────────────
[secrets]
backend = airflow.providers.hashicorp.secrets.vault.VaultBackend
backend_kwargs = {"connections_path": "connections", "variables_path": "variables", "mount_point": "airflow"}

# ── GCP Secret Manager ────────────────────────────────
[secrets]
backend = airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend
backend_kwargs = {"project_id": "my-gcp-project"}
```

---

## Practical Patterns

### Pattern 1: Config-Driven DAG

```python
from airflow.models import Variable

@dag(dag_id="config_driven_pipeline", ...)
def config_driven():

    @task()
    def get_config() -> dict:
        return {
            "source_path": Variable.get("source_data_path"),
            "target_schema": Variable.get("target_schema", "silver"),
            "batch_size": int(Variable.get("batch_size", 5000)),
            "run_dbt": Variable.get("enable_dbt", "true").lower() == "true",
            "notify_on_success": Variable.get("notify_success", "false") == "true"
        }

    @task()
    def run_pipeline(config: dict, run_date: str):
        logger.info(f"Running with config: {config}")
        df = pd.read_csv(config["source_path"])
        # Use config throughout...
        return {"rows": len(df)}

    config = get_config()
    result = run_pipeline(config, "{{ ds }}")

instance = config_driven()
```

### Pattern 2: Pass File Paths (Not Data)

```python
# ✅ Good — pass file path via XCom, read data in each task
@task()
def extract(run_date: str) -> str:
    filepath = f"/tmp/extract_{run_date}.parquet"
    df = pd.read_csv("source.csv")
    df.to_parquet(filepath)
    return filepath          # XCom carries path, not DataFrame!

@task()
def transform(input_path: str) -> str:
    output_path = input_path.replace("extract", "transform")
    df = pd.read_parquet(input_path)     # Read from file
    df_clean = clean(df)
    df_clean.to_parquet(output_path)
    return output_path

# ❌ Bad — DataFrames are too large for XCom
@task()
def extract_bad() -> pd.DataFrame:
    return pd.read_csv("source.csv")    # Will fail for large data!
```

---

## Quick Reference

```python
# Variables
from airflow.models import Variable
Variable.get("key", default_var="default")
Variable.get("key", deserialize_json=True)
Variable.set("key", "value")
# Jinja: {{ var.value.key_name }}

# Connections
from airflow.hooks.base import BaseHook
conn = BaseHook.get_connection("conn_id")
conn.host / conn.login / conn.password / conn.schema / conn.port

# XCom (classic)
ti.xcom_push(key="name", value=data)
ti.xcom_pull(task_ids="task_id", key="name")
ti.xcom_pull(task_ids="task_id")  # Gets return_value

# XCom (Taskflow — automatic)
@task() def t1() -> dict: return data
@task() def t2(input: dict): use(input)
t2(t1())  # XCom automatic!

# Environment variable overrides
AIRFLOW_CONN_{CONN_ID_UPPER}=connection_uri
AIRFLOW_VAR_{VARIABLE_NAME_UPPER}=value
```

---

## Previous | Next
← [[03 - Airflow Taskflow API and Best Practices]] | → [[05 - Airflow Production Deployment]]
