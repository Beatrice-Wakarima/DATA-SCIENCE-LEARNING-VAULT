---
title: dbt Incremental Models
tags: [dbt, incremental, performance, data-engineering]
created: 2026-05-20
up:: [[DBT MOC]]
---

# ⚡ dbt Incremental Models

> Incremental models only process new or changed data instead of rebuilding the entire table. They are the key to making dbt fast and cost-efficient at scale — processing millions of rows in seconds instead of hours.

---

## The Problem With Tables

```
Non-incremental (table materialisation):
  Every dbt run → DROP TABLE → CREATE TABLE → INSERT ALL ROWS
  
  Monday:   Process 1M rows  (60 seconds)
  Tuesday:  Process 1M rows  (60 seconds) ← same 1M rows again!
  Wednesday: Process 1M rows (60 seconds) ← same again!
  
Incremental:
  First run: Process 1M rows (60 seconds)
  Tuesday:   Process 1,000 NEW rows (1 second) ← only new data!
  Wednesday: Process 500 NEW rows (0.5 seconds) ← only new data!
```

---

## Basic Incremental Model

```sql
-- models/marts/fct_transactions.sql
{{
    config(
        materialized='incremental',
        unique_key='transaction_id'     -- Used to handle duplicates
    )
}}

SELECT
    transaction_id,
    customer_id,
    amount,
    type,
    created_at
FROM {{ ref('stg_transactions') }}

-- This is the KEY block — only runs on incremental runs
{% if is_incremental() %}
WHERE created_at > (
    SELECT MAX(created_at)
    FROM {{ this }}         -- {{ this }} = the existing table
)
{% endif %}
```

---

## How Incremental Works

```
First run (--full-refresh or new table):
  is_incremental() = FALSE
  → Runs without WHERE clause
  → Creates table with ALL rows

Subsequent runs:
  is_incremental() = TRUE
  → Runs WITH WHERE clause
  → Only processes rows newer than max(created_at)
  → Merges/inserts into existing table
```

---

## Incremental Strategies

### Strategy 1: append (fastest, simplest)
```sql
{{
    config(
        materialized='incremental',
        incremental_strategy='append'   -- Just INSERT new rows
    )
}}

SELECT * FROM {{ ref('stg_transactions') }}
{% if is_incremental() %}
WHERE created_at > (SELECT MAX(created_at) FROM {{ this }})
{% endif %}
-- Note: No unique_key needed. Duplicates possible if run twice!
```

### Strategy 2: merge (most robust)
```sql
{{
    config(
        materialized='incremental',
        unique_key='transaction_id',
        incremental_strategy='merge'    -- UPDATE existing + INSERT new
    )
}}

SELECT * FROM {{ ref('stg_transactions') }}
{% if is_incremental() %}
WHERE created_at > (SELECT MAX(created_at) FROM {{ this }})
{% endif %}
-- Safe: updates if exists, inserts if new
```

### Strategy 3: delete+insert (PostgreSQL default)
```sql
{{
    config(
        materialized='incremental',
        unique_key='transaction_id',
        incremental_strategy='delete+insert'
    )
}}

SELECT * FROM {{ ref('stg_transactions') }}
{% if is_incremental() %}
WHERE created_at > (SELECT MAX(created_at) FROM {{ this }})
{% endif %}
-- Deletes matching unique_key rows then re-inserts
-- Good for when rows can be updated (not just appended)
```

---

## Safe Incremental with Buffer

```sql
-- models/marts/fct_transactions_incremental.sql
{{
    config(
        materialized='incremental',
        unique_key='transaction_id',
        incremental_strategy='merge'
    )
}}

WITH source AS (
    SELECT * FROM {{ ref('stg_transactions') }}
),

incremental_filter AS (
    SELECT *
    FROM source
    
    {% if is_incremental() %}
    -- Load last 3 days to catch late-arriving data
    WHERE created_at >= (
        SELECT MAX(created_at) - INTERVAL '3 days'
        FROM {{ this }}
    )
    {% endif %}
)

SELECT
    transaction_id,
    customer_id,
    amount,
    type,
    created_at,
    DATE_TRUNC('month', created_at) AS transaction_month,
    CASE
        WHEN amount > 100000 THEN 'large'
        WHEN amount > 10000  THEN 'medium'
        ELSE 'small'
    END AS transaction_size
FROM incremental_filter
```

---

## Partition-Based Incremental

```sql
-- Efficient for date-partitioned data
{{
    config(
        materialized='incremental',
        unique_key=['customer_id', 'transaction_month'],
        incremental_strategy='merge',
        partition_by={
            "field": "transaction_month",
            "data_type": "date",
            "granularity": "month"
        }
    )
}}

WITH monthly_agg AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', created_at)::DATE   AS transaction_month,
        COUNT(*)                                AS transaction_count,
        SUM(amount)                             AS total_amount,
        MAX(created_at)                         AS last_transaction
    FROM {{ ref('stg_transactions') }}
    
    {% if is_incremental() %}
    -- Only process current and previous month
    WHERE DATE_TRUNC('month', created_at) >= (
        SELECT DATE_TRUNC('month', MAX(transaction_month)) - INTERVAL '1 month'
        FROM {{ this }}
    )
    {% endif %}
    
    GROUP BY 1, 2
)

SELECT * FROM monthly_agg
```

---

## Handling Late-Arriving Data

```sql
-- Some events arrive days late (webhooks, retries, etc.)
-- Solution: always look back N days

{{
    config(
        materialized='incremental',
        unique_key='event_id'
    )
}}

SELECT
    event_id,
    customer_id,
    event_type,
    event_timestamp,
    processed_at
FROM {{ ref('stg_events') }}

{% if is_incremental() %}
-- Look back 7 days to catch late-arriving events
WHERE event_timestamp >= (
    SELECT GREATEST(
        MAX(event_timestamp) - INTERVAL '7 days',
        CURRENT_DATE - INTERVAL '30 days'   -- Hard limit
    )
    FROM {{ this }}
)
{% endif %}
```

---

## On Schema Change

```sql
-- What happens when you add a column to an incremental model?
{{
    config(
        materialized='incremental',
        unique_key='transaction_id',
        on_schema_change='sync_all_columns'  -- Options below
    )
}}
```

```
on_schema_change options:
  'ignore'           — Default. New columns ignored, old columns kept
  'fail'             — Raise error if schema changes
  'append_new_columns' — Add new columns, keep existing data
  'sync_all_columns'  — Add new cols, remove deleted cols (risky!)
```

---

## Full Refresh — Rebuild from Scratch

```bash
# Force full rebuild (ignores is_incremental() check)
dbt run --full-refresh --select fct_transactions

# When to use full refresh:
# - Schema changed significantly
# - Data quality issue found in historical data
# - Adding new column that needs backfill
# - First time setting up model
```

---

## Incremental vs Table — Decision Guide

```
Use TABLE when:
  ✅ Small dataset (< 1M rows)
  ✅ Complex transformations (easier to debug)
  ✅ Reference/dimension tables
  ✅ Run time < 5 minutes anyway

Use INCREMENTAL when:
  ✅ Large dataset (> 1M rows)
  ✅ Append-only data (events, transactions, logs)
  ✅ Run time is too long with TABLE
  ✅ Cost-sensitive (Snowflake, BigQuery charge per query)
  ✅ Clear timestamp or updated_at column exists
```

---

## Real World — Bank Marketing Pipeline

```sql
-- models/marts/fct_daily_campaign_stats.sql
-- Daily aggregation — incremental to avoid rebuilding years of data

{{
    config(
        materialized='incremental',
        unique_key=['stat_date', 'job', 'balance_segment'],
        incremental_strategy='merge'
    )
}}

WITH daily_contacts AS (
    SELECT
        CURRENT_DATE                            AS stat_date,
        job,
        balance_segment,
        age_segment,
        COUNT(*)                                AS total_contacts,
        SUM(CASE WHEN subscribed THEN 1 ELSE 0 END) AS subscriptions,
        ROUND(AVG(balance), 2)                 AS avg_balance,
        ROUND(AVG(call_duration_seconds), 0)   AS avg_call_duration
    FROM {{ ref('stg_bank_marketing') }}
    
    {% if is_incremental() %}
    -- Only process today's new contacts
    WHERE loaded_at >= (
        SELECT MAX(loaded_at) - INTERVAL '1 hour'
        FROM {{ this }}
    )
    {% endif %}
    
    GROUP BY 1, 2, 3, 4
)

SELECT
    stat_date,
    job,
    balance_segment,
    age_segment,
    total_contacts,
    subscriptions,
    ROUND(
        100.0 * subscriptions / NULLIF(total_contacts, 0),
        2
    )                                           AS conversion_rate,
    avg_balance,
    avg_call_duration,
    {{ current_timestamp() }}                   AS updated_at
FROM daily_contacts
```

---

## Monitoring Incremental Models

```sql
-- Check how much data was loaded in each run
-- Add an audit column to your incremental model:

SELECT
    transaction_id,
    customer_id,
    amount,
    created_at,
    -- Audit columns
    CURRENT_TIMESTAMP           AS dbt_loaded_at,
    '{{ invocation_id }}'       AS dbt_invocation_id
FROM {{ ref('stg_transactions') }}

{% if is_incremental() %}
WHERE created_at > (SELECT MAX(created_at) FROM {{ this }})
{% endif %}
```

```sql
-- Query: how many rows loaded per run?
SELECT
    dbt_loaded_at::DATE         AS load_date,
    COUNT(*)                    AS rows_loaded,
    MIN(created_at)             AS earliest_transaction,
    MAX(created_at)             AS latest_transaction
FROM marts.fct_transactions
GROUP BY 1
ORDER BY 1 DESC;
```

---

## Quick Reference

```sql
-- Basic incremental
{{ config(materialized='incremental', unique_key='id') }}
SELECT * FROM source
{% if is_incremental() %}
WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}

-- With 3-day buffer for late data
{% if is_incremental() %}
WHERE updated_at >= (SELECT MAX(updated_at) - INTERVAL '3 days' FROM {{ this }})
{% endif %}

-- Strategies
incremental_strategy='append'         -- INSERT only
incremental_strategy='merge'          -- UPDATE + INSERT
incremental_strategy='delete+insert'  -- DELETE + INSERT

-- Schema changes
on_schema_change='sync_all_columns'

-- Commands
dbt run --select model                 -- Incremental run
dbt run --full-refresh --select model  -- Full rebuild
```

---

## Previous | Next
← [[06 - dbt Snapshots and Seeds]] | → [[08 - dbt with Docker and Airflow]]
