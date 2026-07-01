---
title: Snowflake Storage and Tables
tags: [snowflake, tables, storage, data-types]
created: 2026-05-20
up:: [[Snowflake MOC]]
---

# 🗄️ Snowflake Storage & Tables

> Snowflake's storage layer is the foundation of your data platform. Understanding table types, data types, clustering, and micro-partitioning lets you build fast, cost-efficient data warehouses.

---

## How Snowflake Stores Data

```
Data is stored as compressed, columnar micro-partitions
Each micro-partition: 50–500MB of uncompressed data

Benefits:
  ✅ Automatic compression (saves 3-7x vs raw)
  ✅ Column pruning (only read needed columns)
  ✅ Partition pruning (skip irrelevant partitions)
  ✅ Automatic management (no indexes needed!)
  ✅ Zero admin overhead

Snowflake automatically:
  - Partitions data
  - Compresses data  
  - Gathers statistics
  - Optimises queries
```

---

## Table Types

### Permanent Table (Default)
```sql
-- Persists until explicitly dropped
-- Time travel: up to 90 days (Enterprise)
-- Fail-safe: 7 days after time travel
CREATE TABLE DATA_VAULT.BRONZE.RAW_BANK_MARKETING (
    age         NUMBER,
    job         VARCHAR(50),
    balance     DECIMAL(12,2),
    y           VARCHAR(5),
    loaded_at   TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

### Temporary Table
```sql
-- Exists only for current session
-- No time travel, no fail-safe
-- Great for intermediate ETL results
CREATE TEMPORARY TABLE temp_staging AS
SELECT * FROM BRONZE.RAW_BANK_MARKETING
WHERE loaded_at::DATE = CURRENT_DATE();
-- Automatically dropped when session ends
```

### Transient Table
```sql
-- Persists across sessions (like permanent)
-- NO fail-safe storage (saves cost for staging)
-- Time travel: 0 or 1 day only
CREATE TRANSIENT TABLE STAGING.BANK_MARKETING_STAGE (
    age     NUMBER,
    job     VARCHAR(50),
    balance NUMBER
);
```

### External Table
```sql
-- Query files in cloud storage directly
-- No data copied into Snowflake
CREATE EXTERNAL TABLE BRONZE.EXT_TRANSACTIONS (
    transaction_id  VARCHAR   AS (VALUE:c1::VARCHAR),
    amount          NUMBER    AS (VALUE:c2::NUMBER),
    created_at      TIMESTAMP AS (VALUE:c3::TIMESTAMP)
)
LOCATION = @my_s3_stage/transactions/
FILE_FORMAT = (TYPE = PARQUET);

-- Query external data
SELECT * FROM BRONZE.EXT_TRANSACTIONS LIMIT 100;
```

---

## Snowflake Data Types

```sql
-- ── NUMERIC ───────────────────────────────────────────
NUMBER(precision, scale)    -- e.g. NUMBER(12,2) for money
DECIMAL(12,2)               -- Same as NUMBER
FLOAT / DOUBLE              -- Floating point
INT / INTEGER               -- Whole numbers
BIGINT                      -- Large integers
TINYINT / SMALLINT          -- Small integers

-- ── TEXT ──────────────────────────────────────────────
VARCHAR(n) / STRING(n)      -- Variable length text
CHAR(n)                     -- Fixed length
TEXT                        -- Up to 16MB
BINARY(n)                   -- Binary data

-- ── DATE & TIME ───────────────────────────────────────
DATE                        -- 2026-05-20
TIME                        -- 14:30:00
TIMESTAMP_NTZ               -- No timezone (recommended for ETL)
TIMESTAMP_LTZ               -- Local timezone
TIMESTAMP_TZ                -- With timezone offset
DATETIME                    -- Alias for TIMESTAMP_NTZ

-- ── BOOLEAN ───────────────────────────────────────────
BOOLEAN                     -- TRUE / FALSE / NULL

-- ── SEMI-STRUCTURED ───────────────────────────────────
VARIANT                     -- Any JSON/XML/Avro data
OBJECT                      -- JSON object
ARRAY                       -- JSON array

-- ── GEOGRAPHY ─────────────────────────────────────────
GEOGRAPHY                   -- Geospatial data
GEOMETRY                    -- Geometric shapes
```

---

## Creating Production Tables

```sql
-- Bank Marketing — Production Tables

-- Bronze: Raw data (as-is)
CREATE TABLE IF NOT EXISTS DATA_VAULT.BRONZE.RAW_BANK_MARKETING (
    -- Source columns (all VARCHAR to preserve raw data)
    age             VARCHAR(10),
    job             VARCHAR(50),
    marital         VARCHAR(20),
    education       VARCHAR(50),
    "default"       VARCHAR(5),
    balance         VARCHAR(20),
    housing         VARCHAR(5),
    loan            VARCHAR(5),
    contact         VARCHAR(20),
    day             VARCHAR(5),
    month           VARCHAR(10),
    duration        VARCHAR(10),
    campaign        VARCHAR(10),
    pdays           VARCHAR(10),
    previous        VARCHAR(10),
    poutcome        VARCHAR(20),
    y               VARCHAR(5),
    -- Metadata
    _source_file    VARCHAR(500),
    _loaded_at      TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    _run_date       DATE
)
COMMENT = 'Raw bank marketing data — loaded as-is from source'
DATA_RETENTION_TIME_IN_DAYS = 7;

-- Silver: Cleaned and typed
CREATE TABLE IF NOT EXISTS DATA_VAULT.SILVER.BANK_CUSTOMERS (
    customer_sk         NUMBER AUTOINCREMENT PRIMARY KEY,
    age                 NUMBER(3) NOT NULL,
    job                 VARCHAR(50),
    marital             VARCHAR(20),
    education           VARCHAR(50),
    balance             DECIMAL(12,2),
    balance_segment     VARCHAR(20),
    age_segment         VARCHAR(20),
    has_housing_loan    BOOLEAN,
    has_personal_loan   BOOLEAN,
    contact_method      VARCHAR(20),
    campaign_contacts   NUMBER(3),
    call_duration_secs  NUMBER,
    subscribed          BOOLEAN,
    _processed_at       TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    _run_date           DATE
)
CLUSTER BY (age_segment, balance_segment)
COMMENT = 'Cleaned and validated bank customer campaign data'
DATA_RETENTION_TIME_IN_DAYS = 30;

-- Gold: Business-ready aggregations
CREATE TABLE IF NOT EXISTS DATA_VAULT.GOLD.CAMPAIGN_PERFORMANCE (
    report_date         DATE,
    job                 VARCHAR(50),
    education           VARCHAR(50),
    balance_segment     VARCHAR(20),
    age_segment         VARCHAR(20),
    total_contacts      NUMBER,
    subscriptions       NUMBER,
    conversion_rate     DECIMAL(5,2),
    avg_balance         DECIMAL(12,2),
    avg_call_duration   NUMBER,
    _refreshed_at       TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
)
CLUSTER BY (report_date, job)
COMMENT = 'Campaign performance aggregations for BI reporting'
DATA_RETENTION_TIME_IN_DAYS = 90;
```

---

## Clustering Keys — Query Acceleration

```sql
-- Clustering organises micro-partitions for common query patterns
-- Best for large tables (>1TB or >100M rows) frequently filtered by same columns

-- Add cluster key
ALTER TABLE SILVER.BANK_CUSTOMERS
    CLUSTER BY (age_segment, balance_segment);

-- Check clustering depth (lower = better)
SELECT SYSTEM$CLUSTERING_DEPTH('SILVER.BANK_CUSTOMERS');
SELECT SYSTEM$CLUSTERING_INFORMATION('SILVER.BANK_CUSTOMERS');

-- Re-cluster manually (usually automatic)
ALTER TABLE SILVER.BANK_CUSTOMERS RECLUSTER;

-- Drop clustering
ALTER TABLE SILVER.BANK_CUSTOMERS DROP CLUSTERING KEY;

-- When to use clustering:
-- ✅ Table > 1TB
-- ✅ Common WHERE filters on same columns
-- ✅ Query takes >1 minute and you see full table scans
-- ❌ Small tables (overhead not worth it)
-- ❌ Random access patterns
```

---

## VARIANT — Semi-Structured Data

```sql
-- Create table with VARIANT column
CREATE TABLE API_RESPONSES (
    response_id     NUMBER AUTOINCREMENT,
    raw_response    VARIANT,
    loaded_at       TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Insert JSON
INSERT INTO API_RESPONSES (raw_response)
SELECT PARSE_JSON('{
    "customer_id": 1001,
    "name": "Beatrice Wakarima",
    "address": {
        "city": "Nairobi",
        "country": "Kenya"
    },
    "transactions": [
        {"amount": 45000, "type": "deposit"},
        {"amount": 10000, "type": "withdrawal"}
    ]
}');

-- Query JSON using : notation
SELECT
    raw_response:customer_id::NUMBER           AS customer_id,
    raw_response:name::STRING                  AS name,
    raw_response:address:city::STRING          AS city,
    raw_response:address:country::STRING       AS country,
    ARRAY_SIZE(raw_response:transactions)      AS txn_count
FROM API_RESPONSES;

-- Flatten nested arrays
SELECT
    r.raw_response:customer_id::NUMBER     AS customer_id,
    t.value:amount::NUMBER                 AS amount,
    t.value:type::STRING                   AS type
FROM API_RESPONSES r,
LATERAL FLATTEN(INPUT => r.raw_response:transactions) t;
```

---

## Table DDL Operations

```sql
-- Add columns
ALTER TABLE SILVER.BANK_CUSTOMERS
    ADD COLUMN is_premium BOOLEAN DEFAULT FALSE;

ALTER TABLE SILVER.BANK_CUSTOMERS
    ADD COLUMN risk_score NUMBER(3,1);

-- Modify column
ALTER TABLE SILVER.BANK_CUSTOMERS
    MODIFY COLUMN balance DECIMAL(15,2);

-- Rename column
ALTER TABLE SILVER.BANK_CUSTOMERS
    RENAME COLUMN balance TO account_balance;

-- Drop column
ALTER TABLE SILVER.BANK_CUSTOMERS
    DROP COLUMN risk_score;

-- Rename table
ALTER TABLE SILVER.BANK_CUSTOMERS
    RENAME TO SILVER.BANK_CUSTOMERS_V2;

-- Copy table structure only
CREATE TABLE SILVER.BANK_CUSTOMERS_BACKUP
    LIKE SILVER.BANK_CUSTOMERS;

-- Swap tables (zero-downtime deployment!)
ALTER TABLE SILVER.BANK_CUSTOMERS
    SWAP WITH SILVER.BANK_CUSTOMERS_NEW;
```

---

## Table Best Practices

```sql
-- ✅ Use TIMESTAMP_NTZ for ETL pipelines (no timezone ambiguity)
_loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()

-- ✅ Add metadata columns to every table
_source_file    VARCHAR(500),
_loaded_at      TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
_run_date       DATE,
_pipeline_run   VARCHAR(100)

-- ✅ Use NUMBER AUTOINCREMENT for surrogate keys
customer_sk NUMBER AUTOINCREMENT PRIMARY KEY

-- ✅ Set DATA_RETENTION_TIME_IN_DAYS appropriately
DATA_RETENTION_TIME_IN_DAYS = 7    -- Bronze (cheap)
DATA_RETENTION_TIME_IN_DAYS = 30   -- Silver
DATA_RETENTION_TIME_IN_DAYS = 90   -- Gold (max for standard)

-- ✅ Use transient tables for staging (no fail-safe cost)
CREATE TRANSIENT TABLE STAGING.temp_data ...

-- ✅ Add COMMENT to all tables and columns
COMMENT = 'Description of what this table contains'

-- ✅ Cluster large tables on common filter columns
CLUSTER BY (date_column, category_column)
```

---

## Quick Reference

```sql
-- Table types
CREATE TABLE name (...);                    -- Permanent
CREATE TEMPORARY TABLE name (...);         -- Session only
CREATE TRANSIENT TABLE name (...);         -- No fail-safe
CREATE TABLE name LIKE other_table;        -- Copy structure
CREATE TABLE name CLONE other_table;       -- Zero-copy clone
CREATE TABLE name AS SELECT ...;           -- CTAS

-- Data types
NUMBER(12,2)   VARCHAR(100)   BOOLEAN
DATE           TIMESTAMP_NTZ  VARIANT

-- Clustering
CLUSTER BY (col1, col2)
ALTER TABLE t CLUSTER BY (col1)
SELECT SYSTEM$CLUSTERING_DEPTH('table')

-- JSON
col:field::TYPE
col:nested:field::TYPE
PARSE_JSON('{"key": "value"}')
LATERAL FLATTEN(INPUT => col:array)
```

---

## Previous | Next
← [[01 - Introduction to Snowflake]] | → [[03 - Snowflake Loading Data]]
