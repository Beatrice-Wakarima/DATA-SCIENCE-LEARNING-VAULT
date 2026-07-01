---
title: Snowflake Loading Data
tags: [snowflake, loading, stages, copy, snowpipe]
created: 2026-05-20
up:: [[Snowflake MOC]]
---

# 📥 Snowflake Loading Data

> Loading data into Snowflake efficiently is a core data engineering skill. Snowflake uses Stages as landing zones and COPY INTO as the primary load command — orders of magnitude faster than row-by-row INSERT.

---

## The Loading Flow

```
Source Data (CSV/JSON/Parquet)
          ↓
    Stage (Internal or External)
          ↓
    COPY INTO (bulk load)
          ↓
    Snowflake Table
    
OR for continuous loading:
    S3/GCS → Snowpipe → Table (real-time)
```

---

## Stages — Landing Zones

### Internal Stage (Snowflake-managed)
```sql
-- User stage (one per user, auto-created)
-- Reference as @~
PUT file://data/bank_marketing.csv @~;

-- Table stage (one per table, auto-created)  
-- Reference as @%table_name
PUT file://data/bank_marketing.csv @%RAW_BANK_MARKETING;

-- Named internal stage (create yourself)
CREATE STAGE DATA_VAULT.BRONZE.bank_marketing_stage
    COMMENT = 'Stage for bank marketing CSV files';

-- Upload file to named stage
PUT file:///local/path/bank_marketing.csv 
    @DATA_VAULT.BRONZE.bank_marketing_stage
    AUTO_COMPRESS = TRUE;
```

### External Stage (Cloud Storage)
```sql
-- AWS S3 Stage
CREATE STAGE DATA_VAULT.BRONZE.s3_bank_stage
    URL = 's3://beatrice-data-lake/bank-marketing/'
    CREDENTIALS = (
        AWS_KEY_ID = '...',
        AWS_SECRET_KEY = '...'
    )
    COMMENT = 'S3 stage for bank marketing data';

-- Better: Use Storage Integration (no credentials in code)
CREATE STORAGE INTEGRATION s3_integration
    TYPE = EXTERNAL_STAGE
    STORAGE_PROVIDER = 'S3'
    ENABLED = TRUE
    STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456:role/snowflake-role'
    STORAGE_ALLOWED_LOCATIONS = ('s3://beatrice-data-lake/');

CREATE STAGE DATA_VAULT.BRONZE.s3_stage
    URL = 's3://beatrice-data-lake/bank-marketing/'
    STORAGE_INTEGRATION = s3_integration;

-- GCS Stage
CREATE STAGE DATA_VAULT.BRONZE.gcs_stage
    URL = 'gcs://beatrice-data-lake/bank-marketing/'
    STORAGE_INTEGRATION = gcs_integration;
```

---

## File Formats

```sql
-- CSV File Format
CREATE FILE FORMAT DATA_VAULT.BRONZE.csv_format
    TYPE = CSV
    FIELD_DELIMITER = ','
    RECORD_DELIMITER = '\n'
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('NULL', 'null', 'N/A', '')
    EMPTY_FIELD_AS_NULL = TRUE
    TRIM_SPACE = TRUE
    DATE_FORMAT = 'YYYY-MM-DD'
    TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS'
    COMMENT = 'Standard CSV format';

-- Bank Marketing uses semicolon delimiter
CREATE FILE FORMAT DATA_VAULT.BRONZE.bank_csv_format
    TYPE = CSV
    FIELD_DELIMITER = ';'
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('NULL', 'unknown', '')
    TRIM_SPACE = TRUE;

-- JSON File Format
CREATE FILE FORMAT DATA_VAULT.BRONZE.json_format
    TYPE = JSON
    STRIP_OUTER_ARRAY = TRUE
    STRIP_NULL_VALUES = FALSE
    IGNORE_UTF8_ERRORS = TRUE;

-- Parquet File Format
CREATE FILE FORMAT DATA_VAULT.BRONZE.parquet_format
    TYPE = PARQUET
    SNAPPY_COMPRESSION = TRUE;
```

---

## COPY INTO — Bulk Loading

```sql
-- Basic CSV load
COPY INTO DATA_VAULT.BRONZE.RAW_BANK_MARKETING
FROM @DATA_VAULT.BRONZE.bank_marketing_stage/bank_marketing.csv
FILE_FORMAT = (FORMAT_NAME = 'DATA_VAULT.BRONZE.bank_csv_format')
ON_ERROR = 'CONTINUE';          -- Skip bad rows

-- Load from S3 with wildcards
COPY INTO DATA_VAULT.BRONZE.RAW_BANK_MARKETING
FROM @DATA_VAULT.BRONZE.s3_stage/
PATTERN = '.*bank_marketing.*\.csv'
FILE_FORMAT = (FORMAT_NAME = 'DATA_VAULT.BRONZE.bank_csv_format')
ON_ERROR = 'ABORT_STATEMENT';   -- Fail on any error

-- Load Parquet from S3
COPY INTO DATA_VAULT.SILVER.BANK_CUSTOMERS
FROM (
    SELECT
        $1:age::NUMBER,
        $1:job::VARCHAR,
        $1:balance::DECIMAL(12,2),
        $1:subscribed::BOOLEAN,
        CURRENT_TIMESTAMP()
    FROM @s3_stage/silver/bank_customers/
)
FILE_FORMAT = (FORMAT_NAME = 'DATA_VAULT.BRONZE.parquet_format');

-- Load JSON (semi-structured)
COPY INTO DATA_VAULT.BRONZE.API_RESPONSES (raw_response)
FROM (
    SELECT $1 FROM @DATA_VAULT.BRONZE.json_stage/api/
)
FILE_FORMAT = (FORMAT_NAME = 'DATA_VAULT.BRONZE.json_format');
```

---

## ON_ERROR Options

```sql
-- CONTINUE — skip bad rows, continue loading
ON_ERROR = 'CONTINUE'

-- ABORT_STATEMENT — fail entire load if any error (default)
ON_ERROR = 'ABORT_STATEMENT'

-- SKIP_FILE — skip files with errors
ON_ERROR = 'SKIP_FILE'

-- SKIP_FILE_n — skip files with more than n errors
ON_ERROR = 'SKIP_FILE_10'

-- SKIP_FILE_n% — skip files with more than n% error rate
ON_ERROR = 'SKIP_FILE_10%'
```

---

## Validate Before Loading

```sql
-- Check files in stage
LIST @DATA_VAULT.BRONZE.bank_marketing_stage;

-- Preview file contents (no loading)
SELECT $1, $2, $3
FROM @DATA_VAULT.BRONZE.bank_marketing_stage/bank_marketing.csv
(FILE_FORMAT => 'DATA_VAULT.BRONZE.bank_csv_format')
LIMIT 10;

-- Validate without actually loading
COPY INTO DATA_VAULT.BRONZE.RAW_BANK_MARKETING
FROM @DATA_VAULT.BRONZE.bank_marketing_stage
FILE_FORMAT = (FORMAT_NAME = 'DATA_VAULT.BRONZE.bank_csv_format')
VALIDATION_MODE = 'RETURN_ALL_ERRORS';  -- Shows errors without loading

-- Or validate a sample
VALIDATION_MODE = 'RETURN_10_ROWS';     -- Returns first 10 rows
```

---

## Monitor Load History

```sql
-- Check recent COPY INTO operations
SELECT *
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'RAW_BANK_MARKETING',
    START_TIME => DATEADD(HOURS, -24, CURRENT_TIMESTAMP())
))
ORDER BY LAST_LOAD_TIME DESC;

-- Check load errors
SELECT *
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'RAW_BANK_MARKETING',
    START_TIME => DATEADD(DAYS, -7, CURRENT_TIMESTAMP())
))
WHERE STATUS != 'Loaded'
ORDER BY LAST_LOAD_TIME DESC;
```

---

## Snowpipe — Continuous Loading

```sql
-- Snowpipe loads files automatically as they land in a stage
-- Triggered by S3/GCS event notifications

-- Create the pipe
CREATE PIPE DATA_VAULT.BRONZE.bank_marketing_pipe
    AUTO_INGEST = TRUE     -- Triggered by cloud storage events
    COMMENT = 'Auto-load bank marketing files from S3'
    AS
    COPY INTO DATA_VAULT.BRONZE.RAW_BANK_MARKETING
    FROM @DATA_VAULT.BRONZE.s3_stage/bank-marketing/
    FILE_FORMAT = (FORMAT_NAME = 'DATA_VAULT.BRONZE.bank_csv_format');

-- Get SQS ARN for S3 event notification
SHOW PIPES LIKE 'bank_marketing_pipe';
-- Copy notification_channel value → configure in S3 bucket

-- Monitor Snowpipe
SELECT SYSTEM$PIPE_STATUS('DATA_VAULT.BRONZE.bank_marketing_pipe');

SELECT *
FROM TABLE(INFORMATION_SCHEMA.PIPE_USAGE_HISTORY(
    DATE_RANGE_START => DATEADD('day', -1, CURRENT_DATE()),
    PIPE_NAME => 'DATA_VAULT.BRONZE.bank_marketing_pipe'
));

-- Pause/resume pipe
ALTER PIPE DATA_VAULT.BRONZE.bank_marketing_pipe PAUSE;
ALTER PIPE DATA_VAULT.BRONZE.bank_marketing_pipe RESUME;
```

---

## Python + Snowflake Loading

```python
# pip install snowflake-connector-python
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
import os

def get_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse="ETL_WH",
        database="DATA_VAULT",
        schema="BRONZE"
    )

def load_csv_via_stage(filepath: str,
                        table: str,
                        schema: str = "BRONZE"):
    """Load CSV to Snowflake via internal stage"""
    conn = get_connection()
    cursor = conn.cursor()

    # Upload to stage
    cursor.execute(f"PUT file://{filepath} @%{table} AUTO_COMPRESS=TRUE")

    # Load from stage
    cursor.execute(f"""
        COPY INTO {schema}.{table}
        FROM @%{table}
        FILE_FORMAT = (
            TYPE = CSV
            SKIP_HEADER = 1
            FIELD_DELIMITER = ';'
            FIELD_OPTIONALLY_ENCLOSED_BY = '"'
            NULL_IF = ('NULL', '')
        )
        ON_ERROR = CONTINUE
        PURGE = TRUE
    """)

    result = cursor.fetchone()
    print(f"✅ Loaded {result[0]} rows, {result[1]} errors")
    conn.close()
    return result

def load_dataframe(df: pd.DataFrame,
                    table: str,
                    schema: str = "SILVER",
                    overwrite: bool = False):
    """Load pandas DataFrame directly to Snowflake"""
    conn = get_connection()

    success, nchunks, nrows, _ = write_pandas(
        conn=conn,
        df=df,
        table_name=table.upper(),
        schema=schema.upper(),
        auto_create_table=True,
        overwrite=overwrite,
        chunk_size=10000
    )

    print(f"✅ Loaded {nrows:,} rows in {nchunks} chunks")
    conn.close()
    return nrows

# Usage
df = pd.read_csv("data/bank_marketing.csv", sep=";")
load_dataframe(df, "RAW_BANK_MARKETING", schema="BRONZE", overwrite=True)
```

---

## COPY INTO for Unloading (Export)

```sql
-- Export table to S3 as CSV
COPY INTO @s3_stage/exports/bank_customers/
FROM DATA_VAULT.GOLD.CAMPAIGN_PERFORMANCE
FILE_FORMAT = (
    TYPE = CSV
    HEADER = TRUE
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
)
SINGLE = FALSE              -- Multiple files (parallel)
MAX_FILE_SIZE = 104857600;  -- 100MB per file

-- Export as Parquet (best for data science)
COPY INTO @s3_stage/exports/parquet/
FROM DATA_VAULT.SILVER.BANK_CUSTOMERS
FILE_FORMAT = (TYPE = PARQUET SNAPPY_COMPRESSION = TRUE)
INCLUDE_QUERY_ID = TRUE;    -- Adds query ID to filename

-- Export query result
COPY INTO @s3_stage/exports/
FROM (
    SELECT job, COUNT(*) AS contacts,
           SUM(CASE WHEN subscribed THEN 1 ELSE 0 END) AS subscriptions
    FROM DATA_VAULT.SILVER.BANK_CUSTOMERS
    GROUP BY job
    ORDER BY subscriptions DESC
)
FILE_FORMAT = (TYPE = CSV HEADER = TRUE);
```

---

## Quick Reference

```sql
-- Stages
CREATE STAGE stage_name URL = 's3://bucket/path/';
LIST @stage_name;
PUT file://local.csv @stage_name;
GET @stage_name/file.csv file://local/;
REMOVE @stage_name/file.csv;

-- File formats
CREATE FILE FORMAT fmt TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1;
CREATE FILE FORMAT fmt TYPE = JSON STRIP_OUTER_ARRAY = TRUE;
CREATE FILE FORMAT fmt TYPE = PARQUET;

-- Load
COPY INTO table FROM @stage FILE_FORMAT = (FORMAT_NAME = 'fmt');
COPY INTO table FROM @stage PATTERN = '.*\.csv' ON_ERROR = CONTINUE;

-- Validate
COPY INTO table FROM @stage VALIDATION_MODE = 'RETURN_ALL_ERRORS';
SELECT * FROM @stage/file.csv (FILE_FORMAT => 'fmt') LIMIT 10;

-- Monitor
SELECT * FROM INFORMATION_SCHEMA.COPY_HISTORY(...);
SELECT SYSTEM$PIPE_STATUS('pipe_name');
```

---

## Previous | Next
← [[02 - Snowflake Storage and Tables]] | → [[04 - Snowflake Transformations and SQL]]
