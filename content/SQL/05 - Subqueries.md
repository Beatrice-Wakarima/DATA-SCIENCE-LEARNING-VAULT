---
title: Subqueries
tags: [sql, intermediate]
created: 2026-05-20
up:: [[SQL MOC]]
---

# 🪆 Subqueries

> A subquery is a query inside another query. They let you break complex problems into smaller steps — like variables in Python.

---

## What is a Subquery?

```sql
-- Outer query uses result of inner query
SELECT name, balance
FROM customers
WHERE balance > (SELECT AVG(balance) FROM customers);
--               └─────── subquery ──────────────┘
```

---

## Subquery in WHERE

```sql
-- Customers with above-average balance
SELECT name, balance
FROM customers
WHERE balance > (SELECT AVG(balance) FROM customers)
ORDER BY balance DESC;

-- Customers who made a transaction last month
SELECT name, tier
FROM customers
WHERE id IN (
    SELECT DISTINCT customer_id
    FROM transactions
    WHERE created_at >= DATE_TRUNC('month', NOW() - INTERVAL '1 month')
    AND   created_at <  DATE_TRUNC('month', NOW())
);

-- Customers who have NEVER transacted
SELECT name, joined_date
FROM customers
WHERE id NOT IN (
    SELECT DISTINCT customer_id
    FROM transactions
    WHERE customer_id IS NOT NULL
);
```

---

## Subquery in FROM (Derived Table)

```sql
-- Average of averages (can't directly AVG(AVG()))
SELECT AVG(city_avg) AS grand_average
FROM (
    SELECT city, AVG(balance) AS city_avg
    FROM customers
    GROUP BY city
) AS city_averages;

-- Top earners per department
SELECT dept_stats.*
FROM (
    SELECT
        department,
        AVG(salary)     AS avg_salary,
        MAX(salary)     AS max_salary,
        COUNT(*)        AS headcount
    FROM employees
    GROUP BY department
) AS dept_stats
WHERE dept_stats.avg_salary > 100000;
```

---

## Subquery in SELECT (Scalar Subquery)

```sql
-- Add a comparison column to each row
SELECT
    name,
    balance,
    (SELECT AVG(balance) FROM customers)        AS overall_avg,
    balance - (SELECT AVG(balance) FROM customers) AS diff_from_avg,
    ROUND(
        100.0 * balance / (SELECT SUM(balance) FROM customers),
        2
    )                                           AS pct_of_total
FROM customers
ORDER BY balance DESC;
```

---

## Correlated Subquery — References Outer Query

```sql
-- For each customer, get their latest transaction
SELECT
    c.name,
    c.tier,
    (
        SELECT MAX(t.created_at)
        FROM transactions t
        WHERE t.customer_id = c.id     -- References outer query!
    ) AS last_transaction_date
FROM customers c;

-- Customers whose balance is above their city's average
SELECT name, city, balance
FROM customers c
WHERE balance > (
    SELECT AVG(balance)
    FROM customers
    WHERE city = c.city         -- Same city as outer row
)
ORDER BY city, balance DESC;
```

---

## EXISTS — Check if Subquery Returns Rows

```sql
-- Customers who have at least one transaction
SELECT name, tier
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM transactions t
    WHERE t.customer_id = c.id
);

-- Customers with NO transactions (more efficient than NOT IN)
SELECT name, tier
FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM transactions t
    WHERE t.customer_id = c.id
);

-- EXISTS vs IN:
-- EXISTS stops at first match → faster for large tables
-- IN collects all values → better for small subqueries
```

---

## Real World Example — Campaign Analysis

```sql
-- Bank marketing: subscribers vs non-subscribers
SELECT
    sub.job,
    sub.education,
    sub.total_contacted,
    sub.subscribed,
    ROUND(100.0 * sub.subscribed / sub.total_contacted, 2) AS conversion_rate
FROM (
    -- Subquery summarizes by job and education
    SELECT
        job,
        education,
        COUNT(*)                                        AS total_contacted,
        SUM(CASE WHEN y = 'yes' THEN 1 ELSE 0 END)     AS subscribed
    FROM bank_marketing
    GROUP BY job, education
) AS sub
WHERE sub.total_contacted >= 20         -- Only meaningful sample sizes
ORDER BY conversion_rate DESC
LIMIT 15;
```

---

## Nested Subqueries

```sql
-- Customers in the top 10% by balance
SELECT name, balance
FROM customers
WHERE balance >= (
    SELECT PERCENTILE_CONT(0.9)
           WITHIN GROUP (ORDER BY balance)
    FROM customers
    WHERE is_active = TRUE      -- Nested filter inside subquery
)
ORDER BY balance DESC;
```

---

## Subquery vs JOIN — When to Use Which

```sql
-- These are often equivalent:

-- Using subquery
SELECT name FROM customers
WHERE id IN (SELECT customer_id FROM transactions WHERE amount > 50000);

-- Using JOIN (usually faster)
SELECT DISTINCT c.name
FROM customers c
JOIN transactions t ON c.id = t.customer_id
WHERE t.amount > 50000;

-- Rule of thumb:
-- JOIN → when you need columns from both tables
-- Subquery → when you need a single value or existence check
-- CTE → when logic is complex and reused (next note!)
```

---

## Practice Exercises

```sql
-- 1. Find customers with balance above the overall average
SELECT name, balance
FROM customers
WHERE balance > (SELECT AVG(balance) FROM customers)
ORDER BY balance DESC;

-- 2. Which job type has the highest subscription rate?
SELECT job, 
    ROUND(100.0 * SUM(CASE WHEN y='yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS rate
FROM bank_marketing
GROUP BY job
ORDER BY rate DESC;

-- 3. Get the most recent transaction for each customer
SELECT customer_id, MAX(created_at) AS last_transaction
FROM transactions
GROUP BY customer_id;

-- 4. Customers who transacted more than the average customer
SELECT name
FROM customers
WHERE id IN (
    SELECT customer_id
    FROM transactions
    GROUP BY customer_id
    HAVING COUNT(*) > (
        SELECT AVG(txn_count)
        FROM (
            SELECT customer_id, COUNT(*) AS txn_count
            FROM transactions
            GROUP BY customer_id
        ) AS counts
    )
);
```

---

## Previous | Next
← [[04 - JOINs]] | → [[06 - CTEs and Window Functions]]
