---
title: Snowflake Performance and Cost Optimisation
tags: [snowflake, performance, cost, optimisation]
created: 2026-05-20
up:: [[Snowflake MOC]]
---

# ⚡ Snowflake Performance & Cost Optimisation

> Snowflake can be expensive if misused and blazing fast if optimised. This note covers every technique to make your queries faster and your bills smaller — essential for production data platforms.

---

## How Snowflake Charges

```
Two cost components:

1. COMPUTE (Virtual Warehouses)
   Charged per credit
   Price: ~$2-4 per credit (cloud/region dependent)
   X-Small = 1 credit/hour
   Small   = 2 credits/hour
   Medium  = 4 credits/hour
   Large   = 8 credits/hour
   
   Auto-suspend STOPS billing when idle
   Auto-resume starts billing again

2. STORAGE
   Charged per TB per month
   ~$23/TB/month (compressed)
   Time travel data also counts
   Fail-safe data (7 days) also counts
```

---

## Warehouse Optimisation

```sql
-- ── AUTO-SUSPEND: Most important cost control ──────────

-- Suspend after 60 seconds idle (save money)
ALTER WAREHOUSE ETL_WH
    SET AUTO_SUSPEND = 60;          -- 60 seconds (minimum)

-- Suspend faster for dev warehouses
ALTER WAREHOUSE DEV_WH
    SET AUTO_SUSPEND = 30;

-- Never suspend for 24/7 production workloads (rare)
ALTER WAREHOUSE PROD_WH
    SET AUTO_SUSPEND = 0;           -- Never suspend

-- ── RIGHT-SIZE YOUR WAREHOUSE ─────────────────────────

-- Check if queries are spilling to disk (need bigger WH)
SELECT
    query_id,
    query_text,
    warehouse_size,
    bytes_spilled_to_local_storage,
    bytes_spilled_to_remote_storage,
    execution_time / 1000           AS execution_secs
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE bytes_spilled_to_remote_storage > 0
  AND start_time >= DATEADD(DAY, -7, CURRENT_TIMESTAMP())
ORDER BY bytes_spilled_to_remote_storage DESC
LIMIT 20;
-- If spilling: increase warehouse size

-- Check if warehouse is sitting idle
SELECT
    start_time::DATE AS date,
    warehouse_name,
    SUM(credits_used)               AS total_credits,
    SUM(credits_used_cloud_services) AS cloud_credits
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time >= DATEADD(MONTH, -1, CURRENT_TIMESTAMP())
GROUP BY 1, 2
ORDER BY total_credits DESC;
```

---

## Query Optimisation

```sql
-- ── MICRO-PARTITION PRUNING ────────────────────────────
-- Snowflake automatically skips micro-partitions that don't match
-- your WHERE clause. Help it by filtering on partition boundaries.

-- ✅ Good: filter on a column with good clustering
SELECT * FROM SILVER.BANK_CUSTOMERS
WHERE _run_date = CURRENT_DATE()        -- Prunes micro-partitions
  AND balance_segment = 'high';

-- ❌ Bad: function on column prevents pruning
SELECT * FROM SILVER.BANK_CUSTOMERS
WHERE YEAR(_run_date) = 2026            -- Can't prune! Wrap in function

-- ✅ Fix: avoid functions on filter columns
SELECT * FROM SILVER.BANK_CUSTOMERS
WHERE _run_date BETWEEN '2026-01-01' AND '2026-12-31'

-- ── AVOID SELECT * ────────────────────────────────────
-- Snowflake is columnar — only read what you need

-- ❌ Bad: reads all columns
SELECT * FROM SILVER.BANK_CUSTOMERS;

-- ✅ Good: reads only needed columns
SELECT customer_sk, job, balance, subscribed
FROM SILVER.BANK_CUSTOMERS;

-- ── USE APPROXIMATE FUNCTIONS ────────────────────────
-- For dashboards that don't need exact counts

-- ❌ Exact (slow for huge tables)
SELECT COUNT(DISTINCT customer_sk) FROM TRANSACTIONS;

-- ✅ Approximate (very fast, ~2% error)
SELECT APPROX_COUNT_DISTINCT(customer_sk) FROM TRANSACTIONS;

-- ── LIMIT DURING DEVELOPMENT ─────────────────────────
-- Always LIMIT when exploring large tables
SELECT * FROM BRONZE.RAW_BANK_MARKETING LIMIT 100;
```

---

## Caching — Free Query Acceleration

```sql
-- Snowflake has 3 cache layers:
-- 1. Result Cache   — identical query → instant (24 hours)
-- 2. Local Cache    — warehouse memory cache
-- 3. Remote Cache   — SSD cache on warehouse nodes

-- ── RESULT CACHE ──────────────────────────────────────
-- Same query + same data = returns instantly (no compute cost!)

-- First run: 15 seconds
SELECT job, COUNT(*), AVG(balance)
FROM SILVER.BANK_CUSTOMERS
GROUP BY job;

-- Second run: 0.0 seconds (from result cache!)
SELECT job, COUNT(*), AVG(balance)
FROM SILVER.BANK_CUSTOMERS
GROUP BY job;

-- Check if query used result cache
SELECT
    query_id,
    query_text,
    execution_status,
    is_client_generated_child_queries,
    QUERY_TAG
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
WHERE query_text ILIKE '%bank_customers%'
LIMIT 10;
-- Look for "resultCacheHit" in query profile

-- ── FORCE FRESH RESULTS (bypass cache) ────────────────
ALTER SESSION SET USE_CACHED_RESULT = FALSE;
SELECT ...;
ALTER SESSION SET USE_CACHED_RESULT = TRUE;  -- Re-enable
```

---

## Search Optimisation Service

```sql
-- Accelerates point lookups and high-cardinality searches
-- Useful for specific customer lookups, ID searches

-- Enable search optimisation on a table
ALTER TABLE SILVER.BANK_CUSTOMERS
    ADD SEARCH OPTIMIZATION;

-- Enable on specific columns only (more targeted, cheaper)
ALTER TABLE SILVER.BANK_CUSTOMERS
    ADD SEARCH OPTIMIZATION ON EQUALITY(customer_sk, job);

-- Check search optimisation status
SHOW SEARCH OPTIMIZATION ON SILVER.BANK_CUSTOMERS;

-- Remove when not needed
ALTER TABLE SILVER.BANK_CUSTOMERS
    DROP SEARCH OPTIMIZATION;

-- Use case: fast lookup by ID in large table
-- Without search optimization: full table scan
-- With search optimization: near-instant

SELECT * FROM SILVER.BANK_CUSTOMERS
WHERE customer_sk = 12345;  -- Instant with search optimization!
```

---

## Resource Monitors — Budget Control

```sql
-- Set spending limits at account/warehouse level

-- Create a resource monitor
CREATE RESOURCE MONITOR monthly_limit
    WITH
    CREDIT_QUOTA = 500              -- 500 credits per month
    FREQUENCY = MONTHLY
    START_TIMESTAMP = IMMEDIATELY
    TRIGGERS
        ON 75 PERCENT DO NOTIFY     -- Alert at 75%
        ON 90 PERCENT DO NOTIFY     -- Alert at 90%
        ON 100 PERCENT DO SUSPEND   -- Suspend warehouses at 100%
        ON 110 PERCENT DO SUSPEND_IMMEDIATE;

-- Apply to account level
ALTER ACCOUNT SET RESOURCE_MONITOR = monthly_limit;

-- Apply to specific warehouse
ALTER WAREHOUSE ETL_WH SET RESOURCE_MONITOR = monthly_limit;

-- Create per-team monitors
CREATE RESOURCE MONITOR engineering_monitor
    WITH CREDIT_QUOTA = 100
    FREQUENCY = MONTHLY
    TRIGGERS
        ON 90 PERCENT DO NOTIFY
        ON 100 PERCENT DO SUSPEND;

ALTER WAREHOUSE ETL_WH SET RESOURCE_MONITOR = engineering_monitor;
```

---

## Query Profile Analysis

```sql
-- Find slowest queries in last 7 days
SELECT
    query_id,
    LEFT(query_text, 100)               AS query_preview,
    warehouse_name,
    warehouse_size,
    execution_time / 1000               AS execution_secs,
    total_elapsed_time / 1000           AS total_secs,
    bytes_scanned / 1024 / 1024 / 1024 AS gb_scanned,
    partitions_scanned,
    partitions_total,
    ROUND(
        100.0 * partitions_scanned / NULLIF(partitions_total, 0),
        1
    )                                   AS pct_partitions_scanned
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time >= DATEADD(DAY, -7, CURRENT_TIMESTAMP())
  AND execution_status = 'SUCCESS'
  AND query_type = 'SELECT'
ORDER BY execution_time DESC
LIMIT 20;

-- Find full table scans (high partition scan %)
SELECT
    LEFT(query_text, 150)               AS query,
    partitions_scanned,
    partitions_total,
    ROUND(100.0 * partitions_scanned / partitions_total, 1) AS pct_scanned,
    execution_time / 1000               AS secs
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time >= DATEADD(DAY, -7, CURRENT_TIMESTAMP())
  AND partitions_total > 100
  AND 100.0 * partitions_scanned / partitions_total > 80   -- >80% = full scan
ORDER BY execution_time DESC
LIMIT 20;

-- Credit consumption by warehouse
SELECT
    warehouse_name,
    SUM(credits_used)                   AS total_credits,
    ROUND(SUM(credits_used) * 3.5, 2)  AS est_cost_usd,
    COUNT(DISTINCT query_id)            AS total_queries,
    ROUND(AVG(execution_time) / 1000, 1) AS avg_query_secs
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time >= DATEADD(MONTH, -1, CURRENT_TIMESTAMP())
GROUP BY 1
ORDER BY total_credits DESC;
```

---

## Materialised Views

```sql
-- Materialised views store pre-computed results
-- Automatically updated when base table changes
-- Great for expensive aggregations queried frequently

CREATE MATERIALIZED VIEW DATA_VAULT.GOLD.MV_CAMPAIGN_SUMMARY AS
SELECT
    job,
    balance_segment,
    COUNT(*)                                            AS total_contacts,
    SUM(CASE WHEN subscribed THEN 1 ELSE 0 END)        AS subscriptions,
    ROUND(
        100.0 * SUM(CASE WHEN subscribed THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 2
    )                                                   AS conversion_rate,
    ROUND(AVG(balance), 2)                             AS avg_balance
FROM DATA_VAULT.SILVER.BANK_CUSTOMERS
GROUP BY 1, 2;

-- Query the materialised view (fast! pre-computed)
SELECT * FROM DATA_VAULT.GOLD.MV_CAMPAIGN_SUMMARY
WHERE conversion_rate > 15
ORDER BY conversion_rate DESC;

-- Suspend/resume materialised view refresh
ALTER MATERIALIZED VIEW DATA_VAULT.GOLD.MV_CAMPAIGN_SUMMARY SUSPEND;
ALTER MATERIALIZED VIEW DATA_VAULT.GOLD.MV_CAMPAIGN_SUMMARY RESUME;
```

---

## Cost Optimisation Checklist

```
Compute:
  ✅ Auto-suspend on all warehouses (60-300 seconds)
  ✅ Right-size warehouses (don't use Large for small queries)
  ✅ Separate warehouses for ETL and BI (different sizing)
  ✅ Resource monitors with spending alerts
  ✅ Use X-Small for dev/testing

Storage:
  ✅ Use TRANSIENT tables for staging (no fail-safe)
  ✅ Set DATA_RETENTION_TIME_IN_DAYS appropriately
  ✅ Drop temporary staging tables after use
  ✅ Use Parquet format (compressed) over CSV

Queries:
  ✅ Avoid SELECT * on large tables
  ✅ Filter on clustering key columns
  ✅ Use APPROX_COUNT_DISTINCT for dashboards
  ✅ Use RESULT_SCAN to reuse cached results
  ✅ Cluster large tables on common filter columns
  ✅ Use materialised views for expensive repeated queries

Architecture:
  ✅ Medallion architecture (Bronze/Silver/Gold)
  ✅ Incremental loading (not full refreshes)
  ✅ Separate ETL and BI warehouses
  ✅ Use streams + tasks for ELT (vs always-on pipeline)
```

---

## Quick Reference

```sql
-- Warehouse management
ALTER WAREHOUSE wh SET AUTO_SUSPEND = 60;
ALTER WAREHOUSE wh SET WAREHOUSE_SIZE = 'LARGE';
ALTER WAREHOUSE wh SUSPEND;
ALTER WAREHOUSE wh RESUME;

-- Cost monitoring
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY;
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY;

-- Resource monitors
CREATE RESOURCE MONITOR mon WITH CREDIT_QUOTA = 100
    TRIGGERS ON 90 PERCENT DO NOTIFY ON 100 PERCENT DO SUSPEND;
ALTER WAREHOUSE wh SET RESOURCE_MONITOR = mon;

-- Performance
ALTER TABLE t ADD SEARCH OPTIMIZATION;
ALTER TABLE t CLUSTER BY (col1, col2);
CREATE MATERIALIZED VIEW mv AS SELECT ...;

-- Caching
ALTER SESSION SET USE_CACHED_RESULT = FALSE;  -- Bypass cache
SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));  -- Reuse results
```

---

## Previous | Next
← [[04 - Snowflake Transformations and SQL]] | → [[06 - Snowflake Time Travel and Cloning]]
