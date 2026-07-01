---
title: Snowflake with dbt and Python
tags: [snowflake, dbt, python, data-engineering, production]
created: 2026-05-20
up:: [[Snowflake MOC]]
---

# 🔧 Snowflake with dbt & Python

> This note brings Snowflake into your production stack — connecting it to dbt for transformations, Python for pipelines, Airflow for orchestration, and Power BI for reporting. This is the full modern data stack.

---

## The Modern Stack with Snowflake

```
CSV/API/DB
    ↓ Python (extraction + raw load)
Snowflake BRONZE
    ↓ dbt (transformations + tests)
Snowflake SILVER → GOLD
    ↓ Power BI / FastAPI
Dashboards + APIs
    ↑
Airflow (orchestrates everything)
```

---

## dbt Profile for Snowflake

```yaml
# ~/.dbt/profiles.yml
bank_marketing:
  target: dev
  outputs:
    
    dev:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"    # xy12345.eu-west-1
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      role: DBT_TRANSFORMER
      warehouse: ETL_WH
      database: DATA_VAULT
      schema: DBT_DEV                                   # Dev uses separate schema
      threads: 4
      client_session_keep_alive: false
    
    prod:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      role: DBT_TRANSFORMER
      warehouse: ETL_WH
      database: DATA_VAULT
      schema: SILVER                                    # Prod writes to SILVER
      threads: 8
      query_tag: "dbt_production"                       -- Tag queries for monitoring
```

---

## dbt_project.yml for Snowflake

```yaml
# dbt_project.yml
name: 'bank_marketing'
version: '1.0.0'

profile: 'bank_marketing'

models:
  bank_marketing:
    staging:
      +materialized: view
      +schema: STAGING
      +snowflake_warehouse: ETL_WH
    
    intermediate:
      +materialized: ephemeral
    
    marts:
      +materialized: table
      +schema: GOLD
      +snowflake_warehouse: BI_WH           # BI warehouse for mart builds
      +cluster_by: ['_run_date']            # Auto-cluster mart tables
      
      finance:
        +materialized: incremental
        +unique_key: ['report_date', 'job', 'balance_segment']
        +incremental_strategy: merge
```

---

## dbt Models for Snowflake

```sql
-- models/staging/stg_bank_marketing.sql
-- Snowflake-specific: use TRY_CAST for safe type conversion

{{
    config(
        materialized='view',
        schema='STAGING'
    )
}}

SELECT
    TRY_CAST(age AS NUMBER(3))                              AS age,
    TRIM(LOWER(job))                                        AS job,
    TRIM(LOWER(marital))                                    AS marital,
    TRIM(LOWER(education))                                  AS education,
    TRY_CAST(balance AS DECIMAL(12,2))                      AS balance,

    CASE
        WHEN TRY_CAST(balance AS NUMBER) > 10000    THEN 'high'
        WHEN TRY_CAST(balance AS NUMBER) > 1000     THEN 'medium'
        WHEN TRY_CAST(balance AS NUMBER) >= 0       THEN 'low'
        ELSE 'negative'
    END                                                     AS balance_segment,

    IFF(LOWER(TRIM(y)) = 'yes', TRUE, FALSE)               AS subscribed,

    -- Snowflake-specific: use CONVERT_TIMEZONE
    CONVERT_TIMEZONE('UTC', 'Africa/Nairobi', _loaded_at)   AS loaded_at_eat,
    _run_date

FROM {{ source('bronze', 'RAW_BANK_MARKETING') }}
WHERE TRY_CAST(age AS NUMBER) BETWEEN 18 AND 95
  AND balance IS NOT NULL
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY age, job, balance, y
    ORDER BY _loaded_at DESC
) = 1   -- Remove duplicates using Snowflake QUALIFY
```

```sql
-- models/marts/fct_campaign_performance.sql
-- Snowflake incremental with MERGE strategy

{{
    config(
        materialized='incremental',
        unique_key=['report_date', 'job', 'balance_segment'],
        incremental_strategy='merge',
        cluster_by=['report_date'],
        schema='GOLD',
        snowflake_warehouse='BI_WH'
    )
}}

SELECT
    CURRENT_DATE()                                          AS report_date,
    job,
    education,
    balance_segment,
    age_segment,
    COUNT(*)                                                AS total_contacts,
    SUM(IFF(subscribed, 1, 0))                             AS subscriptions,
    ROUND(100.0 * SUM(IFF(subscribed, 1, 0)) / NULLIF(COUNT(*), 0), 2)
                                                            AS conversion_rate,
    ROUND(AVG(balance), 2)                                 AS avg_balance,
    ROUND(MEDIAN(balance), 2)                              AS median_balance,
    CURRENT_TIMESTAMP()                                     AS _refreshed_at

FROM {{ ref('stg_bank_marketing') }}

{% if is_incremental() %}
WHERE _run_date >= (SELECT MAX(report_date) - 3 FROM {{ this }})
{% endif %}

GROUP BY 1, 2, 3, 4, 5
```

---

## Python + Snowflake Pipeline

```python
# pipeline/snowflake_pipeline.py
"""
Complete ETL pipeline: CSV → Snowflake Bronze → dbt → Gold
"""
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import subprocess
import logging
import os
from datetime import date

logger = logging.getLogger(__name__)

class SnowflakePipeline:

    def __init__(self):
        self.conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse="ETL_WH",
            database="DATA_VAULT",
            schema="BRONZE",
            session_parameters={
                "QUERY_TAG": "python_pipeline",
                "TIMEZONE": "Africa/Nairobi"
            }
        )
        self.cursor = self.conn.cursor()

    def extract(self, filepath: str) -> pd.DataFrame:
        """Extract from CSV"""
        logger.info(f"Extracting: {filepath}")
        df = pd.read_csv(filepath, sep=";")
        logger.info(f"Extracted {len(df):,} rows")
        return df

    def load_bronze(self, df: pd.DataFrame,
                    run_date: str) -> int:
        """Load raw data to Snowflake Bronze"""
        logger.info("Loading to Bronze...")

        # Add metadata
        df = df.copy()
        df.columns = [c.upper().replace('.', '_') for c in df.columns]
        df["_SOURCE_FILE"] = os.getenv("DATA_PATH", "bank_marketing.csv")
        df["_RUN_DATE"] = run_date

        # Idempotent: delete today's data first
        self.cursor.execute(f"""
            DELETE FROM DATA_VAULT.BRONZE.RAW_BANK_MARKETING
            WHERE _RUN_DATE = '{run_date}'
        """)

        # Load DataFrame
        success, nchunks, nrows, _ = write_pandas(
            conn=self.conn,
            df=df,
            table_name="RAW_BANK_MARKETING",
            schema="BRONZE",
            database="DATA_VAULT",
            overwrite=False,
            chunk_size=10000
        )

        logger.info(f"✅ Bronze: {nrows:,} rows loaded")
        return nrows

    def run_dbt(self, target: str = "prod") -> bool:
        """Run dbt transformations"""
        logger.info(f"Running dbt (target={target})...")

        result = subprocess.run(
            ["dbt", "build", "--target", target, "--select", "staging+"],
            capture_output=True,
            text=True,
            cwd="/opt/dbt"
        )

        if result.returncode == 0:
            logger.info("✅ dbt build successful")
            return True
        else:
            logger.error(f"❌ dbt failed:\n{result.stderr}")
            return False

    def validate_gold(self) -> dict:
        """Validate gold layer after dbt run"""
        self.cursor.execute("""
            SELECT
                COUNT(*) AS total_rows,
                SUM(total_contacts) AS total_contacts,
                ROUND(AVG(conversion_rate), 2) AS avg_conversion_rate,
                MAX(_refreshed_at) AS last_refresh
            FROM DATA_VAULT.GOLD.CAMPAIGN_PERFORMANCE
        """)
        row = self.cursor.fetchone()
        stats = {
            "total_rows": row[0],
            "total_contacts": row[1],
            "avg_conversion_rate": row[2],
            "last_refresh": str(row[3])
        }
        logger.info(f"✅ Gold validated: {stats}")
        return stats

    def run(self, filepath: str) -> dict:
        """Run complete pipeline"""
        run_date = str(date.today())
        logger.info(f"🚀 Starting pipeline for {run_date}")

        try:
            # 1. Extract
            df = self.extract(filepath)

            # 2. Load Bronze
            bronze_rows = self.load_bronze(df, run_date)

            # 3. dbt transformations
            dbt_success = self.run_dbt()
            if not dbt_success:
                raise Exception("dbt build failed")

            # 4. Validate
            stats = self.validate_gold()

            logger.info(f"✅ Pipeline complete!")
            return {
                "status": "success",
                "run_date": run_date,
                "bronze_rows": bronze_rows,
                "gold_stats": stats
            }

        except Exception as e:
            logger.error(f"❌ Pipeline failed: {e}")
            raise
        finally:
            self.conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s")

    pipeline = SnowflakePipeline()
    result = pipeline.run("data/bank_marketing.csv")
    print(result)
```

---

## Airflow DAG for Snowflake + dbt

```python
# dags/snowflake_dbt_pipeline.py
from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.operators.bash import BashOperator
from airflow.decorators import task
from datetime import datetime, timedelta

default_args = {
    "owner": "beatrice",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["beatiewakarima1@gmail.com"]
}

with DAG(
    dag_id="snowflake_dbt_pipeline",
    default_args=default_args,
    schedule_interval="0 5 * * 1-5",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["snowflake", "dbt", "production"]
) as dag:

    # Check Snowflake connection
    check_connection = SnowflakeOperator(
        task_id="check_snowflake_connection",
        sql="SELECT CURRENT_VERSION(), CURRENT_TIMESTAMP()",
        snowflake_conn_id="snowflake_data_vault"
    )

    # Source freshness check
    check_bronze_freshness = SnowflakeOperator(
        task_id="check_bronze_freshness",
        sql="""
            SELECT CASE
                WHEN MAX(_loaded_at) < DATEADD(HOUR, -2, CURRENT_TIMESTAMP())
                THEN iff(1=1, null, null)  -- Force error if stale
            END
            FROM DATA_VAULT.BRONZE.RAW_BANK_MARKETING
        """,
        snowflake_conn_id="snowflake_data_vault"
    )

    # Run dbt staging
    dbt_staging = BashOperator(
        task_id="dbt_staging",
        bash_command=(
            "cd /opt/dbt && "
            "dbt build --select staging --target prod "
            "--vars '{run_date: {{ ds }}}'"
        )
    )

    # Run dbt marts
    dbt_marts = BashOperator(
        task_id="dbt_marts",
        bash_command=(
            "cd /opt/dbt && "
            "dbt build --select marts --target prod"
        )
    )

    # Validate gold layer
    validate_gold = SnowflakeOperator(
        task_id="validate_gold",
        sql="""
            SELECT
                ASSERT_TRUE(COUNT(*) > 0, 'Gold table is empty!')
            FROM DATA_VAULT.GOLD.CAMPAIGN_PERFORMANCE
            WHERE report_date = CURRENT_DATE()
        """,
        snowflake_conn_id="snowflake_data_vault"
    )

    # Refresh materialised view
    refresh_mv = SnowflakeOperator(
        task_id="refresh_materialised_view",
        sql="ALTER MATERIALIZED VIEW DATA_VAULT.GOLD.MV_CAMPAIGN_SUMMARY RESUME",
        snowflake_conn_id="snowflake_data_vault"
    )

    (
        check_connection
        >> check_bronze_freshness
        >> dbt_staging
        >> dbt_marts
        >> validate_gold
        >> refresh_mv
    )
```

---

## Power BI → Snowflake Connection

```
In Power BI Desktop:
1. Get Data → Snowflake
2. Server: xy12345.eu-west-1.snowflakecomputing.com
3. Warehouse: BI_WH
4. Database: DATA_VAULT
5. Schema: GOLD
6. Data Connectivity: DirectQuery (real-time) or Import (cached)

Service account setup:
  User: POWERBI_SERVICE
  Role: BI_READER
  Warehouse: BI_WH (auto-suspend 300s)
  
DirectQuery DAX → Snowflake SQL translation happens automatically
Snowflake returns results to Power BI
```

---

## Docker Compose — Full Snowflake Stack

```yaml
# docker-compose.snowflake.yml
version: "3.8"

services:

  pipeline:
    build: ./pipeline
    environment:
      SNOWFLAKE_ACCOUNT: ${SNOWFLAKE_ACCOUNT}
      SNOWFLAKE_USER: ${SNOWFLAKE_USER}
      SNOWFLAKE_PASSWORD: ${SNOWFLAKE_PASSWORD}
    volumes:
      - ./data:/app/data

  dbt:
    image: ghcr.io/dbt-labs/dbt-snowflake:1.7.0
    environment:
      SNOWFLAKE_ACCOUNT: ${SNOWFLAKE_ACCOUNT}
      SNOWFLAKE_USER: ${SNOWFLAKE_USER}
      SNOWFLAKE_PASSWORD: ${SNOWFLAKE_PASSWORD}
    volumes:
      - ./dbt:/usr/app/dbt
    command: dbt build --target prod

  airflow:
    image: apache/airflow:2.7.0
    environment:
      SNOWFLAKE_ACCOUNT: ${SNOWFLAKE_ACCOUNT}
      SNOWFLAKE_USER: ${SNOWFLAKE_USER}
      SNOWFLAKE_PASSWORD: ${SNOWFLAKE_PASSWORD}
    volumes:
      - ./dags:/opt/airflow/dags
      - ./dbt:/opt/dbt
    ports:
      - "8080:8080"
```

---

## Quick Reference

```python
# Python connection
conn = snowflake.connector.connect(
    user=..., password=..., account=...,
    warehouse=..., database=..., schema=...
)
cursor = conn.cursor()
cursor.execute("SQL")
results = cursor.fetchall()

# Pandas → Snowflake
write_pandas(conn, df, "TABLE", schema="SCHEMA", overwrite=True)

# SQLAlchemy
engine = create_engine(f"snowflake://user:pass@account/db/schema?warehouse=wh")
df = pd.read_sql("SELECT ...", engine)
df.to_sql("table", engine, if_exists="replace")

# dbt profile
type: snowflake
account: xy12345.eu-west-1
user/password/role/warehouse/database/schema/threads
```

---

## Previous | Next
← [[07 - Snowflake Security and Governance]] | → [[Snowflake MOC]]
