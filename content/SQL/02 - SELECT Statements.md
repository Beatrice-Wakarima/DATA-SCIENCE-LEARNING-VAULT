---
title: SELECT Statements
tags: [sql, basics]
created: 2026-05-20
up:: [[SQL MOC]]
---

# 🔍 SELECT Statements

> SELECT is the most used SQL command. You'll write it hundreds of times a day. Master every variation here.

---

## Basic SELECT

```sql
-- All columns
SELECT * FROM customers;

-- Specific columns
SELECT name, city, tier FROM customers;

-- With alias (rename columns in results)
SELECT 
    name        AS customer_name,
    balance     AS account_balance,
    tier        AS membership_tier
FROM customers;
```

---

## DISTINCT — Remove Duplicates

```sql
-- All cities (with duplicates)
SELECT city FROM customers;

-- Unique cities only
SELECT DISTINCT city FROM customers;

-- Unique combinations
SELECT DISTINCT city, tier FROM customers;

-- Count unique values
SELECT COUNT(DISTINCT city) AS unique_cities FROM customers;
SELECT COUNT(DISTINCT tier) AS tier_types FROM customers;
```

---

## WHERE — Filtering Rows

```sql
-- Single condition
SELECT * FROM customers WHERE tier = 'Gold';
SELECT * FROM customers WHERE balance > 50000;
SELECT * FROM customers WHERE age < 30;

-- Multiple conditions
SELECT * FROM customers 
WHERE tier = 'Gold' AND city = 'Nairobi';

SELECT * FROM customers 
WHERE tier = 'Gold' OR tier = 'Platinum';

SELECT * FROM customers 
WHERE NOT tier = 'Bronze';
```

---

## Comparison Operators

```sql
WHERE balance = 95000       -- Equal
WHERE balance != 95000      -- Not equal
WHERE balance <> 95000      -- Not equal (alternative)
WHERE balance > 50000       -- Greater than
WHERE balance < 50000       -- Less than
WHERE balance >= 50000      -- Greater or equal
WHERE balance <= 50000      -- Less or equal
```

---

## BETWEEN — Range Filter

```sql
-- Between (inclusive on both ends)
SELECT * FROM customers 
WHERE balance BETWEEN 50000 AND 200000;

-- Equivalent to:
SELECT * FROM customers 
WHERE balance >= 50000 AND balance <= 200000;

-- Date range
SELECT * FROM transactions
WHERE created_at BETWEEN '2026-01-01' AND '2026-05-31';

-- Age range
SELECT * FROM customers WHERE age BETWEEN 25 AND 40;
```

---

## IN — Match a List

```sql
-- Instead of multiple OR conditions
SELECT * FROM customers 
WHERE tier IN ('Gold', 'Platinum');

-- Same as:
WHERE tier = 'Gold' OR tier = 'Platinum'

-- Cities
SELECT * FROM customers
WHERE city IN ('Nairobi', 'Mombasa', 'Kisumu');

-- NOT IN
SELECT * FROM customers
WHERE tier NOT IN ('Bronze', 'Silver');

-- With subquery
SELECT * FROM customers
WHERE id IN (SELECT customer_id FROM transactions WHERE amount > 100000);
```

---

## LIKE — Pattern Matching

```sql
-- % = any number of characters
-- _ = exactly one character

-- Names starting with 'B'
SELECT * FROM customers WHERE name LIKE 'B%';

-- Names ending with 'a'
SELECT * FROM customers WHERE name LIKE '%a';

-- Names containing 'ea'
SELECT * FROM customers WHERE name LIKE '%ea%';

-- Email from Gmail
SELECT * FROM customers WHERE email LIKE '%@gmail.com';

-- Exactly 5-letter names
SELECT * FROM customers WHERE name LIKE '_____';

-- Names starting with 'Be' (4 letters total)
SELECT * FROM customers WHERE name LIKE 'Be__';

-- Case-insensitive (PostgreSQL)
SELECT * FROM customers WHERE name ILIKE 'beatrice%';
```

---

## IS NULL / IS NOT NULL

```sql
-- Customers without email
SELECT * FROM customers WHERE email IS NULL;

-- Customers with email
SELECT * FROM customers WHERE email IS NOT NULL;

-- Count nulls
SELECT COUNT(*) FROM customers WHERE email IS NULL;

-- Never use = NULL (doesn't work!)
SELECT * FROM customers WHERE email = NULL;    -- ❌ Wrong!
SELECT * FROM customers WHERE email IS NULL;   -- ✅ Correct
```

---

## ORDER BY — Sorting

```sql
-- Ascending (default)
SELECT * FROM customers ORDER BY balance;
SELECT * FROM customers ORDER BY balance ASC;

-- Descending
SELECT * FROM customers ORDER BY balance DESC;

-- Sort by name alphabetically
SELECT * FROM customers ORDER BY name ASC;

-- Multiple columns
SELECT * FROM customers 
ORDER BY tier ASC, balance DESC;

-- Sort by column position (2 = second column)
SELECT name, balance, tier FROM customers
ORDER BY 2 DESC;
```

---

## LIMIT & OFFSET — Pagination

```sql
-- First 10 rows
SELECT * FROM customers LIMIT 10;

-- Top 5 by balance
SELECT name, balance FROM customers
ORDER BY balance DESC
LIMIT 5;

-- Skip first 10, get next 10 (page 2)
SELECT * FROM customers
ORDER BY id
LIMIT 10 OFFSET 10;

-- Page 3 (rows 21-30)
SELECT * FROM customers
ORDER BY id
LIMIT 10 OFFSET 20;
```

---

## Calculated Columns

```sql
-- Math in SELECT
SELECT 
    name,
    salary,
    salary * 0.10           AS bonus,
    salary + salary * 0.10  AS total_comp,
    salary * 12             AS annual_salary
FROM employees;

-- String operations
SELECT 
    UPPER(name)             AS name_upper,
    LOWER(email)            AS email_lower,
    LENGTH(name)            AS name_length,
    CONCAT(first_name, ' ', last_name) AS full_name
FROM customers;

-- Date calculations
SELECT 
    name,
    joined_date,
    CURRENT_DATE - joined_date      AS days_as_customer,
    AGE(joined_date)                AS tenure
FROM customers;
```

---

## CASE WHEN — Conditional Columns

```sql
-- Like an IF statement in SQL
SELECT 
    name,
    balance,
    CASE 
        WHEN balance >= 100000  THEN 'Platinum'
        WHEN balance >= 50000   THEN 'Gold'
        WHEN balance >= 10000   THEN 'Silver'
        ELSE                         'Bronze'
    END AS calculated_tier
FROM customers;

-- Binary flag
SELECT 
    name,
    age,
    CASE WHEN age >= 18 THEN 'Adult' ELSE 'Minor' END AS age_group
FROM customers;

-- Count by condition
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN tier = 'Gold' THEN 1 ELSE 0 END) AS gold_customers,
    SUM(CASE WHEN tier = 'Platinum' THEN 1 ELSE 0 END) AS platinum_customers,
    SUM(CASE WHEN balance > 100000 THEN 1 ELSE 0 END) AS high_balance
FROM customers;
```

---

## Real World Example — Customer Report

```sql
-- Full customer analysis query
SELECT
    c.id,
    c.name,
    c.city,
    c.age,
    c.balance,
    c.tier,
    
    -- Calculated fields
    CASE
        WHEN c.age < 30 THEN 'Young'
        WHEN c.age < 50 THEN 'Middle-aged'
        ELSE 'Senior'
    END AS age_segment,
    
    CASE
        WHEN c.balance >= 200000 THEN '⭐⭐⭐ VIP'
        WHEN c.balance >= 100000 THEN '⭐⭐ Premium'
        WHEN c.balance >= 50000  THEN '⭐ Standard'
        ELSE 'Basic'
    END AS value_segment,
    
    ROUND(c.balance * 0.08, 2) AS annual_interest,
    
    CURRENT_DATE - c.joined_date AS days_as_customer

FROM customers c
WHERE c.is_active = TRUE
    AND c.balance > 0
ORDER BY c.balance DESC
LIMIT 20;
```

---

## Practice Exercises

```sql
-- 1. Get all Platinum customers in Nairobi
SELECT * FROM customers
WHERE tier = 'Platinum' AND city = 'Nairobi';

-- 2. Find customers aged between 25-40 with balance over 50000
SELECT name, age, balance FROM customers
WHERE age BETWEEN 25 AND 40
AND balance > 50000
ORDER BY balance DESC;

-- 3. Find customers whose name starts with 'B' or 'J'
SELECT * FROM customers
WHERE name LIKE 'B%' OR name LIKE 'J%'
ORDER BY name;

-- 4. Get top 5 customers by balance who are active
SELECT name, tier, balance
FROM customers
WHERE is_active = TRUE
ORDER BY balance DESC
LIMIT 5;

-- 5. Find customers with no email on record
SELECT name, city, tier
FROM customers
WHERE email IS NULL
ORDER BY tier, name;
```

---

## Previous | Next
← [[01 - Introduction to SQL]] | → [[03 - Aggregate Functions]]
