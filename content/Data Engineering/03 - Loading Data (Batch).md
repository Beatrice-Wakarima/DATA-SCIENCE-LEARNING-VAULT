---
title: Loading Data (Batch)
tags: [data-engineering, loading, etl, batch]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# 📤 Loading Data (Batch)

> Loading is the process of writing extracted (and optionally transformed) data into your target storage. Getting this right — with idempotency, error recovery, and performance — separates production pipelines from scripts.

---

## Load Strategies

```
Full Load         — Replace entire target table every run
                    Simple but slow for large tables

Append            — Add new rows only
                    Fast but duplicates possible if run twice

Upsert (Merge)    — Insert new, update existing
                    Safe and idempotent

Incremental       — Load only changed data since last run
                    Fast and scalable

Partition Swap    — Replace specific partitions (date/month)
                    Very fast for time-series data
```

---

## Loading to PostgreSQL

```python
# src/load/postgres_loader.py
import pandas as pd
from sqlalchemy import create_engine, text
import logging
import os
from typing import Literal

logger = logging.getLogger(__name__)

class PostgresLoader:
    """Load DataFrames into PostgreSQL tables"""
    
    def __init__(self, db_url: str = None):
        url = db_url or os.getenv("TARGET_DB_URL")
        self.engine = create_engine(
            url,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True          # Test connections before use
        )
    
    def load(self,
             df: pd.DataFrame,
             table: str,
             schema: str = None,
             if_exists: Literal["replace","append","fail"] = "append",
             chunk_size: int = 5000) -> int:
        """Load DataFrame to PostgreSQL"""
        
        full_table = f"{schema}.{table}" if schema else table
        logger.info(f"Loading {len(df):,} rows → {full_table}")
        
        df.to_sql(
            name=table,
            con=self.engine,
            schema=schema,
            if_exists=if_exists,
            index=False,
            chunksize=chunk_size,
            method="multi"              # Batch INSERT (faster)
        )
        
        logger.info(f"✅ Loaded {len(df):,} rows to {full_table}")
        return len(df)
    
    def upsert(self,
               df: pd.DataFrame,
               table: str,
               unique_key: list,
               schema: str = None) -> dict:
        """Upsert — insert new rows, update existing"""
        
        full_table = f"{schema}.{table}" if schema else table
        
        # Stage data in temp table
        temp_table = f"temp_{table}_{os.getpid()}"
        df.to_sql(temp_table, self.engine, if_exists="replace",
                  index=False, chunksize=5000)
        
        # Build upsert SQL
        columns = df.columns.tolist()
        update_cols = [c for c in columns if c not in unique_key]
        
        key_match = " AND ".join(
            [f"target.{k} = source.{k}" for k in unique_key]
        )
        update_set = ", ".join(
            [f"{c} = source.{c}" for c in update_cols]
        )
        insert_cols = ", ".join(columns)
        insert_vals = ", ".join([f"source.{c}" for c in columns])
        
        upsert_sql = f"""
            INSERT INTO {full_table} ({insert_cols})
            SELECT {insert_vals} FROM {temp_table} source
            ON CONFLICT ({", ".join(unique_key)})
            DO UPDATE SET {update_set}
        """
        
        with self.engine.connect() as conn:
            result = conn.execute(text(upsert_sql))
            conn.execute(text(f"DROP TABLE IF EXISTS {temp_table}"))
            conn.commit()
        
        logger.info(f"✅ Upserted to {full_table}")
        return {"rows_processed": len(df)}
    
    def load_partitioned(self,
                          df: pd.DataFrame,
                          table: str,
                          partition_col: str,
                          schema: str = None) -> dict:
        """Load by partition — replaces each partition"""
        
        partitions = df[partition_col].unique()
        total_loaded = 0
        
        for partition_value in sorted(partitions):
            partition_df = df[df[partition_col] == partition_value]
            full_table = f"{schema}.{table}" if schema else table
            
            with self.engine.connect() as conn:
                # Delete existing partition
                conn.execute(text(f"""
                    DELETE FROM {full_table}
                    WHERE {partition_col} = :val
                """), {"val": str(partition_value)})
                conn.commit()
            
            # Insert new partition data
            partition_df.to_sql(table, self.engine, schema=schema,
                               if_exists="append", index=False,
                               chunksize=5000)
            
            total_loaded += len(partition_df)
            logger.info(f"Partition {partition_value}: "
                       f"{len(partition_df):,} rows")
        
        logger.info(f"✅ Partitioned load complete: {total_loaded:,} rows")
        return {"rows_loaded": total_loaded, "partitions": len(partitions)}
```

---

## Loading to Files (Data Lake)

```python
# src/load/file_loader.py
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class FileLoader:
    """Load DataFrames to file storage (local or cloud)"""
    
    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def load_parquet(self,
                     df: pd.DataFrame,
                     filename: str,
                     partition_cols: list = None) -> str:
        """Save as Parquet (best for analytics)"""
        filepath = self.base_path / filename
        
        if partition_cols:
            # Partitioned Parquet (like Hive partitioning)
            df.to_parquet(filepath, partition_cols=partition_cols,
                         index=False, compression="snappy")
        else:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            df.to_parquet(filepath, index=False, compression="snappy")
        
        size = self._get_size(filepath)
        logger.info(f"✅ Saved Parquet: {filepath} ({size})")
        return str(filepath)
    
    def load_csv(self, df: pd.DataFrame, filename: str) -> str:
        """Save as CSV"""
        filepath = self.base_path / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filepath, index=False)
        logger.info(f"✅ Saved CSV: {filepath}")
        return str(filepath)
    
    def load_dated(self, df: pd.DataFrame,
                   name: str, fmt: str = "parquet") -> str:
        """Save with date in filename (prevents overwrites)"""
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{date_str}.{fmt}"
        
        if fmt == "parquet":
            return self.load_parquet(df, filename)
        elif fmt == "csv":
            return self.load_csv(df, filename)
    
    def _get_size(self, path: Path) -> str:
        """Get human-readable file size"""
        size = path.stat().st_size if path.is_file() else \
               sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
```

---

## Idempotent Loading — Run Safely Multiple Times

```python
def load_idempotent(df: pd.DataFrame,
                    table: str,
                    run_date: str,
                    engine) -> int:
    """
    Idempotent load — safe to run multiple times.
    Delete today's data then reload fresh.
    Result is always the same regardless of how many times you run.
    """
    with engine.connect() as conn:
        # Step 1: Delete today's existing data
        deleted = conn.execute(text(f"""
            DELETE FROM {table}
            WHERE DATE(loaded_at) = :run_date
        """), {"run_date": run_date})
        
        logger.info(f"Deleted {deleted.rowcount} existing rows for {run_date}")
        conn.commit()
    
    # Step 2: Add run metadata
    df["loaded_at"] = run_date
    df["pipeline_run_id"] = os.getenv("AIRFLOW_RUN_ID", "manual")
    
    # Step 3: Load fresh data
    df.to_sql(table, engine, if_exists="append", index=False)
    
    logger.info(f"✅ Idempotent load: {len(df):,} rows for {run_date}")
    return len(df)
```

---

## Staging Pattern — Bronze to Silver

```python
# src/load/staging_loader.py
"""
Implements Medallion Architecture loading:
  Raw CSV → Bronze (as-is)
  Bronze → Silver (via dbt or Python transforms)
"""

import pandas as pd
from sqlalchemy import create_engine, text
import logging

logger = logging.getLogger(__name__)

class StagingLoader:
    """Load data through Bronze → Silver stages"""
    
    def __init__(self, engine):
        self.engine = engine
    
    def load_bronze(self, df: pd.DataFrame,
                    table: str, source_file: str) -> int:
        """Load raw data to Bronze layer — no transformation"""
        
        # Add metadata columns
        df["_source_file"] = source_file
        df["_loaded_at"] = pd.Timestamp.now()
        df["_pipeline_run"] = os.getenv("PIPELINE_RUN_ID", "manual")
        
        # Convert all to string — preserve raw data
        df = df.astype(str)
        df = df.replace("nan", None)
        
        # Load to bronze schema
        df.to_sql(
            name=table,
            con=self.engine,
            schema="bronze",
            if_exists="append",
            index=False,
            chunksize=5000
        )
        
        logger.info(f"🟤 Bronze: {len(df):,} rows → bronze.{table}")
        return len(df)
    
    def load_silver(self, df: pd.DataFrame,
                    table: str) -> int:
        """Load cleaned data to Silver layer"""
        
        df["_processed_at"] = pd.Timestamp.now()
        
        df.to_sql(
            name=table,
            con=self.engine,
            schema="silver",
            if_exists="append",
            index=False,
            chunksize=5000
        )
        
        logger.info(f"⚪ Silver: {len(df):,} rows → silver.{table}")
        return len(df)
    
    def validate_row_counts(self,
                             source_count: int,
                             table: str,
                             schema: str,
                             tolerance: float = 0.01) -> bool:
        """Validate loaded row count matches source"""
        
        with self.engine.connect() as conn:
            result = conn.execute(text(
                f"SELECT COUNT(*) FROM {schema}.{table}"
            ))
            loaded_count = result.scalar()
        
        diff_pct = abs(loaded_count - source_count) / source_count
        
        if diff_pct > tolerance:
            logger.error(
                f"Row count mismatch! Source: {source_count:,}, "
                f"Loaded: {loaded_count:,}, Diff: {diff_pct:.1%}"
            )
            return False
        
        logger.info(f"✅ Row count validated: {loaded_count:,} rows in "
                   f"{schema}.{table}")
        return True
```

---

## Load Audit Table

```sql
-- Track every pipeline load for observability
CREATE TABLE pipeline_audit (
    id              SERIAL PRIMARY KEY,
    pipeline_name   VARCHAR(100) NOT NULL,
    run_date        DATE NOT NULL,
    target_table    VARCHAR(100) NOT NULL,
    rows_extracted  INTEGER,
    rows_loaded     INTEGER,
    rows_rejected   INTEGER DEFAULT 0,
    status          VARCHAR(20) DEFAULT 'running',
    started_at      TIMESTAMP DEFAULT NOW(),
    completed_at    TIMESTAMP,
    error_message   TEXT,
    run_id          VARCHAR(100)
);
```

```python
def log_pipeline_run(engine, pipeline_name: str,
                     run_date: str, target_table: str,
                     rows_extracted: int, rows_loaded: int,
                     status: str = "success",
                     error_msg: str = None) -> int:
    """Log pipeline execution to audit table"""
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            INSERT INTO pipeline_audit
                (pipeline_name, run_date, target_table,
                 rows_extracted, rows_loaded, status,
                 completed_at, error_message)
            VALUES
                (:pipeline, :date, :table,
                 :extracted, :loaded, :status,
                 NOW(), :error)
            RETURNING id
        """), {
            "pipeline": pipeline_name,
            "date": run_date,
            "table": target_table,
            "extracted": rows_extracted,
            "loaded": rows_loaded,
            "status": status,
            "error": error_msg
        })
        audit_id = result.scalar()
        conn.commit()
    
    logger.info(f"Audit logged: ID={audit_id}, "
               f"{rows_loaded:,}/{rows_extracted:,} rows")
    return audit_id
```

---

## Quick Reference

```python
# Full load (replace)
df.to_sql("table", engine, if_exists="replace", index=False)

# Append
df.to_sql("table", engine, if_exists="append", index=False)

# Chunked (large datasets)
df.to_sql("table", engine, if_exists="append",
          index=False, chunksize=5000, method="multi")

# Upsert (PostgreSQL)
INSERT INTO table (...) SELECT ... FROM staging
ON CONFLICT (unique_key) DO UPDATE SET ...

# Parquet (best for analytics)
df.to_parquet("file.parquet", compression="snappy", index=False)

# Partitioned Parquet
df.to_parquet("folder/", partition_cols=["year", "month"])

# Idempotent pattern
DELETE WHERE date = run_date
INSERT fresh data for run_date
```

---

## Previous | Next
← [[02 - Data Sources and Extraction]] | → [[04 - Pipeline Orchestration with Airflow]]
