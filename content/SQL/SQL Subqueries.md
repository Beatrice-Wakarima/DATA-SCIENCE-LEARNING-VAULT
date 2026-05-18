# SQL Subqueries - Complete Guide

_Master the art of nested queries and advanced data filtering techniques_

## What are SQL Subqueries?

A **subquery** (also called a nested query or inner query) is a query nested inside another SQL query. The subquery executes first, and its result is used by the outer query to complete the operation. Subqueries are powerful tools for [[Advanced SQL]] operations and complex [[Data Analysis]].

> [!note] Think of It Like This A subquery is like asking a question within a question: "Show me customers who have placed orders (inner question) with amounts greater than $200 (outer question)."

### Basic Structure

```sql
SELECT column1, column2
FROM table1
WHERE column3 IN (
    SELECT column4
    FROM table2
    WHERE condition
);
```

### Why Use Subqueries?

- **Complex filtering**: Filter based on calculations from other tables
- **Dynamic comparisons**: Compare against calculated values
- **Data validation**: Find records that meet complex criteria
- **Avoiding joins**: Sometimes simpler than complex joins
- **Step-by-step logic**: Break complex problems into manageable parts

## Sample Tables for Examples

We'll use these tables throughout the guide:

### CUSTOMERS Table

```sql
+-------------+--------------+------------------+----------+
| customer_id | name         | email            | city     |
+-------------+--------------+------------------+----------+
| 1           | John Smith   | john@email.com   | New York |
| 2           | Jane Doe     | jane@email.com   | Los Angeles |
| 3           | Bob Johnson  | bob@email.com    | Chicago  |
| 4           | Alice Brown  | alice@email.com  | Miami    |
| 5           | Charlie Wilson| charlie@email.com| New York |
+-------------+--------------+------------------+----------+
```

### ORDERS Table

```sql
+----------+-------------+--------+------------+
| order_id | customer_id | amount | order_date |
+----------+-------------+--------+------------+
| 101      | 1           | 250.00 | 2024-01-15 |
| 102      | 1           | 175.50 | 2024-01-20 |
| 103      | 2           | 300.00 | 2024-01-18 |
| 104      | 2           | 425.75 | 2024-01-22 |
| 105      | 3           | 150.00 | 2024-01-19 |
| 106      | 5           | 275.25 | 2024-01-21 |
+----------+-------------+--------+------------+
```

### PRODUCTS Table

```sql
+------------+--------------+-------+-------------+
| product_id | product_name | price | category_id |
+------------+--------------+-------+-------------+
| 1          | Laptop       | 999.99| 1           |
| 2          | Mouse        | 29.99 | 1           |
| 3          | Keyboard     | 79.99 | 1           |
| 4          | Chair        | 199.99| 2           |
| 5          | Desk         | 299.99| 2           |
+------------+--------------+-------+-------------+
```

### CATEGORIES Table

```sql
+-------------+---------------+
| category_id | category_name |
+-------------+---------------+
| 1           | Electronics   |
| 2           | Furniture     |
+-------------+---------------+
```

## Types of Subqueries

### Classification by Return Type

|Subquery Type|Returns|Example Use|
|---|---|---|
|**Scalar Subquery**|Single value|Compare against average|
|**Column Subquery**|Single column, multiple rows|IN, ANY, ALL operations|
|**Row Subquery**|Single row, multiple columns|Compare multiple values|
|**Table Subquery**|Multiple rows and columns|FROM clause, complex filtering|

### Classification by Execution

|Execution Type|Description|Performance|
|---|---|---|
|**Independent**|Runs once, result used by outer query|Generally faster|
|**Correlated**|Runs for each row of outer query|Can be slower|

## 1. Scalar Subqueries

**Scalar subqueries** return exactly one value (single row, single column). They can be used anywhere a single value is expected.

### Basic Scalar Subquery

```sql
-- Find customers who spent more than the average order amount
SELECT name, customer_id
FROM customers
WHERE customer_id IN (
    SELECT customer_id
    FROM orders
    WHERE amount > (
        SELECT AVG(amount)  -- Scalar subquery
        FROM orders
    )
);
```

**Step-by-step execution:**

1. Inner subquery calculates: `AVG(amount) = 262.71`
2. Middle subquery finds orders > 262.71
3. Outer query finds customers with those orders

**Result:**

```sql
+--------------+-------------+
| name         | customer_id |
+--------------+-------------+
| Jane Doe     | 2           |
| Charlie Wilson| 5           |
+--------------+-------------+
```

### Scalar Subqueries in SELECT

```sql
-- Show each customer with total order count and average order amount
SELECT c.name,
       (SELECT COUNT(*) 
        FROM orders o 
        WHERE o.customer_id = c.customer_id) as order_count,
       (SELECT AVG(amount) 
        FROM orders o 
        WHERE o.customer_id = c.customer_id) as avg_order_amount
FROM customers c;
```

**Result:**

```sql
+----------------+-------------+------------------+
| name           | order_count | avg_order_amount |
+----------------+-------------+------------------+
| John Smith     | 2           | 212.75           |
| Jane Doe       | 2           | 362.88           |
| Bob Johnson    | 1           | 150.00           |
| Alice Brown    | 0           | NULL             |
| Charlie Wilson | 1           | 275.25           |
+----------------+-------------+------------------+
```

### Scalar Subqueries in WHERE

```sql
-- Find products priced above average
SELECT product_name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

> [!tip] Performance Note Scalar subqueries in SELECT can be expensive if they execute for each row. Consider using JOINs or window functions for better performance with large datasets.

## 2. Column Subqueries (List Subqueries)

**Column subqueries** return multiple values in a single column. They're commonly used with IN, ANY, ALL, and EXISTS operators.

### Using IN with Subqueries

```sql
-- Find customers who have placed orders
SELECT name, email
FROM customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id
    FROM orders
);
```

**Result:**

```sql
+----------------+------------------+
| name           | email            |
+----------------+------------------+
| John Smith     | john@email.com   |
| Jane Doe       | jane@email.com   |
| Bob Johnson    | bob@email.com    |
| Charlie Wilson | charlie@email.com|
+----------------+------------------+
```

### Using NOT IN

```sql
-- Find customers who haven't placed any orders
SELECT name, email
FROM customers
WHERE customer_id NOT IN (
    SELECT customer_id
    FROM orders
    WHERE customer_id IS NOT NULL  -- Important: handle NULLs
);
```

> [!warning] NULL Trap with NOT IN If the subquery returns any NULL values, NOT IN will return no results! Always filter out NULLs or use NOT EXISTS instead.

### Safe NOT IN Alternative

```sql
-- Safer approach using NOT EXISTS
SELECT name, email
FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
);
```

### Using ANY/SOME

```sql
-- Find products cheaper than ANY electronics item
SELECT product_name, price
FROM products
WHERE price < ANY (
    SELECT price
    FROM products
    WHERE category_id = 1  -- Electronics
);
```

**Result:** Products cheaper than the most expensive electronics item.

### Using ALL

```sql
-- Find products more expensive than ALL furniture items
SELECT product_name, price
FROM products
WHERE price > ALL (
    SELECT price
    FROM products
    WHERE category_id = 2  -- Furniture
);
```

**Result:** Products more expensive than the most expensive furniture item.

> [!note] ANY vs ALL
> 
> - **ANY**: True if condition is true for at least one value
> - **ALL**: True if condition is true for every value
> - `> ANY` means "greater than the minimum"
> - `> ALL` means "greater than the maximum"

## 3. EXISTS and NOT EXISTS

**EXISTS** checks if a subquery returns any rows. It's often more efficient than IN for large datasets because it stops as soon as it finds one matching row.

### Basic EXISTS

```sql
-- Find customers who have placed orders (using EXISTS)
SELECT name, email
FROM customers c
WHERE EXISTS (
    SELECT 1  -- The actual value doesn't matter
    FROM orders o
    WHERE o.customer_id = c.customer_id
);
```

### NOT EXISTS

```sql
-- Find customers who haven't placed orders
SELECT name, email
FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
);
```

### Complex EXISTS Conditions

```sql
-- Find customers who have placed orders over $200
SELECT c.name, c.email
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
    AND o.amount > 200
);
```

### EXISTS vs IN Performance

```sql
-- EXISTS: Generally faster for large datasets
SELECT name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

-- IN: Can be faster for small datasets
SELECT name FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders);
```

> [!tip] When to Use EXISTS vs IN
> 
> - **EXISTS**: Better for large outer tables, checking existence only
> - **IN**: Better when you need to return specific values, small datasets
> - **EXISTS**: Handles NULLs better than NOT IN

## 4. Correlated Subqueries

**Correlated subqueries** reference columns from the outer query. They execute once for each row of the outer query, making them potentially slower but very powerful.

### Basic Correlated Subquery

```sql
-- Find each customer's most recent order
SELECT c.name,
       o.order_id,
       o.amount,
       o.order_date
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date = (
    SELECT MAX(order_date)  -- Correlated: references c.customer_id
    FROM orders
    WHERE customer_id = c.customer_id
);
```

### Finding Top N Records per Group

```sql
-- Find the top 2 highest orders for each customer
SELECT c.name, o.order_id, o.amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE (
    SELECT COUNT(*)
    FROM orders o2
    WHERE o2.customer_id = c.customer_id
    AND o2.amount > o.amount
) < 2  -- Less than 2 orders with higher amounts
ORDER BY c.customer_id, o.amount DESC;
```

### Correlated EXISTS

```sql
-- Find customers whose average order amount is above overall average
SELECT c.name
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
    HAVING AVG(o.amount) > (
        SELECT AVG(amount) FROM orders
    )
);
```

### Update with Correlated Subqueries

```sql
-- Update customer records with their total order amount
UPDATE customers
SET total_spent = (
    SELECT COALESCE(SUM(amount), 0)
    FROM orders
    WHERE orders.customer_id = customers.customer_id
);
```

> [!warning] Performance Consideration Correlated subqueries can be slow on large datasets because they execute for each outer row. Consider using window functions or JOINs for better performance when possible.

## 5. Subqueries in FROM Clause (Derived Tables)

Subqueries in the FROM clause create temporary result sets (derived tables) that can be queried like regular tables.

### Basic Derived Table

```sql
-- Calculate customer order statistics
SELECT avg_stats.customer_id,
       avg_stats.avg_amount,
       avg_stats.order_count
FROM (
    SELECT customer_id,
           AVG(amount) as avg_amount,
           COUNT(*) as order_count
    FROM orders
    GROUP BY customer_id
) as avg_stats
WHERE avg_stats.order_count > 1;
```

### Complex Derived Tables

```sql
-- Find customers with above-average order frequency
SELECT c.name, stats.order_count, stats.avg_amount
FROM customers c
JOIN (
    SELECT customer_id,
           COUNT(*) as order_count,
           AVG(amount) as avg_amount
    FROM orders
    WHERE order_date >= '2024-01-01'
    GROUP BY customer_id
) as stats ON c.customer_id = stats.customer_id
WHERE stats.order_count > (
    SELECT AVG(order_count)
    FROM (
        SELECT COUNT(*) as order_count
        FROM orders
        WHERE order_date >= '2024-01-01'
        GROUP BY customer_id
    ) as avg_calc
);
```

### Derived Tables with Rankings

```sql
-- Rank customers by total spending
SELECT ranked_customers.name,
       ranked_customers.total_spent,
       ranked_customers.spending_rank
FROM (
    SELECT c.name,
           SUM(o.amount) as total_spent,
           RANK() OVER (ORDER BY SUM(o.amount) DESC) as spending_rank
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
) as ranked_customers
WHERE ranked_customers.spending_rank <= 3;
```

> [!tip] Derived Table Best Practices
> 
> - Always alias derived tables (AS alias_name)
> - Use meaningful alias names
> - Consider creating views for frequently used derived tables
> - For complex logic, window functions might be more readable

## Advanced Subquery Patterns

### 1. Multiple Column Subqueries

```sql
-- Find orders that match both the maximum amount and most recent date for each customer
SELECT o.*
FROM orders o
WHERE (o.customer_id, o.amount, o.order_date) IN (
    SELECT customer_id, MAX(amount), MAX(order_date)
    FROM orders
    GROUP BY customer_id
);
```

### 2. Subqueries with CASE Statements

```sql
-- Categorize customers based on their ordering behavior
SELECT name,
       CASE
           WHEN customer_id IN (
               SELECT customer_id
               FROM orders
               GROUP BY customer_id
               HAVING COUNT(*) > 2
           ) THEN 'Frequent'
           WHEN customer_id IN (
               SELECT customer_id
               FROM orders
               GROUP BY customer_id
               HAVING AVG(amount) > 300
           ) THEN 'High Value'
           ELSE 'Regular'
       END as customer_type
FROM customers;
```

### 3. Nested Subqueries

```sql
-- Find customers in cities where the average customer order value is above global average
SELECT name, city
FROM customers
WHERE city IN (
    SELECT city
    FROM customers c
    WHERE c.customer_id IN (
        SELECT customer_id
        FROM orders
        GROUP BY customer_id
        HAVING AVG(amount) > (
            SELECT AVG(amount) FROM orders
        )
    )
    GROUP BY city
    HAVING COUNT(DISTINCT c.customer_id) > 0
);
```

### 4. Subqueries with Aggregation

```sql
-- Monthly order summary with comparisons to overall averages
SELECT order_month,
       monthly_orders,
       monthly_revenue,
       CASE
           WHEN monthly_orders > (SELECT AVG(monthly_orders) FROM monthly_stats) 
           THEN 'Above Average'
           ELSE 'Below Average'
       END as order_volume_status
FROM (
    SELECT DATE_FORMAT(order_date, '%Y-%m') as order_month,
           COUNT(*) as monthly_orders,
           SUM(amount) as monthly_revenue
    FROM orders
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
) as monthly_data
CROSS JOIN (
    SELECT AVG(monthly_orders) as avg_orders
    FROM (
        SELECT COUNT(*) as monthly_orders
        FROM orders
        GROUP BY DATE_FORMAT(order_date, '%Y-%m')
    ) as monthly_stats
) as averages;
```

## Common Subquery Use Cases

### 1. Data Cleaning and Validation

```sql
-- Find duplicate email addresses
SELECT email, COUNT(*) as duplicate_count
FROM customers
WHERE email IN (
    SELECT email
    FROM customers
    GROUP BY email
    HAVING COUNT(*) > 1
)
GROUP BY email;

-- Find orders without valid customers (orphaned records)
SELECT *
FROM orders
WHERE customer_id NOT IN (
    SELECT customer_id
    FROM customers
    WHERE customer_id IS NOT NULL
);
```

### 2. Business Intelligence Queries

```sql
-- Customer lifetime value analysis
SELECT c.name,
       c.registration_date,
       customer_stats.total_spent,
       customer_stats.order_count,
       customer_stats.avg_order_value,
       CASE
           WHEN customer_stats.total_spent > (
               SELECT AVG(total_spent) * 1.5
               FROM (
                   SELECT SUM(amount) as total_spent
                   FROM orders
                   GROUP BY customer_id
               ) as all_customers
           ) THEN 'VIP'
           WHEN customer_stats.total_spent > (
               SELECT AVG(total_spent)
               FROM (
                   SELECT SUM(amount) as total_spent
                   FROM orders
                   GROUP BY customer_id
               ) as all_customers
           ) THEN 'Premium'
           ELSE 'Standard'
       END as customer_tier
FROM customers c
LEFT JOIN (
    SELECT customer_id,
           SUM(amount) as total_spent,
           COUNT(*) as order_count,
           AVG(amount) as avg_order_value
    FROM orders
    GROUP BY customer_id
) as customer_stats ON c.customer_id = customer_stats.customer_id;
```

### 3. Cohort Analysis

```sql
-- Monthly customer cohorts
SELECT cohort_month,
       users_count,
       (users_count * 100.0 / total_users) as percentage_of_total
FROM (
    SELECT DATE_FORMAT(registration_date, '%Y-%m') as cohort_month,
           COUNT(*) as users_count
    FROM customers
    GROUP BY DATE_FORMAT(registration_date, '%Y-%m')
) as monthly_cohorts
CROSS JOIN (
    SELECT COUNT(*) as total_users FROM customers
) as totals
ORDER BY cohort_month;
```

## Performance Optimization

### 1. Subquery vs JOIN Performance

```sql
-- Subquery approach
SELECT name
FROM customers
WHERE customer_id IN (
    SELECT customer_id FROM orders WHERE amount > 200
);

-- JOIN approach (often faster)
SELECT DISTINCT c.name
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.amount > 200;
```

### 2. EXISTS vs IN Optimization

```sql
-- Slower with large datasets
SELECT name FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders);

-- Faster with large datasets
SELECT name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```

### 3. Avoid Correlated Subqueries When Possible

```sql
-- Slower: Correlated subquery
SELECT c.name,
       (SELECT MAX(amount) FROM orders WHERE customer_id = c.customer_id) as max_order
FROM customers c;

-- Faster: JOIN with aggregation
SELECT c.name, o.max_order
FROM customers c
LEFT JOIN (
    SELECT customer_id, MAX(amount) as max_order
    FROM orders
    GROUP BY customer_id
) o ON c.customer_id = o.customer_id;
```

### 4. Use Indexes Strategically

```sql
-- Ensure indexes exist on columns used in subqueries
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_amount ON orders(amount);
CREATE INDEX idx_orders_date_amount ON orders(order_date, amount);
```

> [!tip] Performance Guidelines
> 
> 1. **Profile your queries** - Use EXPLAIN to understand execution plans
> 2. **Consider alternatives** - JOINs, window functions, or CTEs might be faster
> 3. **Index subquery columns** - Especially for correlated subqueries
> 4. **Limit subquery results** - Use TOP/LIMIT when you only need a subset
> 5. **Test with realistic data** - Performance characteristics change with data size

## Troubleshooting Subqueries

### Common Issues and Solutions

#### 1. Subquery Returns Too Many Rows

**Error**: "Subquery returns more than 1 row" **Problem**: Using a subquery that returns multiple values where only one is expected

```sql
-- Problem: This might return multiple values
SELECT name
FROM customers
WHERE customer_id = (
    SELECT customer_id FROM orders  -- Could return multiple rows
);

-- Solution: Use IN or add LIMIT/aggregation
SELECT name
FROM customers
WHERE customer_id IN (
    SELECT customer_id FROM orders
);

-- Or use aggregation
SELECT name
FROM customers
WHERE customer_id = (
    SELECT customer_id FROM orders ORDER BY order_date DESC LIMIT 1
);
```

#### 2. NULL Handling Issues

```sql
-- Problem: NOT IN with NULLs returns no results
SELECT name FROM customers
WHERE customer_id NOT IN (
    SELECT customer_id FROM orders  -- If any value is NULL, result is empty
);

-- Solution: Filter out NULLs or use NOT EXISTS
SELECT name FROM customers
WHERE customer_id NOT IN (
    SELECT customer_id FROM orders WHERE customer_id IS NOT NULL
);

-- Better solution: Use NOT EXISTS
SELECT name FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);
```

#### 3. Performance Issues with Correlated Subqueries

```sql
-- Slow: Correlated subquery executes for each row
SELECT c.name,
       (SELECT COUNT(*) FROM orders WHERE customer_id = c.customer_id) as order_count
FROM customers c;

-- Faster: Use JOIN
SELECT c.name, COALESCE(o.order_count, 0) as order_count
FROM customers c
LEFT JOIN (
    SELECT customer_id, COUNT(*) as order_count
    FROM orders
    GROUP BY customer_id
) o ON c.customer_id = o.customer_id;
```

## Alternative Approaches

### 1. Common Table Expressions (CTEs)

```sql
-- Instead of complex nested subqueries, use CTEs
WITH customer_stats AS (
    SELECT customer_id,
           COUNT(*) as order_count,
           SUM(amount) as total_spent,
           AVG(amount) as avg_order
    FROM orders
    GROUP BY customer_id
),
high_value_customers AS (
    SELECT customer_id
    FROM customer_stats
    WHERE total_spent > (SELECT AVG(total_spent) FROM customer_stats)
)
SELECT c.name, cs.total_spent, cs.order_count
FROM customers c
JOIN customer_stats cs ON c.customer_id = cs.customer_id
WHERE c.customer_id IN (SELECT customer_id FROM high_value_customers);
```

### 2. Window Functions

```sql
-- Instead of correlated subqueries for rankings
-- Subquery approach (slower)
SELECT name, total_spent
FROM (
    SELECT c.name,
           SUM(o.amount) as total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
) customer_totals
WHERE total_spent = (
    SELECT MAX(total_spent)
    FROM (
        SELECT SUM(amount) as total_spent
        FROM orders
        GROUP BY customer_id
    ) all_totals
);

-- Window function approach (faster)
SELECT name, total_spent
FROM (
    SELECT c.name,
           SUM(o.amount) as total_spent,
           RANK() OVER (ORDER BY SUM(o.amount) DESC) as rank
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
) ranked_customers
WHERE rank = 1;
```

## Practice Exercises

### Exercise 1: Basic Subqueries

```sql
-- 1. Find customers who have spent more than the average order amount
SELECT name
FROM customers
WHERE customer_id IN (
    SELECT customer_id
    FROM orders
    WHERE amount > (SELECT AVG(amount) FROM orders)
);

-- 2. Find the most expensive product in each category
SELECT product_name, price, category_id
FROM products p1
WHERE price = (
    SELECT MAX(price)
    FROM products p2
    WHERE p2.category_id = p1.category_id
);

-- 3. Find customers who haven't placed any orders
SELECT name, email
FROM customers
WHERE customer_id NOT IN (
    SELECT customer_id
    FROM orders
    WHERE customer_id IS NOT NULL
);
```

### Exercise 2: EXISTS and Correlated Subqueries

```sql
-- 4. Find customers who have placed orders in the last 30 days
SELECT name
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
    AND o.order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
);

-- 5. Find customers whose most recent order was over $250
SELECT c.name, c.email
FROM customers c
WHERE 250 < (
    SELECT amount
    FROM orders o
    WHERE o.customer_id = c.customer_id
    ORDER BY o.order_date DESC
    LIMIT 1
);
```

### Exercise 3: Advanced Patterns

```sql
-- 6. Find the second highest order amount for each customer
SELECT c.name, o.amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE 1 = (
    SELECT COUNT(DISTINCT amount)
    FROM orders o2
    WHERE o2.customer_id = c.customer_id
    AND o2.amount > o.amount
);

-- 7. Create a customer segmentation based on order behavior
SELECT name,
       CASE
           WHEN customer_id IN (
               SELECT customer_id
               FROM orders
               GROUP BY customer_id
               HAVING COUNT(*) >= 3 AND AVG(amount) > 250
           ) THEN 'VIP'
           WHEN customer_id IN (
               SELECT customer_id
               FROM orders
               GROUP BY customer_id
               HAVING COUNT(*) >= 2
           ) THEN 'Regular'
           ELSE 'New'
       END as segment
FROM customers;
```

> [!question] Challenge Exercise Write a query to find customers who have ordered every product in the Electronics category. This requires understanding of relational division - a classic SQL problem!

## Real-World Applications

### 1. E-commerce Analytics

```sql
-- Product recommendation: Find products frequently bought together
SELECT p1.product_name, p2.product_name, COUNT(*) as frequency
FROM order_items oi1
JOIN order_items oi2 ON oi1.order_id = oi2.order_id AND oi1.product_id < oi2.product_id
JOIN products p1 ON oi1.product_id = p1.product_id
JOIN products p2 ON oi2.product_id = p2.product_id
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.order_id = oi1.order_id
    AND o.order_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
)
GROUP BY p1.product_id, p2.product_id, p1.product_name, p2.product_name
HAVING COUNT(*) >= 3
ORDER BY frequency DESC;
```

### 2. Financial Analysis

```sql
-- Customer credit worthiness based on payment history
SELECT c.customer_id,
       c.name,
       payment_score.score,
       payment_score.risk_category
FROM customers c
JOIN (
    SELECT customer_id,
           CASE
               WHEN AVG(CASE WHEN payment_date <= due_date THEN 100 ELSE 50 END) >= 90 THEN 'Low Risk'
               WHEN AVG(CASE WHEN payment_date <= due_date THEN 100 ELSE 50 END) >= 70 THEN 'Medium Risk'
               ELSE 'High Risk'
           END as risk_category,
           AVG(CASE WHEN payment_date <= due_date THEN 100 ELSE 50 END) as score
    FROM payments
    WHERE payment_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
    GROUP BY customer_id
) payment_score ON c.customer_id = payment_score.customer_id;
```

### 3. Inventory Management

```sql
-- Products that need restocking based on sales velocity
SELECT p.product_name,
       p.stock_quantity,
       sales_data.monthly_sales,
       CEIL(sales_data.monthly_sales * 2) as recommended_stock
FROM products p
JOIN (
    SELECT oi.product_id,
           AVG(monthly_quantity) as monthly_sales
    FROM (
        SELECT product_id,
               DATE_FORMAT(o.order_date, '%Y-%m') as month,
               SUM(quantity) as monthly_quantity
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        GROUP BY product_id, DATE_FORMAT(o.order_date, '%Y-%m')
    ) monthly_data
    GROUP BY product_id
) sales_data ON p.product_id = sales_data.product_id
WHERE p.stock_quantity < (sales_data.monthly_sales * 2);
```

## Related Topics

- [[SQL Joins]] - Combining tables for complex queries
- [[SQL Window Functions]] - Advanced analytical functions
- [[Common Table Expressions (CTEs)]] - Readable complex queries
- [[SQL Performance Optimization]] - Query tuning techniques
- [[Database Design]] - Schema optimization for subqueries
- [[Advanced SQL]] - Complex query patterns
- [[Data Analysis with SQL]] - Analytical techniques
- [[SQL Indexes]] - Performance improvement strategies

## Summary

### Key Subquery Types Mastered

- **Scalar Subqueries**: Return single values for comparisons
- **Column Subqueries**: Return lists for IN, ANY, ALL operations
- **Correlated Subqueries**: Reference outer query columns
- **Derived Tables**: Subqueries in FROM clause creating temporary tables
- **EXISTS/NOT EXISTS**: Efficient existence checking

### Essential Concepts

- **Execution Order**: Inner queries execute first (except correlated)
- **Data Types**: Subquery results must match expected data types
- **NULL Handling**: Special consideration for NOT IN operations
- **Performance**: Choose between subqueries, JOINs, and window functions
- **Nesting Levels**: Balance readability vs. functionality

### Best Practices Learned

✅ **Use EXISTS** instead of IN for better NULL handling  
✅ **Filter NULLs** when using NOT IN operations  
✅ **Consider JOINs** for better performance with large datasets  
✅ **Use meaningful aliases** for derived tables  
✅ **Profile complex queries** to understand performance  
✅ **Break down complex logic** into readable steps

### Common Use Cases

- Dynamic filtering based on calculations
- Finding records without relationships (orphaned data)
- Top N queries and rankings
- Data validation and quality checks
- Business intelligence and reporting
- Customer segmentation and analysis

### Performance Guidelines

- **Correlated subqueries**: Can be slow on large datasets
- **EXISTS vs IN**: EXISTS often performs better for existence checks
- **Subqueries vs JOINs**: JOINs usually faster for retrieving data
- **Indexing**: Critical for subquery performance, especially on join columns
- **Alternatives**: Consider CTEs and window functions for complex logic

### Troubleshooting Checklist

- ✅ **Check for NULL values** in NOT IN operations
- ✅ **Verify single value** returns for scalar subqueries
- ✅ **Use EXPLAIN** to analyze query execution plans
- ✅ **Test with realistic data sizes** for performance validation
- ✅ **Consider query alternatives** when performance is poor

### What You Can Do Now

- ✅ Write complex filtering queries using subqueries
- ✅ Use EXISTS for efficient existence checking
- ✅ Create derived tables for multi-step analysis
- ✅ Handle correlated subqueries for row-by-row operations
- ✅ Choose appropriate subquery types for different scenarios
- ✅ Optimize subquery performance through proper indexing
- ✅ Troubleshoot common subquery issues

### Next Learning Goals

- [ ] Master [[Common Table Expressions (CTEs)]] for complex hierarchical queries
- [ ] Learn [[SQL Window Functions]] for advanced analytics
- [ ] Explore [[SQL Performance Tuning]] for query optimization
- [ ] Practice with [[Advanced SQL Patterns]] and real-world scenarios
- [ ] Study [[Database Query Optimization]] principles

### Advanced Topics to Explore

- **Recursive CTEs**: For hierarchical data processing
- **Window Functions**: Modern alternative to many correlated subqueries
- **Query Optimization**: Understanding execution plans and indexes
- **Stored Procedures**: Encapsulating complex subquery logic
- **Views**: Creating reusable complex queries

> [!tip] Mastery Through Practice Subqueries are powerful but can be complex. Start with simple scalar subqueries and gradually work up to correlated and nested patterns. Practice converting between subqueries, JOINs, and window functions to understand when each approach works best.

> [!note] Modern SQL Alternatives While subqueries are essential to understand, modern SQL offers alternatives like CTEs and window functions that can be more readable and performant for many use cases. Learn subqueries as a foundation, then explore these modern approaches.

---

_Tags: #SQL #Subqueries #AdvancedSQL #Database #DataAnalysis #NestedQueries #EXISTS #CorrelatedSubqueries #Performance #QueryOptimization_