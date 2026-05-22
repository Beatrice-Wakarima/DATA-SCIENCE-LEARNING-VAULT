---
title: Data Warehouse Design
tags: [data-engineering, warehouse, architecture, sql]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# 🏛️ Data Warehouse Design

> A well-designed data warehouse is the foundation of reliable analytics. Poor design leads to slow queries, incorrect numbers, and unhappy stakeholders. Good design makes every downstream task — dbt, Power BI, ML — easier.

---

## What is a Data Warehouse?

```
OLTP Database               Data Warehouse (OLAP)
────────────────────        ──────────────────────────
Optimised for writes        Optimised for reads
Many small transactions      Few large analytical queries
Normalised (3NF)            Denormalised (Star/Snowflake)
Row-oriented storage        Column-oriented storage
Current state only          Historical data preserved
e.g. PostgreSQL (prod)      e.g. Snowflake, BigQuery
```

---

## Kimball's Dimensional Modelling

The most widely used data warehouse design pattern:

```
FACT TABLE                  DIMENSION TABLES
──────────────              ────────────────────
Measurements/metrics        Descriptive attributes
Foreign keys                Primary key
Numeric values              Low cardinality fields
Grain = one row per event   Static or slowly changing
e.g. fct_transactions       e.g. dim_customers, dim_date
```

---

## Star Schema

```
                    dim_date
                        │
dim_customers ──── fct_transactions ──── dim_products
                        │
                    dim_location

Central fact table joined directly to dimension tables.
Simpler, faster queries. Most common pattern.
```

---

## Bank Marketing Star Schema

```sql
-- ── DIMENSION TABLES ──────────────────────────────────────

-- Customer dimension
CREATE TABLE dim_customers (
    customer_sk         BIGSERIAL PRIMARY KEY,      -- Surrogate key
    customer_id         INTEGER NOT NULL,            -- Natural key
    customer_name       VARCHAR(100),
    email               VARCHAR(100),
    city                VARCHAR(50),
    tier                VARCHAR(20),
    age                 INTEGER,
    age_segment         VARCHAR(20),
    job                 VARCHAR(50),
    job_category        VARCHAR(50),
    marital             VARCHAR(20),
    education           VARCHAR(50),
    balance             DECIMAL(12,2),
    balance_segment     VARCHAR(20),
    is_active           BOOLEAN,
    -- SCD Type 2 fields
    valid_from          DATE NOT NULL,
    valid_to            DATE,
    is_current          BOOLEAN DEFAULT TRUE,
    -- Metadata
    created_at          TIMESTAMP DEFAULT NOW()
);

-- Date dimension (pre-populated)
CREATE TABLE dim_date (
    date_key            INTEGER PRIMARY KEY,    -- YYYYMMDD format
    full_date           DATE NOT NULL,
    day_of_week         INTEGER,
    day_name            VARCHAR(10),
    day_of_month        INTEGER,
    day_of_year         INTEGER,
    week_of_year        INTEGER,
    month_number        INTEGER,
    month_name          VARCHAR(10),
    month_short         CHAR(3),
    quarter             INTEGER,
    quarter_name        VARCHAR(6),
    year                INTEGER,
    is_weekend          BOOLEAN,
    is_holiday          BOOLEAN DEFAULT FALSE,
    fiscal_year         INTEGER,
    fiscal_quarter      INTEGER
);

-- Campaign dimension
CREATE TABLE dim_campaigns (
    campaign_sk         BIGSERIAL PRIMARY KEY,
    campaign_id         INTEGER,
    campaign_number     INTEGER,
    contact_method      VARCHAR(20),
    month               VARCHAR(10),
    year                INTEGER,
    campaign_quarter    VARCHAR(6)
);

-- ── FACT TABLE ────────────────────────────────────────────

-- Campaign contacts fact table
CREATE TABLE fct_campaign_contacts (
    contact_sk          BIGSERIAL PRIMARY KEY,

    -- Foreign keys to dimensions
    customer_sk         BIGINT REFERENCES dim_customers(customer_sk),
    date_key            INTEGER REFERENCES dim_date(date_key),
    campaign_sk         BIGINT REFERENCES dim_campaigns(campaign_sk),

    -- Degenerate dimensions (no separate table needed)
    contact_method      VARCHAR(20),
    outcome             VARCHAR(20),

    -- Facts / measures
    call_duration_secs  INTEGER,
    num_contacts        INTEGER,
    days_since_last     INTEGER,
    previous_contacts   INTEGER,

    -- Boolean outcomes
    subscribed          BOOLEAN,
    defaulted           BOOLEAN,
    has_housing_loan    BOOLEAN,
    has_personal_loan   BOOLEAN,

    -- Loaded metadata
    loaded_at           TIMESTAMP DEFAULT NOW()
);

-- Create indexes for query performance
CREATE INDEX idx_fct_customer ON fct_campaign_contacts(customer_sk);
CREATE INDEX idx_fct_date ON fct_campaign_contacts(date_key);
CREATE INDEX idx_fct_subscribed ON fct_campaign_contacts(subscribed);
CREATE INDEX idx_fct_campaign ON fct_campaign_contacts(campaign_sk);
```

---

## Populate the Date Dimension

```sql
-- Generate date dimension for 10 years
INSERT INTO dim_date
SELECT
    TO_CHAR(d, 'YYYYMMDD')::INTEGER         AS date_key,
    d                                        AS full_date,
    EXTRACT(DOW FROM d)::INTEGER             AS day_of_week,
    TO_CHAR(d, 'Day')                        AS day_name,
    EXTRACT(DAY FROM d)::INTEGER             AS day_of_month,
    EXTRACT(DOY FROM d)::INTEGER             AS day_of_year,
    EXTRACT(WEEK FROM d)::INTEGER            AS week_of_year,
    EXTRACT(MONTH FROM d)::INTEGER           AS month_number,
    TO_CHAR(d, 'Month')                      AS month_name,
    TO_CHAR(d, 'Mon')                        AS month_short,
    EXTRACT(QUARTER FROM d)::INTEGER         AS quarter,
    'Q' || EXTRACT(QUARTER FROM d)::TEXT     AS quarter_name,
    EXTRACT(YEAR FROM d)::INTEGER            AS year,
    EXTRACT(DOW FROM d) IN (0, 6)            AS is_weekend,
    FALSE                                    AS is_holiday,
    EXTRACT(YEAR FROM d)::INTEGER            AS fiscal_year,
    EXTRACT(QUARTER FROM d)::INTEGER         AS fiscal_quarter
FROM GENERATE_SERIES(
    '2015-01-01'::DATE,
    '2030-12-31'::DATE,
    '1 day'::INTERVAL
) AS d;

-- Mark Kenyan public holidays
UPDATE dim_date SET is_holiday = TRUE
WHERE full_date IN (
    '2026-01-01',   -- New Year's Day
    '2026-04-03',   -- Good Friday
    '2026-04-06',   -- Easter Monday
    '2026-05-01',   -- Labour Day
    '2026-06-01',   -- Madaraka Day
    '2026-10-10',   -- Moi Day
    '2026-10-20',   -- Mashujaa Day
    '2026-12-12',   -- Jamhuri Day
    '2026-12-25',   -- Christmas
    '2026-12-26'    -- Boxing Day
);
```

---

## Slowly Changing Dimensions (SCD)

```sql
-- SCD Type 1 — Overwrite (no history)
UPDATE dim_customers
SET tier = 'Platinum', city = 'Nairobi'
WHERE customer_id = 1 AND is_current = TRUE;

-- SCD Type 2 — Keep history (most common)
-- Step 1: Expire old record
UPDATE dim_customers
SET valid_to = CURRENT_DATE - 1,
    is_current = FALSE
WHERE customer_id = 1
  AND is_current = TRUE;

-- Step 2: Insert new current record
INSERT INTO dim_customers
    (customer_id, customer_name, tier, city, valid_from, is_current)
VALUES
    (1, 'Beatrice Wakarima', 'Platinum', 'Nairobi', CURRENT_DATE, TRUE);

-- Query: current state
SELECT * FROM dim_customers WHERE is_current = TRUE;

-- Query: state at a point in time
SELECT * FROM dim_customers
WHERE customer_id = 1
  AND valid_from <= '2025-06-01'
  AND (valid_to IS NULL OR valid_to >= '2025-06-01');
```

---

## Analytical Queries on Star Schema

```sql
-- Monthly subscription rate by job type
SELECT
    dd.month_name,
    dd.year,
    dc.job,
    dc.balance_segment,
    COUNT(*)                                        AS total_contacts,
    SUM(CASE WHEN f.subscribed THEN 1 ELSE 0 END)  AS subscriptions,
    ROUND(
        100.0 * SUM(CASE WHEN f.subscribed THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0),
        2
    )                                               AS conversion_rate
FROM fct_campaign_contacts f
JOIN dim_customers dc ON f.customer_sk = dc.customer_sk
JOIN dim_date dd ON f.date_key = dd.date_key
JOIN dim_campaigns dcamp ON f.campaign_sk = dcamp.campaign_sk
WHERE dc.is_current = TRUE
GROUP BY 1, 2, 3, 4
ORDER BY dd.year, dd.month_number, conversion_rate DESC;

-- Customer value segmentation over time
SELECT
    dd.quarter_name,
    dd.year,
    dc.tier,
    dc.age_segment,
    COUNT(DISTINCT f.customer_sk)                   AS unique_customers,
    SUM(f.call_duration_secs) / 3600.0             AS total_hours,
    AVG(f.call_duration_secs)                       AS avg_call_secs,
    SUM(CASE WHEN f.subscribed THEN 1 ELSE 0 END)  AS total_subscriptions
FROM fct_campaign_contacts f
JOIN dim_customers dc ON f.customer_sk = dc.customer_sk
JOIN dim_date dd ON f.date_key = dd.date_key
GROUP BY 1, 2, 3, 4
ORDER BY dd.year, dd.quarter_name;
```

---

## Data Warehouse Best Practices

```sql
-- ✅ Always use surrogate keys (not natural keys) as foreign keys
-- Natural keys can change; surrogate keys never do
customer_sk BIGSERIAL PRIMARY KEY      -- Good
customer_id INTEGER PRIMARY KEY        -- Risky (can change)

-- ✅ Consistent naming conventions
-- Dimensions:   dim_customers, dim_date, dim_products
-- Facts:        fct_orders, fct_transactions, fct_campaign_contacts
-- Staging:      stg_bank_marketing, stg_customers
-- Measures end in _amount, _count, _duration, _rate
-- Flags end in is_, has_

-- ✅ Document grain in fact table comment
COMMENT ON TABLE fct_campaign_contacts IS
    'Grain: one row per customer phone contact in the campaign. '
    'One customer may appear multiple times across campaigns.';

-- ✅ Create covering indexes for common query patterns
CREATE INDEX idx_fct_customer_date
    ON fct_campaign_contacts(customer_sk, date_key);

-- ✅ Partition large fact tables by date
CREATE TABLE fct_transactions_2026
    PARTITION OF fct_transactions
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
```

---

## Schema Organisation

```sql
-- Recommended schema structure
CREATE SCHEMA bronze;    -- Raw data (as loaded)
CREATE SCHEMA silver;    -- Cleaned, typed, validated
CREATE SCHEMA gold;      -- Business aggregations
CREATE SCHEMA marts;     -- Star schema (dims + facts)
CREATE SCHEMA staging;   -- Temporary load staging
CREATE SCHEMA reference; -- Static lookup tables (seeds)
CREATE SCHEMA snapshots; -- SCD Type 2 history

-- Grant access levels
GRANT USAGE ON SCHEMA gold TO bi_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA gold TO bi_reader;

GRANT USAGE ON SCHEMA silver TO dbt_user;
GRANT ALL ON ALL TABLES IN SCHEMA silver TO dbt_user;
```

---

## Quick Reference

```
Fact table:
  - Numeric measurements (amounts, counts, durations)
  - Foreign keys to all related dimensions
  - Grain documented in comments
  - Indexed on all foreign keys

Dimension table:
  - Descriptive attributes (names, categories, flags)
  - Surrogate key (BIGSERIAL) as primary key
  - Natural key for reference
  - SCD Type 2 fields if history needed

Naming:
  dim_*     → dimensions
  fct_*     → fact tables
  stg_*     → staging
  int_*     → intermediate
  *_sk      → surrogate key
  *_id      → natural/business key
  is_*      → boolean flag
  has_*     → boolean flag
  *_amount  → money
  *_count   → integers
  *_date    → dates
```

---

## Previous | Next
← [[04 - Pipeline Orchestration with Airflow]] | → [[06 - Data Quality and Validation]]
