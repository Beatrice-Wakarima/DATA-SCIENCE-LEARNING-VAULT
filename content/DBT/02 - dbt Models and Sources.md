---
title: dbt Models and Sources
tags: [dbt, models, sources, sql]
created: 2026-05-20
up:: [[DBT MOC]]
---

# 🧱 dbt Models & Sources

> Models are the heart of dbt — SQL SELECT statements that define your transformations. Sources define the raw tables dbt reads from. Together they form the foundation of every dbt project.

---

## What is a dbt Model?

```sql
-- models/staging/stg_customers.sql
-- A model is just a SELECT statement!
-- dbt wraps it in CREATE TABLE/VIEW automatically

SELECT
    id          AS customer_id,
    name        AS customer_name,
    email,
    city,
    balance,
    tier,
    is_active,
    joined_date AS created_at
FROM raw.customers
WHERE name IS NOT NULL
```

That's it. dbt handles the rest:
- Creates `staging.stg_customers` as a view or table
- Tracks lineage
- Enables testing
- Generates documentation

---

## Referencing Models with ref()

```sql
-- models/marts/dim_customers.sql
-- Use {{ ref() }} to reference other models (NEVER hardcode table names)

SELECT
    c.customer_id,
    c.customer_name,
    c.email,
    c.city,
    c.tier,
    c.created_at,
    COUNT(t.transaction_id)     AS total_transactions,
    SUM(t.amount)               AS lifetime_value
FROM {{ ref('stg_customers') }} c          -- References staging model!
LEFT JOIN {{ ref('stg_transactions') }} t
    ON c.customer_id = t.customer_id
GROUP BY 1, 2, 3, 4, 5, 6
```

Why `ref()` instead of table names?
- dbt resolves the correct schema automatically
- Builds the dependency graph (lineage)
- Enables model ordering during `dbt run`
- Works across environments (dev/prod)

---

## Defining Sources

```yaml
# models/staging/_sources.yml
version: 2

sources:
  - name: raw                           # Source name
    database: data_vault                # Optional: specific database
    schema: bronze                      # Schema in warehouse
    
    tables:
      - name: customers
        description: "Raw customer data from CRM system"
        loaded_at_field: loaded_at      # For freshness checks
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
        
        columns:
          - name: id
            description: "Primary key"
            tests:
              - unique
              - not_null
          - name: email
            tests:
              - unique
      
      - name: transactions
        description: "Raw transaction data from banking system"
        loaded_at_field: loaded_at
        freshness:
          warn_after: {count: 1, period: hour}
          error_after: {count: 6, period: hour}
      
      - name: bank_marketing
        description: "Bank marketing campaign data"
```

```sql
-- Reference sources with source() function
-- models/staging/stg_bank_marketing.sql

SELECT *
FROM {{ source('raw', 'bank_marketing') }}   -- source('name', 'table')
WHERE age IS NOT NULL
  AND balance IS NOT NULL
```

---

## Complete Staging Layer — Bank Marketing

```sql
-- models/staging/stg_bank_marketing.sql
{{
    config(
        materialized='view',
        schema='staging'
    )
}}

WITH source AS (
    SELECT * FROM {{ source('raw', 'bank_marketing') }}
),

cleaned AS (
    SELECT
        -- Integer fields
        CAST(age AS INTEGER)                                AS age,

        -- Cleaned strings
        TRIM(LOWER(job))                                    AS job,
        TRIM(LOWER(marital))                                AS marital,
        TRIM(LOWER(education))                              AS education,
        TRIM(LOWER(contact))                                AS contact,
        TRIM(LOWER(month))                                  AS month,
        TRIM(LOWER(poutcome))                               AS poutcome,

        -- Numeric fields
        CAST(balance AS DECIMAL(12,2))                      AS balance,
        CAST(duration AS INTEGER)                           AS call_duration_seconds,
        CAST(campaign AS INTEGER)                           AS campaign_contacts,
        CAST(previous AS INTEGER)                           AS previous_contacts,

        -- Boolean target
        CASE
            WHEN LOWER(TRIM(y)) = 'yes' THEN TRUE
            ELSE FALSE
        END                                                 AS subscribed,

        -- Derived fields
        CASE
            WHEN CAST(balance AS DECIMAL) > 10000   THEN 'high'
            WHEN CAST(balance AS DECIMAL) > 1000    THEN 'medium'
            WHEN CAST(balance AS DECIMAL) > 0       THEN 'low'
            ELSE 'negative'
        END                                                 AS balance_segment,

        CASE
            WHEN CAST(age AS INTEGER) < 30  THEN 'young'
            WHEN CAST(age AS INTEGER) < 50  THEN 'middle'
            ELSE 'senior'
        END                                                 AS age_segment,

        -- Metadata
        loaded_at

    FROM source
    WHERE age IS NOT NULL
      AND CAST(age AS INTEGER) BETWEEN 18 AND 95
      AND balance IS NOT NULL
)

SELECT * FROM cleaned
```

---

## Staging Models — Best Practices

```sql
-- ✅ Good staging model pattern
-- models/staging/stg_customers.sql
{{
    config(materialized='view')
}}

WITH source AS (
    -- Always reference source, not raw table name
    SELECT * FROM {{ source('raw', 'customers') }}
),

renamed AS (
    SELECT
        -- Rename and cast in staging
        id                          AS customer_id,
        TRIM(INITCAP(name))         AS customer_name,
        LOWER(TRIM(email))          AS email,
        TRIM(INITCAP(city))         AS city,
        CAST(balance AS DECIMAL(12,2)) AS balance,
        LOWER(TRIM(tier))           AS tier,
        is_active,
        CAST(joined_date AS DATE)   AS created_date,
        loaded_at
    FROM source
    WHERE id IS NOT NULL            -- Basic quality filter
)

SELECT * FROM renamed
```

---

## Intermediate Models — Business Logic

```sql
-- models/intermediate/int_customer_transactions.sql
-- Join and enrich — business logic goes here
{{
    config(materialized='ephemeral')   -- Used as CTE, not stored
}}

WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

transactions AS (
    SELECT * FROM {{ ref('stg_transactions') }}
),

transaction_summary AS (
    SELECT
        customer_id,
        COUNT(*)                        AS total_transactions,
        SUM(amount)                     AS lifetime_value,
        AVG(amount)                     AS avg_transaction,
        MAX(created_at)                 AS last_transaction_date,
        MIN(created_at)                 AS first_transaction_date,
        SUM(CASE WHEN type = 'deposit' THEN amount ELSE 0 END) AS total_deposits,
        SUM(CASE WHEN type = 'withdrawal' THEN amount ELSE 0 END) AS total_withdrawals
    FROM transactions
    GROUP BY customer_id
)

SELECT
    c.*,
    COALESCE(ts.total_transactions, 0)  AS total_transactions,
    COALESCE(ts.lifetime_value, 0)      AS lifetime_value,
    COALESCE(ts.avg_transaction, 0)     AS avg_transaction,
    ts.last_transaction_date,
    ts.first_transaction_date,
    COALESCE(ts.total_deposits, 0)      AS total_deposits,
    COALESCE(ts.total_withdrawals, 0)   AS total_withdrawals,

    -- Derived
    CASE
        WHEN ts.lifetime_value > 500000 THEN 'platinum'
        WHEN ts.lifetime_value > 100000 THEN 'gold'
        WHEN ts.lifetime_value > 10000  THEN 'silver'
        ELSE 'bronze'
    END                                 AS calculated_tier

FROM customers c
LEFT JOIN transaction_summary ts ON c.customer_id = ts.customer_id
```

---

## Mart Models — Business-Ready

```sql
-- models/marts/finance/fct_monthly_revenue.sql
-- Fact table for Power BI dashboards
{{
    config(
        materialized='table',
        schema='marts'
    )
}}

WITH customer_transactions AS (
    SELECT * FROM {{ ref('int_customer_transactions') }}
),

transactions AS (
    SELECT * FROM {{ ref('stg_transactions') }}
),

monthly_agg AS (
    SELECT
        DATE_TRUNC('month', t.created_at)   AS month,
        c.city,
        c.tier,
        c.calculated_tier,
        c.age_segment,

        COUNT(DISTINCT t.customer_id)        AS unique_customers,
        COUNT(t.transaction_id)             AS total_transactions,
        SUM(t.amount)                       AS total_revenue,
        AVG(t.amount)                       AS avg_transaction,
        MAX(t.amount)                       AS max_transaction,
        SUM(CASE WHEN t.type = 'deposit'
            THEN t.amount ELSE 0 END)       AS deposit_volume,
        SUM(CASE WHEN t.type = 'withdrawal'
            THEN t.amount ELSE 0 END)       AS withdrawal_volume

    FROM transactions t
    JOIN customer_transactions c ON t.customer_id = c.customer_id
    GROUP BY 1, 2, 3, 4, 5
)

SELECT
    month,
    city,
    tier,
    calculated_tier,
    age_segment,
    unique_customers,
    total_transactions,
    total_revenue,
    avg_transaction,
    max_transaction,
    deposit_volume,
    withdrawal_volume,

    -- Running totals (window functions work in dbt!)
    SUM(total_revenue) OVER (ORDER BY month) AS cumulative_revenue,

    -- Growth
    LAG(total_revenue) OVER (ORDER BY month) AS prev_month_revenue,
    ROUND(
        100.0 * (total_revenue - LAG(total_revenue) OVER (ORDER BY month))
        / NULLIF(LAG(total_revenue) OVER (ORDER BY month), 0),
        1
    )                                       AS mom_growth_pct

FROM monthly_agg
ORDER BY month, total_revenue DESC
```

---

## Model Configuration Options

```sql
-- Inline config (top of model file)
{{
    config(
        materialized='table',           -- view | table | incremental | ephemeral
        schema='marts',                 -- Override schema
        alias='my_custom_table_name',   -- Override table name
        tags=['finance', 'daily'],      -- For selective runs
        pre_hook="TRUNCATE TABLE ...",  -- Run before model
        post_hook="GRANT SELECT ...",   -- Run after model
        indexes=[
            {'columns': ['customer_id'], 'unique': True},
            {'columns': ['created_at']}
        ]
    )
}}
```

```yaml
# Or in dbt_project.yml (applies to whole folder)
models:
  my_project:
    marts:
      finance:
        +materialized: table
        +tags: ['finance']
        +post_hook: "GRANT SELECT ON {{ this }} TO bi_reader"
```

---

## Selective Model Runs

```bash
# Run specific model
dbt run --select stg_customers

# Run model and everything downstream
dbt run --select stg_customers+

# Run model and everything upstream
dbt run --select +dim_customers

# Run model and all dependencies in both directions
dbt run --select +dim_customers+

# Run by tag
dbt run --select tag:finance

# Run by folder
dbt run --select staging
dbt run --select marts.finance

# Run changed models only (using git state)
dbt run --select state:modified+

# Exclude specific models
dbt run --exclude stg_old_data
```

---

## Quick Reference

```sql
-- Source reference
{{ source('source_name', 'table_name') }}

-- Model reference
{{ ref('model_name') }}

-- Config block
{{ config(materialized='table', schema='marts') }}

-- Jinja variable
{{ var('start_date', '2026-01-01') }}

-- Environment variable
{{ env_var('DB_PASSWORD') }}
```

---

## Previous | Next
← [[01 - Introduction to dbt]] | → [[03 - dbt Tests]]
