---
title: Introduction to Snowflake
tags: [snowflake, cloud, data-warehouse, basics]
created: 2026-05-20
up:: [[Snowflake MOC]]
---

# ❄️ Introduction to Snowflake

> Snowflake is the leading cloud data warehouse — a fully managed, elastic SQL engine that separates storage from compute. It powers the modern data stack at companies like Adobe, DoorDash, and Capital One.

---

## What is Snowflake?

```
Traditional Database:        Snowflake:
  Storage + Compute          Storage    Compute
  tightly coupled            separated  elastic
  
  Scale one = scale both     Scale independently
  Pay for max capacity       Pay only for what you use
  Manage servers yourself    Fully managed — no DBA needed
  One region                 Multi-cloud, multi-region
```

---

## Snowflake vs Traditional Warehouses

| Feature | Snowflake | Redshift | BigQuery | On-Premise |
|---|---|---|---|---|
| **Architecture** | Shared storage | Shared nothing | Serverless | Traditional |
| **Scaling** | Instant, elastic | Manual resize | Auto | Manual |
| **Concurrency** | Multi-cluster | Limited | High | Limited |
| **Pricing** | Credits + storage | Instance + storage | Per query | CapEx |
| **Zero-copy clone** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Time travel** | ✅ Up to 90 days | ❌ No | ❌ No | ❌ No |
| **Data sharing** | ✅ Native | Limited | Limited | No |
| **Semi-structured** | ✅ Native VARIANT | Limited | JSON | No |

---

## Snowflake Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Cloud Services Layer               │
│   (Authentication, Metadata, Query Optimizer,       │
│    Security, Infrastructure Management)             │
├───────────────────────────────────────┬─────────────┤
│         Virtual Warehouses            │             │
│   ┌──────────┐  ┌──────────┐         │             │
│   │ WH Small │  │ WH Large │  ...    │  Storage    │
│   │ (compute)│  │ (compute)│         │  Layer      │
│   └──────────┘  └──────────┘         │             │
│    ETL Pipeline   BI Queries         │  (Micro-    │
│                                      │  partitions │
│                                      │  compressed │
│                                      │  columnar)  │
└──────────────────────────────────────┴─────────────┘
```

**Key insight**: Compute (warehouses) and Storage are completely separate. Multiple warehouses can query the same data simultaneously without contention.

---

## Core Concepts

```
Virtual Warehouse   = Compute cluster (XS to 6XL)
                      You start/stop/scale independently
                      Auto-suspends when idle

Database            = Container for schemas and objects

Schema              = Namespace within a database
                      e.g. BRONZE, SILVER, GOLD

Table               = Data storage (standard, external, temporary)

Stage               = Location for loading/unloading data
                      (internal or external S3/GCS/Azure)

File Format         = Instructions for parsing files (CSV, JSON, Parquet)

Pipe                = Continuous data ingestion (Snowpipe)

Stream              = Change data capture on a table

Task                = Scheduled SQL execution

Share               = Share data with other Snowflake accounts

Role                = Set of privileges (RBAC)

Credit              = Unit of compute consumption
```

---

## Snowflake Editions

```
Standard     — Basic SQL, time travel (1 day), 
               columnar storage
Enterprise   — Multi-cluster, time travel (90 days),
               dynamic data masking
Business     — Private Link, HIPAA, PCI compliance
Critical     — 99.99% SLA, cross-region replication
```

---

## Getting Started — Free Trial

```
1. Sign up at: app.snowflake.com
2. Choose cloud provider (AWS/GCP/Azure) and region
3. You get $400 free credits (about 30 days)
4. Access via:
   - Snowsight (web UI — recommended)
   - SQL Worksheets
   - Snowflake CLI (SnowSQL)
   - Python connector
   - dbt
```

---

## First Steps in Snowsight

```sql
-- Set context (run these first in every session)
USE ROLE SYSADMIN;
USE WAREHOUSE COMPUTE_WH;
USE DATABASE MY_DATABASE;
USE SCHEMA PUBLIC;

-- Check your current context
SELECT CURRENT_USER();
SELECT CURRENT_ROLE();
SELECT CURRENT_WAREHOUSE();
SELECT CURRENT_DATABASE();
SELECT CURRENT_SCHEMA();
SELECT CURRENT_VERSION();
```

---

## Create Your Data Platform

```sql
-- Step 1: Create databases (Medallion Architecture)
CREATE DATABASE IF NOT EXISTS DATA_VAULT;

-- Step 2: Create schemas
USE DATABASE DATA_VAULT;
CREATE SCHEMA IF NOT EXISTS BRONZE;
CREATE SCHEMA IF NOT EXISTS SILVER;
CREATE SCHEMA IF NOT EXISTS GOLD;
CREATE SCHEMA IF NOT EXISTS STAGING;
CREATE SCHEMA IF NOT EXISTS REFERENCE;

-- Step 3: Create warehouses
CREATE WAREHOUSE IF NOT EXISTS ETL_WH
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60           -- Suspend after 60s idle
    AUTO_RESUME = TRUE          -- Resume automatically
    COMMENT = 'ETL pipeline compute';

CREATE WAREHOUSE IF NOT EXISTS BI_WH
    WAREHOUSE_SIZE = 'SMALL'
    AUTO_SUSPEND = 300          -- Suspend after 5 min
    AUTO_RESUME = TRUE
    COMMENT = 'Power BI and reporting queries';

-- Step 4: Create roles
CREATE ROLE IF NOT EXISTS DATA_ENGINEER;
CREATE ROLE IF NOT EXISTS DATA_ANALYST;
CREATE ROLE IF NOT EXISTS BI_READER;

-- Step 5: Grant privileges
GRANT USAGE ON DATABASE DATA_VAULT TO ROLE DATA_ENGINEER;
GRANT USAGE ON ALL SCHEMAS IN DATABASE DATA_VAULT TO ROLE DATA_ENGINEER;
GRANT ALL ON ALL TABLES IN SCHEMA DATA_VAULT.SILVER TO ROLE DATA_ENGINEER;

GRANT USAGE ON DATABASE DATA_VAULT TO ROLE BI_READER;
GRANT USAGE ON SCHEMA DATA_VAULT.GOLD TO ROLE BI_READER;
GRANT SELECT ON ALL TABLES IN SCHEMA DATA_VAULT.GOLD TO ROLE BI_READER;
```

---

## Warehouse Sizes and Credits

```
Size        Servers   Credits/hr   Use Case
──────────────────────────────────────────────
X-Small     1         1            Dev, small ETL
Small       2         2            Small BI queries
Medium      4         4            Standard analytics
Large       8         8            Complex queries
X-Large     16        16           Large data loads
2X-Large    32        32           Very large workloads
3X-Large    64        64           Massive parallel
4X-Large    128       128          Extreme workloads

Cost: ~$3-4 per credit (varies by cloud/region)
X-Small for 1 hour = ~$3-4
Auto-suspend saves money when not in use!
```

---

## Snowflake SQL — What's Different

```sql
-- Snowflake SQL is ANSI-compatible with extensions

-- Semi-structured data (VARIANT type)
SELECT data:customer.name::STRING AS name
FROM json_table;

-- Zero-copy clone
CREATE TABLE my_table_dev CLONE my_table;

-- Time travel
SELECT * FROM my_table AT (OFFSET => -3600);  -- 1 hour ago
SELECT * FROM my_table BEFORE (STATEMENT => '019f...');

-- Data sharing
CREATE SHARE my_share;
GRANT USAGE ON DATABASE DATA_VAULT TO SHARE my_share;

-- Streams (CDC)
CREATE STREAM customer_stream ON TABLE customers;

-- Tasks (scheduled SQL)
CREATE TASK daily_refresh
    WAREHOUSE = ETL_WH
    SCHEDULE = 'USING CRON 0 6 * * * Africa/Nairobi'
    AS
    INSERT INTO gold.daily_summary SELECT ...;
```

---

## Connect Python to Snowflake

```python
# pip install snowflake-connector-python snowflake-sqlalchemy
import snowflake.connector
import os

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),     # e.g. xy12345.eu-west-1
    warehouse="ETL_WH",
    database="DATA_VAULT",
    schema="BRONZE"
)

cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM SILVER.BANK_CUSTOMERS")
print(cursor.fetchone())
conn.close()

# SQLAlchemy (for pandas)
from sqlalchemy import create_engine
engine = create_engine(
    f"snowflake://{os.getenv('SNOWFLAKE_USER')}:{os.getenv('SNOWFLAKE_PASSWORD')}"
    f"@{os.getenv('SNOWFLAKE_ACCOUNT')}/DATA_VAULT/SILVER"
    f"?warehouse=ETL_WH"
)
```

---

## Quick Reference

```sql
-- Context
USE ROLE role_name;
USE WAREHOUSE wh_name;
USE DATABASE db_name;
USE SCHEMA schema_name;

-- Objects
SHOW DATABASES;
SHOW SCHEMAS;
SHOW TABLES;
SHOW WAREHOUSES;
SHOW ROLES;

-- Warehouse control
ALTER WAREHOUSE ETL_WH SUSPEND;
ALTER WAREHOUSE ETL_WH RESUME;
ALTER WAREHOUSE ETL_WH SET WAREHOUSE_SIZE = 'LARGE';

-- Describe objects
DESCRIBE TABLE table_name;
DESCRIBE WAREHOUSE wh_name;
```

---

## Previous | Next
← Start | → [[02 - Snowflake Storage and Tables]]
