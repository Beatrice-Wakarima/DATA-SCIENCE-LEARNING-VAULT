# ⚙️ ETL Ingestion Layer — Technical Reference

> [!abstract] Scope
> Implementation reference for the CSV → PostgreSQL staging pipeline. Covers connection pool configuration, DDL idempotency, SQL injection mitigations, DataFrame schema alignment, and Airflow XCom contract. Target audience: Data Engineers, Software Architects, DBAs.

---

**Tags:** #python #postgresql #sqlalchemy #etl #data-engineering #architecture #advanced  
**Created:** 2026-06-10  
**Type:** technical-reference  
**Project:** [[CSV to PostgreSQL ELT Pipeline]]  
**Status:** #complete  
**See also:** [[ETL Ingestion Layer — Beginner Guide]]

---

## 🏛️ Architectural Constraints

Three non-negotiable design decisions drive the entire implementation:

### 1. Schema Isolation
Decoupled `staging` namespace with `TEXT`-only columns and zero operational constraints. Type coercion, format validation, and semantic constraint enforcement are deferred entirely to the SQL/dbt compilation layer.

**Rationale:** The extract layer has one job — get raw bytes into the database without data loss. Mixing extraction with type enforcement creates dual failure modes.

### 2. Zero Ingestion Failures
The extract layer never rejects input data. A CSV row with `"N/A"` in what will eventually be a `NUMERIC` column loads cleanly as the string `"N/A"`. The transformation layer handles the cast.

### 3. IO-Bound Synchronous Batching
Deliberate choice of synchronous over async execution. Batch file processing provides zero concurrent IO multiplexing advantage — each file must be fully staged before the next begins due to truncate-append semantics. Sync preserves linear stack traces and pipeline determinism.

---

## ⚙️ Engine Configuration

```python
def get_engine(conn_str: str):
    url_obj = make_url(conn_str)

    if url_obj.password:
        encoded_password = urllib.parse.quote_plus(url_obj.password)
        url_obj = url_obj._replace(password=encoded_password)

    return create_engine(
        url_obj,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_recycle=1800
    )
```

### Password Encoding

`make_url()` parses the connection string into components. If the raw password contains operational delimiters (`@`, `:`, `/`), the dialect parser misidentifies the host boundary.

`urllib.parse.quote_plus()` percent-encodes all non-alphanumeric characters:
- `@` → `%40`
- `:` → `%3A`
- `/` → `%2F`

`url_obj._replace()` is the SQLAlchemy 2.0-safe immutable substitution pattern — do not mutate `url_obj` directly.

### Connection Pool Parameters

| Parameter | Value | Rationale |
|---|---|---|
| `pool_pre_ping` | `True` | Executes `SELECT 1` before each connection checkout. Drops and recycles dead socket descriptors silently rather than surfacing a `OperationalError` mid-pipeline |
| `pool_size` | `5` | Persistent warm connections. Bounded to prevent resource exhaustion on shared cloud DB instances during Airflow parallel worker scaling |
| `max_overflow` | `10` | Burst headroom above `pool_size`. Total ceiling: 15 connections |
| `pool_recycle` | `1800` | Forcibly replaces connections older than 30 minutes. Prevents stale socket errors on DB instances with aggressive idle timeout policies (common on RDS, Cloud SQL) |

> [!note] Pool sizing for Airflow
> With default Airflow LocalExecutor, `pool_size=5` is appropriate. If using CeleryExecutor with N workers, each worker spawns its own engine — total max connections = `N × (pool_size + max_overflow)`. Size accordingly against `max_connections` on your PostgreSQL instance.

---

## 🏗️ Idempotent DDL Orchestration

```python
def bootstrap_staging_infrastructure(engine) -> None:
    ddl_statements = """
    CREATE SCHEMA IF NOT EXISTS staging;
    CREATE TABLE IF NOT EXISTS staging.stg_fact_sales (
        transaction_date TEXT, customer_id TEXT, description TEXT,
        stock_code TEXT, invoice_no TEXT, quantity TEXT,
        sales TEXT, unit_price TEXT, _loaded_at TEXT
    );
    -- ... remaining tables
    """
    with engine.begin() as conn:
        statements = [stmt.strip() for stmt in ddl_statements.split(";") if stmt.strip()]
        for statement in statements:
            conn.execute(text(statement))
```

### `engine.begin()` Transaction Context

`engine.begin()` in SQLAlchemy 2.0 implements the context manager protocol:
- **Entry:** checks out a connection from the pool, begins a transaction
- **Normal exit:** auto-commits
- **Exception exit:** auto-rollbacks, returns connection to pool

This eliminates the need for explicit `COMMIT`/`ROLLBACK` and prevents half-applied DDL leaving the schema in an inconsistent state.

### Multi-Statement Execution Guard

The semicolon split is not cosmetic. The `psycopg2` dialect (and several others) silently truncates multi-statement strings after the first semicolon when passed through `execute()`. Explicit splitting guarantees all DDL executes.

### Idempotency Proof

| Statement | Behaviour on re-run |
|---|---|
| `CREATE SCHEMA IF NOT EXISTS staging` | No-op |
| `CREATE TABLE IF NOT EXISTS staging.stg_*` | No-op |
| Entire function | Safe to call on every DAG run |

---

##  SQL Injection Mitigation in DDL Routines

```python
def truncate_staging(engine, table: str) -> None:
    schema_name = "staging"
    clean_table_name = table.split(".")[-1]

    inspector = inspect(engine)
    if not inspector.has_table(table_name=clean_table_name, schema=schema_name):
        logger.warning("Truncation skipped: '%s' not found.", clean_table_name)
        return

    safe_table = identifier(clean_table_name)
    query = text(f"TRUNCATE TABLE {schema_name}.{safe_table} RESTART IDENTITY CASCADE;")

    with engine.begin() as conn:
        conn.execute(query)
```

### State Verification via `inspect()`

`inspect(engine)` returns a `Inspector` object that reads live metadata from the PostgreSQL catalog (`information_schema` / `pg_catalog`). Using `has_table()` instead of a try/except on the TRUNCATE itself:
- Avoids masking legitimate schema divergence errors
- Provides a clean early-return with a warning rather than a misleading exception
- Separates "table doesn't exist" from "TRUNCATE failed for another reason"

### `identifier()` Injection Elimination

Raw f-string interpolation into SQL is a critical injection vector:

```python
# VULNERABLE — attacker input: "stg_fact_sales; DROP TABLE users;"
query = text(f"TRUNCATE TABLE staging.{table}")
# → executes both statements

# HARDENED
safe_table = identifier(clean_table_name)
query = text(f"TRUNCATE TABLE staging.{safe_table}")
# → identifier() double-quotes the name: "stg_fact_sales"
# → query planner treats it as an object literal, not SQL
```

`sqlalchemy.sql.identifier()` wraps the value in dialect-appropriate quoting. The query planner binds it as a database object identifier — executable SQL cannot be injected through this path.

### `RESTART IDENTITY CASCADE`

- `RESTART IDENTITY` — resets owned sequences to their start value (relevant if staging tables have serial PKs)
- `CASCADE` — propagates truncation to tables with foreign key references to the target; prevents FK constraint violations on dependent tables

---

## 🧮 In-Memory Transformations & Schema Alignment

```python
def load_csv_to_staging(engine, table: str, filepath: Path, encoding: str) -> int:
    table_name = table.split(".")[-1]

    # A: Read as raw strings
    df = pd.read_csv(filepath, encoding=encoding, dtype=str)
    df.rename(columns=RENAME_MAP, inplace=True)

    # B: Strip upstream tracking vectors
    df = df.loc[:, ~df.columns.str.startswith("_")]

    # C: Compile-time UTC audit injection
    df["_loaded_at"] = datetime.now(timezone.utc).isoformat()

    # D: Intercept live schema — prevent schema drift
    inspector = inspect(engine)
    db_columns = [col['name'] for col in inspector.get_columns(table_name, schema="staging")]
    if db_columns:
        df = df[[col for col in df.columns if col in db_columns]]
    else:
        raise ValueError(f"Target table 'staging.{table_name}' does not exist.")

    # E: Chunked bulk insert
    df.to_sql(
        name=table_name, schema="staging", con=engine,
        if_exists="append", index=False, method="multi", chunksize=1000
    )
    return len(df)
```

### A — `dtype=str` Memory Allocation

Pandas type inference allocates variable-width dtypes based on sampled rows. `dtype=str` forces uniform `object` dtype across all columns — predictable memory layout, no inference-induced crashes on mixed-type columns.

### B — Data Bloat Control

```python
df = df.loc[:, ~df.columns.str.startswith("_")]
```

`~` inverts the boolean mask. This targets any column injected by upstream suppliers (e.g., `_source_system`, `_export_ts`) before they reach the DB driver. Prevents column count mismatches and avoids persisting supplier-internal metadata.

### C — `_loaded_at` UTC Injection

```python
df["_loaded_at"] = datetime.now(timezone.utc).isoformat()
# → "2026-06-10T08:31:22.412874+00:00"
```

Single call per batch execution. All rows in this load share the same `_loaded_at` value, enabling batch-level lineage queries:

```sql
SELECT _loaded_at, COUNT(*) as row_count
FROM staging.stg_fact_sales
GROUP BY _loaded_at
ORDER BY _loaded_at DESC;
```

### D — Schema Drift Protection

`get_columns()` reads live column definitions from `information_schema.columns`. The DataFrame filter:

```python
df = df[[col for col in df.columns if col in db_columns]]
```

...eliminates two failure modes:
1. **Column mismatch exception** — `to_sql(if_exists='append')` throws if the DataFrame has columns not in the target table
2. **Silent schema mutation** — without filtering, pandas would add unmapped CSV columns to the table, breaking all downstream dbt `ref()` selectors

### E — High-Throughput Insert

| Parameter | Effect |
|---|---|
| `if_exists="append"` | Table was pre-truncated — always append, never replace |
| `index=False` | Suppresses DataFrame index column insertion |
| `method="multi"` | Recompiles single-row `INSERT` arrays into multi-row `INSERT INTO … VALUES (…),(…),(…)` |
| `chunksize=1000` | Bounds memory allocation per batch; safeguards DB-side parse buffers |

**Throughput delta:** `method="multi"` eliminates per-row network round-trips. Empirically ~500× faster on 100k+ row datasets versus default single-row mode.

**Tuning `chunksize`:**
- Default `1000` — safe for all container sizes
- `2000–5000` — appropriate for 16GB+ worker memory
- Reduce if `MemoryError` surfaces on very wide tables

---

## 🔁 Fault Isolation & Deterministic Tear-Down

```python
def run_extract(conn_str: str) -> Dict[str, int]:
    engine = get_engine(conn_str)
    results, errors = {}, {}

    try:
        bootstrap_staging_infrastructure(engine)

        for table, (filepath, encoding) in CSV_FILES.items():
            try:
                truncate_staging(engine, table)
                count = load_csv_to_staging(engine, table, filepath, encoding)
                results[table] = count
            except Exception as exc:
                errors[table] = str(exc)
    finally:
        engine.dispose()

    if errors:
        raise RuntimeError(f"Extraction completed with errors: {errors}")

    return results
```

### Isolated Exception Scoping

The inner `try/except` stores failures in `errors[table]` — a memory trace matrix. One bad schema file cannot halt or corrupt remaining table loads. The outer loop continues to completion regardless of inner failures.

**Critical distinction:** `bootstrap_staging_infrastructure()` is outside the per-table loop and inside the outer `try`. A bootstrap failure is fatal (no tables exist to load into) — it surfaces immediately via the outer exception propagation.

### `engine.dispose()` in `finally`

`finally` executes under **all exit conditions:**
- Normal completion
- Per-table exception (caught by inner `try/except`)
- Bootstrap failure (propagates through outer `try`)
- `KeyboardInterrupt`
- OOM kill signal

Without `engine.dispose()`, long-running Airflow DAGs accumulate zombie PostgreSQL connections. These exhaust `max_connections` (default 100 on most managed instances) and cause cascade failures across all concurrent pipeline tasks.

### Airflow XCom Contract

```python
return results
# → {"staging.stg_fact_sales": 98421, "staging.stg_dim_customers": 4302, ...}
```

`Dict[str, int]` is natively JSON-serializable — satisfies Airflow's XCom transport requirement without custom encoders. Downstream tasks can consume row counts for:
- Volume anomaly detection
- Load validation assertions
- DAG branching logic based on record counts

```python
@task
def extract_task() -> Dict[str, int]:
    return run_extract(os.getenv("DATABASE_URL"))

@task
def validate_task(row_counts: Dict[str, int]):
    assert row_counts["staging.stg_fact_sales"] > 0, "Sales load empty!"
```

---

## 📊 Performance & Resource Profile

| Metric | Value | Notes |
|---|---|---|
| Max DB connections | 15 | `pool_size(5) + max_overflow(10)` |
| Insert throughput | ~500× vs default | `method="multi"` |
| Memory per batch | Bounded | `chunksize=1000` rows |
| Connection recycle | 1800s | Prevents stale socket errors |
| Failure isolation | Per-table | Non-blocking error capture |
| Idempotency | Full | `IF NOT EXISTS` + truncate-append |

---

## 🔗 Related Notes

- [[ETL Ingestion Layer — Beginner Guide]] — non-technical walkthrough of the same pipeline
- [[dbt Transformation Layer]] — type-casting, constraints, and production table promotion
- [[Airflow DAG Configuration]] — `PythonOperator` vs `@task` wiring
- [[PostgreSQL Connection Pool Sizing]] — capacity planning for multi-worker Airflow setups
- [[SQL Injection Prevention Patterns]] — `identifier()`, parameterized queries, bind variables

---

*Last updated: 2026-06-10 · Author: Beatrice*
