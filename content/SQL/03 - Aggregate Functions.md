---
title: Aggregate Functions
tags: [sql, basics]
created: 2026-05-20
up:: [[SQL MOC]]
---

# 📊 Aggregate Functions

> Aggregate functions summarize many rows into a single value. They are the foundation of every dashboard, KPI, and report you will ever build.

---

## The Core Aggregate Functions

```sql
SELECT
    COUNT(*)            AS total_rows,
    COUNT(email)        AS rows_with_email,    -- Ignores NULLs
    SUM(balance)        AS total_balance,
    AVG(balance)        AS average_balance,
    MIN(balance)        AS lowest_balance,
    MAX(balance)        AS highest_balance,
    ROUND(AVG(balance), 2) AS avg_rounded
FROM customers;
```

---

## COUNT Variations

```sql
-- Count all rows
SELECT COUNT(*) FROM customers;

-- Count non-null values in a column
SELECT COUNT(email) FROM customers;

-- Count distinct values
SELECT COUNT(DISTINCT city) FROM customers;
SELECT COUNT(DISTINCT tier) FROM customers;

-- Count with condition
SELECT COUNT(*) FROM customers WHERE tier = 'Gold';
SELECT COUNT(*) FROM customers WHERE balance > 50000;
```

---

## GROUP BY — Aggregating by Category

```sql
-- Total customers per tier
SELECT tier, COUNT(*) AS total_customers
FROM customers
GROUP BY tier;

-- Average balance per city
SELECT 
    city,
    COUNT(*)            AS customers,
    ROUND(AVG(balance), 0)  AS avg_balance,
    SUM(balance)        AS total_deposits,
    MAX(balance)        AS highest_balance
FROM customers
GROUP BY city
ORDER BY total_deposits DESC;

-- Multiple columns
SELECT 
    city,
    tier,
    COUNT(*) AS count
FROM customers
GROUP BY city, tier
ORDER BY city, tier;
```

---

## HAVING — Filter After Grouping

```sql
-- WHERE filters ROWS (before grouping)
-- HAVING filters GROUPS (after grouping)

-- Cities with more than 100 customers
SELECT city, COUNT(*) AS total
FROM customers
GROUP BY city
HAVING COUNT(*) > 100;

-- Tiers with average balance over 50000
SELECT 
    tier,
    ROUND(AVG(balance), 0) AS avg_balance
FROM customers
GROUP BY tier
HAVING AVG(balance) > 50000
ORDER BY avg_balance DESC;

-- Using WHERE and HAVING together
SELECT 
    tier,
    COUNT(*) AS active_customers,
    SUM(balance) AS total_balance
FROM customers
WHERE is_active = TRUE          -- Filter rows first
GROUP BY tier
HAVING COUNT(*) >= 10           -- Then filter groups
ORDER BY total_balance DESC;
```

---

## Aggregate with CASE WHEN

```sql
-- Conditional aggregation — very powerful!
SELECT
    city,
    COUNT(*)                                                AS total,
    SUM(CASE WHEN tier = 'Gold'     THEN 1 ELSE 0 END)     AS gold,
    SUM(CASE WHEN tier = 'Platinum' THEN 1 ELSE 0 END)     AS platinum,
    SUM(CASE WHEN balance > 100000  THEN 1 ELSE 0 END)     AS high_value,
    SUM(CASE WHEN is_active = TRUE  THEN 1 ELSE 0 END)     AS active,
    ROUND(
        100.0 * SUM(CASE WHEN is_active = TRUE THEN 1 ELSE 0 END) / COUNT(*),
        1
    )                                                       AS active_pct
FROM customers
GROUP BY city
ORDER BY total DESC;
```

---

## Statistical Functions

```sql
SELECT
    AVG(balance)                        AS mean,
    PERCENTILE_CONT(0.5) WITHIN GROUP 
        (ORDER BY balance)              AS median,
    PERCENTILE_CONT(0.25) WITHIN GROUP 
        (ORDER BY balance)              AS q1,
    PERCENTILE_CONT(0.75) WITHIN GROUP 
        (ORDER BY balance)              AS q3,
    STDDEV(balance)                     AS std_deviation,
    VARIANCE(balance)                   AS variance,
    MIN(balance)                        AS minimum,
    MAX(balance)                        AS maximum,
    MAX(balance) - MIN(balance)         AS range
FROM customers
WHERE is_active = TRUE;
```

---

## Real World Example — Bank KPI Dashboard

```sql
-- Executive KPI summary
SELECT
    -- Volume
    COUNT(*)                            AS total_customers,
    SUM(CASE WHEN is_active THEN 1 ELSE 0 END) AS active_customers,

    -- Balance KPIs
    SUM(balance)                        AS total_deposits,
    ROUND(AVG(balance), 0)              AS avg_balance,
    MAX(balance)                        AS highest_balance,

    -- Tier breakdown
    SUM(CASE WHEN tier = 'Platinum' THEN 1 ELSE 0 END) AS platinum_count,
    SUM(CASE WHEN tier = 'Gold'     THEN 1 ELSE 0 END) AS gold_count,
    SUM(CASE WHEN tier = 'Silver'   THEN 1 ELSE 0 END) AS silver_count,
    SUM(CASE WHEN tier = 'Bronze'   THEN 1 ELSE 0 END) AS bronze_count,

    -- Revenue estimate
    ROUND(SUM(balance) * 0.08, 0)      AS estimated_interest_revenue

FROM customers;
```

---

## Monthly Transaction Analysis

```sql
SELECT
    DATE_TRUNC('month', created_at)     AS month,
    COUNT(*)                            AS total_transactions,
    SUM(amount)                         AS total_volume,
    ROUND(AVG(amount), 0)               AS avg_transaction,
    MAX(amount)                         AS largest_transaction,
    COUNT(DISTINCT customer_id)         AS unique_customers,
    SUM(CASE WHEN type = 'deposit'   THEN amount ELSE 0 END) AS deposits,
    SUM(CASE WHEN type = 'withdrawal' THEN amount ELSE 0 END) AS withdrawals
FROM transactions
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month;
```

---

## Practice Exercises

```sql
-- 1. How many customers are in each city?
SELECT city, COUNT(*) AS total
FROM customers
GROUP BY city
ORDER BY total DESC;

-- 2. What is the average balance per tier?
SELECT tier, ROUND(AVG(balance), 2) AS avg_balance
FROM customers
GROUP BY tier
ORDER BY avg_balance DESC;

-- 3. Which cities have more than 50 customers?
SELECT city, COUNT(*) AS total
FROM customers
GROUP BY city
HAVING COUNT(*) > 50
ORDER BY total DESC;

-- 4. Monthly transaction totals for 2026
SELECT
    EXTRACT(MONTH FROM created_at) AS month,
    COUNT(*) AS transactions,
    SUM(amount) AS total_amount
FROM transactions
WHERE EXTRACT(YEAR FROM created_at) = 2026
GROUP BY EXTRACT(MONTH FROM created_at)
ORDER BY month;

-- 5. Tier distribution with percentages
SELECT
    tier,
    COUNT(*) AS count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) AS percentage
FROM customers
GROUP BY tier
ORDER BY count DESC;
```

---

## Previous | Next
← [[02 - SELECT Statements]] | → [[04 - JOINs]]
