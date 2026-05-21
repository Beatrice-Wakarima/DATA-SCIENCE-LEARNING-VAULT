---
title: SQL for Data Engineering
tags: [sql, data-engineering, advanced]
created: 2026-05-20
up:: [[SQL MOC]]
---

# ⚙️ SQL for Data Engineering

> This note brings everything together — how SQL powers production data pipelines, Medallion Architecture, data quality checks, and warehouse patterns used at scale.

---

## SQL in the Data Pipeline

```
Source Systems (APIs, CSVs, DBs)
          ↓
    BRONZE layer  ← Raw data, loaded as-is
          ↓  SQL transformations
    SILVER layer  ← Cleaned, validated, typed
          ↓  SQL aggregations
    GOLD layer    ← Business-ready, aggregated
          ↓
    BI Tools (Power BI, Tableau)
```

---

## Medallion Architecture in SQL

### Bronze — Raw Ingestion
```sql
-- Load raw data exactly as received
CREATE TABLE bronze.raw_bank_marketing (
    raw_id      BIGSERIAL PRIMARY KEY,
    age         TEXT,           -- Keep as TEXT — don't assume type
    job         TEXT,
    marital     TEXT,
    education   TEXT,
    balance     TEXT,
    y           TEXT,
    source_file TEXT,
    loaded_at   TIMESTAMP DEFAULT NOW()
);

-- Load from CSV (PostgreSQL COPY command)
COPY bronze.raw_bank_marketing (age, job, marital, education, balance, y)
FROM '/data/bank_marketing.csv'
WITH (FORMAT CSV, HEADER TRUE);
```

### Silver — Clean & Validate
```sql
-- Transform bronze → silver
INSERT INTO silver.bank_customers (
    age, job, marital, education, balance,
    balance_segment, subscribed, processed_at
)
SELECT
    -- Type cast with validation
    CASE WHEN age ~ '^\d+$' THEN age::INTEGER ELSE NULL END AS age,
    TRIM(LOWER(job))        AS job,
    TRIM(LOWER(marital))    AS marital,
    TRIM(LOWER(education))  AS education,

    -- Clean balance
    CASE
        WHEN balance ~ '^-?\d+\.?\d*$'
        THEN balance::DECIMAL(12,2)
        ELSE 0
    END AS balance,

    -- Derived field
    CASE
        WHEN balance::DECIMAL > 10000  THEN 'High'
        WHEN balance::DECIMAL > 1000   THEN 'Medium'
        ELSE 'Low'
    END AS balance_segment,

    -- Standardize target
    CASE
        WHEN LOWER(TRIM(y)) = 'yes' THEN TRUE
        ELSE FALSE
    END AS subscribed,

    NOW() AS processed_at

FROM bronze.raw_bank_marketing
WHERE age ~ '^\d+$'             -- Only valid ages
  AND balance ~ '^-?\d+\.?\d*$' -- Only valid balances
  AND job IS NOT NULL;
```

### Gold — Business Aggregations
```sql
-- Campaign performance summary
CREATE TABLE gold.campaign_performance AS
SELECT
    job,
    education,
    marital,
    balance_segment,
    COUNT(*)                                            AS total_contacts,
    SUM(CASE WHEN subscribed THEN 1 ELSE 0 END)        AS subscriptions,
    ROUND(
        100.0 * SUM(CASE WHEN subscribed THEN 1 ELSE 0 END) / COUNT(*),
        2
    )                                                   AS conversion_rate_pct,
    ROUND(AVG(balance), 0)                             AS avg_balance,
    NOW()                                               AS created_at
FROM silver.bank_customers
GROUP BY job, education, marital, balance_segment;

-- Create indexes for Power BI performance
CREATE INDEX idx_gold_job ON gold.campaign_performance(job);
CREATE INDEX idx_gold_conversion ON gold.campaign_performance(conversion_rate_pct);
```

---

## Data Quality Checks in SQL

```sql
-- Run these before promoting bronze → silver

-- 1. Row count check
SELECT COUNT(*) AS total_rows FROM bronze.raw_bank_marketing;
-- Expected: > 0

-- 2. Null checks on critical columns
SELECT
    COUNT(*) AS total,
    SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END)      AS null_age,
    SUM(CASE WHEN job IS NULL THEN 1 ELSE 0 END)      AS null_job,
    SUM(CASE WHEN balance IS NULL THEN 1 ELSE 0 END)  AS null_balance
FROM bronze.raw_bank_marketing;
-- Expected: 0 nulls in critical columns

-- 3. Duplicate check
SELECT age, job, balance, COUNT(*) AS duplicates
FROM bronze.raw_bank_marketing
GROUP BY age, job, balance
HAVING COUNT(*) > 1;
-- Expected: 0 rows

-- 4. Value range check
SELECT
    MIN(age::INTEGER) AS min_age,
    MAX(age::INTEGER) AS max_age,
    MIN(balance::DECIMAL) AS min_balance,
    MAX(balance::DECIMAL) AS max_balance
FROM bronze.raw_bank_marketing
WHERE age ~ '^\d+$';
-- Expected: age 18-100, balance not extreme

-- 5. Referential integrity check
SELECT t.*
FROM transactions t
LEFT JOIN customers c ON t.customer_id = c.id
WHERE c.id IS NULL;
-- Expected: 0 rows (no orphan transactions)

-- 6. Distribution check
SELECT y, COUNT(*), ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) AS pct
FROM bronze.raw_bank_marketing
GROUP BY y;
-- Check for unexpected values
```

---

## Slowly Changing Dimensions (SCD)

```sql
-- SCD Type 2: Track historical changes to dimension data

CREATE TABLE dim_customers (
    customer_sk     BIGSERIAL PRIMARY KEY,     -- Surrogate key
    customer_id     INTEGER NOT NULL,           -- Natural key
    name            VARCHAR(100),
    tier            VARCHAR(20),
    city            VARCHAR(50),
    -- SCD Type 2 fields
    valid_from      DATE NOT NULL DEFAULT CURRENT_DATE,
    valid_to        DATE,                       -- NULL = current record
    is_current      BOOLEAN DEFAULT TRUE
);

-- Insert new record when customer changes tier
INSERT INTO dim_customers (customer_id, name, tier, city, valid_from, is_current)
VALUES (1, 'Beatrice', 'Platinum', 'Nairobi', CURRENT_DATE, TRUE);

-- Expire old record
UPDATE dim_customers
SET valid_to = CURRENT_DATE - 1, is_current = FALSE
WHERE customer_id = 1 AND is_current = TRUE;

-- Query current state
SELECT * FROM dim_customers WHERE is_current = TRUE;

-- Query historical state at a specific date
SELECT * FROM dim_customers
WHERE customer_id = 1
  AND valid_from <= '2025-01-01'
  AND (valid_to IS NULL OR valid_to >= '2025-01-01');
```

---

## Incremental Loading Pattern

```sql
-- Only load NEW records since last run

-- Track last load
CREATE TABLE pipeline_watermarks (
    pipeline_name   VARCHAR(100) PRIMARY KEY,
    last_loaded_at  TIMESTAMP,
    rows_loaded     INTEGER
);

-- Incremental insert
WITH watermark AS (
    SELECT last_loaded_at
    FROM pipeline_watermarks
    WHERE pipeline_name = 'transactions_load'
),
new_records AS (
    SELECT *
    FROM source_transactions
    WHERE created_at > (SELECT last_loaded_at FROM watermark)
)
INSERT INTO silver.transactions
SELECT * FROM new_records;

-- Update watermark
UPDATE pipeline_watermarks
SET
    last_loaded_at = NOW(),
    rows_loaded    = (SELECT COUNT(*) FROM new_records)
WHERE pipeline_name = 'transactions_load';
```

---

## Pivot Tables in SQL

```sql
-- Turn rows into columns (pivot)
SELECT
    month,
    SUM(CASE WHEN tier = 'Bronze'   THEN revenue ELSE 0 END) AS bronze_revenue,
    SUM(CASE WHEN tier = 'Silver'   THEN revenue ELSE 0 END) AS silver_revenue,
    SUM(CASE WHEN tier = 'Gold'     THEN revenue ELSE 0 END) AS gold_revenue,
    SUM(CASE WHEN tier = 'Platinum' THEN revenue ELSE 0 END) AS platinum_revenue,
    SUM(revenue) AS total_revenue
FROM (
    SELECT
        TO_CHAR(t.created_at, 'YYYY-MM') AS month,
        c.tier,
        SUM(t.amount) AS revenue
    FROM transactions t
    JOIN customers c ON t.customer_id = c.id
    GROUP BY 1, 2
) AS monthly_tier_revenue
GROUP BY month
ORDER BY month;
```

---

## EXPLAIN — Query Performance

```sql
-- See how PostgreSQL executes a query
EXPLAIN SELECT * FROM customers WHERE city = 'Nairobi';

-- With actual timing
EXPLAIN ANALYZE SELECT * FROM customers WHERE city = 'Nairobi';

-- Look for:
-- Seq Scan = full table scan (SLOW on large tables → add index)
-- Index Scan = uses index (FAST)
-- Nested Loop = joining rows one by one
-- Hash Join = building hash table (efficient for large joins)

-- Fix slow query by adding index
CREATE INDEX idx_customers_city ON customers(city);
EXPLAIN ANALYZE SELECT * FROM customers WHERE city = 'Nairobi';
-- Should now show Index Scan
```

---

## Useful Data Engineering Queries

```sql
-- Table sizes
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Column statistics
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'customers'
ORDER BY ordinal_position;

-- Find duplicate rows
SELECT *, COUNT(*) OVER (PARTITION BY email) AS duplicates
FROM customers
ORDER BY email;

-- Data freshness check
SELECT
    MAX(created_at) AS latest_record,
    NOW() - MAX(created_at) AS data_lag
FROM transactions;

-- Row counts across all tables
SELECT
    table_name,
    (SELECT COUNT(*) FROM information_schema.tables t2
     WHERE t2.table_name = t.table_name)
FROM information_schema.tables t
WHERE table_schema = 'public';
```

---

## SQL MOC Summary

This is the final note in the SQL series. Here's everything covered:

| Note | Topic |
|---|---|
| 01 | Introduction to SQL |
| 02 | SELECT Statements |
| 03 | Aggregate Functions |
| 04 | JOINs |
| 05 | Subqueries |
| 06 | CTEs & Window Functions |
| 07 | INSERT, UPDATE, DELETE |
| 08 | DDL — Creating Tables |
| 09 | String & Date Functions |
| 10 | SQL for Data Engineering |

---

## Previous | Next
← [[09 - String and Date Functions]] | → [[SQL MOC]]
