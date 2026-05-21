---
title: dbt Snapshots and Seeds
tags: [dbt, snapshots, seeds, scd]
created: 2026-05-20
up:: [[DBT MOC]]
---

# 📸 dbt Snapshots & Seeds

> Snapshots track how records change over time (SCD Type 2). Seeds load static CSV data into your warehouse. Together they complete your data warehouse's reference and historical data layers.

---

## dbt Seeds — Static Reference Data

Seeds are CSV files that dbt loads directly into your warehouse as tables. Perfect for lookup tables, mapping files, and static reference data.

### When to Use Seeds
```
✅ Country codes, currency codes
✅ Product category mappings
✅ Region/territory definitions
✅ Campaign tier thresholds
✅ Any small, rarely-changing reference table
❌ Large datasets (use sources instead)
❌ Frequently changing data (use sources)
```

---

## Creating Seeds

```
seeds/
├── country_codes.csv
├── job_categories.csv
├── campaign_tiers.csv
└── region_mapping.csv
```

```csv
# seeds/country_codes.csv
country_code,country_name,region,currency
KE,Kenya,East Africa,KES
UG,Uganda,East Africa,UGX
TZ,Tanzania,East Africa,TZS
NG,Nigeria,West Africa,NGN
ZA,South Africa,Southern Africa,ZAR
GH,Ghana,West Africa,GHS
ET,Ethiopia,East Africa,ETB
```

```csv
# seeds/job_categories.csv
job,job_category,is_professional
admin,White Collar,true
management,White Collar,true
technician,Technical,true
blue-collar,Blue Collar,false
services,Services,false
retired,Retired,false
student,Student,false
entrepreneur,Business,true
self-employed,Business,true
housemaid,Services,false
unemployed,Other,false
unknown,Other,false
```

```csv
# seeds/campaign_tier_thresholds.csv
tier_name,min_balance,max_balance,interest_rate,annual_fee
bronze,0,9999,0.03,0
silver,10000,49999,0.05,500
gold,50000,99999,0.08,0
platinum,100000,999999999,0.12,0
```

---

## Configuring Seeds

```yaml
# dbt_project.yml
seeds:
  my_project:
    +schema: reference              # Load to reference schema
    +quote_columns: false
    
    country_codes:
      +column_types:
        country_code: varchar(2)
        country_name: varchar(100)
    
    campaign_tier_thresholds:
      +column_types:
        min_balance: decimal(12,2)
        max_balance: decimal(12,2)
        interest_rate: decimal(5,4)
```

```bash
# Load seeds to warehouse
dbt seed

# Load specific seed
dbt seed --select country_codes

# Reload seed (drop and recreate)
dbt seed --full-refresh
```

---

## Using Seeds in Models

```sql
-- models/staging/stg_bank_marketing.sql
-- Enrich with job category lookup

WITH raw AS (
    SELECT * FROM {{ source('raw', 'bank_marketing') }}
),

job_categories AS (
    SELECT * FROM {{ ref('job_categories') }}   -- Reference seed!
),

country_codes AS (
    SELECT * FROM {{ ref('country_codes') }}
)

SELECT
    r.age,
    r.job,
    jc.job_category,
    jc.is_professional,
    r.balance,
    r.subscribed
FROM raw r
LEFT JOIN job_categories jc ON LOWER(r.job) = LOWER(jc.job)
```

```sql
-- models/marts/dim_customers.sql
-- Enrich customers with tier thresholds

WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

tiers AS (
    SELECT * FROM {{ ref('campaign_tier_thresholds') }}
)

SELECT
    c.*,
    t.tier_name AS calculated_tier,
    t.interest_rate,
    ROUND(c.balance * t.interest_rate, 2) AS estimated_annual_interest
FROM customers c
LEFT JOIN tiers t
    ON c.balance >= t.min_balance
    AND c.balance <= t.max_balance
```

---

## dbt Snapshots — Track Historical Changes

Snapshots implement **SCD Type 2** — they track how records change over time by creating a new row for each change, with `valid_from` and `valid_to` timestamps.

### The Problem Snapshots Solve

```
Monday:   Customer tier = Silver, balance = 45,000
Tuesday:  Customer gets promoted to Gold, balance = 52,000

Without snapshots: Only see current state (Gold)
With snapshots:    See full history (Silver → Gold with dates)
```

---

## Creating a Snapshot

```sql
-- snapshots/customers_snapshot.sql
{% snapshot customers_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='timestamp',           -- Track by updated_at timestamp
        updated_at='updated_at',        -- Column that changes when record updates
        invalidate_hard_deletes=True    -- Mark deleted records as expired
    )
}}

SELECT
    customer_id,
    customer_name,
    email,
    city,
    tier,
    balance,
    is_active,
    updated_at
FROM {{ ref('stg_customers') }}

{% endsnapshot %}
```

---

## Snapshot Strategies

### Strategy 1: Timestamp (Recommended)
```sql
{% snapshot customers_snapshot %}
{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='timestamp',
        updated_at='updated_at'     -- Must exist in source
    )
}}
SELECT * FROM {{ ref('stg_customers') }}
{% endsnapshot %}
```

### Strategy 2: Check (No updated_at column)
```sql
{% snapshot customers_snapshot_check %}
{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='check',
        check_cols=['tier', 'balance', 'city']  -- Track changes to these
    )
}}
SELECT * FROM {{ ref('stg_customers') }}
{% endsnapshot %}
```

---

## What dbt Creates

After running `dbt snapshot`, dbt adds these columns:

```sql
-- snapshots.customers_snapshot
SELECT
    customer_id,
    customer_name,
    tier,
    balance,
    -- dbt-added SCD columns:
    dbt_scd_id,         -- Unique key for each version
    dbt_updated_at,     -- When this version was created
    dbt_valid_from,     -- When this version became active
    dbt_valid_to        -- When this version expired (NULL = current)
FROM snapshots.customers_snapshot
```

---

## Querying Snapshot Data

```sql
-- Current state (like regular table)
SELECT *
FROM snapshots.customers_snapshot
WHERE dbt_valid_to IS NULL;

-- Historical state at a specific date
SELECT *
FROM snapshots.customers_snapshot
WHERE customer_id = 1
  AND dbt_valid_from <= '2025-06-01'
  AND (dbt_valid_to > '2025-06-01' OR dbt_valid_to IS NULL);

-- Full history for a customer
SELECT
    customer_id,
    tier,
    balance,
    dbt_valid_from,
    dbt_valid_to,
    CASE WHEN dbt_valid_to IS NULL THEN 'Current' ELSE 'Historical' END AS record_status
FROM snapshots.customers_snapshot
WHERE customer_id = 1
ORDER BY dbt_valid_from;

-- How many customers changed tier each month?
SELECT
    DATE_TRUNC('month', dbt_valid_from)     AS month,
    tier AS new_tier,
    COUNT(*)                                AS tier_changes
FROM snapshots.customers_snapshot
WHERE dbt_valid_from != (
    SELECT MIN(dbt_valid_from)
    FROM snapshots.customers_snapshot s2
    WHERE s2.customer_id = customers_snapshot.customer_id
)
GROUP BY 1, 2
ORDER BY 1, 3 DESC;
```

---

## Real World Snapshot — Bank Marketing

```sql
-- snapshots/bank_customers_snapshot.sql
-- Track customer tier and balance changes over time

{% snapshot bank_customers_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='check',
        check_cols=['tier', 'balance', 'is_active', 'city'],
        invalidate_hard_deletes=True
    )
}}

SELECT
    customer_id,
    customer_name,
    email,
    city,
    tier,
    balance,
    is_active,
    created_date
FROM {{ ref('stg_customers') }}

{% endsnapshot %}
```

```sql
-- Using snapshot in a mart model
-- models/marts/dim_customers_history.sql

SELECT
    customer_id,
    customer_name,
    tier,
    balance,
    city,
    dbt_valid_from                      AS valid_from,
    COALESCE(dbt_valid_to,
        '9999-12-31'::DATE)             AS valid_to,
    dbt_valid_to IS NULL                AS is_current,

    -- Tier progression
    LAG(tier) OVER (
        PARTITION BY customer_id
        ORDER BY dbt_valid_from
    )                                   AS previous_tier,

    CASE
        WHEN LAG(tier) OVER (
            PARTITION BY customer_id ORDER BY dbt_valid_from
        ) IS NULL THEN 'New Customer'
        WHEN tier > LAG(tier) OVER (
            PARTITION BY customer_id ORDER BY dbt_valid_from
        ) THEN 'Upgraded'
        WHEN tier < LAG(tier) OVER (
            PARTITION BY customer_id ORDER BY dbt_valid_from
        ) THEN 'Downgraded'
        ELSE 'No Change'
    END                                 AS tier_movement

FROM {{ ref('bank_customers_snapshot') }}
ORDER BY customer_id, dbt_valid_from
```

---

## Running Snapshots

```bash
# Run all snapshots
dbt snapshot

# Run specific snapshot
dbt snapshot --select bank_customers_snapshot

# Run snapshot in full refresh (rebuild from scratch)
# WARNING: loses history!
dbt snapshot --full-refresh

# Snapshots as part of full build
# Note: dbt build does NOT run snapshots
# Run separately:
dbt snapshot && dbt build
```

---

## Seeds + Snapshots Together

```sql
-- models/marts/fct_tier_analysis.sql
-- Combine snapshot history with seed reference data

WITH customer_history AS (
    SELECT * FROM {{ ref('bank_customers_snapshot') }}
    WHERE dbt_valid_to IS NULL       -- Current records only
),

tier_thresholds AS (
    SELECT * FROM {{ ref('campaign_tier_thresholds') }}   -- Seed
),

job_categories AS (
    SELECT * FROM {{ ref('job_categories') }}              -- Seed
),

customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
)

SELECT
    ch.customer_id,
    ch.customer_name,
    ch.tier,
    tt.interest_rate,
    tt.annual_fee,
    jc.job_category,
    ch.balance,
    ROUND(ch.balance * tt.interest_rate, 2) AS annual_interest,
    ch.dbt_valid_from                       AS current_tier_since
FROM customer_history ch
JOIN customers c ON ch.customer_id = c.customer_id
LEFT JOIN tier_thresholds tt ON ch.tier = LOWER(tt.tier_name)
LEFT JOIN job_categories jc ON c.job = jc.job
```

---

## Quick Reference

```bash
# Seeds
dbt seed                    # Load all seeds
dbt seed --select seed_name # Load specific seed
dbt seed --full-refresh     # Drop and reload

# Snapshots
dbt snapshot                # Run all snapshots
dbt snapshot --select name  # Run specific snapshot

# Snapshot columns (auto-added by dbt)
dbt_scd_id      # Unique per version
dbt_updated_at  # When version was created
dbt_valid_from  # Version start date
dbt_valid_to    # Version end date (NULL = current)

# Query current state
WHERE dbt_valid_to IS NULL

# Query at a point in time
WHERE dbt_valid_from <= 'date'
  AND (dbt_valid_to > 'date' OR dbt_valid_to IS NULL)
```

---

## Previous | Next
← [[05 - dbt Macros and Jinja]] | → [[07 - dbt Incremental Models]]
