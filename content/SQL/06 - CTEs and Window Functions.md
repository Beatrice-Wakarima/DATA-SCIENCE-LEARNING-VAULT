---
title: CTEs and Window Functions
tags: [sql, advanced]
created: 2026-05-20
up:: [[SQL MOC]]
---

# 🪟 CTEs & Window Functions

> CTEs make complex queries readable. Window functions calculate across rows without collapsing them. Together they are the most powerful SQL tools for analytics.

---

## CTEs — Common Table Expressions

```sql
-- WITH clause creates a named temporary result
WITH cte_name AS (
    SELECT ...      -- Your subquery here
)
SELECT * FROM cte_name;
```

---

## Basic CTE

```sql
-- Without CTE (hard to read)
SELECT * FROM (
    SELECT city, AVG(balance) AS avg_balance
    FROM customers GROUP BY city
) AS city_stats
WHERE avg_balance > 50000;

-- With CTE (clean and readable!)
WITH city_stats AS (
    SELECT city, AVG(balance) AS avg_balance
    FROM customers
    GROUP BY city
)
SELECT city, ROUND(avg_balance, 0) AS avg_balance
FROM city_stats
WHERE avg_balance > 50000
ORDER BY avg_balance DESC;
```

---

## Multiple CTEs

```sql
-- Chain multiple CTEs with commas
WITH

-- Step 1: Active customers
active_customers AS (
    SELECT id, name, city, tier, balance
    FROM customers
    WHERE is_active = TRUE
),

-- Step 2: Their transaction summary
transaction_summary AS (
    SELECT
        customer_id,
        COUNT(*)        AS txn_count,
        SUM(amount)     AS total_spent,
        MAX(created_at) AS last_txn_date
    FROM transactions
    GROUP BY customer_id
),

-- Step 3: Combined profile
customer_profile AS (
    SELECT
        ac.*,
        COALESCE(ts.txn_count, 0)   AS transactions,
        COALESCE(ts.total_spent, 0) AS lifetime_value,
        ts.last_txn_date
    FROM active_customers ac
    LEFT JOIN transaction_summary ts ON ac.id = ts.customer_id
)

-- Final query on the CTE
SELECT *
FROM customer_profile
WHERE lifetime_value > 100000
ORDER BY lifetime_value DESC;
```

---

## Recursive CTE — Hierarchical Data

```sql
-- Org chart: find all reports under a manager
WITH RECURSIVE org_chart AS (
    -- Base case: top-level manager
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: add direct reports
    SELECT e.id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT level, name FROM org_chart ORDER BY level, name;
```

---

## Window Functions — The Concept

```sql
-- Aggregate: collapses rows → ONE result
SELECT AVG(balance) FROM customers;     -- Returns 1 row

-- Window: calculates across rows → KEEPS all rows
SELECT name, balance, AVG(balance) OVER() AS overall_avg
FROM customers;                         -- Returns all rows + avg column
```

The `OVER()` clause defines the "window" — what rows to look at.

---

## OVER() — Basic Window

```sql
-- Add overall stats to every row
SELECT
    name,
    city,
    balance,
    AVG(balance)    OVER()  AS overall_avg,
    SUM(balance)    OVER()  AS total_deposits,
    MAX(balance)    OVER()  AS highest_balance,
    COUNT(*)        OVER()  AS total_customers,
    ROUND(
        100.0 * balance / SUM(balance) OVER(), 2
    )                       AS pct_of_total
FROM customers
ORDER BY balance DESC;
```

---

## PARTITION BY — Window per Group

```sql
-- Calculate within each tier (like GROUP BY but keeps all rows)
SELECT
    name,
    tier,
    balance,
    AVG(balance)    OVER (PARTITION BY tier) AS tier_avg,
    MAX(balance)    OVER (PARTITION BY tier) AS tier_max,
    COUNT(*)        OVER (PARTITION BY tier) AS tier_count,
    balance - AVG(balance) OVER (PARTITION BY tier) AS diff_from_tier_avg
FROM customers
ORDER BY tier, balance DESC;
```

---

## ORDER BY in Window — Running Totals

```sql
-- Running total (cumulative sum)
SELECT
    created_at::DATE    AS date,
    amount,
    SUM(amount) OVER (ORDER BY created_at)  AS running_total,
    AVG(amount) OVER (ORDER BY created_at)  AS running_avg,
    COUNT(*)    OVER (ORDER BY created_at)  AS running_count
FROM transactions
ORDER BY created_at;

-- Running total per customer
SELECT
    customer_id,
    created_at,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id
        ORDER BY created_at
    ) AS customer_running_total
FROM transactions;
```

---

## ROW_NUMBER, RANK, DENSE_RANK

```sql
SELECT
    name,
    city,
    balance,

    -- Unique number for each row
    ROW_NUMBER()    OVER (ORDER BY balance DESC)             AS row_num,

    -- Ties get same rank, next rank skips (1,2,2,4)
    RANK()          OVER (ORDER BY balance DESC)             AS rank,

    -- Ties get same rank, no gaps (1,2,2,3)
    DENSE_RANK()    OVER (ORDER BY balance DESC)             AS dense_rank,

    -- Rank within each city
    ROW_NUMBER()    OVER (PARTITION BY city ORDER BY balance DESC) AS city_rank

FROM customers;

-- Get top customer per city
WITH ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY city ORDER BY balance DESC) AS rn
    FROM customers
)
SELECT name, city, balance, tier
FROM ranked
WHERE rn = 1
ORDER BY city;
```

---

## LAG & LEAD — Previous and Next Rows

```sql
-- Month-over-month comparison
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', created_at) AS month,
        SUM(amount) AS revenue
    FROM transactions
    GROUP BY 1
)
SELECT
    month,
    revenue,
    LAG(revenue)  OVER (ORDER BY month)     AS prev_month_revenue,
    LEAD(revenue) OVER (ORDER BY month)     AS next_month_revenue,
    revenue - LAG(revenue) OVER (ORDER BY month) AS mom_change,
    ROUND(
        100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
        / LAG(revenue) OVER (ORDER BY month),
        1
    ) AS mom_growth_pct
FROM monthly_sales
ORDER BY month;
```

---

## NTILE — Percentile Buckets

```sql
-- Divide customers into quartiles
SELECT
    name,
    balance,
    NTILE(4)    OVER (ORDER BY balance) AS quartile,
    NTILE(10)   OVER (ORDER BY balance) AS decile,
    NTILE(100)  OVER (ORDER BY balance) AS percentile
FROM customers;

-- Label the quartiles
WITH quartiles AS (
    SELECT name, balance,
        NTILE(4) OVER (ORDER BY balance) AS q
    FROM customers
)
SELECT name, balance,
    CASE q
        WHEN 1 THEN 'Bottom 25%'
        WHEN 2 THEN 'Lower-Mid 25%'
        WHEN 3 THEN 'Upper-Mid 25%'
        WHEN 4 THEN 'Top 25%'
    END AS segment
FROM quartiles;
```

---

## FIRST_VALUE & LAST_VALUE

```sql
SELECT
    name,
    city,
    balance,
    FIRST_VALUE(name) OVER (
        PARTITION BY city ORDER BY balance DESC
    ) AS top_customer_in_city,
    LAST_VALUE(name) OVER (
        PARTITION BY city
        ORDER BY balance DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS lowest_customer_in_city
FROM customers;
```

---

## Real World Example — Sales Analytics

```sql
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', t.created_at)   AS month,
        c.city,
        SUM(t.amount)                       AS revenue
    FROM transactions t
    JOIN customers c ON t.customer_id = c.id
    GROUP BY 1, 2
),
ranked_months AS (
    SELECT *,
        -- Rank each month within the city
        RANK() OVER (PARTITION BY city ORDER BY revenue DESC) AS revenue_rank,
        -- Running total per city
        SUM(revenue) OVER (PARTITION BY city ORDER BY month) AS city_running_total,
        -- Month over month growth
        LAG(revenue) OVER (PARTITION BY city ORDER BY month) AS prev_revenue,
        -- Contribution to city total
        ROUND(
            100.0 * revenue / SUM(revenue) OVER (PARTITION BY city),
            1
        ) AS pct_of_city_total
    FROM monthly_revenue
)
SELECT
    month,
    city,
    revenue,
    revenue_rank,
    city_running_total,
    ROUND(100.0 * (revenue - prev_revenue) / NULLIF(prev_revenue, 0), 1) AS mom_growth,
    pct_of_city_total
FROM ranked_months
ORDER BY city, month;
```

---

## Window Function Cheatsheet

```sql
-- Syntax
function() OVER (
    PARTITION BY column      -- Group by (optional)
    ORDER BY column          -- Sort within window (optional)
    ROWS BETWEEN ... AND ... -- Frame (optional)
)

-- Ranking
ROW_NUMBER()    -- 1,2,3,4,5 (always unique)
RANK()          -- 1,2,2,4,5 (gaps on ties)
DENSE_RANK()    -- 1,2,2,3,4 (no gaps)
NTILE(n)        -- Bucket into n groups

-- Offset
LAG(col, n)     -- Value n rows BEFORE
LEAD(col, n)    -- Value n rows AFTER
FIRST_VALUE(col)-- First value in window
LAST_VALUE(col) -- Last value in window

-- Aggregates as windows
SUM()   OVER()  -- Running total
AVG()   OVER()  -- Running average
COUNT() OVER()  -- Running count
```

---

## Previous | Next
← [[05 - Subqueries]] | → [[07 - Data Manipulation (INSERT UPDATE DELETE)]]
