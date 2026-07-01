---
tags: [python, postgres, sqlalchemy, etl, data-engineering, beginner]
created: 2026-06-09
type: guide
---

#  Building a Safe Postgres ETL Ingestion Script with Python

This guide breaks down a Python script that safely grabs raw CSV files and streams them into a **PostgreSQL Staging Layer**. 

```mermaid
graph LR
    A[Raw CSV Files] -->|1. Extract & Clean| B(Pandas DataFrame)
    B -->|2. Sanitize & Verify| C(SQLAlchemy Engine)
    C -->|3. Load as TEXT| D[(Postgres Staging Schema)]
```

---

##  Why This Architecture Works
Before looking at the code, understand these two critical design choices:
1. **TEXT-Only Staging Layer:** We load everything into columns configured as `TEXT` with zero validation rules. This ensures your code **never crashes** during a load if an automated sensor accidentally dumps a word into a number column. We isolate dirty data first, then fix it later using SQL.
2. **Synchronous over Async:** For scripts that run automatically on a fixed timer (like batch jobs), sequential execution is safer, easier to debug, and doesn't waste CPU cycles like complex asynchronous architectures.

---

## Step-by-Step Code Walkthrough

### 1. Global Setup & Configurations
At the top of the file, we pull in tools from standard Python libraries and local environment configurations.

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
load_dotenv() # Loads sensitive variables from your hidden .env file
```

> [!NOTE] What is a `Path` object?
> Instead of using rigid text strings like `"/my_folder/data.csv"` which break if your script moves from Windows to Linux, `pathlib.Path` dynamically modifies directory slashes (`/` vs `\`) to match whatever computer is running the script.

---

### 2. Initializing the Database Engine safely
Connecting to a database requires an address called a connection string. This function constructs that engine cleanly.

```python
def get_engine(conn_str: str):
    """Create SQLAlchemy engine with standardized URI and pooling."""
    try:
        url_obj = make_url(conn_str)
        if url_obj.password:
            #  URL-encode passwords containing special characters like @, !, or :
            encoded_password = urllib.parse.quote_plus(url_obj.password)
            url_obj = url_obj._replace(password=encoded_password)
            
        return create_engine(
            url_obj,
            pool_pre_ping=True,      # Checks if the database is awake before trying to run a query
            pool_size=5,             # Keeps 5 persistent connections open to speed up batch inserts
            max_overflow=10,         # Allows building up to 10 connections if a massive burst occurs
            pool_recycle=1800        # Kills and replaces network paths older than 30 minutes
        )
    except Exception as e:
        raise RuntimeError(f"Failed to initialize SQLAlchemy engine: {str(e)}")
```

> [!WARNING] The Danger of Raw Passwords
> If your password is `Secret@123`, a connection string looks like `postgresql://user:Secret@123@localhost`. 
> The computer gets confused trying to figure out which `@` symbol divides your password from your server location! `urllib.parse.quote_plus` changes `@` into `%40` so your string parses correctly.

---

### 3. Automatically Bootstrapping the Infrastructure
To keep things automated, your code shouldn't break if your database is completely blank. This function builds your sandbox tables automatically.

```python
def bootstrap_staging_infrastructure(engine) -> None:
    """Executes DDL to ensure the staging schema and TEXT-only tables exist."""
    ddl_statements = """
    CREATE SCHEMA IF NOT EXISTS staging;
    CREATE TABLE IF NOT EXISTS staging.stg_fact_sales (
        transaction_date TEXT, customer_id TEXT, description TEXT, 
        stock_code TEXT, invoice_no TEXT, quantity TEXT, sales TEXT, unit_price TEXT, _loaded_at TEXT
    );
    """
    with engine.begin() as conn:
        # Split text commands by semicolons, strip whitespace, drop blank lines
        statements = [stmt.strip() for stmt in ddl_statements.split(";") if stmt.strip()]
        for statement in statements:
            conn.execute(text(statement))
```

> [!TIP] What does `engine.begin()` mean?
> It opens a **Database Transaction**. This acts like an "All-or-Nothing" insurance policy. If statement #1 runs perfectly, but statement #2 fails due to a network glitch, Python rolls back the clock and deletes statement #1 so your database structure never gets trapped half-baked.

---

### 4. Clearing Out Yesterday's Mess Safely
Because this is a "Full-Refresh" pattern, we wipe our staging playground tables completely clean right before pouring fresh data inside them.

```python
def truncate_staging(engine, table: str) -> None:
    """Safely verifies table existence using an Inspector, then truncates the staging table."""
    schema_name = "staging"
    clean_table_name = table.split(".")[-1] # Grabs 'stg_fact_sales' out of 'staging.stg_fact_sales'
    
    #  Check if the table even exists before trying to wipe it
    inspector = inspect(engine)
    if not inspector.has_table(table_name=clean_table_name, schema=schema_name):
        logger.warning("Truncation skipped: Table '%s' does not exist.", clean_table_name)
        return  
        
    #  Protect against SQL Injection
    safe_table = identifier(clean_table_name)
    query = text(f"TRUNCATE TABLE {schema_name}.{safe_table} RESTART IDENTITY CASCADE;")
    
    with engine.begin() as conn:
        conn.execute(query)
```

> [!BUG] Why use `identifier()`?
> Typing `f"TRUNCATE TABLE {table}"` directly creates a huge security vulnerability called **SQL Injection**. If an attacker tricks your input variable into reading `"stg_fact_sales; DROP TABLE users;"`, an f-string evaluates both commands and deletes your core application! Wrapping it in `identifier()` forces the database engine to treat the entire string as a harmless literal table label.

---

### 5. Cleaning and Shoveling the CSV File
This is the core workforce module. It opens the flat file, maps user-friendly names into clean column standards, and streams rows directly down to Postgres.

```python
def load_csv_to_staging(engine, table: str, filepath: Path, encoding: str) -> int:
    """Loads a CSV file into a staging table securely, enforcing schema constraints."""
    schema_name = "staging"
    table_name = table.split(".")[-1]
    
    # Step A: Load file into temporary memory as string rows
    df = pd.read_csv(filepath, encoding=encoding, dtype=str)
    df.rename(columns=RENAME_MAP, inplace=True)
    df = df.loc[:, ~df.columns.str.startswith("_")] # Wipe external tracking junk
    
    # Step B: Inject an automated system audit timestamp
    df["_loaded_at"] = datetime.now(timezone.utc).isoformat()

    # Step C: Match file columns with real database structure
    inspector = inspect(engine)
    db_columns = [col['name'] for col in inspector.get_columns(table_name, schema=schema_name)]
    if db_columns:
        df = df[[col for col in df.columns if col in db_columns]]
    else:
        raise ValueError(f"Target table '{schema_name}.{table_name}' does not exist.")

    # Step D: Stream rows to the database in chunks
    df.to_sql(
        name=table_name, schema=schema_name, con=engine,
        if_exists="append", index=False, method="multi", chunksize=1000
    )
    return len(df)
```

> [!SUCCESS] What does `method="multi"` do?
> Normally, saving data saves rows one-by-one, which triggers thousands of slow network calls. Setting `method="multi"` bundles rows into tight 1,000-unit packets (`chunksize=1000`), scaling up your pipeline insertion speed by over 500%!

---

### 6. The Pipeline Controller
This loop coordinates all the functions above. If data loading crashes on your third file, it won't kill the script instantly; it records the failure, processes everything else, and summarizes issues at the finish line.

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
                results[table] = count # Stores successful row count metrics
            except Exception as exc:
                errors[table] = str(exc) # Grabs failure message safely
    finally:
        # 🛡️ This block ALWAYS runs no matter what breaks during the loops
        engine.dispose()

    if errors:
        raise RuntimeError(f"Extraction task finished with system errors: {errors}")

    return results
```

---

##  Summary Checklist for Local Devs
* [ ] Create an environment file named exactly `.env`.
* [ ] Assign `DATA_DIR="/your/source/folder"` inside it.
* [ ] Verify that your database password strings don't conflict with database configurations.
* [ ] Hook `run_extract()` into your Airflow scheduler tasks or wrap it in a local engine trigger to begin processing.
