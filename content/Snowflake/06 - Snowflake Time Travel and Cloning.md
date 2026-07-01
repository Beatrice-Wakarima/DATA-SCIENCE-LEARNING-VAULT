---
title: Snowflake Time Travel and Cloning
tags: [snowflake, time-travel, cloning, data-recovery]
created: 2026-05-20
up:: [[Snowflake MOC]]
---

# ⏰ Snowflake Time Travel & Cloning

> Time Travel lets you query historical data and recover from mistakes — no backup/restore needed. Zero-copy cloning creates instant copies of databases, schemas, or tables for testing and development. Both are unique Snowflake superpowers.

---

## Time Travel — The Concept

```
Data is modified at 10:00 AM
You query at 10:05 AM — you see current data
You query AT OFFSET => -300 — you see data as of 10:00 AM

Time travel retention:
  Standard edition:   1 day
  Enterprise edition: up to 90 days
  
Cost: Time travel data is stored (adds to storage cost)
```

---

## Querying Historical Data

```sql
-- ── BY TIMESTAMP ──────────────────────────────────────

-- See data as of exactly 1 hour ago
SELECT * FROM SILVER.BANK_CUSTOMERS
AT (TIMESTAMP => DATEADD(HOUR, -1, CURRENT_TIMESTAMP()));

-- See data at a specific time
SELECT * FROM SILVER.BANK_CUSTOMERS
AT (TIMESTAMP => '2026-05-20 09:00:00'::TIMESTAMP_NTZ);

-- Data BEFORE a specific timestamp
SELECT * FROM SILVER.BANK_CUSTOMERS
BEFORE (TIMESTAMP => '2026-05-20 09:00:00'::TIMESTAMP_NTZ);

-- ── BY OFFSET (seconds) ───────────────────────────────

-- 1 hour ago (3600 seconds)
SELECT * FROM SILVER.BANK_CUSTOMERS
AT (OFFSET => -3600);

-- 1 day ago
SELECT * FROM SILVER.BANK_CUSTOMERS
AT (OFFSET => -86400);

-- ── BY STATEMENT (query ID) ───────────────────────────

-- Get the query ID of a DELETE/UPDATE
SELECT LAST_QUERY_ID();

-- See data BEFORE that statement ran
SELECT * FROM SILVER.BANK_CUSTOMERS
BEFORE (STATEMENT => '019f4b3a-0504-89a3-0000-...');

-- ── COMPARE VERSIONS ──────────────────────────────────

-- What changed in the last hour?
SELECT 
    'current'   AS version,
    COUNT(*)    AS row_count,
    SUM(balance) AS total_balance
FROM SILVER.BANK_CUSTOMERS

UNION ALL

SELECT 
    '1 hour ago',
    COUNT(*),
    SUM(balance)
FROM SILVER.BANK_CUSTOMERS AT (OFFSET => -3600);
```

---

## Data Recovery — Undrop

```sql
-- ── ACCIDENTALLY DROPPED A TABLE? ─────────────────────

-- Drop a table
DROP TABLE SILVER.BANK_CUSTOMERS;

-- Oops! Restore it instantly
UNDROP TABLE SILVER.BANK_CUSTOMERS;

-- ── ACCIDENTALLY DROPPED A SCHEMA? ────────────────────
DROP SCHEMA DATA_VAULT.SILVER;
UNDROP SCHEMA DATA_VAULT.SILVER;

-- ── ACCIDENTALLY DROPPED A DATABASE? ──────────────────
DROP DATABASE DATA_VAULT;
UNDROP DATABASE DATA_VAULT;

-- Note: UNDROP works within the retention period
-- After retention expires, data is gone (fail-safe only)
```

---

## Recovering Bad DML (DELETE/UPDATE)

```sql
-- SCENARIO: Someone ran DELETE without WHERE clause!
DELETE FROM SILVER.BANK_CUSTOMERS;
-- Oh no — all rows gone!

-- Step 1: Find when the DELETE happened
SELECT
    query_id,
    query_text,
    start_time,
    end_time
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE query_type = 'DELETE'
  AND query_text ILIKE '%bank_customers%'
ORDER BY start_time DESC
LIMIT 10;

-- Step 2: Restore data from before the DELETE
-- Method 1: Use query ID
INSERT INTO SILVER.BANK_CUSTOMERS
SELECT *
FROM SILVER.BANK_CUSTOMERS
BEFORE (STATEMENT => '019f4b3a-...-delete-query-id');

-- Method 2: Use timestamp
INSERT INTO SILVER.BANK_CUSTOMERS
SELECT *
FROM SILVER.BANK_CUSTOMERS
AT (OFFSET => -300);   -- 5 minutes ago

-- Method 3: Clone from historical state
CREATE TABLE SILVER.BANK_CUSTOMERS_RESTORED
    CLONE SILVER.BANK_CUSTOMERS
    AT (OFFSET => -300);

-- Then swap or copy back
ALTER TABLE SILVER.BANK_CUSTOMERS
    SWAP WITH SILVER.BANK_CUSTOMERS_RESTORED;
```

---

## Setting Retention Period

```sql
-- Set at table level
ALTER TABLE SILVER.BANK_CUSTOMERS
    SET DATA_RETENTION_TIME_IN_DAYS = 30;

-- Set at schema level (applies to new tables)
ALTER SCHEMA DATA_VAULT.SILVER
    SET DATA_RETENTION_TIME_IN_DAYS = 30;

-- Set at database level
ALTER DATABASE DATA_VAULT
    SET DATA_RETENTION_TIME_IN_DAYS = 7;

-- No retention (transient tables — cheapest)
CREATE TRANSIENT TABLE STAGING.temp_work (...);
-- Transient tables: 0 or 1 day maximum

-- Check current retention
SHOW TABLES LIKE 'BANK_CUSTOMERS' IN SCHEMA DATA_VAULT.SILVER;
-- Look at DATA_RETENTION_TIME column
```

---

## Zero-Copy Cloning — The Superpower

```sql
-- Zero-copy clone creates an INSTANT copy
-- No data is physically copied — only metadata!
-- Changes to clone don't affect original (copy-on-write)
-- Cost: only pay for data changed after cloning

-- Clone a table
CREATE TABLE SILVER.BANK_CUSTOMERS_DEV
    CLONE SILVER.BANK_CUSTOMERS;
-- Instant! Even for billions of rows.

-- Clone a schema (includes all tables)
CREATE SCHEMA DATA_VAULT.SILVER_DEV
    CLONE DATA_VAULT.SILVER;

-- Clone an entire database
CREATE DATABASE DATA_VAULT_DEV
    CLONE DATA_VAULT;
-- All schemas, tables, views, stages — everything!

-- Clone with time travel (clone from yesterday)
CREATE TABLE SILVER.BANK_CUSTOMERS_YESTERDAY
    CLONE SILVER.BANK_CUSTOMERS
    AT (OFFSET => -86400);

-- Clone from before a bad deployment
CREATE DATABASE DATA_VAULT_ROLLBACK
    CLONE DATA_VAULT
    BEFORE (STATEMENT => 'bad-deployment-query-id');
```

---

## Use Cases for Cloning

```sql
-- ── USE CASE 1: ZERO-RISK DEVELOPMENT ─────────────────

-- Create dev environment instantly
CREATE DATABASE DATA_VAULT_DEV CLONE DATA_VAULT;

-- Developers work in DEV, production unaffected
-- Merge changes back when ready

-- ── USE CASE 2: TESTING BEFORE DEPLOYMENT ─────────────

-- Clone production before running risky migration
CREATE TABLE SILVER.BANK_CUSTOMERS_BACKUP
    CLONE SILVER.BANK_CUSTOMERS;

-- Run the risky migration
ALTER TABLE SILVER.BANK_CUSTOMERS
    ADD COLUMN risk_score NUMBER(3,1);

UPDATE SILVER.BANK_CUSTOMERS
SET risk_score = CASE
    WHEN balance > 100000 THEN 1
    WHEN balance > 50000  THEN 2
    ELSE 3
END;

-- If bad: restore instantly
DROP TABLE SILVER.BANK_CUSTOMERS;
ALTER TABLE SILVER.BANK_CUSTOMERS_BACKUP
    RENAME TO SILVER.BANK_CUSTOMERS;

-- ── USE CASE 3: DATA SCIENCE SANDBOX ──────────────────

-- Data scientists get production-size data for free!
CREATE DATABASE DS_SANDBOX CLONE DATA_VAULT;

-- Scientists can do anything — production is safe
DROP TABLE DS_SANDBOX.SILVER.BANK_CUSTOMERS;    -- No problem!
CREATE TABLE DS_SANDBOX.SILVER.EXPERIMENTS AS SELECT ...;

-- ── USE CASE 4: POINT-IN-TIME REPORTING ───────────────

-- Create month-end snapshot for audit
CREATE TABLE GOLD.MONTHLY_SNAPSHOT_202605
    CLONE GOLD.CAMPAIGN_PERFORMANCE
    AT (TIMESTAMP => '2026-05-31 23:59:59'::TIMESTAMP_NTZ);

-- ── USE CASE 5: CI/CD PIPELINE TESTING ────────────────

-- Clone prod for integration testing
CREATE DATABASE CI_TEST_${{ env.BUILD_ID }}
    CLONE DATA_VAULT;

-- Run tests against cloned data
-- Drop when done
DROP DATABASE CI_TEST_${{ env.BUILD_ID }};
```

---

## Streams — Change Data Capture

```sql
-- A stream tracks changes (INSERT/UPDATE/DELETE) to a table
-- Used for incremental processing

-- Create stream on bank customers table
CREATE STREAM DATA_VAULT.SILVER.BANK_CUSTOMERS_STREAM
    ON TABLE DATA_VAULT.SILVER.BANK_CUSTOMERS
    APPEND_ONLY = FALSE;   -- Track all DML (not just inserts)

-- Check stream contents
SELECT * FROM DATA_VAULT.SILVER.BANK_CUSTOMERS_STREAM;
-- Shows rows changed since stream was last consumed
-- Special columns: METADATA$ACTION, METADATA$ISUPDATE, METADATA$ROW_ID

-- Process stream changes
INSERT INTO DATA_VAULT.GOLD.CUSTOMER_CHANGES
SELECT
    customer_sk,
    job,
    balance,
    subscribed,
    METADATA$ACTION        AS change_type,     -- INSERT or DELETE
    METADATA$ISUPDATE      AS is_update,        -- TRUE if part of UPDATE
    CURRENT_TIMESTAMP()    AS changed_at
FROM DATA_VAULT.SILVER.BANK_CUSTOMERS_STREAM
WHERE METADATA$ACTION = 'INSERT';

-- After consuming, stream resets (only new changes appear next time)
SELECT COUNT(*) FROM DATA_VAULT.SILVER.BANK_CUSTOMERS_STREAM;
-- Returns 0 if all changes consumed
```

---

## Tasks — Scheduled Execution

```sql
-- Tasks run SQL on a schedule (like cron)
-- Perfect for automated dbt runs, data refreshes, etc.

-- Simple scheduled task
CREATE TASK DATA_VAULT.SILVER.DAILY_REFRESH
    WAREHOUSE = ETL_WH
    SCHEDULE = 'USING CRON 0 5 * * * Africa/Nairobi'
    AS
    CALL DATA_VAULT.SILVER.TRANSFORM_BANK_MARKETING(CURRENT_DATE());

-- Task triggered by stream (event-driven)
CREATE TASK DATA_VAULT.GOLD.REFRESH_ON_CHANGE
    WAREHOUSE = ETL_WH
    SCHEDULE = '5 MINUTE'            -- Check every 5 minutes
    WHEN SYSTEM$STREAM_HAS_DATA('DATA_VAULT.SILVER.BANK_CUSTOMERS_STREAM')
    AS
    INSERT INTO DATA_VAULT.GOLD.CAMPAIGN_PERFORMANCE
    SELECT ... FROM DATA_VAULT.SILVER.BANK_CUSTOMERS_STREAM;

-- Enable task (tasks start in SUSPENDED state)
ALTER TASK DATA_VAULT.SILVER.DAILY_REFRESH RESUME;

-- Suspend task
ALTER TASK DATA_VAULT.SILVER.DAILY_REFRESH SUSPEND;

-- Monitor task history
SELECT *
FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(
    TASK_NAME => 'DAILY_REFRESH',
    SCHEDULED_TIME_RANGE_START => DATEADD(DAY, -7, CURRENT_TIMESTAMP())
))
ORDER BY SCHEDULED_TIME DESC;
```

---

## Quick Reference

```sql
-- Time Travel queries
SELECT * FROM table AT (OFFSET => -3600);          -- 1 hour ago
SELECT * FROM table AT (TIMESTAMP => 'ts');        -- Specific time
SELECT * FROM table BEFORE (STATEMENT => 'qid');   -- Before query

-- Recovery
UNDROP TABLE table_name;
UNDROP SCHEMA schema_name;
UNDROP DATABASE database_name;
INSERT INTO t SELECT * FROM t BEFORE (STATEMENT => 'qid');

-- Cloning
CREATE TABLE clone CLONE original;
CREATE TABLE clone CLONE original AT (OFFSET => -3600);
CREATE SCHEMA s_clone CLONE s_original;
CREATE DATABASE db_clone CLONE db_original;

-- Streams
CREATE STREAM stream ON TABLE table;
SELECT * FROM stream;   -- Shows changes
-- METADATA$ACTION: INSERT or DELETE
-- METADATA$ISUPDATE: TRUE if UPDATE pair

-- Tasks
CREATE TASK t WAREHOUSE = wh SCHEDULE = 'CRON' AS sql;
ALTER TASK t RESUME;
ALTER TASK t SUSPEND;
```

---

## Previous | Next
← [[05 - Snowflake Performance and Cost]] | → [[07 - Snowflake Security and Governance]]
