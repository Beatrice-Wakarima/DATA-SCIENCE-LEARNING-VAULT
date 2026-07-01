#  Building a Safe Postgres ETL Ingestion Script

> [!info] About This Note
> This note explains a Python script that safely extracts raw CSV files and loads them into a PostgreSQL staging layer. It's written for **all levels** — no prior database experience needed. Code examples are included throughout.

---

**Tags:** #python #postgresql #sqlalchemy #etl #data-engineering #beginner  
**Created:** 2026-06-10  
**Type:** guide  
**Project:** [[CSV to PostgreSQL ELT Pipeline]]  
**Status:** #complete

---

##  What This Script Does

```mermaid
graph LR
    A[📄 Raw CSV Files] -->|1. Read & Rename| B(🐼 Pandas DataFrame)
    B -->|2. Clean & Validate| C(⚙️ SQLAlchemy Engine)
    C -->|3. Load as TEXT| D[(🐘 Postgres Staging Schema)]
```

At a high level, the script does four things:

1. **Reads** raw CSV files into memory using pandas
2. **Cleans** column names and strips junk headers
3. **Connects** to PostgreSQL via a safe, pooled engine
4. **Loads** everything into staging tables as plain text strings

> [!tip] Why load as TEXT?
> Staging tables store everything as `TEXT` with zero constraints — no numbers, no dates, no rules. This means the script **never crashes** if a CSV has a bad value in a number column. We fix data types later, in SQL. Isolate first, clean second.

---

##  File & Table Map

The script loads four CSV files, each mapping to a staging table:

| CSV File | Staging Table | Encoding |
|---|---|---|
| `fact_sales.csv` | `staging.stg_fact_sales` | utf-8 |
| `dim_customers.csv` | `staging.stg_dim_customers` | utf-8 |
| `dim_products.csv` | `staging.stg_dim_products` | latin-1 |
| `state_region_mapping.csv` | `staging.stg_state_region` | utf-8 |

> [!note] What is `latin-1`?
> Some older files — especially exports from Excel — use `latin-1` encoding instead of `utf-8`. If you try to read a `latin-1` file as `utf-8`, Python throws a `UnicodeDecodeError`. Setting the correct encoding per file prevents this.

---

##  Step 1 — Global Setup & Imports

```python
import logging
import os
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine.url import make_url
from sqlalchemy.sql import identifier

logger = logging.getLogger(__name__)
load_dotenv()
```

### What each import does

| Import | Purpose |
|---|---|
| `pandas` | Reads CSV files and loads data into the database |
| `sqlalchemy` | Connects to PostgreSQL and runs SQL safely |
| `pathlib.Path` | Handles file paths across Windows and Linux |
| `dotenv` | Loads secrets from a hidden `.env` file |
| `urllib.parse` | Encodes special characters in passwords |
| `datetime / timezone` | Generates UTC timestamps for audit tracking |

> [!note] What is a `Path` object?
> Instead of hardcoding `"/home/beatrice/data/sales.csv"`, `pathlib.Path` builds the path dynamically so it works on any operating system. A path that works on Linux may break on Windows — `Path` handles that automatically.

---

##  Step 2 — Building the Database Engine

```python
def get_engine(conn_str: str):
    """Create SQLAlchemy engine with standardized URI and pooling."""
    try:
        url_obj = make_url(conn_str)

        if url_obj.password:
            encoded_password = urllib.parse.quote_plus(url_obj.password)
            url_obj = url_obj._replace(password=encoded_password)

        return create_engine(
            url_obj,
            pool_pre_ping=True,   # Checks if connection is alive before querying
            pool_size=5,          # Keeps 5 connections warm in the pool
            max_overflow=10,      # Allows up to 10 extra burst connections
            pool_recycle=1800     # Recycles idle connections every 30 minutes
        )
    except Exception as e:
        raise RuntimeError(f"Failed to initialize SQLAlchemy engine: {str(e)}")
```

### Why encode the password?

> [!warning] The Special Character Trap
> If your password is `Secret@123`, your connection string looks like:
> ```
> postgresql://user:Secret@123@localhost/mydb
> ```
> The computer gets confused — it can't tell which `@` separates the password from the host address!
>
> `urllib.parse.quote_plus()` converts `@` → `%40`, making it:
> ```
> postgresql://user:Secret%40123@localhost/mydb
> ```
> Now it parses correctly.

###  Connection Pool Settings Explained

A **connection pool** is like a team of pre-assigned messengers between your script and the database. Instead of hiring a new messenger for every single query, you keep a team standing by.

| Parameter | Value | Meaning |
|---|---|---|
| `pool_pre_ping` | `True` | Before using a connection, sends a `SELECT 1` to check it's still alive |
| `pool_size` | `5` | Maximum permanent connections kept open |
| `max_overflow` | `10` | Extra temporary connections allowed during peak load |
| `pool_recycle` | `1800` | Replaces connections older than 30 minutes (prevents stale sockets) |

> [!tip] Max concurrent connections
> `pool_size(5) + max_overflow(10) = **15 total connections maximum**`. This prevents overwhelming a cloud database during parallel Airflow worker runs.

---

##  Step 3 — Bootstrapping the Staging Infrastructure

```python
def bootstrap_staging_infrastructure(engine) -> None:
    """Executes DDL to ensure the staging schema and TEXT-only tables exist."""
    ddl_statements = """
    CREATE SCHEMA IF NOT EXISTS staging;

    CREATE TABLE IF NOT EXISTS staging.stg_fact_sales (
        transaction_date TEXT, customer_id TEXT, description TEXT,
        stock_code TEXT, invoice_no TEXT, quantity TEXT,
        sales TEXT, unit_price TEXT, _loaded_at TEXT
    );
    -- (other tables follow the same pattern)
    """
    with engine.begin() as conn:
        statements = [
            stmt.strip()
            for stmt in ddl_statements.split(";")
            if stmt.strip()
        ]
        for statement in statements:
            conn.execute(text(statement))
```

###  What is `engine.begin()`?

> [!tip] Transactions — All or Nothing
> `engine.begin()` opens a **database transaction**. Think of it like making a group of changes inside a protective bubble:
> - If **all** statements succeed → the changes are saved permanently (committed)
> - If **any** statement fails midway → all previous changes in that group are erased (rolled back)
>
> This means your database structure never gets stuck in a half-built state.

###  Why split on semicolons?

```python
statements = [stmt.strip() for stmt in ddl_statements.split(";") if stmt.strip()]
```

Some PostgreSQL drivers have a bug where if you send multiple SQL statements as one string, they silently ignore everything after the first semicolon. Splitting them manually and executing one by one guarantees all statements run.

###  What `IF NOT EXISTS` means

Every DDL statement uses `IF NOT EXISTS`, which makes this function **idempotent** — safe to run multiple times:

| Scenario | What happens |
|---|---|
| Schema/table doesn't exist | It gets created |
| Schema/table already exists | Nothing happens, no error |
| Script re-runs tomorrow | Still safe — no duplicates |

---

##  Step 4 — Truncating Stale Data Safely

```python
def truncate_staging(engine, table: str) -> None:
    """Safely verifies table existence, then truncates the staging table."""
    schema_name = "staging"
    clean_table_name = table.split(".")[-1]  # "stg_fact_sales" from "staging.stg_fact_sales"

    inspector = inspect(engine)
    if not inspector.has_table(table_name=clean_table_name, schema=schema_name):
        logger.warning("Truncation skipped: Table '%s' does not exist.", clean_table_name)
        return

    safe_table = identifier(clean_table_name)
    query = text(f"TRUNCATE TABLE {schema_name}.{safe_table} RESTART IDENTITY CASCADE;")

    with engine.begin() as conn:
        conn.execute(query)
```

###  Two Security Layers

**Layer 1 — `inspect()` existence check:**

Before wiping anything, the code asks the database directly: "does this table exist?" This uses SQLAlchemy's metadata catalog reader, which is more reliable than wrapping everything in a `try/except` and hoping for the best.

**Layer 2 — `identifier()` SQL injection protection:**

> [!bug] What is SQL Injection?
> If you build a query like this:
> ```python
> query = text(f"TRUNCATE TABLE staging.{table}")
> ```
> ...an attacker could pass in a value like `stg_fact_sales; DROP TABLE users;`
>
> Python would evaluate **both** statements, deleting your users table.
>
> `identifier()` wraps the name in proper database quoting so it's treated as a literal string — never as executable SQL:
> ```python
> safe_table = identifier(clean_table_name)
> # → "stg_fact_sales"  (double-quoted, not executable)
> ```

###  `RESTART IDENTITY CASCADE`

- `RESTART IDENTITY` — resets any auto-increment counters back to 1
- `CASCADE` — also clears any other tables that reference this one via foreign keys

---

##  Step 5 — Loading CSV Data into Staging

```python
def load_csv_to_staging(engine, table: str, filepath: Path, encoding: str) -> int:
    """Loads a CSV into a staging table. Returns number of rows written."""
    schema_name = "staging"
    table_name = table.split(".")[-1]

    # A: Read as raw text strings — no type guessing
    df = pd.read_csv(filepath, encoding=encoding, dtype=str)
    df.rename(columns=RENAME_MAP, inplace=True)

    # B: Drop external tracking columns (anything starting with "_")
    df = df.loc[:, ~df.columns.str.startswith("_")]

    # C: Inject audit timestamp
    df["_loaded_at"] = datetime.now(timezone.utc).isoformat()

    # D: Align DataFrame columns to actual database schema
    inspector = inspect(engine)
    db_columns = [col['name'] for col in inspector.get_columns(table_name, schema=schema_name)]
    if db_columns:
        df = df[[col for col in df.columns if col in db_columns]]
    else:
        raise ValueError(f"Target table '{schema_name}.{table_name}' does not exist.")

    # E: Stream to PostgreSQL in chunks
    df.to_sql(
        name=table_name,
        schema=schema_name,
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000,
    )

    return len(df)
```

### Breaking Down Each Step

#### A — `dtype=str` (No Type Guessing)

By default, pandas tries to be clever: it reads `"42"` as the integer `42`, and `"2023-01-15"` as a date. This is dangerous for a staging layer — if one row has `"N/A"` in a column pandas decided is numeric, the whole load crashes.

`dtype=str` forces **every column to be read as plain text**. No guessing, no crashes.

#### B — Dropping Tracking Columns

```python
df = df.loc[:, ~df.columns.str.startswith("_")]
```

Some upstream data suppliers add their own metadata columns like `_source_id` or `_export_timestamp`. This line drops any column whose name starts with `_` before loading, preventing conflicts with our own `_loaded_at` column.

#### C — Injecting `_loaded_at`

```python
df["_loaded_at"] = datetime.now(timezone.utc).isoformat()
# Result: "2026-06-10T08:31:22.412874+00:00"
```

Every single row gets a UTC timestamp showing exactly when it was loaded. This enables lineage queries like:
- *"Which batch loaded this record?"*
- *"Did yesterday's run overwrite today's?"*

> [!note] Why UTC?
> UTC (Coordinated Universal Time) is timezone-neutral. If your pipeline runs on a server in Frankfurt, your Airflow workers are in US-East, and your analyst is in Nairobi, they all see the same timestamp with zero confusion.

#### D — Schema Drift Protection

```python
db_columns = [col['name'] for col in inspector.get_columns(table_name, schema=schema_name)]
df = df[[col for col in df.columns if col in db_columns]]
```

This intercepts the **live database schema** and filters the DataFrame to only include columns that actually exist in the target table.

> [!warning] Without this step
> If your CSV supplier adds a new column (`promo_code`) that doesn't exist in your staging table, `to_sql(if_exists='append')` would either:
> - Throw a `column mismatch` exception and crash the load, OR
> - Silently add a new `promo_code` column to your staging table, breaking all downstream dbt models
>
> Schema drift protection prevents both scenarios.

#### E — Chunked Multi-Row Insert

```python
df.to_sql(
    if_exists="append",   # Table was pre-truncated — always append
    method="multi",       # Bulk multi-row INSERT
    chunksize=1000,       # Process 1,000 rows per batch
)
```

| Setting | Default Behaviour | With `method="multi"` |
|---|---|---|
| Insert pattern | One `INSERT` per row | One `INSERT` per 1,000 rows |
| Network round-trips for 50k rows | 50,000 | 50 |
| Approximate speed gain | baseline | **~500× faster** |

> [!tip] Tuning `chunksize`
> - `1000` is a safe default for most workloads
> - Increase to `2000–5000` if your container has 16GB+ RAM
> - Decrease if you're seeing memory errors on large files

---

## 🎛️ Step 6 — The Pipeline Controller

```python
def run_extract(conn_str: str) -> Dict[str, int]:
    """
    Main entry point. Returns {table: row_count}.
    Collects all errors and raises a summary at the end.
    """
    engine = get_engine(conn_str)
    results = {}
    errors = {}

    try:
        # Step 1: Ensure infrastructure exists
        bootstrap_staging_infrastructure(engine)

        # Step 2: Process each file sequentially
        for table, (filepath, encoding) in CSV_FILES.items():
            try:
                truncate_staging(engine, table)
                count = load_csv_to_staging(engine, table, filepath, encoding)
                results[table] = count
            except Exception as exc:
                errors[table] = str(exc)   # ← capture, don't crash

    finally:
        # ALWAYS runs — even if an exception occurred above
        engine.dispose()

    # Step 3: Raise a consolidated error summary if anything failed
    if errors:
        raise RuntimeError(f"Extraction completed with errors: {errors}")

    return results
```

### Execution Flow

```
run_extract(conn_str)
│
├── get_engine()                  → pooled, password-safe engine
├── bootstrap_staging_...()       → create schema + tables if missing
│
├── for each CSV file:
│   ├── truncate_staging()        → wipe stale data
│   ├── load_csv_to_staging()     → clean + stream load
│   └── [on error] errors[table] = str(exc)  → non-blocking capture
│
├── finally: engine.dispose()     → ALWAYS closes connections
│
└── if errors: raise RuntimeError → consolidated failure summary
```

### 🚫 Non-Blocking Error Capture

The inner `try/except` around each table load is intentional. If `stg_dim_products` fails due to a bad file encoding, the script:
1. Records the error in `errors["staging.stg_dim_products"]`
2. Continues processing `stg_state_region`
3. Reports all failures together at the end

Without this pattern, one bad file would silently skip all remaining files.

### 🛡️ `engine.dispose()` in `finally`

> [!warning] Why `finally` matters
> `finally` runs **no matter what** — whether the loop completes successfully, crashes halfway through, or even hits a keyboard interrupt. Without it:
> - SQLAlchemy's connection pool stays open
> - PostgreSQL accumulates zombie connections
> - Long-running Airflow DAGs eventually hit `max_connections` and fail
>
> Always dispose the engine in `finally`.

---

## ✅ Summary — Design Patterns Used

| Pattern | Where | Why |
|---|---|---|
| TEXT-only staging | DDL tables | Zero load failures from type mismatches |
| Idempotent DDL | `bootstrap_...()` | Safe to re-run at any time |
| Password URL encoding | `get_engine()` | Handles special characters safely |
| Connection pooling | `create_engine()` | Performance + resource control |
| `inspect()` table check | `truncate_staging()` | No blind DDL execution |
| `identifier()` sanitization | `truncate_staging()` | SQL injection prevention |
| `dtype=str` CSV read | `load_csv_to_staging()` | No type-guessing crashes |
| `_loaded_at` injection | `load_csv_to_staging()` | Row-level audit trail |
| Schema drift filter | `load_csv_to_staging()` | Prevents silent table mutation |
| `method="multi"` insert | `to_sql()` | ~500× throughput gain |
| Non-blocking error capture | `run_extract()` | One bad file doesn't kill the batch |
| `engine.dispose()` in `finally` | `run_extract()` | Always releases DB connections |

---

## 🚀 Local Dev Checklist

- [ ] Create `.env` file in project root
- [ ] Add `DATA_DIR=/path/to/your/csv/folder`
- [ ] Add `DATABASE_URL=postgresql://user:password@localhost:5432/dbname`
- [ ] Verify Docker / PostgreSQL is running
- [ ] Confirm CSV files match the names in `CSV_FILES` dict
- [ ] Run: `python -c "from extract import run_extract; run_extract(os.getenv('DATABASE_URL'))"`
- [ ] Hook `run_extract()` into Airflow `PythonOperator` or `@task` decorator

---

## 🔗 Related Notes

- [[dbt Transformation Layer]] — downstream type-casting and constraint enforcement
- [[Airflow DAG Setup]] — how to wire `run_extract()` as an Airflow task
- [[PostgreSQL Staging Schema Design]] — DDL reference for all staging tables
- [[SPAERO Revenue Analysis]] — earlier pipeline this pattern was adapted from

---

*Last updated: 2026-06-10 · Author: Beatrice*
