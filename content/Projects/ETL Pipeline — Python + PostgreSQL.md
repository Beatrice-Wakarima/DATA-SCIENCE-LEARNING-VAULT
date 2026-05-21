---
tags:
  - DataPipeline
  - python
dg-publish: true
---
An ETL pipeline that **Extracts** raw sales data from CSV,
**Transforms** it with Pandas, and **Loads** it into a local PostgreSQL database.

## Table of Contents

  

1. [Project Overview](#-project-overview)

2. [Tech Stack](#-tech-stack)

3. [Project Structure](#-project-structure)

4. [Prerequisites](#-prerequisites)

5. [Quick Start](#-quick-start)

6. [Step-by-Step Guide](#-step-by-step-guide)

7. [Pipeline Walkthrough](#-pipeline-walkthrough)

8. [Running the ETL](#-running-the-etl)

9. [Verification](#-verification)

10. [Troubleshooting](#-troubleshooting)

11. [Next Steps](#-next-steps)

  

## Project Overview

  This project demonstrates the **core ETL pattern** — the foundation of data engineering:

```

CSV File  ──► Extract ──► Transform ──► Load ──► PostgreSQL

              (read)      (clean +        (insert

                          enrich)         rows)

```

  **What it does:**

- Reads a raw sales CSV (`data/sales_data.csv`)

- Validates and cleans each row (drops nulls, coerces types)

- Computes a derived `total_amount = quantity × price` column

- Inserts only **new** rows into PostgreSQL (idempotent — safe to re-run)

- Writes structured logs to `logs/etl.log`

**Skills demonstrated:** Python scripting, Pandas data wrangling, psycopg2 / PostgreSQL,

incremental loading with unique constraints, structured logging.

  

## Tech Stack

  

| Layer       | Tool                        |

|-------------|-----------------------------|

| Language    | Python 3.10+                |

| Data layer  | Pandas 2.x                  |

| Database    | PostgreSQL 15               |

| DB driver   | psycopg2-binary             |

| ORM (opt.)  | SQLAlchemy 2.x              |

  

## Project Structure

  

```

etl_local/

├── data/

│   └── sales_data.csv          # Raw input data

├── scripts/

│   ├── db_connect.py           # Connection smoke-test

│   ├── setup_db.py             # One-time schema creation

│   ├── etl_pipeline.py         # Main ETL script (Extract → Transform → Load)

│   └── verify_data.py          # Post-load sanity check

├── logs/

│   └── etl.log                 # Auto-created on first run

├── requirements.txt

└── README.md

```

  

## Prerequisites

  

| Requirement | Version | Download |

|-------------|---------|----------|

| Python      | 3.10+   | [python.org](https://python.org) |

| PostgreSQL  | 15+     | [postgresql.org/download](https://www.postgresql.org/download/) |

| pgAdmin 4   | any     | bundled with PostgreSQL installer |

  

## Quick Start

  

```bash

# 1. Clone / download the project

cd etl_local

  

# 2. Create and activate virtual environment

python -m venv venv

source venv/bin/activate       # Mac / Linux

venv\Scripts\activate          # Windows

  

# 3. Install dependencies

pip install -r requirements.txt

  

# 4. Create the database in PostgreSQL (psql or pgAdmin)

#    CREATE DATABASE sales_db;

  

# 5. Set up the schema

python scripts/setup_db.py

  

# 6. Test your connection

python scripts/db_connect.py

  

# 7. Run the pipeline

python scripts/etl_pipeline.py

  

# 8. Verify the data

python scripts/verify_data.py

```

  
  

## Step-by-Step Guide

  

### 1 — Install PostgreSQL

  

Download and install PostgreSQL from [postgresql.org/download](https://www.postgresql.org/download/).

  

During installation:

- Note your **superuser password** (used as `postgres123` in config files — change it).

- Install **pgAdmin 4**

  

### 2 — Create the Database

  

Open **pgAdmin 4** → right-click **Databases** → **Create** → **Database**.

Name it `sales_db` and click **Save**.

  

Or use `psql`:

```sql

CREATE DATABASE sales_db;

```

  

### 3 — Set Up the Virtual Environment

  

```bash

python -m venv venv

source venv/bin/activate     # Mac/Linux

venv\Scripts\activate        # Windows

  

pip install -r requirements.txt

```

  

### 4 — Update Credentials

  

Open any script in `scripts/` and update the `DB_CONFIG` dict:

  

```python

DB_CONFIG = {

    "dbname":   "sales_db",

    "user":     "postgres",

    "password": "YOUR_ACTUAL_PASSWORD",   # ← change this

    "host":     "localhost",

    "port":     "5432",

}

```

  

### 5 — Create the Schema

  

```bash

python scripts/setup_db.py

```

  

This runs:

```sql

CREATE TABLE IF NOT EXISTS sales_data (

    sale_id      SERIAL PRIMARY KEY,

    product_name VARCHAR(100)   NOT NULL,

    quantity     INT            NOT NULL,

    price        NUMERIC(10, 2) NOT NULL,

    sale_date    DATE           NOT NULL,

    total_amount NUMERIC(12, 2) NOT NULL

);

-- + UNIQUE constraint on (product_name, sale_date)

```

  
  

## Pipeline Walkthrough

  

### Extract (`extract()`)

  

```python

df = pd.read_csv("data/sales_data.csv")

```

  

Reads the CSV into a Pandas DataFrame. No filtering yet — raw data in, raw data out.

  

### Transform (`transform()`)

  

```python

df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

df["price"]    = pd.to_numeric(df["price"],    errors="coerce")

df = df.dropna(subset=["product_name", "quantity", "price", "sale_date"])

df["total_amount"] = (df["quantity"] * df["price"]).round(2)

```

  

1. **Coerce** `quantity` and `price` to numeric — non-numeric values become `NaN`

2. **Drop** rows missing any required field

3. **Compute** `total_amount` as a derived column

  

### Load (`load()`)

  

```python

INSERT INTO sales_data (product_name, quantity, price, sale_date, total_amount)

VALUES (%s, %s, %s, %s, %s)

```

  

- Iterates row-by-row (suitable for small datasets; use `execute_batch` for large loads)

- Catches `UniqueViolation` → rolls back that row and increments `skipped` counter

- All other exceptions are logged and counted under `errors`

  

---

  

## Running the ETL

  

```bash

python scripts/etl_pipeline.py

```

  

Sample output:

```

2025-08-01 10:00:00 | INFO | ============================================================

2025-08-01 10:00:00 | INFO | ETL JOB STARTED

2025-08-01 10:00:00 | INFO | ============================================================

2025-08-01 10:00:00 | INFO | EXTRACT   reading .../data/sales_data.csv

2025-08-01 10:00:00 | INFO | EXTRACT   10 rows loaded

2025-08-01 10:00:00 | INFO | TRANSFORM  starting with 10 rows

2025-08-01 10:00:00 | INFO | TRANSFORM  10 rows ready for load

2025-08-01 10:00:00 | INFO | LOAD   connecting to PostgreSQL

2025-08-01 10:00:00 | INFO | ETL JOB COMPLETED | inserted=10 | skipped=0 | errors=0

```

  

Re-running the script on the same CSV will show `skipped=10 | inserted=0` — idempotent by design.

  

## Verification

  

```bash

python scripts/verify_data.py

```

  

Prints the latest rows and total revenue:

```

sale_id  product_name           qty      price    sale_date   total_amount

------------------------------------------------------------------------

10       Mousepad                10      350.00   2025-08-10       3500.00

 9       Laptop Stand             2     2200.00   2025-08-09       4400.00

...

```

  

You can also verify directly in pgAdmin or psql:

```sql

SELECT * FROM sales_data ORDER BY sale_id DESC LIMIT 10;

SELECT SUM(total_amount) AS total_revenue FROM sales_data;

```

  

---

  

## Troubleshooting

  

| Symptom | Likely Cause | Fix |

|---------|-------------|-----|

| `OperationalError: password authentication failed` | Wrong password in `DB_CONFIG` | Update `DB_CONFIG` in the script |

| `OperationalError: could not connect to server` | PostgreSQL not running | Start the service via pgAdmin or `pg_ctl start` |

| `FileNotFoundError: sales_data.csv` | Wrong working directory | Run scripts from the project root: `python scripts/etl_pipeline.py` |

| `ModuleNotFoundError: psycopg2` | Dependencies not installed | Activate venv, then `pip install -r requirements.txt` |

| Duplicate rows on re-run | Expected behaviour | Rows are intentionally skipped — check `skipped` counter in output |

  
  

## Next Steps
  

- **Bigger datasets** — swap the sample CSV for a Kaggle dataset

- **Scheduling** — use Python's `schedule` library or cron for daily runs

- **Dockerized version** — see the companion project `etl_docker/` for Airflow orchestration

- **Data warehouse** — extend the load step to target BigQuery, Redshift, or Snowflake

- **Dashboard** — connect Power BI or Grafana to `sales_db` for live reporting

  

*Built to demonstrate core ETL skills: data extraction, transformation, incremental loading, and structured logging.*