---
title: Snowflake Transformations and SQL
tags: [snowflake, sql, transformations, data-engineering]
created: 2026-05-20
up:: [[Snowflake MOC]]
---

# 🔄 Snowflake Transformations & SQL

> Snowflake SQL is ANSI-compatible with powerful extensions. This note covers everything from basic queries to advanced transformation patterns used in production data pipelines.

---

## Snowflake SQL Extensions

```sql
-- These features go beyond standard SQL

-- 1. QUALIFY — filter window functions (like HAVING for aggregates)
-- 2. SAMPLE  — random sampling
-- 3. FLATTEN — expand arrays/JSON
-- 4. MATCH_RECOGNIZE — pattern matching
-- 5. PIVOT/UNPIVOT — reshape data
-- 6. GENERATOR — generate rows
-- 7. RESULT_SCAN — query previous results
-- 8. CHANGES — query change tracking
```

---

## QUALIFY — Filter Window Functions

```sql
-- Standard way (subquery needed)
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY job ORDER BY balance DESC) AS rn
    FROM SILVER.BANK_CUSTOMERS
) ranked
WHERE rn = 1;

-- Snowflake QUALIFY (much cleaner!)
SELECT *
FROM SILVER.BANK_CUSTOMERS
QUALIFY ROW_NUMBER() OVER (PARTITION BY job ORDER BY balance DESC) = 1;

-- Get top 3 customers per job by balance
SELECT customer_sk, job, balance, age
FROM SILVER.BANK_CUSTOMERS
QUALIFY RANK() OVER (PARTITION BY job ORDER BY balance DESC) <= 3;

-- Remove duplicates (keep latest record)
SELECT *
FROM BRONZE.RAW_BANK_MARKETING
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY age, job, balance
    ORDER BY _loaded_at DESC
) = 1;
```

---

## SAMPLE — Random Sampling

```sql
-- Sample 10% of rows (row-level sampling)
SELECT * FROM SILVER.BANK_CUSTOMERS SAMPLE (10);

-- Sample exact number of rows
SELECT * FROM SILVER.BANK_CUSTOMERS SAMPLE (1000 ROWS);

-- Block sampling (faster for large tables)
SELECT * FROM SILVER.BANK_CUSTOMERS SAMPLE BLOCK (5);

-- Reproducible sample (seed)
SELECT * FROM SILVER.BANK_CUSTOMERS SAMPLE (10) SEED (42);

-- Use for model training/testing split
-- Training set (80%)
CREATE TABLE ML.TRAIN_DATA AS
SELECT * FROM SILVER.BANK_CUSTOMERS SAMPLE (80) SEED (42);

-- Test set (remaining 20%)
CREATE TABLE ML.TEST_DATA AS
SELECT * FROM SILVER.BANK_CUSTOMERS
WHERE customer_sk NOT IN (SELECT customer_sk FROM ML.TRAIN_DATA)
SAMPLE (100);
```

---

## FLATTEN — Expand Arrays and JSON

```sql
-- Sample VARIANT data
CREATE TABLE API_RESPONSES AS
SELECT PARSE_JSON('{
    "campaign_id": 1,
    "contacts": [
        {"name": "Beatrice", "age": 28, "subscribed": true},
        {"name": "John", "age": 35, "subscribed": false},
        {"name": "Alice", "age": 42, "subscribed": true}
    ]
}') AS data;

-- Flatten nested array
SELECT
    data:campaign_id::NUMBER            AS campaign_id,
    f.value:name::STRING                AS customer_name,
    f.value:age::NUMBER                 AS age,
    f.value:subscribed::BOOLEAN         AS subscribed
FROM API_RESPONSES,
LATERAL FLATTEN(INPUT => data:contacts) f;

-- Result:
-- 1 | Beatrice | 28 | TRUE
-- 1 | John     | 35 | FALSE
-- 1 | Alice    | 42 | TRUE

-- Flatten with path
SELECT
    f.key        AS field_name,
    f.value      AS field_value,
    f.index      AS array_position
FROM API_RESPONSES,
LATERAL FLATTEN(INPUT => data, RECURSIVE => TRUE) f;
```

---

## PIVOT and UNPIVOT

```sql
-- UNPIVOT: Convert columns to rows
-- Before: Wide format
-- job     | q1_subscriptions | q2_subscriptions | q3_subscriptions
-- admin   | 120              | 135              | 148

-- After UNPIVOT: Long format
-- job   | quarter | subscriptions

SELECT job, quarter, subscriptions
FROM quarterly_stats
UNPIVOT (
    subscriptions FOR quarter IN (q1_subscriptions, q2_subscriptions, q3_subscriptions)
);

-- PIVOT: Convert rows to columns (opposite)
-- Before: Long format
-- job | month | conversion_rate

-- After PIVOT: Wide format
-- job | jan | feb | mar ...

SELECT *
FROM (
    SELECT job, month, conversion_rate
    FROM SILVER.BANK_CUSTOMERS
    GROUP BY 1, 2
)
PIVOT (
    AVG(conversion_rate) FOR month IN ('jan', 'feb', 'mar', 'apr', 'may', 'jun')
) AS p (job, jan, feb, mar, apr, may, jun);
```

---

## GENERATOR — Create Rows

```sql
-- Generate a sequence of numbers
SELECT SEQ4() AS n
FROM TABLE(GENERATOR(ROWCOUNT => 100));

-- Generate date spine
SELECT
    DATEADD(DAY, SEQ4(), '2026-01-01'::DATE) AS date_day
FROM TABLE(GENERATOR(ROWCOUNT => 365));

-- Build a complete date dimension table
CREATE TABLE REFERENCE.DIM_DATE AS
SELECT
    TO_NUMBER(TO_CHAR(d.date_day, 'YYYYMMDD'))  AS date_key,
    d.date_day                                   AS full_date,
    YEAR(d.date_day)                             AS year,
    QUARTER(d.date_day)                          AS quarter,
    MONTH(d.date_day)                            AS month_number,
    MONTHNAME(d.date_day)                        AS month_name,
    DAY(d.date_day)                              AS day_of_month,
    DAYOFWEEK(d.date_day)                        AS day_of_week,
    DAYNAME(d.date_day)                          AS day_name,
    WEEKOFYEAR(d.date_day)                       AS week_of_year,
    DAYOFYEAR(d.date_day)                        AS day_of_year,
    CASE WHEN DAYOFWEEK(d.date_day) IN (0,6) THEN TRUE ELSE FALSE END AS is_weekend,
    'Q' || QUARTER(d.date_day)                   AS quarter_name,
    TO_CHAR(d.date_day, 'YYYY-MM')               AS year_month,
    TO_CHAR(d.date_day, 'MON YYYY')              AS month_year
FROM (
    SELECT DATEADD(DAY, SEQ4(), '2015-01-01'::DATE) AS date_day
    FROM TABLE(GENERATOR(ROWCOUNT => 6000))     -- ~16 years
    WHERE date_day <= '2030-12-31'
) d;
```

---

## Medallion Architecture in Snowflake SQL

```sql
-- ── BRONZE → SILVER ────────────────────────────────────

-- Stored Procedure for Bronze → Silver transformation
CREATE OR REPLACE PROCEDURE DATA_VAULT.SILVER.TRANSFORM_BANK_MARKETING(
    run_date DATE
)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN

    -- Step 1: Delete existing records for this run date (idempotent)
    DELETE FROM DATA_VAULT.SILVER.BANK_CUSTOMERS
    WHERE _run_date = :run_date;

    -- Step 2: Transform and insert
    INSERT INTO DATA_VAULT.SILVER.BANK_CUSTOMERS (
        age, job, marital, education,
        balance, balance_segment, age_segment,
        has_housing_loan, has_personal_loan,
        contact_method, campaign_contacts,
        call_duration_secs, subscribed,
        _run_date, _processed_at
    )
    SELECT
        TRY_CAST(age AS NUMBER(3))                      AS age,
        TRIM(LOWER(job))                                AS job,
        TRIM(LOWER(marital))                            AS marital,
        TRIM(LOWER(education))                          AS education,
        TRY_CAST(balance AS DECIMAL(12,2))              AS balance,

        CASE
            WHEN TRY_CAST(balance AS NUMBER) > 10000   THEN 'high'
            WHEN TRY_CAST(balance AS NUMBER) > 1000    THEN 'medium'
            WHEN TRY_CAST(balance AS NUMBER) >= 0      THEN 'low'
            ELSE 'negative'
        END                                             AS balance_segment,

        CASE
            WHEN TRY_CAST(age AS NUMBER) < 30           THEN 'young'
            WHEN TRY_CAST(age AS NUMBER) < 50           THEN 'middle'
            ELSE 'senior'
        END                                             AS age_segment,

        CASE WHEN LOWER(TRIM(housing)) = 'yes' THEN TRUE ELSE FALSE END
                                                        AS has_housing_loan,
        CASE WHEN LOWER(TRIM(loan)) = 'yes' THEN TRUE ELSE FALSE END
                                                        AS has_personal_loan,

        TRIM(LOWER(contact))                            AS contact_method,
        TRY_CAST(campaign AS NUMBER(3))                 AS campaign_contacts,
        TRY_CAST(duration AS NUMBER)                    AS call_duration_secs,

        CASE WHEN LOWER(TRIM(y)) = 'yes' THEN TRUE ELSE FALSE END
                                                        AS subscribed,

        :run_date                                       AS _run_date,
        CURRENT_TIMESTAMP()                             AS _processed_at

    FROM DATA_VAULT.BRONZE.RAW_BANK_MARKETING
    WHERE _run_date = :run_date
      AND TRY_CAST(age AS NUMBER) BETWEEN 18 AND 95
      AND balance IS NOT NULL;

    RETURN 'Transformed ' || SQLROWCOUNT || ' rows for ' || run_date;

END;
$$;

-- Call the procedure
CALL DATA_VAULT.SILVER.TRANSFORM_BANK_MARKETING(CURRENT_DATE());
```

---

## Silver → Gold Aggregations

```sql
-- ── GOLD LAYER ─────────────────────────────────────────

CREATE OR REPLACE TABLE DATA_VAULT.GOLD.CAMPAIGN_PERFORMANCE AS
SELECT
    CURRENT_DATE()                                      AS report_date,
    job,
    education,
    marital,
    balance_segment,
    age_segment,
    contact_method,

    COUNT(*)                                            AS total_contacts,
    SUM(CASE WHEN subscribed THEN 1 ELSE 0 END)        AS subscriptions,
    SUM(CASE WHEN NOT subscribed THEN 1 ELSE 0 END)    AS non_subscriptions,

    ROUND(
        100.0 * SUM(CASE WHEN subscribed THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0),
        2
    )                                                   AS conversion_rate_pct,

    ROUND(AVG(balance), 2)                             AS avg_balance,
    ROUND(MEDIAN(balance), 2)                          AS median_balance,
    ROUND(AVG(call_duration_secs), 0)                  AS avg_call_duration_secs,
    SUM(call_duration_secs) / 3600.0                   AS total_call_hours,

    ROUND(
        AVG(call_duration_secs) / 60.0, 1
    )                                                   AS avg_call_mins,

    -- Efficiency metric
    ROUND(
        SUM(CASE WHEN subscribed THEN 1 ELSE 0 END)
        / NULLIF(SUM(call_duration_secs) / 3600.0, 0),
        2
    )                                                   AS subscriptions_per_hour,

    CURRENT_TIMESTAMP()                                 AS _refreshed_at

FROM DATA_VAULT.SILVER.BANK_CUSTOMERS
GROUP BY 1, 2, 3, 4, 5, 6, 7
ORDER BY conversion_rate_pct DESC;
```

---

## Useful Snowflake Functions

```sql
-- ── STRING ────────────────────────────────────────────
INITCAP('hello world')          -- Hello World
SPLIT_PART('a,b,c', ',', 2)    -- b
REGEXP_REPLACE(str, pattern, replacement)
REGEXP_SUBSTR(str, pattern)
TRY_CAST('abc' AS NUMBER)       -- NULL (safe cast, no error)
IFF(condition, true, false)     -- Snowflake shorthand for IF

-- ── NULL HANDLING ─────────────────────────────────────
NVL(value, default)             -- Replace NULL with default
NVL2(value, not_null, is_null)  -- Different value based on NULL
NULLIF(a, b)                    -- Return NULL if a = b
ZEROIFNULL(value)               -- Replace NULL with 0
BOOLAND_AGG(column)             -- AND across all rows
BOOLOR_AGG(column)              -- OR across all rows

-- ── NUMERIC ───────────────────────────────────────────
ROUND(3.145, 2)                 -- 3.15
TRUNCATE(3.145, 2)              -- 3.14
DIV0(numerator, denominator)    -- Safe division (0 if div by 0)
LOG(base, value)
SQUARE(value)
BITAND(a, b) / BITOR(a, b)

-- ── DATE ──────────────────────────────────────────────
DATE_TRUNC('MONTH', date)
DATE_PART('YEAR', date)
LAST_DAY(date)                  -- Last day of month
ADD_MONTHS(date, n)
CONVERT_TIMEZONE('UTC', 'Africa/Nairobi', timestamp)

-- ── AGGREGATE ─────────────────────────────────────────
LISTAGG(column, ',') WITHIN GROUP (ORDER BY column)  -- String aggregation
ARRAY_AGG(column)               -- Collect into array
OBJECT_AGG(key, value)          -- Collect into JSON object
APPROX_COUNT_DISTINCT(column)   -- Fast approximate distinct count
PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY column)  -- Median
MODE(column)                    -- Most frequent value
KURTOSIS(column)                -- Statistical kurtosis
SKEW(column)                    -- Statistical skew
```

---

## Dynamic SQL with EXECUTE IMMEDIATE

```sql
-- Run dynamically constructed SQL
DECLARE
    v_table VARCHAR DEFAULT 'BANK_CUSTOMERS';
    v_schema VARCHAR DEFAULT 'SILVER';
    v_sql VARCHAR;
BEGIN
    v_sql := 'SELECT COUNT(*) FROM DATA_VAULT.' || v_schema || '.' || v_table;
    EXECUTE IMMEDIATE v_sql;
END;

-- Dynamic table refresh pattern
CREATE OR REPLACE PROCEDURE REFRESH_GOLD_TABLE(table_name VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    v_sql VARCHAR;
    v_count NUMBER;
BEGIN
    v_sql := 'TRUNCATE TABLE DATA_VAULT.GOLD.' || table_name;
    EXECUTE IMMEDIATE v_sql;

    v_sql := 'INSERT INTO DATA_VAULT.GOLD.' || table_name ||
             ' SELECT * FROM DATA_VAULT.SILVER.TRANSFORM_' || table_name;
    EXECUTE IMMEDIATE v_sql;

    v_count := SQLROWCOUNT;
    RETURN 'Refreshed ' || v_count || ' rows in GOLD.' || table_name;
END;
$$;
```

---

## RESULT_SCAN — Query Previous Results

```sql
-- Get the last query's result ID
SELECT LAST_QUERY_ID();

-- Re-query the results without re-running the query
SELECT *
FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));

-- Use with expensive queries
-- Run the heavy query once:
SELECT job, education, ROUND(AVG(balance),2) AS avg_bal
FROM SILVER.BANK_CUSTOMERS
GROUP BY 1, 2;

-- Grab the ID
SET qid = LAST_QUERY_ID();

-- Filter the cached results (free!)
SELECT * FROM TABLE(RESULT_SCAN($qid))
WHERE avg_bal > 5000
ORDER BY avg_bal DESC;
```

---

## Quick Reference

```sql
-- Snowflake-specific SQL
QUALIFY window_fn = value           -- Filter window functions
SAMPLE (n)                          -- n% random sample
SAMPLE (n ROWS)                     -- Exactly n rows
LATERAL FLATTEN(INPUT => col:array) -- Expand JSON arrays
PIVOT (agg FOR col IN (v1, v2))     -- Rows to columns
UNPIVOT (val FOR col IN (c1, c2))   -- Columns to rows
GENERATOR(ROWCOUNT => n)            -- Generate n rows

-- Safe functions
TRY_CAST(value AS type)             -- NULL on failure
TRY_TO_DATE(string, format)         -- NULL on failure
DIV0(num, den)                      -- 0 on division by zero
ZEROIFNULL(value)                   -- 0 if NULL
NVL(value, default)                 -- default if NULL

-- Useful functions
IFF(cond, true_val, false_val)      -- Inline IF
LISTAGG(col, sep)                   -- String concatenation
ARRAY_AGG(col)                      -- Collect to array
APPROX_COUNT_DISTINCT(col)          -- Fast distinct count
CONVERT_TIMEZONE('from', 'to', ts)  -- Timezone conversion
```

---

## Previous | Next
← [[03 - Snowflake Loading Data]] | → [[05 - Snowflake Performance and Cost]]
