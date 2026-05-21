---
title: JOINs
tags: [sql, basics]
created: 2026-05-20
up:: [[SQL MOC]]
---

# 🔗 JOINs

> JOINs combine rows from two or more tables based on a related column. This is the most powerful feature of relational databases — and the most important SQL skill for data engineers.

---

## The JOIN Concept

```
customers table          transactions table
┌────┬──────────┐        ┌────┬─────────────┬────────┐
│ id │ name     │        │ id │ customer_id │ amount │
├────┼──────────┤        ├────┼─────────────┼────────┤
│  1 │ Beatrice │        │  1 │      1      │ 45000  │
│  2 │ John     │        │  2 │      1      │ 10000  │
│  3 │ Alice    │        │  3 │      2      │ 25000  │
└────┴──────────┘        └────┴─────────────┴────────┘
         ↑                              ↑
         └──────── JOIN ON id ──────────┘
```

---

## INNER JOIN — Only Matching Rows

```sql
-- Get customers WITH transactions only
SELECT
    c.name,
    c.tier,
    t.amount,
    t.type,
    t.created_at
FROM customers c
INNER JOIN transactions t ON c.id = t.customer_id;

-- Customers with their transaction totals
SELECT
    c.name,
    c.city,
    COUNT(t.id)         AS total_transactions,
    SUM(t.amount)       AS total_volume,
    AVG(t.amount)       AS avg_transaction
FROM customers c
INNER JOIN transactions t ON c.id = t.customer_id
GROUP BY c.id, c.name, c.city
ORDER BY total_volume DESC;
```

---

## LEFT JOIN — All Left Rows + Matches

```sql
-- ALL customers, even those with no transactions
SELECT
    c.name,
    c.tier,
    COUNT(t.id)         AS transaction_count,
    COALESCE(SUM(t.amount), 0) AS total_volume
FROM customers c
LEFT JOIN transactions t ON c.id = t.customer_id
GROUP BY c.id, c.name, c.tier
ORDER BY total_volume DESC;

-- Find customers who have NEVER transacted
SELECT c.name, c.tier, c.joined_date
FROM customers c
LEFT JOIN transactions t ON c.id = t.customer_id
WHERE t.id IS NULL          -- NULL means no match found
ORDER BY c.joined_date;
```

---

## RIGHT JOIN — All Right Rows + Matches

```sql
-- All transactions, even if customer was deleted
SELECT
    t.id,
    t.amount,
    t.type,
    c.name,
    c.tier
FROM customers c
RIGHT JOIN transactions t ON c.id = t.customer_id;

-- Note: RIGHT JOIN is rare — usually rewritten as LEFT JOIN
-- by swapping table order
```

---

## FULL OUTER JOIN — All Rows from Both

```sql
-- All customers AND all transactions
-- NULLs where no match exists
SELECT
    c.name,
    t.amount,
    t.type
FROM customers c
FULL OUTER JOIN transactions t ON c.id = t.customer_id;
```

---

## JOIN Types Visual Summary

```
Table A    Table B

INNER JOIN         LEFT JOIN         RIGHT JOIN       FULL OUTER
  ┌──┬──┐           ┌──┬──┐           ┌──┬──┐          ┌──┬──┐
  │  │██│           │██│██│           │  │██│          │██│██│
  └──┴──┘           └──┴──┘           └──┴──┘          └──┴──┘
  Only overlap      All A + overlap   All B + overlap  Everything
```

---

## Joining Multiple Tables

```sql
-- 3 table join: customers + transactions + products
SELECT
    c.name          AS customer,
    c.tier,
    t.amount,
    t.created_at,
    p.name          AS product,
    p.category
FROM customers c
INNER JOIN transactions t   ON c.id = t.customer_id
INNER JOIN products p       ON t.product_id = p.id
WHERE c.is_active = TRUE
ORDER BY t.created_at DESC;
```

---

## Self JOIN — Table Joined to Itself

```sql
-- Find employees and their managers (same table!)
SELECT
    e.name          AS employee,
    e.role,
    m.name          AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id
ORDER BY m.name, e.name;

-- Find customers in the same city
SELECT
    a.name AS customer_1,
    b.name AS customer_2,
    a.city
FROM customers a
JOIN customers b ON a.city = b.city
    AND a.id < b.id     -- Avoid duplicates and self-matches
ORDER BY a.city;
```

---

## CROSS JOIN — Every Combination

```sql
-- Every combination of products and months
SELECT
    p.name      AS product,
    m.month
FROM products p
CROSS JOIN (
    SELECT 'Jan' AS month UNION SELECT 'Feb' UNION
    SELECT 'Mar' UNION SELECT 'Apr'
) m;
-- Useful for creating full grids (e.g. all products × all months)
```

---

## COALESCE — Handle NULLs in JOINs

```sql
-- Replace NULLs from unmatched LEFT JOINs
SELECT
    c.name,
    COALESCE(COUNT(t.id), 0)        AS transactions,
    COALESCE(SUM(t.amount), 0)      AS total_spent,
    COALESCE(c.email, 'No email')   AS contact
FROM customers c
LEFT JOIN transactions t ON c.id = t.customer_id
GROUP BY c.id, c.name, c.email;
```

---

## Real World Example — Customer 360 View

```sql
-- Complete customer profile joining 4 tables
SELECT
    c.id,
    c.name,
    c.city,
    c.tier,
    c.balance,
    c.joined_date,

    -- Transaction summary
    COUNT(DISTINCT t.id)                    AS total_transactions,
    COALESCE(SUM(t.amount), 0)              AS lifetime_value,
    COALESCE(AVG(t.amount), 0)              AS avg_transaction,
    MAX(t.created_at)                       AS last_transaction_date,

    -- Days since last transaction
    CURRENT_DATE - MAX(t.created_at)::DATE  AS days_since_last_txn,

    -- Product preference
    MODE() WITHIN GROUP (ORDER BY p.category) AS favourite_category,

    -- Tenure
    AGE(c.joined_date)                      AS tenure

FROM customers c
LEFT JOIN transactions t    ON c.id = t.customer_id
LEFT JOIN products p        ON t.product_id = p.id
WHERE c.is_active = TRUE
GROUP BY c.id, c.name, c.city, c.tier, c.balance, c.joined_date
ORDER BY lifetime_value DESC;
```

---

## JOIN Best Practices

```sql
-- ✅ Always alias your tables
FROM customers c JOIN transactions t ON c.id = t.customer_id

-- ✅ Qualify column names (avoid ambiguity)
SELECT c.name, t.amount          -- Not just: SELECT name, amount

-- ✅ Join on indexed columns (primary/foreign keys)
ON c.id = t.customer_id          -- id is indexed = fast

-- ❌ Avoid joining on functions (slow!)
ON LOWER(c.name) = LOWER(t.name) -- Forces full scan

-- ✅ Filter early with WHERE
WHERE c.is_active = TRUE         -- Reduces rows before joining

-- ✅ Use LEFT JOIN when NULLs are expected
-- Use INNER JOIN when you only want matches
```

---

## Practice Exercises

```sql
-- 1. List all customers with their transaction count
SELECT c.name, COUNT(t.id) AS txn_count
FROM customers c
LEFT JOIN transactions t ON c.id = t.customer_id
GROUP BY c.id, c.name
ORDER BY txn_count DESC;

-- 2. Find customers who have never made a transaction
SELECT c.name, c.joined_date
FROM customers c
LEFT JOIN transactions t ON c.id = t.customer_id
WHERE t.id IS NULL;

-- 3. Get total transaction volume per city
SELECT c.city, SUM(t.amount) AS total_volume
FROM customers c
INNER JOIN transactions t ON c.id = t.customer_id
GROUP BY c.city
ORDER BY total_volume DESC;

-- 4. Top 10 customers by total spending
SELECT
    c.name,
    c.tier,
    SUM(t.amount) AS total_spent
FROM customers c
JOIN transactions t ON c.id = t.customer_id
GROUP BY c.id, c.name, c.tier
ORDER BY total_spent DESC
LIMIT 10;
```

---

## Previous | Next
← [[03 - Aggregate Functions]] | → [[05 - Subqueries]]
