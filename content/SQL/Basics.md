# Introduction to SQL

_A comprehensive introduction to Structured Query Language for database operations_

## What is SQL?

**SQL** (Structured Query Language) is a standardized programming language designed for managing and manipulating relational databases. It allows you to create, read, update, and delete data stored in database tables.

> [!note] SQL Pronunciation SQL is pronounced either as "S-Q-L" (spelling out the letters) or "sequel". Both are widely accepted in the industry.

### Key Characteristics of SQL

- **Declarative Language**: You specify _what_ you want, not _how_ to get it
- **Standard Language**: Works across different database systems (with minor variations)
- **Set-based Operations**: Works with groups of records rather than individual rows
- **English-like Syntax**: Commands use words like SELECT, FROM, WHERE

## Why Learn SQL?

### Professional Benefits

- **Universal Skill**: Used across industries and job roles
- **Data Access**: Direct access to organizational data
- **Career Advancement**: Essential for [[Data Analysis]], [[Business Intelligence]], and [[Data Science]] roles
- **Efficiency**: Much faster than Excel for large datasets

### Common Use Cases

- Generating reports and dashboards
- Data analysis and exploration
- Database administration
- ETL (Extract, Transform, Load) processes
- Web application backends

> [!tip] Career Impact According to Stack Overflow's Developer Survey, SQL consistently ranks among the most in-demand and highest-paying technical skills.

## Database Fundamentals

### What is a Database?

A **database** is an organized collection of structured information stored electronically. Think of it as a digital filing system where data is stored in tables.

### Relational Database Concepts

#### Tables (Relations)

- Collections of related data organized in rows and columns
- Similar to spreadsheets but with strict rules and relationships

#### Rows (Records/Tuples)

- Individual entries in a table
- Each row represents a single instance of the entity

#### Columns (Fields/Attributes)

- Categories of information stored in the table
- Each column has a specific data type

#### Primary Key

- Unique identifier for each row in a table
- Cannot be NULL and must be unique

#### Foreign Key

- Column that references the primary key of another table
- Creates relationships between tables

### Example Database Structure

```
CUSTOMERS Table:
+-------------+----------+----------+-------+
| customer_id | name     | email    | city  |
+-------------+----------+----------+-------+
| 1           | John Doe | j@ex.com | NYC   |
| 2           | Jane Doe | jane@ex  | LA    |
+-------------+----------+----------+-------+

ORDERS Table:
+----------+-------------+--------+------------+
| order_id | customer_id| amount | order_date |
+----------+-------------+--------+------------+
| 101      | 1          | 250.00 | 2024-01-15 |
| 102      | 2          | 175.50 | 2024-01-16 |
+----------+-------------+--------+------------+
```

> [!question] Think About It How would you design tables to store information about a library system with books, authors, and borrowers?

## SQL Command Categories

### Data Query Language (DQL)

- **Purpose**: Retrieve data from databases
- **Main Command**: `SELECT`
- **Most commonly used category**

### Data Definition Language (DDL)

- **Purpose**: Define and modify database structure
- **Commands**: `CREATE`, `ALTER`, `DROP`
- **Examples**: Creating tables, adding columns

### Data Manipulation Language (DML)

- **Purpose**: Modify data within tables
- **Commands**: `INSERT`, `UPDATE`, `DELETE`
- **Examples**: Adding new records, changing values

### Data Control Language (DCL)

- **Purpose**: Control access to data
- **Commands**: `GRANT`, `REVOKE`
- **Used by database administrators**

## Basic SQL Syntax Rules

### General Guidelines

- SQL statements end with semicolons (`;`)
- Keywords are not case-sensitive (`SELECT` = `select`)
- Table and column names may be case-sensitive (depends on database)
- String values must be enclosed in single quotes (`'text'`)
- Comments use `--` for single line or `/* */` for multi-line

### Formatting Best Practices

```sql
-- Good formatting
SELECT customer_id, 
       name, 
       email
FROM customers
WHERE city = 'New York'
ORDER BY name;

-- Avoid this formatting
select customer_id,name,email from customers where city='New York' order by name;
```

> [!tip] Writing Clean SQL Use consistent indentation and capitalization. Many developers capitalize SQL keywords and use lowercase for table/column names.

## The SELECT Statement

The `SELECT` statement is the foundation of SQL querying. It retrieves data from one or more tables.

### Basic Syntax

```sql
SELECT column1, column2, ...
FROM table_name;
```

### Examples

#### Selecting All Columns

```sql
-- Select all columns from customers table
SELECT * FROM customers;
```

#### Selecting Specific Columns

```sql
-- Select only name and email
SELECT name, email FROM customers;
```

#### Using Column Aliases

```sql
-- Give columns more readable names
SELECT customer_id AS ID,
       name AS "Customer Name",
       email AS "Email Address"
FROM customers;
```

## Filtering Data with WHERE

The `WHERE` clause filters rows based on specified conditions.

### Basic WHERE Syntax

```sql
SELECT column1, column2
FROM table_name
WHERE condition;
```

### Comparison Operators

|Operator|Description|Example|
|---|---|---|
|`=`|Equal to|`WHERE age = 25`|
|`!=` or `<>`|Not equal to|`WHERE city != 'NYC'`|
|`>`|Greater than|`WHERE salary > 50000`|
|`<`|Less than|`WHERE age < 30`|
|`>=`|Greater than or equal|`WHERE price >= 100`|
|`<=`|Less than or equal|`WHERE score <= 85`|

### Pattern Matching with LIKE

```sql
-- Names starting with 'J'
SELECT * FROM customers 
WHERE name LIKE 'J%';

-- Names containing 'son'
SELECT * FROM customers 
WHERE name LIKE '%son%';

-- Names with exactly 4 characters
SELECT * FROM customers 
WHERE name LIKE '____';
```

### Working with NULL Values

```sql
-- Find customers without email
SELECT * FROM customers 
WHERE email IS NULL;

-- Find customers with email
SELECT * FROM customers 
WHERE email IS NOT NULL;
```

> [!note] NULL vs Empty String `NULL` means "no value" while `''` (empty string) means "empty value". They are different in SQL!

## Logical Operators

### AND, OR, NOT

```sql
-- Customers from NYC with age > 25
SELECT * FROM customers 
WHERE city = 'NYC' AND age > 25;

-- Customers from NYC or LA
SELECT * FROM customers 
WHERE city = 'NYC' OR city = 'LA';

-- Customers NOT from NYC
SELECT * FROM customers 
WHERE NOT city = 'NYC';
```

### IN Operator

```sql
-- Multiple values
SELECT * FROM customers 
WHERE city IN ('NYC', 'LA', 'Chicago');

-- Equivalent to:
SELECT * FROM customers 
WHERE city = 'NYC' OR city = 'LA' OR city = 'Chicago';
```

### BETWEEN Operator

```sql
-- Ages between 25 and 35 (inclusive)
SELECT * FROM customers 
WHERE age BETWEEN 25 AND 35;

-- Equivalent to:
SELECT * FROM customers 
WHERE age >= 25 AND age <= 35;
```

## Sorting Results with ORDER BY

### Basic Sorting

```sql
-- Sort by name (ascending - default)
SELECT * FROM customers 
ORDER BY name;

-- Sort by name (descending)
SELECT * FROM customers 
ORDER BY name DESC;
```

### Multiple Column Sorting

```sql
-- Sort by city first, then by name within each city
SELECT * FROM customers 
ORDER BY city ASC, name ASC;
```

### Sorting by Column Position

```sql
-- Sort by the second column in the SELECT list
SELECT name, age FROM customers 
ORDER BY 2 DESC;
```

> [!tip] Performance Note Sorting large datasets can be expensive. Consider adding indexes on frequently sorted columns.

## Limiting Results

### LIMIT (MySQL, PostgreSQL)

```sql
-- Get first 10 customers
SELECT * FROM customers 
LIMIT 10;

-- Skip first 5, get next 10
SELECT * FROM customers 
LIMIT 10 OFFSET 5;
```

### TOP (SQL Server)

```sql
-- Get first 10 customers
SELECT TOP 10 * FROM customers;
```

### ROWNUM (Oracle)

```sql
-- Get first 10 customers
SELECT * FROM customers 
WHERE ROWNUM <= 10;
```

## Aggregate Functions

Aggregate functions perform calculations on sets of rows and return a single value.

### Common Aggregate Functions

|Function|Purpose|Example|
|---|---|---|
|`COUNT()`|Count rows|`COUNT(*)`|
|`SUM()`|Sum numeric values|`SUM(amount)`|
|`AVG()`|Average value|`AVG(price)`|
|`MAX()`|Maximum value|`MAX(salary)`|
|`MIN()`|Minimum value|`MIN(age)`|

### Examples

```sql
-- Count total customers
SELECT COUNT(*) FROM customers;

-- Count customers with email
SELECT COUNT(email) FROM customers;

-- Average order amount
SELECT AVG(amount) FROM orders;

-- Highest and lowest order amounts
SELECT MAX(amount), MIN(amount) FROM orders;
```

> [!note] NULL Handling Aggregate functions (except COUNT(_)) ignore NULL values. COUNT(column) counts non-NULL values, while COUNT(_) counts all rows.

## Grouping Data with GROUP BY

`GROUP BY` groups rows with the same values in specified columns and allows you to apply aggregate functions to each group.

### Basic GROUP BY

```sql
-- Count customers by city
SELECT city, COUNT(*) as customer_count
FROM customers 
GROUP BY city;
```

### Multiple Column Grouping

```sql
-- Count customers by city and age
SELECT city, age, COUNT(*) as count
FROM customers 
GROUP BY city, age
ORDER BY city, age;
```

### HAVING Clause

`HAVING` filters groups (used with GROUP BY), while `WHERE` filters individual rows.

```sql
-- Cities with more than 5 customers
SELECT city, COUNT(*) as customer_count
FROM customers 
GROUP BY city
HAVING COUNT(*) > 5;
```

> [!question] WHERE vs HAVING **WHERE** filters rows before grouping. **HAVING** filters groups after grouping. Can you think of when you'd use each?

## Data Types

### Numeric Types

- **INT/INTEGER**: Whole numbers (-2,147,483,648 to 2,147,483,647)
- **BIGINT**: Large whole numbers
- **DECIMAL(p,s)**: Fixed-point numbers (p=precision, s=scale)
- **FLOAT/REAL**: Approximate floating-point numbers

### String Types

- **CHAR(n)**: Fixed-length string
- **VARCHAR(n)**: Variable-length string (up to n characters)
- **TEXT**: Large text data

### Date/Time Types

- **DATE**: Date only (YYYY-MM-DD)
- **TIME**: Time only (HH:MM:SS)
- **DATETIME/TIMESTAMP**: Date and time combined

### Boolean Type

- **BOOLEAN**: TRUE/FALSE values (implementation varies by database)

## Practice Exercises

### Exercise 1: Basic Queries

Given a `products` table with columns: `product_id`, `name`, `price`, `category`:

```sql
-- 1. Select all products
SELECT * FROM products;

-- 2. Select product names and prices
SELECT name, price FROM products;

-- 3. Find products with price > 50
SELECT * FROM products WHERE price > 50;

-- 4. Find products in 'Electronics' category
SELECT * FROM products WHERE category = 'Electronics';
```

### Exercise 2: Filtering and Sorting

```sql
-- 1. Products priced between $20 and $100
SELECT * FROM products 
WHERE price BETWEEN 20 AND 100;

-- 2. Products in 'Books' or 'Music' categories
SELECT * FROM products 
WHERE category IN ('Books', 'Music');

-- 3. Sort products by price (highest first)
SELECT * FROM products 
ORDER BY price DESC;

-- 4. Find products with names starting with 'A'
SELECT * FROM products 
WHERE name LIKE 'A%';
```

### Exercise 3: Aggregation

```sql
-- 1. Count total products
SELECT COUNT(*) FROM products;

-- 2. Average product price
SELECT AVG(price) FROM products;

-- 3. Count products by category
SELECT category, COUNT(*) as product_count
FROM products 
GROUP BY category;

-- 4. Categories with more than 10 products
SELECT category, COUNT(*) as product_count
FROM products 
GROUP BY category
HAVING COUNT(*) > 10;
```

> [!tip] Practice Recommendation Try these exercises on sample databases like Sakila (MySQL) or Chinook (SQLite) for hands-on experience.

## Common Mistakes to Avoid

### 1. Forgetting WHERE with UPDATE/DELETE

```sql
-- DANGEROUS: Updates ALL rows
UPDATE customers SET city = 'NYC';

-- CORRECT: Update specific rows
UPDATE customers SET city = 'NYC' WHERE customer_id = 1;
```

### 2. Using SELECT * in Production

```sql
-- Avoid: Returns all columns (inefficient)
SELECT * FROM large_table;

-- Better: Specify needed columns
SELECT customer_id, name FROM large_table;
```

### 3. Not Handling NULL Values

```sql
-- May not work as expected
SELECT * FROM customers WHERE age = NULL;

-- Correct way to check for NULL
SELECT * FROM customers WHERE age IS NULL;
```

### 4. Incorrect GROUP BY Usage

```sql
-- ERROR: name not in GROUP BY
SELECT name, COUNT(*) FROM customers GROUP BY city;

-- CORRECT: Include all non-aggregate columns
SELECT city, COUNT(*) FROM customers GROUP BY city;
```

## Next Steps in Your SQL Journey

### Intermediate Topics to Explore

- [[SQL Joins]] - Combining data from multiple tables
- [[SQL Subqueries]] - Queries within queries
- [[SQL Views]] - Virtual tables for simplified access
- [[SQL Indexes]] - Improving query performance
- [[SQL Functions]] - Built-in and custom functions

### Advanced Topics

- [[SQL Window Functions]] - Advanced analytical functions
- [[SQL Stored Procedures]] - Reusable code blocks
- [[SQL Triggers]] - Automated database actions
- [[SQL Performance Optimization]] - Query tuning techniques

### Practical Applications

- [[Database Design]] principles
- [[Data Analysis with SQL]] techniques
- [[ETL Processes]] using SQL
- [[Reporting and Business Intelligence]]

> [!note] Database-Specific Learning While SQL is standardized, each database system (MySQL, PostgreSQL, SQL Server, Oracle) has unique features. Choose one to focus on initially.

## Tools for Practicing SQL

### Online Platforms

- **SQLiteOnline**: Browser-based SQL practice
- **DB Fiddle**: Test queries across different databases
- **HackerRank SQL**: Structured practice problems
- **LeetCode Database**: Interview-style SQL problems

### Desktop Tools

- **MySQL Workbench**: For MySQL databases
- **pgAdmin**: For PostgreSQL databases
- **DBeaver**: Universal database client
- **SQLiteStudio**: For SQLite databases

### Sample Databases

- **Sakila**: DVD rental store (MySQL)
- **Chinook**: Digital media store (multiple formats)
- **Northwind**: Trading company (Microsoft)
- **AdventureWorks**: Bike manufacturer (SQL Server)

## Summary

### Key Concepts Learned

- **SQL Fundamentals**: What SQL is and why it's important
- **Database Concepts**: Tables, rows, columns, keys
- **Basic Queries**: SELECT statements with filtering and sorting
- **Aggregation**: GROUP BY and aggregate functions (COUNT, SUM, AVG)
- **Data Types**: Numeric, string, date/time, and boolean types

### Essential SQL Commands

```sql
-- Data Retrieval
SELECT column FROM table WHERE condition;

-- Filtering
WHERE column = value
WHERE column LIKE 'pattern%'
WHERE column IN (value1, value2)
WHERE column BETWEEN value1 AND value2

-- Sorting
ORDER BY column ASC/DESC

-- Grouping
GROUP BY column
HAVING condition

-- Aggregation
COUNT(*), SUM(column), AVG(column), MAX(column), MIN(column)
```

### What You Can Do Now

- ✅ Write basic SELECT queries
- ✅ Filter data using WHERE clause
- ✅ Sort results with ORDER BY
- ✅ Group data and calculate aggregates
- ✅ Understand fundamental database concepts

### Next Learning Goals

- [ ] Learn SQL JOINs to combine multiple tables
- [ ] Practice with real datasets
- [ ] Explore database-specific features
- [ ] Build a portfolio project using SQL

> [!tip] Remember SQL is best learned through practice. Start with simple queries and gradually increase complexity. The more you practice, the more natural SQL thinking becomes!

---

_Tags: #SQL #Database #DataAnalysis #Programming #Beginner #Tutorial #DataScience #QueryLanguage_
