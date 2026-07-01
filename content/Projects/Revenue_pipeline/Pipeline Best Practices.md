 

**Scope:** What makes a data pipeline production-grade beyond security  

**Parent:** [[SPAERO_REVENUE_ANALYSIS]]  

**Tags:** #pipeline #dataengineering #bestpractices #production

  

---

  

## Overview

  

```

Security        ← keeps bad actors out

Everything below ← keeps the pipeline trustworthy, fast and maintainable

```

  

---

  

## 1. 🔁 Reliability

*"Does it run every time without manual intervention?"*

  

### What it means

```

Idempotency        ← same input always produces same output

Retry logic        ← transient failures retry automatically

Graceful failures  ← one bad file doesn't kill the whole run

Dependency checks  ← don't run transform before extract finishes

```

  

### Current status

| Pattern | Status |

|---|---|

| Idempotency (truncate-then-append) | ✔ |

| Retry logic | ✘ |

| Graceful per-file failure | ✔ |

| Dependency check (healthcheck) | ✔ |

  

### Add retry logic

  

```python

import time

  

def run_with_retry(func, retries=3, delay=5):

    for attempt in range(1, retries + 1):

        try:

            return func()

        except Exception as e:

            logging.warning(f"Attempt {attempt}/{retries} failed: {e}")

            if attempt == retries:

                raise

            time.sleep(delay)

```

  

---

  

## 2. 🔍 Observability

*"Can you tell what happened and when without reading logs line by line?"*

  

### Three pillars

  

```

Logging    ← structured, searchable, timestamped  ✔ (implemented)

Metrics    ← row counts, duration, success rate   ⚠ (partial)

Alerting   ← someone is notified when it breaks   ✘ (missing)

```

  

### Pipeline run log table

  

```sql

CREATE TABLE IF NOT EXISTS raw.pipeline_run_log (

    id               SERIAL PRIMARY KEY,

    run_started_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    run_finished_at  TIMESTAMP,

    status           TEXT,           -- 'running', 'success', 'failed'

    blocks_total     INT,

    blocks_success   INT,

    failed_block     TEXT,

    error_message    TEXT,

    duration_seconds NUMERIC(10,2)

);

```

  

### Check last 10 runs

  

```sql

SELECT

    status,

    blocks_total,

    blocks_success,

    duration_seconds,

    run_started_at,

    failed_block

FROM raw.pipeline_run_log

ORDER BY run_started_at DESC

LIMIT 10;

```

  

### Failure alerting (Gmail SMTP)

  

```python

import smtplib

from email.mime.text import MIMEText

  

def send_failure_alert(script_name, error_message):

    msg = MIMEText(f"""

    Pipeline failure detected.

  

    Script:  {script_name}

    Error:   {error_message}

    Time:    {pd.Timestamp.now()}

  

    Action: check docker logs spaero_elt

    """)

    msg['Subject'] = f"[SPAERO] Pipeline Failed — {script_name}"

    msg['From']    = os.getenv("ALERT_EMAIL")

    msg['To']      = os.getenv("ALERT_RECIPIENT")

  

    with smtplib.SMTP('smtp.gmail.com', 587) as server:

        server.starttls()

        server.login(os.getenv("ALERT_EMAIL"), os.getenv("ALERT_PASSWORD"))

        server.send_message(msg)

```

  

---

  

## 3. ✅ Data Quality

*"Is the data correct, not just present?"*

  

### Three levels

  

```

Level 1 — Completeness   ← all rows loaded, no nulls in key columns

Level 2 — Validity       ← values in expected ranges, correct types

Level 3 — Consistency    ← revenue = units × price, profit = revenue - cogs

```

  

### Business rule validation

  

```python

def validate_business_rules(df, table_name):

    errors = []

  

    if table_name == 'spaero_sales_sales_fact':

        neg_revenue = df[df['revenue'] < 0]

        if not neg_revenue.empty:

            errors.append(f"{len(neg_revenue)} rows with negative revenue")

  

        null_orders = df['order_id'].isnull().sum()

        if null_orders > 0:

            errors.append(f"{null_orders} null order IDs")

  

        future_dates = df[df['order_date'] > pd.Timestamp.today()]

        if not future_dates.empty:

            errors.append(f"{len(future_dates)} future order dates")

  

    if errors:

        for e in errors:

            logging.warning(f"[VALIDATION] {table_name}: {e}")

        return False

    return True

```

  

### Consistency check (SQL)

  

```sql

-- Profit must equal revenue minus COGS

SELECT

    order_id,

    revenue,

    cogs,

    calculated_profit,

    (revenue - cogs)                              AS expected_profit,

    ABS(calculated_profit - (revenue - cogs))     AS discrepancy

FROM int.stg_sales

WHERE ABS(calculated_profit - (revenue - cogs)) > 0.01

LIMIT 10;

```

  

### Schema drift detection

  

```python

EXPECTED_COLUMNS = {

    'spaero_sales_sales_fact': [

        'order_id', 'order_date', 'customer_id', 'product_id',

        'units_sold', 'manufacturing_price', 'target_sale_price',

        'gross_sales', 'discount_premium', 'revenue', 'cogs', 'profit'

    ],

    'spaero_sales_customer_dim': [

        'customer_id', 'segment', 'country', 'discount_premium_band'

    ],

    'employee_fact_sheet1': [

        'employee_id', 'name', 'start_date', 'tenure_(years)', 'department'

    ]

}

  

def check_schema_drift(df, table_name):

    expected = EXPECTED_COLUMNS.get(table_name)

    if not expected:

        return True

    actual  = list(df.columns)

    missing = [c for c in expected if c not in actual]

    extra   = [c for c in actual   if c not in expected]

    if missing:

        logging.error(f"[SCHEMA DRIFT] {table_name}: missing columns {missing}")

        sys.exit(1)

    if extra:

        logging.warning(f"[SCHEMA DRIFT] {table_name}: new columns detected {extra}")

    return True

```

  

### Row reconciliation

  

```python

def reconcile_row_count(engine, table_name, expected_count):

    with engine.connect() as conn:

        actual = conn.execute(

            text(f'SELECT COUNT(*) FROM raw."{table_name}"')

        ).scalar()

    if actual != expected_count:

        logging.error(

            f"[RECONCILIATION] raw.{table_name}: "

            f"expected {expected_count} rows, found {actual}"

        )

        sys.exit(1)

    logging.info(

        f"[RECONCILIATION] raw.{table_name}: {actual} rows confirmed ✔"

    )

```

  

---

  

## 4. ⚡ Performance

*"Does it finish in time for downstream consumers?"*

  

### What to measure

  

```

Extract time    ← how long to read Excel files

Load time       ← how long to write to raw.*

Transform time  ← how long each SQL block takes

Total runtime   ← must finish before Power BI refresh schedule

```

  

### Add timing to each block

  

```python

import time

  

start   = time.time()

# run block

elapsed = round(time.time() - start, 2)

logging.info(f"[TIMING] Block completed in {elapsed}s")

```

  

### Add indexes to raw tables

  

```sql

-- Add after loading raw tables — speeds up mart queries dramatically

CREATE INDEX IF NOT EXISTS idx_sales_date     ON raw.spaero_sales_sales_fact (order_date);

CREATE INDEX IF NOT EXISTS idx_sales_customer ON raw.spaero_sales_sales_fact (customer_id);

CREATE INDEX IF NOT EXISTS idx_sales_product  ON raw.spaero_sales_sales_fact (product_id);

```

  

---

  

## 5. 🛠️ Maintainability

*"Can someone else understand, fix and extend this pipeline?"*

  

### What it means

  

```

Code readability    ← clear names, comments on complex SQL

Configuration       ← no magic numbers hardcoded

Modularity          ← each block does one thing

Documentation       ← README + Obsidian notes  ✔

Version control     ← every change tracked in Git  ✔

```

  

### Move SQL to separate files (at scale)

  

```

scripts/

├── extract_load.py

├── transform.py

├── inspect_views.py

└── sql/

    ├── staging/

    │   ├── stg_customers.sql

    │   ├── stg_sales.sql

    │   └── stg_employees.sql

    ├── marts/

    │   ├── mart_annual_performance.sql

    │   └── mart_customer_sales.sql

    └── presentation/

        ├── vw_exec_kpi_scorecard.sql

        └── vw_customer_rfm.sql

```

  

Load dynamically:

  

```python

import pathlib

  

def load_sql(path):

    return pathlib.Path(path).read_text()

  

{

    "name": "Staging: Sales",

    "sql": load_sql("scripts/sql/staging/stg_sales.sql")

}

```

  

### Comment complex SQL

  

```sql

-- CAGR uses LN/EXP instead of POWER() because Postgres POWER()

-- requires matching numeric types. LN/EXP works on pure NUMERIC

-- avoiding the FLOAT/NUMERIC type conflict that breaks ROUND().

EXP(

    LN(actual_revenue::NUMERIC / base_revenue::NUMERIC)

    / NULLIF((year - base_year)::NUMERIC, 0)

) - 1

```

  

---

  

## 6. 🧪 Testability

*"How do you know a change didn't break something?"*

  

### Three test types

  

```

Unit tests        ← test individual Python functions

Integration tests ← test SQL produces expected output

Contract tests    ← test output schema matches Power BI expectations

```

  

### Integration tests

  

```python

# tests/test_pipeline.py

  

def test_mart_annual_performance_row_count(engine):

    result = engine.execute(

        "SELECT COUNT(*) FROM analytics.mart_annual_performance"

    ).scalar()

    assert result == 7, f"Expected 7 years, got {result}"

  

def test_no_negative_revenue(engine):

    result = engine.execute("""

        SELECT COUNT(*) FROM int.stg_sales

        WHERE revenue < 0

    """).scalar()

    assert result == 0, f"Found {result} rows with negative revenue"

  

def test_profit_reconciliation(engine):

    result = engine.execute("""

        SELECT COUNT(*) FROM int.stg_sales

        WHERE ABS(calculated_profit - (revenue - cogs)) > 0.01

    """).scalar()

    assert result == 0, f"Found {result} rows where profit does not reconcile"

  

def test_all_presentation_views_exist(engine):

    views = engine.execute("""

        SELECT viewname FROM pg_views

        WHERE schemaname = 'presentation'

    """).fetchall()

    view_names = [v[0] for v in views]

    assert 'vw_exec_kpi_scorecard' in view_names

    assert 'vw_customer_rfm' in view_names

    assert 'vw_capex_project_summary' in view_names

```

  

Run with:

  

```bash

docker compose run --rm elt_pipeline python -m pytest tests/ -v

```

  

---

  

## 7. 📈 Scalability

*"What happens when data grows 10x or 100x?"*

  

### Growth path

  

```

Now          Full refresh    (6,320 rows   — seconds)

10x growth   Full refresh    (63,200 rows  — minutes, still ok)

100x growth  Incremental     (630,000 rows — watermark only new rows)

1000x growth Partitioning    (6.3M rows    — partition by year/month)

```

  

### Incremental loading with watermark

  

```python

def get_watermark(engine, table_name):

    with engine.connect() as conn:

        result = conn.execute(text("""

            SELECT MAX(ingested_at)

            FROM raw.ingestion_log

            WHERE table_name = :table

            AND   run_mode   = 'full_refresh'

        """), {"table": table_name}).scalar()

    return result

  

# Filter to only new rows

last_load = get_watermark(engine, 'spaero_sales_sales_fact')

if last_load:

    df = df[df['order_date'] > pd.Timestamp(last_load)]

```

  

### Table partitioning (when data grows large)

  

```sql

-- Partition sales fact by year for faster queries

CREATE TABLE raw.spaero_sales_sales_fact_partitioned (

    LIKE raw.spaero_sales_sales_fact

) PARTITION BY RANGE (order_date);

  

CREATE TABLE raw.sales_2021

    PARTITION OF raw.spaero_sales_sales_fact_partitioned

    FOR VALUES FROM ('2021-01-01') TO ('2022-01-01');

```

  

---

  

## 8. ♻️ Recoverability

*"When it breaks, how quickly can you get back to a good state?"*

  

### Strategy

  

```

Backup before every run    ← pg_dump before pipeline starts

Raw layer preserved        ← transform failure never touches raw.*

Point-in-time restore      ← can go back to any previous state

```

  

### Pre-run backup in Docker CMD

  

```dockerfile

CMD ["sh", "-c",

    "pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME -F c \

     -f /tmp/pre_run_backup_$(date +%Y%m%d_%H%M%S).dump && \

     python extract_load.py && \

     python transform.py && \

     python inspect_views.py"]

```

  

### Manual restore

  

```bash

# Copy backup out of container

docker cp spaero_warehouse:/tmp/pre_run_backup.dump ./backups/

  

# Restore

docker exec -i spaero_warehouse pg_restore \

    -U your_user -d your_dbname -F c /tmp/pre_run_backup.dump

```

  

---

  

## 9. 🔗 Lineage & Auditability

*"Where did this number come from?"*

  

### Full lineage for Spaero

  

```

Excel file

  └─► raw.spaero_sales_sales_fact     (extract_load.py)

        └─► int.stg_sales              (transform block 04-05)

              └─► analytics.mart_annual_performance  (block 15)

                    └─► presentation.vw_exec_kpi_scorecard  (block 20)

                          └─► Power BI KPI card

```

  

### Add lineage columns to raw tables

  

```python

# In extract_load.py before df.to_sql()

df['_source_file']  = file_name

df['_loaded_at']    = pd.Timestamp.now()

df['_pipeline_run'] = run_id

```

  

---

  

## 10. 📚 Documentation

*"Can a new engineer understand and run this in one day?"*

  

### Checklist

  

```

README          ← setup + run instructions          ✔

Obsidian vault  ← architecture + decisions          ✔

SQL comments    ← explain complex logic inline      ⚠ partial

Data dictionary ← what each column means            ✘

Change log      ← what changed and why              ✘

```

  

### Data dictionary template

  

```markdown

| Column | Table | Type | Description | Example |

|---|---|---|---|---|

| order_id | stg_sales | VARCHAR(50) | Unique order identifier | ORD-00001 |

| calculated_profit | stg_sales | NUMERIC(15,2) | revenue - cogs | 45230.50 |

| rfm_segment | vw_customer_rfm | TEXT | RFM classification | Champions |

| npv | vw_capex_project_summary | NUMERIC(15,2) | Net Present Value at assigned discount rate | 11,270,000 |

```

  

---

  

## Priority Matrix

  

| Item | Impact | Effort | When |

|---|---|---|---|

| Data quality checks | High | Low | **Now** |

| Retry logic | High | Low | **Now** |

| Performance timing | Medium | Low | **Now** |

| Schema drift detection | High | Low | **Now** |

| Row reconciliation | High | Low | **Now** |

| Integration tests | High | Medium | **Soon** |

| Pipeline run log | Medium | Medium | **Soon** |

| Failure alerting | High | Medium | **Soon** |

| SQL files separation | Medium | Medium | Soon |

| Incremental loading | High | High | When data grows |

| Table partitioning | High | High | When data grows |

| Full lineage tracking | Medium | High | Enterprise only |

  

---

  

## Enterprise Readiness Score

  

| Area | Current | Target |

|---|---|---|

| Idempotent loads | ✔ | ✔ |

| Transaction safety | ✔ | ✔ |

| Retry logic | ✘ | Automatic 3× retry |

| Data validation | ✘ | Row-level business rules |

| Schema drift detection | ✘ | Column contract check |

| Row reconciliation | ✘ | Source vs target count |

| Pipeline run logging | ⚠ partial | Full run log table |

| Performance timing | ✘ | Per-block timing |

| Failure alerting | ✘ | Email on failure |

| Integration tests | ✘ | pytest suite |

| Incremental loading | ✘ | Watermark-based |

| Backup strategy | ✘ | Pre-run pg_dump |

| SQL organisation | ⚠ inline strings | Separate .sql files |

| Documentation | ✔ | ✔ |

  

---

  

## Summary

  

```

1.  Reliability      ← runs every time without intervention

2.  Observability    ← you know immediately when it doesn't

3.  Data Quality     ← numbers are correct not just present

4.  Performance      ← finishes before consumers need it

5.  Maintainability  ← someone else can fix it at 2am

6.  Testability      ← changes don't break things silently

7.  Scalability      ← grows with the data volume

8.  Recoverability   ← mistakes can be undone quickly

9.  Lineage          ← every number traceable to its source

10. Documentation    ← knowledge lives in the repo not in heads

```

  

> [!TIP]

> Security is the gate. Everything above is what keeps the pipeline trustworthy once you're through it.

  

---

  

## Related

  

- [[SPAERO_REVENUE_ANALYSIS]] — Parent project note

- [[transform]] — Where most of these patterns apply

- [[extract_load]] — Where validation and reconciliation live

- [[docker_setup]] — Where retry and alerting integrate