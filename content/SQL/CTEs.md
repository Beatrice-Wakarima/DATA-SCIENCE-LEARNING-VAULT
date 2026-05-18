# SQL CTEs (Common Table Expressions) - Complete Guide

_Master readable, modular query design with Common Table Expressions for complex data analysis_

## What are Common Table Expressions (CTEs)?

**Common Table Expressions (CTEs)** are temporary named result sets that exist only for the duration of a single SQL statement. They provide a way to write more readable, maintainable, and modular queries by breaking complex logic into manageable, named components.

> [!note] Think of CTEs as... CTEs are like creating temporary "worksheets" in Excel that you can reference in your main calculation. They make complex queries readable by giving meaningful names to intermediate results.

### Key Benefits of CTEs

- **Readability**: Break complex queries into logical, named steps
- **Reusability**: Reference the same CTE multiple times in one query
- **Modularity**: Separate complex logic into manageable components
- **Recursion**: Enable hierarchical and tree-structure queries
- **Debugging**: Easier to test and troubleshoot individual components

### CTE vs Alternatives

|Approach|Readability|Reusability|Performance|Use Case|
|---|---|---|---|---|
|**CTE**|Excellent|High|Good|Complex multi-step logic|
|**Subquery**|Poor|None|Variable|Simple filtering|
|**Temp Table**|Good|High|Excellent|Large intermediate results|
|**View**|Excellent|Very High|Good|Reusable across queries|

## Basic CTE Syntax

### Simple CTE Structure

```sql
WITH cte_name AS (
    SELECT column1, column2, ...
    FROM table_name
    WHERE condition
)
SELECT *
FROM cte_name
WHERE another_condition;
```

### Multiple CTEs

```sql
WITH first_cte AS (
    SELECT ...
    FROM table1
),
second_cte AS (
    SELECT ...
    FROM table2
),
third_cte AS (
    SELECT ...
    FROM first_cte
    JOIN second_cte ON ...
)
SELECT *
FROM third_cte;
```

## Sample Data for Examples

We'll use these tables throughout the guide:

### EMPLOYEES Table

```sql
+--------+----------+--------+------------+----------+
| emp_id | name     | salary | department | manager_id|
+--------+----------+--------+------------+----------+
| 1      | Alice    | 75000  | Sales      | NULL     |
| 2      | Bob      | 80000  | Sales      | 1        |
| 3      | Carol    | 72000  | Sales      | 1        |
| 4      | David    | 90000  | Marketing  | NULL     |
| 5      | Eve      | 85000  | Marketing  | 4        |
| 6      | Frank    | 95000  | Engineering| NULL     |
| 7      | Grace    | 88000  | Engineering| 6        |
| 8      | Henry    | 92000  | Engineering| 6        |
+--------+----------+--------+------------+----------+
```

### ORDERS Table

```sql
+----------+-------------+--------+------------+--------+
| order_id | customer_id | amount | order_date | status |
+----------+-------------+--------+------------+--------+
| 1001     | 101         | 250.00 | 2024-01-15 | completed |
| 1002     | 102         | 175.50 | 2024-01-16 | completed |
| 1003     | 101         | 300.00 | 2024-01-18 | pending   |
| 1004     | 103         | 425.75 | 2024-01-20 | completed |
| 1005     | 102         | 150.00 | 2024-01-22 | cancelled |
| 1006     | 104         | 275.25 | 2024-01-25 | completed |
+----------+-------------+--------+------------+--------+
```

### CUSTOMERS Table

```sql
+-------------+--------------+------------------+----------+------------+
| customer_id | name         | email            | city     | signup_date|
+-------------+--------------+------------------+----------+------------+
| 101         | John Smith   | john@email.com   | New York | 2023-06-15 |
| 102         | Jane Doe     | jane@email.com   | Los Angeles| 2023-08-20 |
| 103         | Bob Johnson  | bob@email.com    | Chicago  | 2023-09-10 |
| 104         | Alice Brown  | alice@email.com  | Miami    | 2023-11-05 |
+-------------+--------------+------------------+----------+------------+
```

## Basic CTE Examples

### 1. Simple Data Preparation

```sql
-- Without CTE (harder to read)
SELECT c.name, c.city, order_summary.total_orders, order_summary.total_amount
FROM customers c
JOIN (
    SELECT customer_id, 
           COUNT(*) as total_orders, 
           SUM(amount) as total_amount
    FROM orders 
    WHERE status = 'completed'
    GROUP BY customer_id
) order_summary ON c.customer_id = order_summary.customer_id
WHERE order_summary.total_amount > 300;

-- With CTE (much clearer)
WITH completed_orders AS (
    SELECT customer_id,
           COUNT(*) as total_orders,
           SUM(amount) as total_amount
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
)
SELECT c.name, 
       c.city,
       co.total_orders,
       co.total_amount
FROM customers c
JOIN completed_orders co ON c.customer_id = co.customer_id
WHERE co.total_amount > 300;
```

### 2. Multi-Step Calculations

```sql
-- Calculate customer lifetime value with multiple steps
WITH customer_metrics AS (
    -- Step 1: Basic customer metrics
    SELECT customer_id,
           COUNT(*) as order_count,
           SUM(amount) as total_spent,
           AVG(amount) as avg_order_value,
           MIN(order_date) as first_order,
           MAX(order_date) as last_order
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
),
customer_segments AS (
    -- Step 2: Add customer segmentation
    SELECT *,
           DATEDIFF(last_order, first_order) as customer_lifespan_days,
           CASE 
               WHEN total_spent > 500 THEN 'High Value'
               WHEN total_spent > 200 THEN 'Medium Value'
               ELSE 'Low Value'
           END as value_segment,
           CASE 
               WHEN order_count >= 3 THEN 'Frequent'
               WHEN order_count = 2 THEN 'Occasional'
               ELSE 'One-time'
           END as frequency_segment
    FROM customer_metrics
),
final_analysis AS (
    -- Step 3: Calculate additional metrics
    SELECT *,
           CASE 
               WHEN customer_lifespan_days > 0 
               THEN total_spent / (customer_lifespan_days / 30.0)
               ELSE total_spent
           END as monthly_value,
           value_segment || ' - ' || frequency_segment as customer_type
    FROM customer_segments
)
SELECT c.name,
       c.city,
       fa.total_spent,
       fa.order_count,
       fa.customer_type,
       ROUND(fa.monthly_value, 2) as estimated_monthly_value
FROM final_analysis fa
JOIN customers c ON fa.customer_id = c.customer_id
ORDER BY fa.total_spent DESC;
```

### 3. Data Quality Analysis

```sql
-- Comprehensive data quality check using CTEs
WITH missing_data AS (
    SELECT 'customers' as table_name,
           COUNT(*) as total_records,
           COUNT(CASE WHEN name IS NULL THEN 1 END) as missing_names,
           COUNT(CASE WHEN email IS NULL THEN 1 END) as missing_emails,
           COUNT(CASE WHEN city IS NULL THEN 1 END) as missing_cities
    FROM customers
    
    UNION ALL
    
    SELECT 'orders' as table_name,
           COUNT(*) as total_records,
           COUNT(CASE WHEN customer_id IS NULL THEN 1 END) as missing_customers,
           COUNT(CASE WHEN amount IS NULL THEN 1 END) as missing_amounts,
           COUNT(CASE WHEN order_date IS NULL THEN 1 END) as missing_dates
    FROM orders
),
orphaned_records AS (
    SELECT 'orphaned_orders' as issue_type,
           COUNT(*) as issue_count
    FROM orders o
    LEFT JOIN customers c ON o.customer_id = c.customer_id
    WHERE c.customer_id IS NULL
),
duplicate_analysis AS (
    SELECT 'duplicate_emails' as issue_type,
           COUNT(*) - COUNT(DISTINCT email) as issue_count
    FROM customers
    WHERE email IS NOT NULL
)
-- Combine all data quality issues
SELECT * FROM missing_data
UNION ALL
SELECT issue_type, issue_count, 0, 0, 0 FROM orphaned_records
UNION ALL
SELECT issue_type, issue_count, 0, 0, 0 FROM duplicate_analysis;
```

> [!tip] CTE Naming Convention Use descriptive names that indicate what the CTE contains: `completed_orders`, `customer_metrics`, `high_value_segments`. This makes your queries self-documenting.

## Advanced CTE Patterns

### 1. CTE with Window Functions

```sql
-- Combine CTEs with window functions for advanced analytics
WITH monthly_sales AS (
    SELECT customer_id,
           DATE_FORMAT(order_date, '%Y-%m') as month,
           SUM(amount) as monthly_total
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id, DATE_FORMAT(order_date, '%Y-%m')
),
sales_with_trends AS (
    SELECT *,
           LAG(monthly_total) OVER (
               PARTITION BY customer_id 
               ORDER BY month
           ) as previous_month,
           ROW_NUMBER() OVER (
               PARTITION BY customer_id 
               ORDER BY monthly_total DESC
           ) as best_month_rank,
           AVG(monthly_total) OVER (
               PARTITION BY customer_id
           ) as avg_monthly_spend
    FROM monthly_sales
),
customer_insights AS (
    SELECT customer_id,
           COUNT(*) as active_months,
           SUM(monthly_total) as total_spent,
           MAX(CASE WHEN best_month_rank = 1 THEN monthly_total END) as best_month_sales,
           AVG(monthly_total) as avg_monthly,
           COUNT(CASE WHEN monthly_total > avg_monthly_spend THEN 1 END) as above_avg_months
    FROM sales_with_trends
    GROUP BY customer_id
)
SELECT c.name,
       ci.active_months,
       ci.total_spent,
       ci.best_month_sales,
       ROUND(ci.avg_monthly, 2) as avg_monthly_spend,
       ROUND(ci.above_avg_months * 100.0 / ci.active_months, 1) as consistency_pct
FROM customer_insights ci
JOIN customers c ON ci.customer_id = c.customer_id
ORDER BY ci.total_spent DESC;
```

### 2. CTEs for Complex Joins

```sql
-- Multi-dimensional analysis using multiple CTEs
WITH product_performance AS (
    SELECT p.product_id,
           p.product_name,
           p.category,
           COUNT(oi.order_id) as times_ordered,
           SUM(oi.quantity) as total_quantity,
           SUM(oi.quantity * p.price) as total_revenue
    FROM products p
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    LEFT JOIN orders o ON oi.order_id = o.order_id AND o.status = 'completed'
    GROUP BY p.product_id, p.product_name, p.category
),
category_metrics AS (
    SELECT category,
           COUNT(*) as products_in_category,
           SUM(total_revenue) as category_revenue,
           AVG(total_revenue) as avg_product_revenue
    FROM product_performance
    GROUP BY category
),
product_rankings AS (
    SELECT pp.*,
           cm.category_revenue,
           cm.avg_product_revenue,
           RANK() OVER (PARTITION BY pp.category ORDER BY pp.total_revenue DESC) as category_rank,
           ROUND(pp.total_revenue * 100.0 / cm.category_revenue, 2) as pct_of_category_revenue
    FROM product_performance pp
    JOIN category_metrics cm ON pp.category = cm.category
)
SELECT product_name,
       category,
       total_revenue,
       category_rank,
       pct_of_category_revenue,
       CASE 
           WHEN category_rank <= 3 THEN 'Top Performer'
           WHEN pct_of_category_revenue > 10 THEN 'Strong Contributor'
           ELSE 'Standard Product'
       END as performance_tier
FROM product_rankings
WHERE total_revenue > 0
ORDER BY category, category_rank;
```

### 3. Conditional CTEs

```sql
-- Dynamic analysis based on conditions
WITH analysis_params AS (
    SELECT 'Q1' as analysis_period,
           '2024-01-01' as start_date,
           '2024-03-31' as end_date,
           500 as high_value_threshold
),
filtered_orders AS (
    SELECT o.*
    FROM orders o
    CROSS JOIN analysis_params ap
    WHERE o.order_date BETWEEN ap.start_date AND ap.end_date
    AND o.status = 'completed'
),
customer_analysis AS (
    SELECT fo.customer_id,
           COUNT(*) as order_count,
           SUM(fo.amount) as total_spent,
           ap.high_value_threshold,
           CASE 
               WHEN SUM(fo.amount) >= ap.high_value_threshold THEN 'High Value'
               ELSE 'Standard'
           END as customer_tier
    FROM filtered_orders fo
    CROSS JOIN analysis_params ap
    GROUP BY fo.customer_id, ap.high_value_threshold
)
SELECT ap.analysis_period,
       ca.customer_tier,
       COUNT(*) as customer_count,
       SUM(ca.total_spent) as tier_revenue,
       ROUND(AVG(ca.total_spent), 2) as avg_customer_value
FROM customer_analysis ca
CROSS JOIN analysis_params ap
GROUP BY ap.analysis_period, ca.customer_tier
ORDER BY ca.customer_tier;
```

## Recursive CTEs

**Recursive CTEs** are a special type that can reference themselves, enabling queries over hierarchical data structures like organizational charts, family trees, or nested categories.

### Basic Recursive Structure

```sql
WITH RECURSIVE recursive_cte_name AS (
    -- Base case (anchor member)
    SELECT initial_columns
    FROM initial_table
    WHERE base_condition
    
    UNION ALL
    
    -- Recursive case (recursive member)
    SELECT recursive_columns
    FROM recursive_cte_name
    JOIN some_table ON join_condition
    WHERE recursive_condition
)
SELECT * FROM recursive_cte_name;
```

### 1. Organizational Hierarchy

```sql
-- Find all employees in a management chain
WITH RECURSIVE employee_hierarchy AS (
    -- Base case: Start with a specific manager
    SELECT emp_id,
           name,
           manager_id,
           salary,
           department,
           0 as level,
           name as hierarchy_path
    FROM employees
    WHERE manager_id IS NULL  -- Top-level managers
    
    UNION ALL
    
    -- Recursive case: Find direct reports
    SELECT e.emp_id,
           e.name,
           e.manager_id,
           e.salary,
           e.department,
           eh.level + 1,
           CONCAT(eh.hierarchy_path, ' -> ', e.name) as hierarchy_path
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.emp_id
    WHERE eh.level < 10  -- Prevent infinite recursion
)
SELECT level,
       REPEAT('  ', level) || name as indented_name,
       salary,
       department,
       hierarchy_path
FROM employee_hierarchy
ORDER BY hierarchy_path;
```

**Result:**

```sql
+-------+-----------------+--------+------------+------------------+
| level | indented_name   | salary | department | hierarchy_path   |
+-------+-----------------+--------+------------+------------------+
| 0     | Alice           | 75000  | Sales      | Alice            |
| 1     |   Bob           | 80000  | Sales      | Alice -> Bob     |
| 1     |   Carol         | 72000  | Sales      | Alice -> Carol   |
| 0     | David           | 90000  | Marketing  | David            |
| 1     |   Eve           | 85000  | Marketing  | David -> Eve     |
| 0     | Frank           | 95000  | Engineering| Frank            |
| 1     |   Grace         | 88000  | Engineering| Frank -> Grace   |
| 1     |   Henry         | 92000  | Engineering| Frank -> Henry   |
+-------+-----------------+--------+------------+------------------+
```

### 2. Finding All Subordinates

```sql
-- Find all employees who report to a specific manager (directly or indirectly)
WITH RECURSIVE subordinates AS (
    -- Base case: Start with the manager
    SELECT emp_id,
           name,
           salary,
           department,
           0 as depth
    FROM employees
    WHERE emp_id = 1  -- Alice's ID
    
    UNION ALL
    
    -- Recursive case: Find all subordinates at any level
    SELECT e.emp_id,
           e.name,
           e.salary,
           e.department,
           s.depth + 1
    FROM employees e
    JOIN subordinates s ON e.manager_id = s.emp_id
)
SELECT name,
       salary,
       department,
       depth,
       CASE depth
           WHEN 0 THEN 'Manager'
           WHEN 1 THEN 'Direct Report'
           ELSE CONCAT('Level ', depth, ' Report')
       END as relationship
FROM subordinates
ORDER BY depth, name;
```

### 3. Calculating Hierarchy Aggregates

```sql
-- Calculate total salary cost for each manager including all subordinates
WITH RECURSIVE manager_totals AS (
    -- Base case: Leaf employees (no subordinates)
    SELECT emp_id,
           name,
           salary,
           salary as total_salary_cost,
           1 as total_employees
    FROM employees e1
    WHERE NOT EXISTS (
        SELECT 1 FROM employees e2 WHERE e2.manager_id = e1.emp_id
    )
    
    UNION ALL
    
    -- Recursive case: Managers with their subordinates' totals
    SELECT e.emp_id,
           e.name,
           e.salary,
           e.salary + COALESCE(SUM(mt.total_salary_cost), 0) as total_salary_cost,
           1 + COALESCE(SUM(mt.total_employees), 0) as total_employees
    FROM employees e
    LEFT JOIN manager_totals mt ON mt.emp_id IN (
        SELECT emp_id FROM employees WHERE manager_id = e.emp_id
    )
    WHERE e.emp_id NOT IN (SELECT emp_id FROM manager_totals)
    GROUP BY e.emp_id, e.name, e.salary
)
SELECT name,
       salary as own_salary,
       total_salary_cost,
       total_employees as team_size,
       ROUND(total_salary_cost / total_employees, 0) as avg_team_salary
FROM manager_totals
WHERE total_employees > 1  -- Only show managers
ORDER BY total_salary_cost DESC;
```

### 4. Graph Traversal Example

```sql
-- Find all possible paths between locations (network analysis)
WITH RECURSIVE location_paths AS (
    -- Base case: Direct connections
    SELECT from_location,
           to_location,
           distance,
           1 as hop_count,
           CAST(from_location || ' -> ' || to_location AS VARCHAR(1000)) as path,
           distance as total_distance
    FROM location_connections
    WHERE from_location = 'New York'  -- Starting point
    
    UNION ALL
    
    -- Recursive case: Extended paths
    SELECT lp.from_location,
           lc.to_location,
           lc.distance,
           lp.hop_count + 1,
           lp.path || ' -> ' || lc.to_location,
           lp.total_distance + lc.distance
    FROM location_paths lp
    JOIN location_connections lc ON lp.to_location = lc.from_location
    WHERE lp.hop_count < 4  -- Limit path length
    AND POSITION(lc.to_location IN lp.path) = 0  -- Avoid cycles
)
SELECT to_location as destination,
       MIN(total_distance) as shortest_distance,
       MIN(hop_count) as fewest_hops
FROM location_paths
WHERE to_location = 'Los Angeles'  -- Destination
GROUP BY to_location;
```

> [!warning] Recursive CTE Safety Always include termination conditions (depth limits, cycle detection) to prevent infinite recursion. Most databases have built-in limits, but it's better to be explicit.

## Performance Considerations

### 1. CTE Materialization

```sql
-- CTEs may be materialized (computed once) or inlined (computed multiple times)
-- Understanding this affects performance optimization

-- This CTE will likely be materialized once
WITH expensive_calculation AS (
    SELECT customer_id,
           COUNT(*) as order_count,
           SUM(amount) as total_spent,
           AVG(amount) as avg_order,
           -- Complex calculations here
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) as median_order
    FROM orders
    WHERE order_date >= '2024-01-01'
    GROUP BY customer_id
)
SELECT c.name,
       ec.order_count,
       ec.total_spent,
       ec.avg_order
FROM expensive_calculation ec
JOIN customers c ON ec.customer_id = c.customer_id
WHERE ec.total_spent > 500;
```

### 2. CTE vs Temporary Tables

```sql
-- For very large intermediate results, consider temp tables
-- CTE approach (good for moderate data)
WITH large_dataset AS (
    SELECT customer_id,
           order_date,
           amount,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_sequence
    FROM orders
    WHERE order_date >= '2020-01-01'
)
SELECT customer_id, COUNT(*) as analysis_count
FROM large_dataset
WHERE order_sequence <= 5
GROUP BY customer_id;

-- Temp table approach (better for very large datasets)
CREATE TEMPORARY TABLE temp_large_dataset AS
SELECT customer_id,
       order_date,
       amount,
       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_sequence
FROM orders
WHERE order_date >= '2020-01-01';

CREATE INDEX idx_temp_customer_sequence ON temp_large_dataset(customer_id, order_sequence);

SELECT customer_id, COUNT(*) as analysis_count
FROM temp_large_dataset
WHERE order_sequence <= 5
GROUP BY customer_id;

DROP TEMPORARY TABLE temp_large_dataset;
```

### 3. Optimizing Recursive CTEs

```sql
-- Efficient recursive CTE with proper indexing and limits
WITH RECURSIVE optimized_hierarchy AS (
    SELECT emp_id,
           name,
           manager_id,
           0 as level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    SELECT e.emp_id,
           e.name,
           e.manager_id,
           oh.level + 1
    FROM employees e
    INNER JOIN optimized_hierarchy oh ON e.manager_id = oh.emp_id
    WHERE oh.level < 5  -- Reasonable depth limit
)
SELECT * 
FROM optimized_hierarchy
ORDER BY level, name;

-- Ensure proper indexing for recursive CTEs
-- CREATE INDEX idx_employees_manager_id ON employees(manager_id);
-- CREATE INDEX idx_employees_emp_id ON employees(emp_id);
```

> [!tip] Performance Tips
> 
> 1. **Index CTE source columns** properly, especially for recursive CTEs
> 2. **Use INNER JOINs** in recursive CTEs when possible (more efficient than LEFT JOINs)
> 3. **Add termination conditions** early in recursive CTEs
> 4. **Consider temp tables** for very large intermediate results that are used multiple times

## Real-World CTE Applications

### 1. Financial Analysis - Portfolio Performance

```sql
-- Complex financial analysis using multiple CTEs
WITH portfolio_positions AS (
    SELECT portfolio_id,
           symbol,
           quantity,
           purchase_price,
           purchase_date
    FROM investments
    WHERE portfolio_id = 'PORTFOLIO_001'
),
current_prices AS (
    SELECT symbol,
           current_price,
           price_date
    FROM stock_prices sp1
    WHERE price_date = (
        SELECT MAX(price_date) 
        FROM stock_prices sp2 
        WHERE sp2.symbol = sp1.symbol
    )
),
position_values AS (
    SELECT pp.portfolio_id,
           pp.symbol,
           pp.quantity,
           pp.purchase_price,
           cp.current_price,
           pp.quantity * pp.purchase_price as cost_basis,
           pp.quantity * cp.current_price as current_value,
           (cp.current_price - pp.purchase_price) * pp.quantity as unrealized_gain_loss,
           DATEDIFF(CURDATE(), pp.purchase_date) as days_held
    FROM portfolio_positions pp
    JOIN current_prices cp ON pp.symbol = cp.symbol
),
portfolio_summary AS (
    SELECT portfolio_id,
           COUNT(*) as num_positions,
           SUM(cost_basis) as total_cost_basis,
           SUM(current_value) as total_current_value,
           SUM(unrealized_gain_loss) as total_unrealized_gain_loss,
           AVG(days_held) as avg_days_held
    FROM position_values
    GROUP BY portfolio_id
)
SELECT ps.portfolio_id,
       ps.num_positions,
       ps.total_cost_basis,
       ps.total_current_value,
       ps.total_unrealized_gain_loss,
       ROUND(ps.total_unrealized_gain_loss * 100.0 / ps.total_cost_basis, 2) as return_pct,
       ps.avg_days_held,
       -- Individual position details
       pv.symbol,
       pv.current_value,
       pv.unrealized_gain_loss,
       ROUND(pv.unrealized_gain_loss * 100.0 / pv.cost_basis, 2) as position_return_pct
FROM portfolio_summary ps
JOIN position_values pv ON ps.portfolio_id = pv.portfolio_id
ORDER BY pv.current_value DESC;
```

### 2. E-commerce - Customer Journey Analysis

```sql
-- Analyze customer journey from acquisition to conversion
WITH customer_touchpoints AS (
    SELECT customer_id,
           event_type,
           event_date,
           channel,
           campaign_id,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY event_date) as touchpoint_sequence,
           FIRST_VALUE(channel) OVER (PARTITION BY customer_id ORDER BY event_date) as first_touch_channel,
           LAST_VALUE(channel) OVER (
               PARTITION BY customer_id 
               ORDER BY event_date 
               ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
           ) as last_touch_channel
    FROM marketing_events
    WHERE event_date >= '2024-01-01'
),
customer_conversions AS (
    SELECT customer_id,
           MIN(order_date) as first_purchase_date,
           COUNT(*) as total_orders,
           SUM(amount) as total_spent
    FROM orders
    WHERE status = 'completed'
    AND order_date >= '2024-01-01'
    GROUP BY customer_id
),
journey_analysis AS (
    SELECT ct.customer_id,
           ct.first_touch_channel,
           ct.last_touch_channel,
           COUNT(DISTINCT ct.touchpoint_sequence) as total_touchpoints,
           MIN(ct.event_date) as journey_start,
           MAX(ct.event_date) as journey_end,
           cc.first_purchase_date,
           cc.total_orders,
           cc.total_spent,
           DATEDIFF(cc.first_purchase_date, MIN(ct.event_date)) as days_to_convert
    FROM customer_touchpoints ct
    LEFT JOIN customer_conversions cc ON ct.customer_id = cc.customer_id
    GROUP BY ct.customer_id, ct.first_touch_channel, ct.last_touch_channel,
             cc.first_purchase_date, cc.total_orders, cc.total_spent
),
conversion_funnel AS (
    SELECT first_touch_channel,
           last_touch_channel,
           COUNT(*) as total_journeys,
           COUNT(first_purchase_date) as conversions,
           ROUND(COUNT(first_purchase_date) * 100.0 / COUNT(*), 2) as conversion_rate,
           AVG(total_touchpoints) as avg_touchpoints,
           AVG(days_to_convert) as avg_days_to_convert,
           SUM(total_spent) as total_revenue,
           AVG(total_spent) as avg_revenue_per_conversion
    FROM journey_analysis
    GROUP BY first_touch_channel, last_touch_channel
)
SELECT *,
       RANK() OVER (ORDER BY conversion_rate DESC) as conversion_rate_rank,
       RANK() OVER (ORDER BY total_revenue DESC) as revenue_rank
FROM conversion_funnel
WHERE total_journeys >= 10  -- Filter for statistical significance
ORDER BY conversion_rate DESC;
```

### 3. Operations - Supply Chain Analysis

```sql
-- Complex supply chain analysis with multiple business rules
WITH demand_forecast AS (
    SELECT product_id,
           DATE_FORMAT(order_date, '%Y-%m') as month,
           SUM(quantity) as monthly_demand,
           AVG(SUM(quantity)) OVER (
               PARTITION BY product_id 
               ORDER BY DATE_FORMAT(order_date, '%Y-%m')
               ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
           ) as three_month_avg_demand
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    AND o.order_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
    GROUP BY product_id, DATE_FORMAT(order_date, '%Y-%m')
),
current_inventory AS (
    SELECT product_id,
           current_stock,
           reorder_point,
           max_stock_level,
           supplier_id,
           lead_time_days
    FROM inventory
),
supplier_performance AS (
    SELECT supplier_id,
           AVG(DATEDIFF(delivered_date, order_date)) as avg_delivery_days,
           COUNT(CASE WHEN delivered_date > promised_date THEN 1 END) * 100.0 / COUNT(*) as late_delivery_pct,
           AVG(quality_score) as avg_quality_score
    FROM purchase_orders
    WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
    GROUP BY supplier_id
),
reorder_analysis AS (
    SELECT ci.product_id,
           ci.current_stock,
           ci.reorder_point,
           ci.max_stock_level,
           df.three_month_avg_demand,
           sp.avg_delivery_days,
           sp.late_delivery_pct,
           sp.avg_quality_score,
           -- Safety stock calculation
           CEIL(df.three_month_avg_demand * (sp.avg_delivery_days / 30.0) * 1.5) as recommended_safety_stock,
           -- Reorder recommendation
           CASE 
               WHEN ci.current_stock <= ci.reorder_point THEN 'URGENT_REORDER'
               WHEN ci.current_stock <= (ci.reorder_point * 1.2) THEN 'REORDER_SOON'
               WHEN ci.current_stock >= ci.max_stock_level THEN 'OVERSTOCKED'
               ELSE 'OPTIMAL'
           END as stock_status,
           -- Economic order quantity (simplified)
           SQRT(2 * df.three_month_avg_demand * 50 / 2) as suggested_order_quantity
    FROM current_inventory ci
    LEFT JOIN demand_forecast df ON ci.product_id = df.product_id 
        AND df.month = DATE_FORMAT(CURDATE(), '%Y-%m')
    LEFT JOIN supplier_performance sp ON ci.supplier_id = sp.supplier_id
),
priority_matrix AS (
    SELECT *,
           CASE 
               WHEN stock_status = 'URGENT_REORDER' AND avg_quality_score >= 8 THEN 1
               WHEN stock_status = 'URGENT_REORDER' AND avg_quality_score < 8 THEN 2
               WHEN stock_status = 'REORDER_SOON' AND late_delivery_pct <= 10 THEN 3
               WHEN stock_status = 'OVERSTOCKED' THEN 5
               ELSE 4
           END as reorder_priority,
           three_month_avg_demand * suggested_order_quantity * 0.5 as estimated_cost_impact
    FROM reorder_analysis
)
SELECT p.product_name,
       pm.current_stock,
       pm.three_month_avg_demand,
       pm.stock_status,
       pm.reorder_priority,
       pm.suggested_order_quantity,
       pm.avg_delivery_days,
       pm.late_delivery_pct,
       pm.estimated_cost_impact,
       s.supplier_name
FROM priority_matrix pm
JOIN products p ON pm.product_id = p.product_id
JOIN suppliers s ON pm.supplier_id = s.supplier_id
WHERE pm.stock_status IN ('URGENT_REORDER', 'REORDER_SOON')
ORDER BY pm.reorder_priority, pm.estimated_cost_impact DESC;
```

## CTEs vs Other Approaches

### 1. CTE vs Subqueries

```sql
-- Subquery approach (harder to read and maintain)
SELECT c.name,
       order_stats.total_orders,
       order_stats.total_spent,
       customer_rank.spending_rank
FROM customers c
JOIN (
    SELECT customer_id, 
           COUNT(*) as total_orders, 
           SUM(amount) as total_spent
    FROM orders 
    WHERE status = 'completed'
    GROUP BY customer_id
) order_stats ON c.customer_id = order_stats.customer_id
JOIN (
    SELECT customer_id,
           RANK() OVER (ORDER BY SUM(amount) DESC) as spending_rank
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
) customer_rank ON c.customer_id = customer_rank.customer_id;

-- CTE approach (much more readable)
WITH order_stats AS (
    SELECT customer_id,
           COUNT(*) as total_orders,
           SUM(amount) as total_spent
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
),
customer_rankings AS (
    SELECT customer_id,
           total_orders,
           total_spent,
           RANK() OVER (ORDER BY total_spent DESC) as spending_rank
    FROM order_stats
)
SELECT c.name,
       cr.total_orders,
       cr.total_spent,
       cr.spending_rank
FROM customers c
JOIN customer_rankings cr ON c.customer_id = cr.customer_id;
```

### 2. CTE vs Views

```sql
-- CTE approach (query-specific)
WITH monthly_sales AS (
    SELECT DATE_FORMAT(order_date, '%Y-%m') as month,
           SUM(amount) as total_sales
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT * FROM monthly_sales WHERE total_sales > 10000;

-- View approach (reusable across queries)
CREATE VIEW monthly_sales_view AS
SELECT DATE_FORMAT(order_date, '%Y-%m') as month,
       SUM(amount) as total_sales
FROM orders
WHERE status = 'completed'
GROUP BY DATE_FORMAT(order_date, '%Y-%m');

-- Then use in multiple queries
SELECT * FROM monthly_sales_view WHERE total_sales > 10000;
SELECT AVG(total_sales) FROM monthly_sales_view;
```

### 3. CTE vs Temporary Tables

```sql
-- CTE approach (exists only during query execution)
WITH large_calculation AS (
    SELECT customer_id,
           order_date,
           amount,
           -- Complex calculations here
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_seq
    FROM orders
    WHERE order_date >= '2020-01-01'
)
SELECT customer_id, COUNT(*) FROM large_calculation GROUP BY customer_id;

-- Temporary table approach (persists for session, can be indexed)
CREATE TEMPORARY TABLE temp_large_calculation AS
SELECT customer_id,
       order_date,
       amount,
       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_seq
FROM orders
WHERE order_date >= '2020-01-01';

CREATE INDEX idx_temp_customer ON temp_large_calculation(customer_id);

-- Can be used in multiple queries
SELECT customer_id, COUNT(*) FROM temp_large_calculation GROUP BY customer_id;
SELECT customer_id, AVG(amount) FROM temp_large_calculation GROUP BY customer_id;

DROP TEMPORARY TABLE temp_large_calculation;
```

## Common CTE Patterns and Use Cases

### 1. Data Deduplication

```sql
-- Remove duplicates using CTEs
WITH ranked_records AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY email 
               ORDER BY created_date DESC
           ) as row_num
    FROM customers
),
clean_customers AS (
    SELECT customer_id, name, email, city, created_date
    FROM ranked_records
    WHERE row_num = 1
)
SELECT * FROM clean_customers ORDER BY name;
```

### 2. Gap Analysis

```sql
-- Find missing sequences or gaps
WITH date_series AS (
    SELECT DATE_ADD('2024-01-01', INTERVAL seq.n DAY) as calendar_date
    FROM (
        SELECT ROW_NUMBER() OVER () - 1 as n
        FROM information_schema.columns
        LIMIT 365
    ) seq
),
actual_sales AS (
    SELECT DATE(order_date) as sale_date,
           SUM(amount) as daily_total
    FROM orders
    WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31'
    GROUP BY DATE(order_date)
),
sales_calendar AS (
    SELECT ds.calendar_date,
           COALESCE(as_table.daily_total, 0) as sales_amount,
           CASE WHEN as_table.sale_date IS NULL THEN 'No Sales' ELSE 'Has Sales' END as sales_status
    FROM date_series ds
    LEFT JOIN actual_sales as_table ON ds.calendar_date = as_table.sale_date
)
SELECT calendar_date,
       sales_amount,
       sales_status
FROM sales_calendar
WHERE sales_status = 'No Sales'
AND DAYOFWEEK(calendar_date) BETWEEN 2 AND 6  -- Weekdays only
ORDER BY calendar_date;
```

### 3. Running Calculations

```sql
-- Complex running calculations across multiple dimensions
WITH daily_sales AS (
    SELECT DATE(order_date) as sale_date,
           customer_id,
           SUM(amount) as daily_amount
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE(order_date), customer_id
),
customer_running_totals AS (
    SELECT sale_date,
           customer_id,
           daily_amount,
           SUM(daily_amount) OVER (
               PARTITION BY customer_id 
               ORDER BY sale_date
               ROWS UNBOUNDED PRECEDING
           ) as customer_running_total,
           AVG(daily_amount) OVER (
               PARTITION BY customer_id 
               ORDER BY sale_date
               ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
           ) as customer_7day_avg
    FROM daily_sales
),
market_context AS (
    SELECT sale_date,
           SUM(daily_amount) as market_daily_total,
           AVG(daily_amount) as market_daily_avg
    FROM daily_sales
    GROUP BY sale_date
)
SELECT crt.sale_date,
       c.name as customer_name,
       crt.daily_amount,
       crt.customer_running_total,
       crt.customer_7day_avg,
       mc.market_daily_total,
       ROUND(crt.daily_amount * 100.0 / mc.market_daily_total, 2) as market_share_pct
FROM customer_running_totals crt
JOIN customers c ON crt.customer_id = c.customer_id
JOIN market_context mc ON crt.sale_date = mc.sale_date
ORDER BY crt.sale_date, crt.daily_amount DESC;
```

### 4. Pivot Table Simulation

```sql
-- Create pivot table functionality using CTEs
WITH monthly_sales AS (
    SELECT DATE_FORMAT(order_date, '%Y-%m') as month,
           CASE 
               WHEN amount < 100 THEN 'Small'
               WHEN amount < 300 THEN 'Medium'
               ELSE 'Large'
           END as order_size,
           COUNT(*) as order_count,
           SUM(amount) as total_amount
    FROM orders
    WHERE status = 'completed'
    AND order_date >= '2024-01-01'
    GROUP BY DATE_FORMAT(order_date, '%Y-%m'), 
             CASE 
                 WHEN amount < 100 THEN 'Small'
                 WHEN amount < 300 THEN 'Medium'
                 ELSE 'Large'
             END
),
pivoted_data AS (
    SELECT month,
           SUM(CASE WHEN order_size = 'Small' THEN order_count ELSE 0 END) as small_orders,
           SUM(CASE WHEN order_size = 'Medium' THEN order_count ELSE 0 END) as medium_orders,
           SUM(CASE WHEN order_size = 'Large' THEN order_count ELSE 0 END) as large_orders,
           SUM(CASE WHEN order_size = 'Small' THEN total_amount ELSE 0 END) as small_revenue,
           SUM(CASE WHEN order_size = 'Medium' THEN total_amount ELSE 0 END) as medium_revenue,
           SUM(CASE WHEN order_size = 'Large' THEN total_amount ELSE 0 END) as large_revenue
    FROM monthly_sales
    GROUP BY month
)
SELECT month,
       small_orders,
       medium_orders,
       large_orders,
       small_orders + medium_orders + large_orders as total_orders,
       small_revenue,
       medium_revenue,
       large_revenue,
       small_revenue + medium_revenue + large_revenue as total_revenue
FROM pivoted_data
ORDER BY month;
```

## Debugging and Testing CTEs

### 1. Step-by-Step Testing

```sql
-- Test each CTE individually during development
-- Step 1: Test the base CTE
WITH customer_orders AS (
    SELECT customer_id,
           COUNT(*) as order_count,
           SUM(amount) as total_spent
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
)
SELECT * FROM customer_orders LIMIT 10;  -- Test first CTE

-- Step 2: Add the next CTE
WITH customer_orders AS (
    SELECT customer_id,
           COUNT(*) as order_count,
           SUM(amount) as total_spent
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
),
customer_segments AS (
    SELECT *,
           CASE 
               WHEN total_spent > 500 THEN 'High'
               WHEN total_spent > 200 THEN 'Medium'
               ELSE 'Low'
           END as segment
    FROM customer_orders
)
SELECT segment, COUNT(*) as customer_count FROM customer_segments GROUP BY segment;

-- Final query with all CTEs...
```

### 2. Adding Debug Information

```sql
-- Include debug columns during development
WITH order_analysis AS (
    SELECT customer_id,
           order_date,
           amount,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_sequence,
           -- Debug info
           'order_analysis' as debug_step,
           NOW() as debug_timestamp
    FROM orders
    WHERE status = 'completed'
),
customer_metrics AS (
    SELECT customer_id,
           COUNT(*) as total_orders,
           SUM(amount) as total_spent,
           MIN(order_date) as first_order,
           MAX(order_date) as last_order,
           -- Debug info
           'customer_metrics' as debug_step,
           COUNT(*) as debug_row_count
    FROM order_analysis
    GROUP BY customer_id
)
SELECT c.name,
       cm.total_orders,
       cm.total_spent,
       cm.first_order,
       cm.last_order,
       -- Keep debug info during testing
       cm.debug_step,
       cm.debug_row_count
FROM customer_metrics cm
JOIN customers c ON cm.customer_id = c.customer_id
ORDER BY cm.total_spent DESC;
```

### 3. Performance Monitoring

```sql
-- Monitor CTE performance with timing
SELECT 'Starting CTE analysis' as status, NOW() as timestamp
UNION ALL

WITH RECURSIVE performance_test AS (
    SELECT emp_id, name, manager_id, 0 as level, NOW() as start_time
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    SELECT e.emp_id, e.name, e.manager_id, pt.level + 1, pt.start_time
    FROM employees e
    JOIN performance_test pt ON e.manager_id = pt.emp_id
    WHERE pt.level < 5
)
SELECT 'Completed CTE analysis' as status, 
       NOW() as timestamp,
       COUNT(*) as total_rows_processed
FROM performance_test

UNION ALL

SELECT 'Final timestamp' as status, NOW() as timestamp, 0 as total_rows;
```

## Best Practices and Guidelines

### 1. Naming Conventions

```sql
-- Good CTE naming practices
WITH 
    -- Use descriptive, business-meaningful names
    completed_orders AS (...),
    customer_lifetime_metrics AS (...),
    high_value_segments AS (...),
    final_customer_analysis AS (...)

-- Avoid generic names like:
-- temp1, data, results, final
```

### 2. Documentation and Comments

```sql
WITH 
    -- Base data: Filter to completed orders from last 12 months
    recent_completed_orders AS (
        SELECT customer_id, order_date, amount
        FROM orders
        WHERE status = 'completed'
        AND order_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
    ),
    
    -- Customer metrics: Calculate key customer statistics
    customer_summary AS (
        SELECT customer_id,
               COUNT(*) as order_frequency,           -- Number of orders
               SUM(amount) as total_value,            -- Total spent
               AVG(amount) as avg_order_value,        -- Average order size
               MIN(order_date) as first_purchase,     -- First order date
               MAX(order_date) as last_purchase       -- Most recent order
        FROM recent_completed_orders
        GROUP BY customer_id
    ),
    
    -- Segmentation: Classify customers using RFM-like approach
    customer_segments AS (
        SELECT *,
               -- Recency: Days since last purchase
               DATEDIFF(CURDATE(), last_purchase) as recency_days,
               
               -- Frequency: Order frequency classification
               CASE 
                   WHEN order_frequency >= 10 THEN 'Frequent'
                   WHEN order_frequency >= 5 THEN 'Regular'
                   ELSE 'Occasional'
               END as frequency_segment,
               
               -- Monetary: Spend level classification
               CASE 
                   WHEN total_value >= 1000 THEN 'High Value'
                   WHEN total_value >= 500 THEN 'Medium Value'
                   ELSE 'Low Value'
               END as value_segment
        FROM customer_summary
    )

-- Final output: Customer analysis with segments
SELECT c.name,
       cs.order_frequency,
       cs.total_value,
       cs.frequency_segment,
       cs.value_segment,
       cs.recency_days
FROM customer_segments cs
JOIN customers c ON cs.customer_id = c.customer_id
ORDER BY cs.total_value DESC;
```

### 3. Error Handling and Validation

```sql
-- Include validation checks in CTEs
WITH data_validation AS (
    SELECT 
        COUNT(*) as total_orders,
        COUNT(CASE WHEN customer_id IS NULL THEN 1 END) as missing_customers,
        COUNT(CASE WHEN amount <= 0 THEN 1 END) as invalid_amounts,
        COUNT(CASE WHEN order_date > CURDATE() THEN 1 END) as future_dates
    FROM orders
),
validated_orders AS (
    SELECT *
    FROM orders o
    CROSS JOIN data_validation dv
    WHERE o.customer_id IS NOT NULL
    AND o.amount > 0
    AND o.order_date <= CURDATE()
    -- Add validation message if there are issues
    AND dv.missing_customers + dv.invalid_amounts + dv.future_dates = 0
)
SELECT COUNT(*) as clean_order_count
FROM validated_orders;
```

## Practice Exercises

### Exercise 1: Basic CTE Operations

```sql
-- 1. Create a CTE to find customers with more than 3 orders, 
--    then calculate their average order value
WITH frequent_customers AS (
    SELECT customer_id,
           COUNT(*) as order_count,
           AVG(amount) as avg_order_value
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
    HAVING COUNT(*) > 3
)
SELECT c.name,
       fc.order_count,
       ROUND(fc.avg_order_value, 2) as avg_order_value
FROM frequent_customers fc
JOIN customers c ON fc.customer_id = c.customer_id
ORDER BY fc.avg_order_value DESC;

-- 2. Use multiple CTEs to calculate monthly sales trends
WITH monthly_sales AS (
    SELECT DATE_FORMAT(order_date, '%Y-%m') as month,
           SUM(amount) as monthly_total
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
),
sales_with_trends AS (
    SELECT month,
           monthly_total,
           LAG(monthly_total) OVER (ORDER BY month) as previous_month,
           monthly_total - LAG(monthly_total) OVER (ORDER BY month) as month_change
    FROM monthly_sales
)
SELECT month,
       monthly_total,
       previous_month,
       month_change,
       CASE 
           WHEN month_change > 0 THEN 'Growth'
           WHEN month_change < 0 THEN 'Decline'
           ELSE 'Stable'
       END as trend
FROM sales_with_trends
WHERE previous_month IS NOT NULL
ORDER BY month;
```

### Exercise 2: Recursive CTE Challenge

```sql
-- 3. Create a recursive CTE to find all employees in a management chain
--    and calculate the total salary cost for each manager's team
WITH RECURSIVE management_hierarchy AS (
    -- Base case: Top-level managers
    SELECT emp_id,
           name,
           salary,
           manager_id,
           0 as level,
           CAST(name AS VARCHAR(500)) as hierarchy_path
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case: Direct reports
    SELECT e.emp_id,
           e.name,
           e.salary,
           e.manager_id,
           mh.level + 1,
           CONCAT(mh.hierarchy_path, ' -> ', e.name)
    FROM employees e
    JOIN management_hierarchy mh ON e.manager_id = mh.emp_id
    WHERE mh.level < 10
),
team_costs AS (
    SELECT manager_id,
           COUNT(*) as team_size,
           SUM(salary) as total_team_salary
    FROM management_hierarchy
    WHERE manager_id IS NOT NULL
    GROUP BY manager_id
)
SELECT e.name as manager_name,
       e.salary as manager_salary,
       COALESCE(tc.team_size, 0) as direct_reports,
       COALESCE(tc.total_team_salary, 0) as team_salary_cost,
       e.salary + COALESCE(tc.total_team_salary, 0) as total_cost_responsibility
FROM employees e
LEFT JOIN team_costs tc ON e.emp_id = tc.manager_id
ORDER BY total_cost_responsibility DESC;
```

### Exercise 3: Complex Business Logic

```sql
-- 4. Customer segmentation using RFM analysis with CTEs
WITH customer_rfm_raw AS (
    SELECT customer_id,
           DATEDIFF(CURDATE(), MAX(order_date)) as recency_days,
           COUNT(*) as frequency,
           SUM(amount) as monetary_value
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT customer_id,
           recency_days,
           frequency,
           monetary_value,
           NTILE(5) OVER (ORDER BY recency_days) as recency_score,
           NTILE(5) OVER (ORDER BY frequency DESC) as frequency_score,
           NTILE(5) OVER (ORDER BY monetary_value DESC) as monetary_score
    FROM customer_rfm_raw
),
customer_segments AS (
    SELECT *,
           CASE 
               WHEN recency_score >= 4 AND frequency_score >= 4 AND monetary_score >= 4 THEN 'Champions'
               WHEN recency_score >= 3 AND frequency_score >= 3 AND monetary_score >= 3 THEN 'Loyal Customers'
               WHEN recency_score >= 3 AND frequency_score <= 2 AND monetary_score >= 3 THEN 'Big Spenders'
               WHEN recency_score >= 4 AND frequency_score >= 2 AND monetary_score <= 3 THEN 'Promising'
               WHEN recency_score >= 3 AND frequency_score >= 2 AND monetary_score >= 2 THEN 'Potential Loyalists'
               WHEN recency_score <= 2 AND frequency_score >= 3 AND monetary_score >= 3 THEN 'At Risk'
               WHEN recency_score <= 2 AND frequency_score >= 2 AND monetary_score >= 2 THEN 'Cannot Lose Them'
               ELSE 'Others'
           END as customer_segment
    FROM rfm_scores
)
SELECT customer_segment,
       COUNT(*) as customer_count,
       AVG(recency_days) as avg_recency,
       AVG(frequency) as avg_frequency,
       AVG(monetary_value) as avg_monetary,
       SUM(monetary_value) as segment_value
FROM customer_segments
GROUP BY customer_segment
ORDER BY segment_value DESC;
```

> [!question] Advanced Challenge Create a CTE that performs cohort analysis: track customer retention by signup month, showing what percentage of customers from each month made purchases in subsequent months.

## Related Topics

- [[SQL Window Functions]] - Advanced analytical functions often used with CTEs
- [[SQL Subqueries]] - Alternative approach for complex filtering
- [[Recursive Queries]] - Deep dive into hierarchical data processing
- [[SQL Performance Optimization]] - Optimizing CTE performance
- [[Advanced SQL]] - Complex query patterns and techniques
- [[Database Design]] - Schema optimization for CTE queries
- [[Business Intelligence]] - Using CTEs for reporting and analytics
- [[Data Analysis with SQL]] - Practical analytical applications
- [[SQL Views]] - Reusable query components similar to CTEs

## Summary

### Key CTE Concepts Mastered

- **Basic CTEs**: Named temporary result sets for query modularity
- **Multiple CTEs**: Chaining and referencing CTEs within single queries
- **Recursive CTEs**: Self-referencing queries for hierarchical data
- **CTE Optimization**: Performance considerations and best practices

### Essential Syntax Components

- **WITH Clause**: Defines one or more CTEs before the main query
- **AS Keyword**: Separates CTE name from its definition
- **Comma Separation**: Multiple CTEs separated by commas
- **RECURSIVE Keyword**: Enables self-referencing CTEs

### Advanced Patterns Learned

✅ **Multi-step Analysis**: Breaking complex business logic into readable steps  
✅ **Data Quality Checks**: Validation and cleansing within CTE chains  
✅ **Hierarchical Traversal**: Organization charts, category trees, graph analysis  
✅ **Business Intelligence**: Customer segmentation, financial analysis, operational metrics  
✅ **Performance Optimization**: When to use CTEs vs alternatives

### Best Practices Applied

- **Meaningful Naming**: Descriptive CTE names that indicate business purpose
- **Documentation**: Comments explaining each CTE's role in the analysis
- **Step-by-step Testing**: Validating each CTE individually during development
- **Error Handling**: Including validation checks within CTE chains
- **Performance Awareness**: Understanding when CTEs vs temp tables vs views are appropriate

### Business Applications Covered

- **Financial Analysis**: Portfolio performance, P&L calculations
- **Customer Analytics**: Journey analysis, segmentation, lifetime value
- **Operations**: Supply chain optimization, inventory management
- **Marketing**: Campaign attribution, conversion funnel analysis
- **Human Resources**: Organizational analysis, cost center reporting

### What You Can Do Now

- ✅ Write readable, maintainable complex queries using CTEs
- ✅ Break down multi-step business logic into modular components
- ✅ Handle hierarchical data with recursive CTEs
- ✅ Choose appropriate alternatives (CTEs vs subqueries vs temp tables)
- ✅ Optimize CTE performance for large datasets
- ✅ Debug and test complex CTE chains effectively
- ✅ Apply CTEs to real-world business intelligence scenarios

### Next Learning Goals

- [ ] Master [[Recursive Query Patterns]] for advanced tree/graph operations
- [ ] Explore [[SQL Performance Tuning]] for CTE optimization
- [ ] Learn [[Advanced Window Functions]] to combine with CTE patterns
- [ ] Study [[Database Query Optimization]] for complex analytical queries
- [ ] Practice [[Statistical Analysis with SQL]] using CTE foundations

### Modern SQL Evolution

CTEs represent a major step forward in SQL readability and maintainability. They bridge the gap between simple queries and complex analytical needs:

- **Readability**: Transform complex nested queries into understandable steps
- **Maintainability**: Easier to modify and debug individual components
- **Collaboration**: Team members can understand and modify CTE-based queries
- **Performance**: Often more efficient than nested subqueries

> [!tip] Mastery Path Start with simple CTEs to replace nested subqueries, then progress to multi-step business logic. Practice recursive CTEs with hierarchical sample data. Focus on making your queries tell a story through well-named CTEs that represent clear business concepts.

> [!note] Database Compatibility CTE support varies across databases:
> 
> - **PostgreSQL, SQL Server, Oracle**: Full CTE and recursive CTE support
> - **MySQL 8.0+**: Complete CTE functionality including recursive
> - **SQLite 3.8.3+**: WITH clause support, recursive CTEs in 3.8.3+
> - **Older MySQL versions**: No CTE support (use subqueries or temp tables)

---

_Tags: #SQL #CTE #CommonTableExpressions #RecursiveCTE #AdvancedSQL #QueryOptimization #BusinessIntelligence #DataAnalysis #HierarchicalData #SQLBestPractices #ReadableSQL_