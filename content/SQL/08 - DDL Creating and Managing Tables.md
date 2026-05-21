---
title: DDL — Creating and Managing Tables
tags: [sql, ddl, data-engineering]
created: 2026-05-20
up:: [[SQL MOC]]
---

# 🏗️ DDL — Creating & Managing Tables

> DDL (Data Definition Language) defines the structure of your database — creating tables, adding columns, setting constraints. The foundation of any data warehouse or pipeline.

---

## CREATE TABLE

```sql
-- Basic table
CREATE TABLE customers (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(100) UNIQUE,
    city        VARCHAR(50),
    balance     DECIMAL(12, 2) DEFAULT 0.00,
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMP DEFAULT NOW()
);

-- Create only if it doesn't exist
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);
```

---

## Data Types

```sql
-- Numbers
SMALLINT                -- -32,768 to 32,767
INTEGER / INT           -- -2.1B to 2.1B
BIGINT                  -- Very large integers
SERIAL                  -- Auto-incrementing integer (1, 2, 3...)
BIGSERIAL               -- Auto-incrementing bigint
DECIMAL(10, 2)          -- Exact: 10 digits, 2 decimal places
NUMERIC(10, 2)          -- Same as DECIMAL
FLOAT / REAL            -- Approximate decimal
DOUBLE PRECISION        -- More precise float

-- Text
VARCHAR(100)            -- Variable length, max 100 chars
CHAR(10)                -- Fixed length, always 10 chars
TEXT                    -- Unlimited length
CITEXT                  -- Case-insensitive text (PostgreSQL)

-- Date & Time
DATE                    -- 2026-05-20
TIME                    -- 14:30:00
TIMESTAMP               -- 2026-05-20 14:30:00
TIMESTAMPTZ             -- With timezone (recommended!)
INTERVAL                -- Duration: '3 days', '2 hours'

-- Boolean
BOOLEAN                 -- TRUE / FALSE / NULL

-- Other
UUID                    -- Universal unique ID
JSON / JSONB            -- JSON data (JSONB = indexed, faster)
ARRAY                   -- Array of any type
```

---

## Constraints

```sql
CREATE TABLE bank_accounts (

    -- PRIMARY KEY: unique, not null, indexed
    id              SERIAL PRIMARY KEY,

    -- NOT NULL: value required
    account_number  VARCHAR(20) NOT NULL,

    -- UNIQUE: no duplicates allowed
    email           VARCHAR(100) UNIQUE,

    -- DEFAULT: value if none provided
    balance         DECIMAL(12,2) DEFAULT 0.00,
    tier            VARCHAR(20) DEFAULT 'Bronze',
    is_active       BOOLEAN DEFAULT TRUE,

    -- CHECK: must satisfy condition
    age             INTEGER CHECK (age >= 18 AND age <= 100),
    balance_check   DECIMAL CHECK (balance >= 0),

    -- FOREIGN KEY: references another table
    branch_id       INTEGER REFERENCES branches(id),
    
    -- Foreign key with behaviour on delete
    customer_id     INTEGER REFERENCES customers(id)
                    ON DELETE CASCADE       -- Delete account if customer deleted
                    ON UPDATE CASCADE,      -- Update if customer id changes

    -- Named constraints (easier to debug)
    CONSTRAINT chk_tier CHECK (tier IN ('Bronze','Silver','Gold','Platinum')),
    CONSTRAINT uq_account_number UNIQUE (account_number)
);
```

---

## ALTER TABLE — Modifying Structure

```sql
-- Add column
ALTER TABLE customers ADD COLUMN phone VARCHAR(20);
ALTER TABLE customers ADD COLUMN last_login TIMESTAMP;

-- Drop column
ALTER TABLE customers DROP COLUMN phone;
ALTER TABLE customers DROP COLUMN IF EXISTS phone;

-- Rename column
ALTER TABLE customers RENAME COLUMN phone TO mobile_number;

-- Change data type
ALTER TABLE customers ALTER COLUMN balance TYPE BIGINT;

-- Add NOT NULL constraint
ALTER TABLE customers ALTER COLUMN email SET NOT NULL;
ALTER TABLE customers ALTER COLUMN email DROP NOT NULL;

-- Add DEFAULT
ALTER TABLE customers ALTER COLUMN tier SET DEFAULT 'Bronze';
ALTER TABLE customers ALTER COLUMN tier DROP DEFAULT;

-- Add constraint
ALTER TABLE customers ADD CONSTRAINT chk_balance CHECK (balance >= 0);

-- Drop constraint
ALTER TABLE customers DROP CONSTRAINT chk_balance;

-- Rename table
ALTER TABLE customers RENAME TO bank_customers;
```

---

## Indexes — Speed Up Queries

```sql
-- Create index (speeds up WHERE and JOIN on that column)
CREATE INDEX idx_customers_city ON customers(city);
CREATE INDEX idx_transactions_customer ON transactions(customer_id);
CREATE INDEX idx_transactions_date ON transactions(created_at);

-- Unique index
CREATE UNIQUE INDEX idx_customers_email ON customers(email);

-- Composite index (for queries filtering on multiple columns)
CREATE INDEX idx_cust_city_tier ON customers(city, tier);

-- Partial index (only index rows matching condition)
CREATE INDEX idx_active_customers ON customers(id) WHERE is_active = TRUE;

-- Drop index
DROP INDEX idx_customers_city;

-- View all indexes on a table
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'customers';
```

---

## DROP — Removing Objects

```sql
-- Drop table
DROP TABLE customers;
DROP TABLE IF EXISTS customers;

-- Drop with cascade (removes dependent objects too)
DROP TABLE customers CASCADE;

-- Drop database
DROP DATABASE my_database;
DROP DATABASE IF EXISTS my_database;

-- Truncate (empty table, keep structure)
TRUNCATE TABLE staging_data;
TRUNCATE TABLE staging_data RESTART IDENTITY;   -- Reset auto-increment
```

---

## Views — Saved Queries

```sql
-- Create a view (saved query — not a table)
CREATE VIEW premium_customers AS
SELECT id, name, city, balance, tier
FROM customers
WHERE tier IN ('Gold', 'Platinum')
  AND is_active = TRUE;

-- Use like a table
SELECT * FROM premium_customers ORDER BY balance DESC;

-- Update a view
CREATE OR REPLACE VIEW premium_customers AS
SELECT id, name, city, balance, tier, email
FROM customers
WHERE tier IN ('Gold', 'Platinum');

-- Drop view
DROP VIEW premium_customers;
DROP VIEW IF EXISTS premium_customers;

-- Materialized view (stores results physically — faster but needs refresh)
CREATE MATERIALIZED VIEW monthly_revenue AS
SELECT
    DATE_TRUNC('month', created_at) AS month,
    SUM(amount) AS revenue
FROM transactions
GROUP BY 1;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW monthly_revenue;
```

---

## Real World — Data Warehouse Schema

```sql
-- Medallion Architecture in SQL
-- Bronze → Silver → Gold

-- BRONZE: Raw data as-is
CREATE TABLE bronze.stg_bank_marketing (
    age             INTEGER,
    job             VARCHAR(50),
    marital         VARCHAR(20),
    education       VARCHAR(50),
    balance         DECIMAL(12,2),
    campaign        INTEGER,
    y               VARCHAR(5),
    loaded_at       TIMESTAMP DEFAULT NOW()
);

-- SILVER: Cleaned and validated
CREATE TABLE silver.bank_customers (
    customer_sk     BIGSERIAL PRIMARY KEY,
    age             SMALLINT CHECK (age BETWEEN 18 AND 100),
    job             VARCHAR(50),
    marital         VARCHAR(20) CHECK (marital IN ('single','married','divorced')),
    education       VARCHAR(50),
    balance_segment VARCHAR(20),
    balance         DECIMAL(12,2) CHECK (balance >= 0),
    processed_at    TIMESTAMP DEFAULT NOW()
);

-- GOLD: Business-ready aggregations
CREATE TABLE gold.campaign_performance (
    report_date     DATE,
    job_type        VARCHAR(50),
    total_contacts  INTEGER,
    subscriptions   INTEGER,
    conversion_rate DECIMAL(5,2),
    avg_balance     DECIMAL(12,2),
    refreshed_at    TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_silver_job ON silver.bank_customers(job);
CREATE INDEX idx_gold_date ON gold.campaign_performance(report_date);
```

---

## Schemas — Organising Tables

```sql
-- Create schema (namespace for tables)
CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;
CREATE SCHEMA staging;

-- Create table in schema
CREATE TABLE bronze.raw_transactions (...);
CREATE TABLE silver.clean_transactions (...);

-- Query across schemas
SELECT b.*, s.cleaned_amount
FROM bronze.raw_transactions b
JOIN silver.clean_transactions s ON b.id = s.source_id;

-- Set default schema
SET search_path TO silver, public;
```

---

## Quick Reference

```sql
-- Create
CREATE TABLE name (col type constraints, ...);
CREATE TABLE IF NOT EXISTS name (...);
CREATE INDEX idx ON table(column);
CREATE VIEW name AS SELECT ...;

-- Modify
ALTER TABLE name ADD COLUMN col type;
ALTER TABLE name DROP COLUMN col;
ALTER TABLE name RENAME COLUMN old TO new;
ALTER TABLE name ALTER COLUMN col TYPE new_type;
ALTER TABLE name ADD CONSTRAINT name CHECK (...);

-- Remove
DROP TABLE name;
DROP TABLE IF EXISTS name CASCADE;
DROP INDEX name;
DROP VIEW name;
TRUNCATE TABLE name;
```

---

## Previous | Next
← [[07 - Data Manipulation (INSERT UPDATE DELETE)]] | → [[09 - String and Date Functions]]
