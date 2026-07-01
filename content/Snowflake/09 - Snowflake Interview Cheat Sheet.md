---
title: Snowflake Interview Cheat Sheet
tags: [snowflake, interview, cheatsheet]
created: 2026-05-20
up:: [[Snowflake MOC]]
---

# 🎯 Snowflake Interview Cheat Sheet

> Everything you need to ace a Snowflake interview — concepts, architecture questions, SQL differences, and real-world scenario answers in one place.

---

## Core Architecture Questions

**Q: Explain Snowflake's architecture.**
A: Snowflake has three independent layers:
- **Cloud Services** — metadata, authentication, query optimisation, security (no user compute)
- **Virtual Warehouses** — compute clusters (MPP) that execute queries, can scale independently
- **Storage** — centralised columnar storage on cloud object storage (S3/GCS/Azure Blob), compressed micro-partitions

The key innovation is **separation of storage and compute** — multiple warehouses can query the same data simultaneously without contention.

**Q: What are micro-partitions?**
A: Contiguous units of storage containing 50–500MB of uncompressed data, stored in columnar format. Snowflake automatically manages them — no manual partitioning needed. Metadata about each partition (min/max values, distinct count) enables **partition pruning**, skipping irrelevant partitions during queries.

**Q: What is a Virtual Warehouse?**
A: A cluster of compute servers (MPP) that processes queries. Key properties:
- Independent of storage — multiple warehouses query the same data
- Sizes: X-Small (1 credit/hr) to 6X-Large
- Auto-suspend/resume — zero cost when idle
- Multi-cluster (Enterprise) — scale out for concurrency

**Q: What is the Cloud Services layer?**
A: The intelligence layer — handles authentication, metadata management, query parsing/optimisation, access control, and infrastructure management. Charged separately at ~10% of compute cost.

---

## Table and Storage Questions

**Q: What are the different table types in Snowflake?**

| Type | Persistence | Time Travel | Fail-Safe | Use Case |
|---|---|---|---|---|
| Permanent | Until dropped | 0-90 days | 7 days | Production |
| Transient | Until dropped | 0-1 day | None | Staging (save cost) |
| Temporary | Session only | 0-1 day | None | Intermediate work |
| External | Metadata only | None | None | Data lake queries |

**Q: When would you use a transient table?**
A: For staging/intermediate tables where historical recovery isn't needed. No fail-safe storage means lower cost. Perfect for ETL staging areas that are rebuilt on every run.

**Q: What is a VARIANT data type?**
A: A flexible type that stores any semi-structured data (JSON, XML, Avro, Parquet). It allows Snowflake to store and query JSON natively without a fixed schema, using the `:` notation to access fields: `col:field::STRING`.

**Q: What are clustering keys and when should you use them?**
A: Clustering keys define how data is physically organised in micro-partitions. Use when: table >1TB, queries consistently filter on the same columns, and query performance is poor despite good pruning. Not needed for small tables — overhead isn't worth it.

---

## Unique Feature Questions

**Q: What is Time Travel?**
A: The ability to query historical data at any point within the retention period (up to 90 days on Enterprise). Uses `AT (OFFSET => -3600)`, `AT (TIMESTAMP => ...)`, or `BEFORE (STATEMENT => query_id)`. Also enables `UNDROP` for accidentally dropped objects.

**Q: What is Zero-Copy Cloning?**
A: Creates an instant copy of a table/schema/database by duplicating only metadata — no physical data copy. Changes to the clone use copy-on-write semantics. Use cases: dev environments, testing before deployment, data science sandboxes, point-in-time snapshots.

**Q: What are Snowflake Streams?**
A: Change Data Capture (CDC) mechanism that tracks INSERT/UPDATE/DELETE changes to a table. Each stream records the delta since last consumption. Used with Tasks for incremental ELT processing. Special columns: `METADATA$ACTION`, `METADATA$ISUPDATE`, `METADATA$ROW_ID`.

**Q: What are Snowflake Tasks?**
A: Scheduled SQL execution (like cron for Snowflake). Can be triggered by schedule or when a stream has data (`WHEN SYSTEM$STREAM_HAS_DATA()`). Used to automate dbt runs, data refreshes, and incremental processing without Airflow.

**Q: What is Snowpipe?**
A: Continuous data ingestion that automatically loads files as they land in a cloud stage, triggered by event notifications (S3 SQS, GCS Pub/Sub, Azure Event Grid). Near-real-time loading without manual intervention.

---

## Performance Questions

**Q: How do you optimise slow Snowflake queries?**
A:
1. Check partition pruning — filter on clustered/frequently queried columns
2. Avoid `SELECT *` — columnar storage reads only needed columns
3. Check if warehouse is undersized (query spilling to disk)
4. Add Search Optimisation for point lookups
5. Use `APPROX_COUNT_DISTINCT` for dashboards
6. Add clustering keys for large tables with consistent filter patterns
7. Use materialised views for expensive repeated aggregations
8. Check result cache — identical queries return instantly

**Q: How does result caching work?**
A: Snowflake caches query results for 24 hours. Subsequent identical queries on unchanged data return instantly at no compute cost. Bypass with `ALTER SESSION SET USE_CACHED_RESULT = FALSE`.

**Q: What is the difference between warehouse sizes?**
A: Each size doubles the compute servers and credits: X-Small=1, Small=2, Medium=4, Large=8 credits/hour. Bigger warehouses process large queries faster but cost more. Right-sizing is important — check if queries spill to disk (too small) or complete in seconds with low utilisation (too large).

---

## Security Questions

**Q: Explain Snowflake's RBAC model.**
A: Role-Based Access Control with a hierarchy: ACCOUNTADMIN > SECURITYADMIN > SYSADMIN > custom roles. Privileges are granted to roles, roles are granted to users. Best practice: create custom roles (DATA_ENGINEER, BI_READER) with least-privilege access.

**Q: What is Dynamic Data Masking?**
A: Column-level security policy that shows different data to different roles without changing the underlying data. Example: DATA_ENGINEER sees full email, DATA_ANALYST sees `***@domain.com`, BI_READER sees `***@***.***`. Applied to columns, evaluated at query time.

**Q: What is a Row Access Policy?**
A: Controls which rows are visible to which roles. Uses a policy function that returns BOOLEAN. Applied to tables — invisible rows are completely hidden, not shown as NULL. Used for multi-tenant data, regional access restrictions, and data compartmentalisation.

---

## SQL Differences from Standard SQL

```sql
-- QUALIFY — filter window functions (no subquery needed)
SELECT * FROM t QUALIFY ROW_NUMBER() OVER (PARTITION BY col ORDER BY val) = 1;

-- IFF — shorthand IF
IFF(condition, true_result, false_result)

-- SAMPLE — random sampling
SELECT * FROM t SAMPLE (10);            -- 10% sample
SELECT * FROM t SAMPLE (100 ROWS);     -- 100 rows

-- TRY_CAST — safe cast (NULL on failure, no error)
TRY_CAST('abc' AS NUMBER)              -- Returns NULL
TRY_CAST('123' AS NUMBER)              -- Returns 123

-- DIV0 — safe division (0 if divisor = 0)
DIV0(numerator, denominator)

-- ZEROIFNULL — replace NULL with 0
ZEROIFNULL(possibly_null_value)

-- NVL — replace NULL
NVL(value, default_if_null)

-- FLATTEN — expand JSON arrays
SELECT f.value:field::STRING
FROM t, LATERAL FLATTEN(INPUT => t.json_col:array) f;

-- GENERATOR — create rows
SELECT SEQ4() FROM TABLE(GENERATOR(ROWCOUNT => 100));

-- PIVOT/UNPIVOT
SELECT * FROM t PIVOT (SUM(val) FOR col IN ('a', 'b', 'c'));

-- RESULT_SCAN — query previous results
SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
```

---

## Scenario Questions

**Q: How would you set up a data platform in Snowflake from scratch?**
A:
1. Create separate databases (or schemas): BRONZE, SILVER, GOLD
2. Create warehouses: ETL_WH (small, 60s auto-suspend), BI_WH (medium, 300s)
3. Create roles: DATA_ENGINEER, DBT_TRANSFORMER, DATA_ANALYST, BI_READER
4. Set up storage integration for S3/GCS
5. Create file formats (CSV, Parquet, JSON)
6. Set up Snowpipe or COPY INTO for ingestion
7. Set up dbt with Snowflake profile
8. Configure Power BI DirectQuery with BI_READER service account
9. Set up Resource Monitors for cost control
10. Enable Dynamic Masking on PII columns

**Q: Production data was accidentally deleted. What do you do?**
A:
1. Don't panic — Snowflake Time Travel covers you
2. Find when the DELETE ran: query `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY`
3. Get the query ID of the DELETE
4. Restore: `INSERT INTO table SELECT * FROM table BEFORE (STATEMENT => 'query_id')`
5. Validate row counts match pre-deletion
6. If table was dropped: `UNDROP TABLE table_name`
7. Post-incident: add row access policy or review who has DELETE privileges

**Q: How would you optimise a 5-minute daily dbt run on Snowflake?**
A:
1. Convert slow full-refresh models to incremental
2. Use the correct warehouse size for each model (staging=XS, marts=S or M)
3. Set `query_tag` to track which queries come from dbt
4. Use `CLUSTER BY` on large mart tables for downstream query speed
5. Use materialised views for frequently-queried Gold aggregations
6. Run staging and marts in parallel where dependencies allow
7. Monitor via `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY` filtered by `query_tag`

---

## Complete Command Reference

```sql
-- Context
USE ROLE / USE WAREHOUSE / USE DATABASE / USE SCHEMA

-- Warehouses
CREATE WAREHOUSE wh WAREHOUSE_SIZE='XSMALL' AUTO_SUSPEND=60 AUTO_RESUME=TRUE;
ALTER WAREHOUSE wh SET WAREHOUSE_SIZE='LARGE';
ALTER WAREHOUSE wh SUSPEND / RESUME;

-- Databases & Schemas
CREATE DATABASE db;
CREATE SCHEMA db.schema;
SHOW DATABASES / SCHEMAS / TABLES / WAREHOUSES;

-- Loading
PUT file://local @stage AUTO_COMPRESS=TRUE;
COPY INTO table FROM @stage FILE_FORMAT=(FORMAT_NAME='fmt') ON_ERROR=CONTINUE;
CREATE PIPE p AUTO_INGEST=TRUE AS COPY INTO table FROM @stage;

-- Time Travel
SELECT * FROM t AT (OFFSET => -3600);
SELECT * FROM t AT (TIMESTAMP => 'ts');
SELECT * FROM t BEFORE (STATEMENT => 'qid');
UNDROP TABLE / SCHEMA / DATABASE;

-- Cloning
CREATE TABLE t2 CLONE t1;
CREATE TABLE t2 CLONE t1 AT (OFFSET => -86400);
CREATE DATABASE db2 CLONE db1;

-- Streams & Tasks
CREATE STREAM s ON TABLE t;
CREATE TASK task WAREHOUSE=wh SCHEDULE='CRON' WHEN SYSTEM$STREAM_HAS_DATA('s') AS sql;
ALTER TASK task RESUME / SUSPEND;

-- Security
CREATE MASKING POLICY p AS (v TYPE) RETURNS TYPE -> CASE...;
ALTER TABLE t MODIFY COLUMN c SET MASKING POLICY p;
CREATE ROW ACCESS POLICY p AS (c TYPE) RETURNS BOOLEAN -> condition;
ALTER TABLE t ADD ROW ACCESS POLICY p ON (c);
CREATE NETWORK POLICY p ALLOWED_IP_LIST=('x.x.x.x/24');

-- Monitoring
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY;
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY;
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY;
```

---

## Previous | Next
← [[08 - Snowflake with dbt and Python]] | → [[Snowflake MOC]]
