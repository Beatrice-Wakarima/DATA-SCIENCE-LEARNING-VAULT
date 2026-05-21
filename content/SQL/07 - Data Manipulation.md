---
title: Data Manipulation (INSERT, UPDATE, DELETE)
tags: [sql, basics, dml]
created: 2026-05-20
up:: [[SQL MOC]]
---

# ✏️ Data Manipulation (INSERT, UPDATE, DELETE)

> DML commands change your data. SELECT reads, INSERT adds, UPDATE modifies, DELETE removes. Always test with SELECT before running UPDATE or DELETE!

---

## INSERT — Adding Data

```sql
-- Insert single row
INSERT INTO customers (name, email, city, tier, balance)
VALUES ('Beatrice Wakarima', 'beatrice@gmail.com', 'Nairobi', 'Gold', 95000);

-- Insert multiple rows at once (more efficient)
INSERT INTO customers (name, email, city, tier, balance)
VALUES
    ('John Doe',    'john@gmail.com',  'Mombasa', 'Silver',   45000),
    ('Alice Smith', 'alice@gmail.com', 'Kisumu',  'Platinum', 250000),
    ('Bob Kamau',   'bob@gmail.com',   'Nairobi', 'Bronze',   8000);

-- Insert with only required columns (others get defaults)
INSERT INTO customers (name, city)
VALUES ('Carol Wanjiru', 'Eldoret');
-- tier defaults to 'Bronze', balance defaults to 0

-- Insert from another table (very useful in ETL!)
INSERT INTO customers_archive
SELECT * FROM customers
WHERE is_active = FALSE;

-- Insert from SELECT with transformation
INSERT INTO customer_summary (customer_id, total_transactions, total_spent)
SELECT
    customer_id,
    COUNT(*),
    SUM(amount)
FROM transactions
GROUP BY customer_id;
```

---

## INSERT ON CONFLICT — Upsert

```sql
-- Insert or update if already exists (PostgreSQL)
INSERT INTO customers (id, name, email, balance)
VALUES (1, 'Beatrice', 'beatrice@gmail.com', 95000)
ON CONFLICT (id)
DO UPDATE SET
    name    = EXCLUDED.name,
    email   = EXCLUDED.email,
    balance = EXCLUDED.balance;

-- Insert or ignore if exists
INSERT INTO customers (email, name)
VALUES ('beatrice@gmail.com', 'Beatrice')
ON CONFLICT (email)
DO NOTHING;
```

---

## UPDATE — Modifying Data

```sql
-- ⚠️ ALWAYS add WHERE clause or you update ALL rows!

-- Update single column
UPDATE customers
SET tier = 'Platinum'
WHERE id = 1;

-- Update multiple columns
UPDATE customers
SET
    tier        = 'Gold',
    balance     = balance + 50000,
    updated_at  = NOW()
WHERE id = 5;

-- Update with calculation
UPDATE employees
SET salary = salary * 1.10          -- 10% raise for everyone
WHERE department = 'Engineering'
  AND performance_rating = 'Excellent';

-- Update based on another table (UPDATE with JOIN)
UPDATE customers c
SET tier = 'Platinum'
FROM (
    SELECT customer_id
    FROM transactions
    GROUP BY customer_id
    HAVING SUM(amount) > 500000
) AS high_value
WHERE c.id = high_value.customer_id;
```

---

## Safe UPDATE Pattern

```sql
-- Step 1: Preview what will change
SELECT id, name, tier, balance
FROM customers
WHERE balance > 100000 AND tier != 'Platinum';

-- Step 2: Update (same WHERE clause!)
UPDATE customers
SET tier = 'Platinum'
WHERE balance > 100000 AND tier != 'Platinum';

-- Step 3: Verify
SELECT id, name, tier, balance
FROM customers
WHERE balance > 100000;
```

---

## DELETE — Removing Data

```sql
-- ⚠️ ALWAYS use WHERE — DELETE without WHERE removes ALL rows!

-- Delete single row
DELETE FROM customers WHERE id = 5;

-- Delete with condition
DELETE FROM customers
WHERE is_active = FALSE
  AND joined_date < '2020-01-01';

-- Delete based on subquery
DELETE FROM transactions
WHERE customer_id IN (
    SELECT id FROM customers WHERE is_active = FALSE
);

-- Delete with JOIN (PostgreSQL)
DELETE FROM transactions t
USING customers c
WHERE t.customer_id = c.id
  AND c.is_active = FALSE;
```

---

## TRUNCATE vs DELETE

```sql
-- DELETE: Removes rows one by one, can be rolled back, slow on large tables
DELETE FROM staging_table;

-- TRUNCATE: Removes ALL rows instantly, faster, harder to recover
TRUNCATE TABLE staging_table;
TRUNCATE TABLE staging_table RESTART IDENTITY;    -- Also resets auto-increment

-- Rule of thumb:
-- DELETE → when you need WHERE clause or rollback option
-- TRUNCATE → when emptying large staging tables in pipelines
```

---

## RETURNING — Get Data Back

```sql
-- INSERT and get the new row back
INSERT INTO customers (name, email, city)
VALUES ('New Customer', 'new@gmail.com', 'Nairobi')
RETURNING id, name, joined_date;

-- UPDATE and see what changed
UPDATE customers
SET tier = 'Platinum'
WHERE balance > 200000
RETURNING id, name, tier, balance;

-- DELETE and log what was removed
DELETE FROM customers
WHERE is_active = FALSE
RETURNING id, name, email;
```

---

## Transactions — All or Nothing

```sql
-- Wrap related changes in a transaction
BEGIN;

    -- Debit sender
    UPDATE accounts
    SET balance = balance - 50000
    WHERE id = 1;

    -- Credit receiver
    UPDATE accounts
    SET balance = balance + 50000
    WHERE id = 2;

    -- Log the transfer
    INSERT INTO transfer_log (from_id, to_id, amount, created_at)
    VALUES (1, 2, 50000, NOW());

COMMIT;     -- Save all changes
-- ROLLBACK; -- Cancel all changes if something went wrong

-- With error handling
BEGIN;
    UPDATE accounts SET balance = balance - 50000 WHERE id = 1;

    -- Check sufficient funds
    DO $$
    BEGIN
        IF (SELECT balance FROM accounts WHERE id = 1) < 0 THEN
            RAISE EXCEPTION 'Insufficient funds';
        END IF;
    END $$;

    UPDATE accounts SET balance = balance + 50000 WHERE id = 2;
COMMIT;
```

---

## Real World ETL Pattern

```sql
-- Daily pipeline: load staging → clean → insert to production

BEGIN;

-- 1. Clear yesterday's staging data
TRUNCATE TABLE stg_transactions;

-- 2. Load fresh data (done by Python/Airflow)
-- COPY stg_transactions FROM '/data/transactions_2026-05-20.csv' CSV HEADER;

-- 3. Validate before inserting
DO $$
DECLARE row_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO row_count FROM stg_transactions;
    IF row_count = 0 THEN
        RAISE EXCEPTION 'Staging table is empty — aborting pipeline';
    END IF;
    RAISE NOTICE 'Staging rows: %', row_count;
END $$;

-- 4. Insert new, valid records only
INSERT INTO transactions (customer_id, amount, type, created_at)
SELECT
    s.customer_id,
    s.amount,
    s.type,
    s.created_at
FROM stg_transactions s
WHERE s.amount > 0
  AND s.customer_id IS NOT NULL
  AND NOT EXISTS (
      SELECT 1 FROM transactions t
      WHERE t.id = s.source_id      -- Skip duplicates
  );

-- 5. Update customer last_activity
UPDATE customers c
SET last_activity = NOW()
FROM stg_transactions s
WHERE c.id = s.customer_id;

-- 6. Commit everything
COMMIT;

RAISE NOTICE '✅ Pipeline complete';
```

---

## Quick Reference

```sql
-- INSERT
INSERT INTO table (col1, col2) VALUES (val1, val2);
INSERT INTO table SELECT ... FROM other_table;
INSERT INTO table VALUES (...) ON CONFLICT DO UPDATE/NOTHING;

-- UPDATE
UPDATE table SET col = value WHERE condition;
UPDATE table SET col = value FROM other WHERE join_condition;

-- DELETE
DELETE FROM table WHERE condition;
DELETE FROM table USING other WHERE join_condition;

-- Safe pattern
SELECT ... WHERE condition;   -- Preview first!
UPDATE/DELETE ... WHERE condition;  -- Same condition

-- Transactions
BEGIN; ... COMMIT;    -- Save
BEGIN; ... ROLLBACK;  -- Cancel
```

---

## Previous | Next
← [[06 - CTEs and Window Functions]] | → [[08 - DDL — Creating and Managing Tables]]
