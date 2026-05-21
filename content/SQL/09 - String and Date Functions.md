---
title: String and Date Functions
tags: [sql, functions, data-engineering]
created: 2026-05-20
up:: [[SQL MOC]]
---

# 🔤📅 String & Date Functions

> String and date manipulation is essential for data cleaning pipelines. Most raw data arrives messy — these functions fix it inside SQL.

---

## String Functions

### Case Functions
```sql
SELECT
    UPPER('beatrice wakarima'),     -- BEATRICE WAKARIMA
    LOWER('BEATRICE WAKARIMA'),     -- beatrice wakarima
    INITCAP('beatrice wakarima');   -- Beatrice Wakarima
```

### Trimming
```sql
SELECT
    TRIM('  hello  '),              -- 'hello'
    LTRIM('  hello  '),             -- 'hello  '
    RTRIM('  hello  '),             -- '  hello'
    TRIM(BOTH 'x' FROM 'xxhelloxx'); -- 'hello'

-- Clean a whole column
SELECT TRIM(LOWER(name)) AS clean_name FROM customers;
```

### Length & Position
```sql
SELECT
    LENGTH('Beatrice'),             -- 8
    CHAR_LENGTH('Beatrice'),        -- 8 (same)
    POSITION('ice' IN 'Beatrice'),  -- 6
    STRPOS('Beatrice', 'ice');      -- 6 (same)
```

### Substring & Extraction
```sql
SELECT
    SUBSTRING('Beatrice Wakarima', 1, 8),   -- 'Beatrice'
    LEFT('Beatrice', 4),                     -- 'Beat'
    RIGHT('Beatrice', 4),                    -- 'rice'
    SUBSTRING('beatrice@gmail.com' FROM '@(.+)$'); -- 'gmail.com'

-- Extract domain from email
SELECT
    email,
    SPLIT_PART(email, '@', 1) AS username,
    SPLIT_PART(email, '@', 2) AS domain
FROM customers;
```

### Concatenation
```sql
SELECT
    'Hello' || ' ' || 'World',             -- Hello World
    CONCAT('Hello', ' ', 'World'),         -- Hello World
    CONCAT_WS(', ', 'Nairobi', 'Kenya');   -- Nairobi, Kenya (with separator)

-- Build full address
SELECT
    CONCAT_WS(', ', street, city, country) AS full_address
FROM addresses;
```

### Replace & Regex
```sql
SELECT
    REPLACE('Hello World', 'World', 'Beatrice'),    -- Hello Beatrice
    REPLACE('KES 95,000', ',', ''),                  -- KES 95000

-- Remove non-numeric characters
SELECT REGEXP_REPLACE('KES 95,000.50', '[^0-9.]', '', 'g');  -- 95000.50

-- Validate email format
SELECT email,
    email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    AS is_valid_email
FROM customers;
```

### Padding
```sql
SELECT
    LPAD('42', 5, '0'),     -- 00042
    RPAD('KES', 10, '-'),   -- KES-------
    LPAD(id::TEXT, 6, '0')  -- 000001, 000002...
FROM customers;
```

---

## Real World String Cleaning

```sql
-- Clean messy customer data
SELECT
    TRIM(INITCAP(name))                         AS clean_name,
    TRIM(LOWER(email))                          AS clean_email,
    TRIM(INITCAP(city))                         AS clean_city,
    REPLACE(REPLACE(phone, ' ', ''), '-', '')   AS clean_phone,
    REGEXP_REPLACE(salary_str, '[^0-9.]', '', 'g')::DECIMAL AS clean_salary
FROM raw_customers;
```

---

## Date Functions

### Current Date & Time
```sql
SELECT
    NOW(),                  -- 2026-05-20 14:30:00.000+03
    CURRENT_DATE,           -- 2026-05-20
    CURRENT_TIME,           -- 14:30:00.000+03
    CURRENT_TIMESTAMP,      -- Same as NOW()
    LOCALTIMESTAMP;         -- Without timezone
```

### Extracting Parts
```sql
SELECT
    EXTRACT(YEAR    FROM created_at) AS year,
    EXTRACT(MONTH   FROM created_at) AS month,
    EXTRACT(DAY     FROM created_at) AS day,
    EXTRACT(HOUR    FROM created_at) AS hour,
    EXTRACT(DOW     FROM created_at) AS day_of_week,    -- 0=Sun, 6=Sat
    EXTRACT(WEEK    FROM created_at) AS week_number,
    EXTRACT(QUARTER FROM created_at) AS quarter
FROM transactions;

-- Date parts as text
SELECT
    TO_CHAR(created_at, 'YYYY')             AS year,
    TO_CHAR(created_at, 'Month')            AS month_name,
    TO_CHAR(created_at, 'Day')              AS day_name,
    TO_CHAR(created_at, 'YYYY-MM')          AS year_month,
    TO_CHAR(created_at, 'DD/MM/YYYY')       AS formatted_date,
    TO_CHAR(amount, 'KES 999,999,990.00')   AS formatted_amount
FROM transactions;
```

### Date Truncation
```sql
SELECT
    DATE_TRUNC('year',    created_at) AS year_start,     -- 2026-01-01
    DATE_TRUNC('quarter', created_at) AS quarter_start,  -- 2026-04-01
    DATE_TRUNC('month',   created_at) AS month_start,    -- 2026-05-01
    DATE_TRUNC('week',    created_at) AS week_start,     -- 2026-05-18
    DATE_TRUNC('day',     created_at) AS day_start       -- 2026-05-20
FROM transactions;

-- Group by month using DATE_TRUNC
SELECT
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*) AS transactions,
    SUM(amount) AS revenue
FROM transactions
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month;
```

### Date Arithmetic
```sql
SELECT
    -- Add/subtract intervals
    CURRENT_DATE + INTERVAL '7 days'    AS next_week,
    CURRENT_DATE - INTERVAL '1 month'   AS last_month,
    CURRENT_DATE + INTERVAL '1 year'    AS next_year,

    -- Difference between dates
    CURRENT_DATE - joined_date          AS days_as_customer,
    AGE(joined_date)                    AS tenure,
    AGE(NOW(), joined_date)             AS exact_tenure,

    -- Days between two dates
    DATE_PART('day', NOW() - joined_date) AS days

FROM customers;

-- Transactions in last 30 days
SELECT * FROM transactions
WHERE created_at >= NOW() - INTERVAL '30 days';

-- This month's transactions
SELECT * FROM transactions
WHERE created_at >= DATE_TRUNC('month', NOW());

-- Last month's transactions
SELECT * FROM transactions
WHERE created_at >= DATE_TRUNC('month', NOW() - INTERVAL '1 month')
  AND created_at <  DATE_TRUNC('month', NOW());
```

### Date Conversion
```sql
-- String to date
SELECT
    TO_DATE('20/05/2026', 'DD/MM/YYYY'),        -- 2026-05-20
    TO_DATE('May 20, 2026', 'Month DD, YYYY'),   -- 2026-05-20
    '2026-05-20'::DATE,                          -- Cast to date
    CAST('2026-05-20' AS DATE);                  -- Same

-- Handle multiple formats (try each)
SELECT
    COALESCE(
        TO_DATE(date_str, 'YYYY-MM-DD'),
        TO_DATE(date_str, 'DD/MM/YYYY'),
        TO_DATE(date_str, 'MM-DD-YYYY')
    ) AS clean_date
FROM messy_dates;
```

---

## Real World Example — Time Intelligence

```sql
-- Full date dimension calculations
WITH date_calcs AS (
    SELECT
        created_at,
        amount,

        -- Period labels
        TO_CHAR(created_at, 'YYYY')         AS year,
        TO_CHAR(created_at, 'YYYY-Q')       AS year_quarter,
        TO_CHAR(created_at, 'YYYY-MM')      AS year_month,
        TO_CHAR(created_at, 'Month YYYY')   AS month_label,

        -- Period truncations (for grouping)
        DATE_TRUNC('month', created_at)     AS month_start,
        DATE_TRUNC('quarter', created_at)   AS quarter_start,

        -- Day analysis
        TO_CHAR(created_at, 'Day')          AS day_name,
        EXTRACT(DOW FROM created_at)        AS day_num,
        CASE
            WHEN EXTRACT(DOW FROM created_at) IN (0, 6)
            THEN 'Weekend'
            ELSE 'Weekday'
        END                                 AS day_type,

        -- Time buckets
        CASE
            WHEN EXTRACT(HOUR FROM created_at) BETWEEN 6 AND 11  THEN 'Morning'
            WHEN EXTRACT(HOUR FROM created_at) BETWEEN 12 AND 16 THEN 'Afternoon'
            WHEN EXTRACT(HOUR FROM created_at) BETWEEN 17 AND 20 THEN 'Evening'
            ELSE 'Night'
        END                                 AS time_of_day

    FROM transactions
)
SELECT
    year_month,
    day_type,
    time_of_day,
    COUNT(*)        AS transactions,
    SUM(amount)     AS total_amount,
    AVG(amount)     AS avg_amount
FROM date_calcs
GROUP BY year_month, day_type, time_of_day
ORDER BY year_month, day_type;
```

---

## Cheatsheet

```sql
-- Strings
UPPER(s) / LOWER(s) / INITCAP(s)
TRIM(s) / LTRIM(s) / RTRIM(s)
LENGTH(s)
LEFT(s,n) / RIGHT(s,n)
SUBSTRING(s, start, length)
SPLIT_PART(s, delimiter, n)
CONCAT(s1, s2) / CONCAT_WS(sep, s1, s2)
REPLACE(s, from, to)
REGEXP_REPLACE(s, pattern, replacement, flags)
LPAD(s, n, fill) / RPAD(s, n, fill)

-- Dates
NOW() / CURRENT_DATE / CURRENT_TIME
EXTRACT(part FROM date)
DATE_TRUNC('unit', date)
TO_CHAR(date, 'format')
TO_DATE(string, 'format')
AGE(date) / AGE(end, start)
date + INTERVAL '1 day'
date - INTERVAL '1 month'
```

---

## Previous | Next
← [[08 - DDL — Creating and Managing Tables]] | → [[10 - SQL for Data Engineering]]
