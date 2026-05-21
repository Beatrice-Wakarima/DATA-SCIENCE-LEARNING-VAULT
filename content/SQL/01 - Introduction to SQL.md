---
title: Introduction to SQL
tags: [sql, basics]
created: 2026-05-20
up:: [[SQL MOC]]
---

# 🗄️ Introduction to SQL

> SQL (Structured Query Language) is the universal language for working with databases. Every data role — analyst, engineer, scientist — uses SQL daily. It's the most important skill in data.

---

## What is SQL?

SQL lets you:
- **Ask questions** of your data (`SELECT`)
- **Add** new data (`INSERT`)
- **Change** existing data (`UPDATE`)
- **Remove** data (`DELETE`)
- **Create** tables and databases (`CREATE`)

---

## Relational Databases

Data is stored in **tables** — like Excel sheets, but connected.

```
customers table:
┌─────┬──────────┬───────────┬─────────┐
│ id  │ name     │ city      │ tier    │
├─────┼──────────┼───────────┼─────────┤
│  1  │ Beatrice │ Nairobi   │ Gold    │
│  2  │ John     │ Mombasa   │ Silver  │
│  3  │ Alice    │ Kisumu    │ Platinum│
└─────┴──────────┴───────────┴─────────┘

transactions table:
┌─────┬─────────────┬────────┬──────────┐
│ id  │ customer_id │ amount │ type     │
├─────┼─────────────┼────────┼──────────┤
│  1  │      1      │ 45000  │ deposit  │
│  2  │      1      │ 10000  │ withdraw │
│  3  │      2      │ 25000  │ deposit  │
└─────┴─────────────┴────────┴──────────┘
```

The `customer_id` in transactions **links** to `id` in customers — this is a **relationship**.

---

## SQL Syntax Rules

```sql
-- Comments use two dashes
/* Multi-line
   comment */

-- Keywords are UPPERCASE by convention (not required)
SELECT name FROM customers;

-- Statements end with semicolon
SELECT * FROM customers;

-- Not case-sensitive for keywords
select * from customers;    -- Same result

-- String values use single quotes
WHERE name = 'Beatrice'     -- ✅
WHERE name = "Beatrice"     -- ❌ (in most databases)
```

---

## The 5 SQL Command Types

| Type | Commands | Purpose |
|---|---|---|
| **DQL** | SELECT | Query/read data |
| **DML** | INSERT, UPDATE, DELETE | Modify data |
| **DDL** | CREATE, ALTER, DROP | Define structure |
| **DCL** | GRANT, REVOKE | Control access |
| **TCL** | COMMIT, ROLLBACK | Manage transactions |

---

## Your First SQL Query

```sql
-- Get all customers
SELECT * FROM customers;

-- Get specific columns
SELECT name, city, tier FROM customers;

-- With a condition
SELECT name, tier 
FROM customers
WHERE tier = 'Gold';

-- Count records
SELECT COUNT(*) FROM customers;
```

---

## SQL Query Execution Order

Understanding this is KEY — SQL doesn't run top to bottom!

```sql
SELECT name, SUM(amount) AS total     -- 6. SELECT
FROM transactions                      -- 1. FROM
JOIN customers ON ...                  -- 2. JOIN
WHERE amount > 1000                    -- 3. WHERE
GROUP BY name                          -- 4. GROUP BY
HAVING SUM(amount) > 50000            -- 5. HAVING
ORDER BY total DESC                    -- 7. ORDER BY
LIMIT 10;                              -- 8. LIMIT
```

**Actual execution order:**
```
1. FROM       → Which table(s)?
2. JOIN       → Combine tables
3. WHERE      → Filter rows
4. GROUP BY   → Group rows
5. HAVING     → Filter groups
6. SELECT     → Choose columns
7. ORDER BY   → Sort results
8. LIMIT      → Restrict rows
```

---

## Popular Databases

| Database | Used For | Notes |
|---|---|---|
| **PostgreSQL** | Production data engineering | Most feature-rich, free |
| **MySQL** | Web applications | Very popular, free |
| **SQLite** | Local/embedded | File-based, no server |
| **SQL Server** | Enterprise (Microsoft) | Windows-heavy |
| **BigQuery** | Google cloud analytics | Serverless |
| **Snowflake** | Cloud data warehouse | Pay-per-query |
| **Redshift** | AWS data warehouse | Good for huge data |

---

## Setting Up PostgreSQL Locally

```bash
# Install via Docker (easiest!)
docker run -d \
  --name postgres-local \
  -e POSTGRES_USER=beatrice \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=learning \
  -p 5432:5432 \
  postgres:15

# Connect via psql
docker exec -it postgres-local psql -U beatrice -d learning
```

---

## Sample Database — We'll Use This Throughout

```sql
-- Customers table
CREATE TABLE customers (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(100) UNIQUE,
    city        VARCHAR(50),
    tier        VARCHAR(20) DEFAULT 'Bronze',
    balance     DECIMAL(12,2) DEFAULT 0,
    age         INTEGER,
    job         VARCHAR(50),
    is_active   BOOLEAN DEFAULT TRUE,
    joined_date DATE DEFAULT CURRENT_DATE
);

-- Transactions table
CREATE TABLE transactions (
    id              SERIAL PRIMARY KEY,
    customer_id     INTEGER REFERENCES customers(id),
    amount          DECIMAL(12,2) NOT NULL,
    type            VARCHAR(20),
    description     VARCHAR(200),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Products table
CREATE TABLE products (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100),
    category    VARCHAR(50),
    price       DECIMAL(10,2),
    stock       INTEGER DEFAULT 0
);
```

---

## Quick Reference — SQL Structure

```sql
SELECT  column1, column2, aggregate_function(column3)
FROM    table_name
JOIN    other_table ON condition
WHERE   filter_condition
GROUP BY column1, column2
HAVING  aggregate_condition
ORDER BY column1 ASC/DESC
LIMIT   number_of_rows
OFFSET  rows_to_skip;
```

---

## Previous | Next
← Start | → [[02 - SELECT Statements]]
