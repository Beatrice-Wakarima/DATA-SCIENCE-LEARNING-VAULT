# SQL Window Functions - Complete Guide

_Master advanced analytical capabilities with SQL window functions for sophisticated data analysis_

## What are SQL Window Functions?

**Window Functions** (also called analytical functions) perform calculations across a set of rows that are related to the current row, without needing to group the data. Unlike aggregate functions that collapse rows, window functions maintain the individual row details while adding calculated columns.

> [!note] The Power of Window Functions Window functions are like having a "sliding window" that can look at different subsets of your data while keeping all rows visible. They're essential for [[Advanced SQL]], [[Data Analysis]], and [[Business Intelligence]] tasks.

### Key Advantages Over Traditional SQL

- **No GROUP BY needed**: Keep all detail rows while adding analytics
- **Multiple calculations**: Different windows in the same query
- **Row-by-row context**: Access to preceding/following rows
- **Ranking and ordering**: Built-in ranking capabilities
- **Running totals**: Cumulative calculations made simple

### Window Function vs Aggregate Function

```sql
-- Traditional aggregate: Loses row detail
SELECT customer_id, SUM(amount) as total
FROM orders
GROUP BY customer_id;

-- Window function: Keeps all rows + adds totals
SELECT customer_id, order_id, amount,
       SUM(amount) OVER (PARTITION BY customer_id) as customer_total
FROM orders;
```

## Sample Data for Examples

We'll use these tables throughout the guide:

### SALES Table

```sql
+----------+-------------+--------+------------+----------+
| sale_id  | salesperson | amount | sale_date  | region   |
+----------+-------------+--------+------------+----------+
| 1        | Alice       | 1000   | 2024-01-15 | North    |
| 2        | Bob         | 1500   | 2024-01-16 | South    |
| 3        | Alice       | 1200   | 2024-01-17 | North    |
| 4        | Carol       | 800    | 2024-01-18 | East     |
| 5        | Bob         | 2000   | 2024-01-19 | South    |
| 6        | Alice       | 900    | 2024-01-20 | North    |
| 7        | Carol       | 1100   | 2024-01-21 | East     |
| 8        | Bob         | 1300   | 2024-01-22 | South    |
+----------+-------------+--------+------------+----------+
```

### EMPLOYEES Table

```sql
+--------+----------+--------+------------+
| emp_id | name     | salary | department |
+--------+----------+--------+------------+
| 1      | Alice    | 75000  | Sales      |
| 2      | Bob      | 80000  | Sales      |
| 3      | Carol    | 72000  | Sales      |
| 4      | David    | 90000  | Marketing  |
| 5      | Eve      | 85000  | Marketing  |
| 6      | Frank    | 95000  | Engineering|
| 7      | Grace    | 88000  | Engineering|
| 8      | Henry    | 92000  | Engineering|
+--------+----------+--------+------------+
```

## Window Function Syntax

### Basic Structure

```sql
SELECT column1, column2,
       WINDOW_FUNCTION() OVER (
           [PARTITION BY column3]
           [ORDER BY column4]
           [ROWS/RANGE frame_specification]
       ) as result_column
FROM table_name;
```

### Components Explained

- **WINDOW_FUNCTION()**: The analytical function (ROW_NUMBER, SUM, etc.)
- **OVER()**: Defines the window specification
- **PARTITION BY**: Divides data into groups (like GROUP BY but keeps rows)
- **ORDER BY**: Sorts data within each partition
- **ROWS/RANGE**: Defines the frame (which rows to include in calculation)

> [!tip] Think of PARTITION BY PARTITION BY is like creating separate "mini-tables" for each group, then applying the window function to each mini-table independently.

## Categories of Window Functions

### 1. Ranking Functions

|Function|Description|Handles Ties|
|---|---|---|
|**ROW_NUMBER()**|Sequential numbering|Always unique|
|**RANK()**|Ranking with gaps|Same rank, skips next|
|**DENSE_RANK()**|Ranking without gaps|Same rank, no skips|
|**NTILE(n)**|Divide into n buckets|Equal distribution|

### 2. Aggregate Functions

|Function|Description|Example Use|
|---|---|---|
|**SUM()**|Running/windowed sum|Cumulative sales|
|**AVG()**|Moving average|Rolling averages|
|**COUNT()**|Running count|Sequential numbering|
|**MIN()/MAX()**|Windowed min/max|Range analysis|

### 3. Value Functions

|Function|Description|Use Case|
|---|---|---|
|**LAG()**|Previous row value|Period comparisons|
|**LEAD()**|Next row value|Future comparisons|
|**FIRST_VALUE()**|First value in window|Baseline comparisons|
|**LAST_VALUE()**|Last value in window|Current vs final|

## 1. Ranking Functions

### ROW_NUMBER()

Assigns a unique sequential number to each row within a partition.

```sql
-- Number sales by salesperson chronologically
SELECT salesperson, 
       sale_date, 
       amount,
       ROW_NUMBER() OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
       ) as sale_sequence
FROM sales;
```

**Result:**

```sql
+-------------+------------+--------+---------------+
| salesperson | sale_date  | amount | sale_sequence |
+-------------+------------+--------+---------------+
| Alice       | 2024-01-15 | 1000   | 1             |
| Alice       | 2024-01-17 | 1200   | 2             |
| Alice       | 2024-01-20 | 900    | 3             |
| Bob         | 2024-01-16 | 1500   | 1             |
| Bob         | 2024-01-19 | 2000   | 2             |
| Bob         | 2024-01-22 | 1300   | 3             |
| Carol       | 2024-01-18 | 800    | 1             |
| Carol       | 2024-01-21 | 1100   | 2             |
+-------------+------------+--------+---------------+
```

### RANK() vs DENSE_RANK()

```sql
-- Compare ranking functions with ties
SELECT salesperson,
       amount,
       RANK() OVER (ORDER BY amount DESC) as rank_with_gaps,
       DENSE_RANK() OVER (ORDER BY amount DESC) as dense_rank,
       ROW_NUMBER() OVER (ORDER BY amount DESC) as row_num
FROM sales
ORDER BY amount DESC;
```

**Result:**

```sql
+-------------+--------+-----------------+------------+---------+
| salesperson | amount | rank_with_gaps  | dense_rank | row_num |
+-------------+--------+-----------------+------------+---------+
| Bob         | 2000   | 1               | 1          | 1       |
| Bob         | 1500   | 2               | 2          | 2       |
| Bob         | 1300   | 3               | 3          | 3       |
| Alice       | 1200   | 4               | 4          | 4       |
| Carol       | 1100   | 5               | 5          | 5       |
| Alice       | 1000   | 6               | 6          | 6       |
| Alice       | 900    | 7               | 7          | 7       |
| Carol       | 800    | 8               | 8          | 8       |
+-------------+--------+-----------------+------------+---------+
```

### NTILE() for Quartiles and Percentiles

```sql
-- Divide salespeople into performance quartiles
SELECT salesperson,
       amount,
       NTILE(4) OVER (ORDER BY amount) as quartile,
       CASE NTILE(4) OVER (ORDER BY amount)
           WHEN 1 THEN 'Bottom 25%'
           WHEN 2 THEN 'Lower Middle 25%'
           WHEN 3 THEN 'Upper Middle 25%'
           WHEN 4 THEN 'Top 25%'
       END as performance_bucket
FROM sales;
```

### Practical Ranking Applications

```sql
-- Find top 3 performers by region
SELECT *
FROM (
    SELECT region,
           salesperson,
           SUM(amount) as total_sales,
           RANK() OVER (
               PARTITION BY region 
               ORDER BY SUM(amount) DESC
           ) as region_rank
    FROM sales
    GROUP BY region, salesperson
) ranked_sales
WHERE region_rank <= 3;

-- Monthly sales ranking for each salesperson
SELECT salesperson,
       DATE_FORMAT(sale_date, '%Y-%m') as month,
       SUM(amount) as monthly_total,
       ROW_NUMBER() OVER (
           PARTITION BY salesperson 
           ORDER BY SUM(amount) DESC
       ) as best_months_rank
FROM sales
GROUP BY salesperson, DATE_FORMAT(sale_date, '%Y-%m');
```

> [!tip] Choosing the Right Ranking Function
> 
> - **ROW_NUMBER()**: When you need unique numbers (pagination, sampling)
> - **RANK()**: When ties should get same rank and skip next positions (competitions)
> - **DENSE_RANK()**: When ties should get same rank without skipping (grade distributions)
> - **NTILE()**: When you want equal-sized buckets (percentiles, AB test groups)

## 2. Aggregate Window Functions

### Running Totals with SUM()

```sql
-- Calculate running total of sales by salesperson
SELECT salesperson,
       sale_date,
       amount,
       SUM(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
           ROWS UNBOUNDED PRECEDING
       ) as running_total
FROM sales
ORDER BY salesperson, sale_date;
```

**Result:**

```sql
+-------------+------------+--------+---------------+
| salesperson | sale_date  | amount | running_total |
+-------------+------------+--------+---------------+
| Alice       | 2024-01-15 | 1000   | 1000          |
| Alice       | 2024-01-17 | 1200   | 2200          |
| Alice       | 2024-01-20 | 900    | 3100          |
| Bob         | 2024-01-16 | 1500   | 1500          |
| Bob         | 2024-01-19 | 2000   | 3500          |
| Bob         | 2024-01-22 | 1300   | 4800          |
+-------------+------------+--------+---------------+
```

### Moving Averages

```sql
-- 3-period moving average
SELECT salesperson,
       sale_date,
       amount,
       AVG(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
           ROWS 2 PRECEDING  -- Current row + 2 previous = 3 rows
       ) as moving_avg_3
FROM sales
ORDER BY salesperson, sale_date;
```

### Percentage of Total

```sql
-- Each sale as percentage of salesperson's total
SELECT salesperson,
       sale_date,
       amount,
       ROUND(
           amount * 100.0 / SUM(amount) OVER (PARTITION BY salesperson),
           2
       ) as pct_of_personal_total,
       ROUND(
           amount * 100.0 / SUM(amount) OVER (),
           2
       ) as pct_of_grand_total
FROM sales;
```

### Cumulative Distributions

```sql
-- Running count and percentage of total records
SELECT salesperson,
       sale_date,
       amount,
       COUNT(*) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
           ROWS UNBOUNDED PRECEDING
       ) as sales_count,
       ROUND(
           COUNT(*) OVER (
               PARTITION BY salesperson 
               ORDER BY sale_date
               ROWS UNBOUNDED PRECEDING
           ) * 100.0 / COUNT(*) OVER (PARTITION BY salesperson),
           1
       ) as pct_of_salesperson_sales
FROM sales;
```

## 3. Value Access Functions (LAG/LEAD)

### LAG() - Previous Values

```sql
-- Compare current sale to previous sale
SELECT salesperson,
       sale_date,
       amount,
       LAG(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
       ) as previous_sale,
       amount - LAG(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
       ) as change_from_previous
FROM sales
ORDER BY salesperson, sale_date;
```

**Result:**

```sql
+-------------+------------+--------+---------------+--------------------+
| salesperson | sale_date  | amount | previous_sale | change_from_previous|
+-------------+------------+--------+---------------+--------------------+
| Alice       | 2024-01-15 | 1000   | NULL          | NULL               |
| Alice       | 2024-01-17 | 1200   | 1000          | 200                |
| Alice       | 2024-01-20 | 900    | 1200          | -300               |
| Bob         | 2024-01-16 | 1500   | NULL          | NULL               |
| Bob         | 2024-01-19 | 2000   | 1500          | 500                |
| Bob         | 2024-01-22 | 1300   | 2000          | -700               |
+-------------+------------+--------+---------------+--------------------+
```

### LEAD() - Next Values

```sql
-- Compare current sale to next sale
SELECT salesperson,
       sale_date,
       amount,
       LEAD(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
       ) as next_sale,
       CASE 
           WHEN LEAD(amount) OVER (
               PARTITION BY salesperson 
               ORDER BY sale_date
           ) > amount THEN 'Improving'
           WHEN LEAD(amount) OVER (
               PARTITION BY salesperson 
               ORDER BY sale_date
           ) < amount THEN 'Declining'
           ELSE 'Stable'
       END as trend
FROM sales;
```

### LAG/LEAD with Offset and Defaults

```sql
-- Look back 2 periods with default value
SELECT salesperson,
       sale_date,
       amount,
       LAG(amount, 2, 0) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
       ) as amount_2_periods_ago,
       -- Calculate percentage change over 2 periods
       ROUND(
           (amount - LAG(amount, 2, amount) OVER (
               PARTITION BY salesperson 
               ORDER BY sale_date
           )) * 100.0 / NULLIF(LAG(amount, 2, amount) OVER (
               PARTITION BY salesperson 
               ORDER BY sale_date
           ), 0),
           2
       ) as pct_change_2_periods
FROM sales;
```

### First and Last Values

```sql
-- Compare each sale to first and last in the period
SELECT salesperson,
       sale_date,
       amount,
       FIRST_VALUE(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
           ROWS UNBOUNDED PRECEDING
       ) as first_sale,
       LAST_VALUE(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) as last_sale
FROM sales;
```

> [!warning] LAST_VALUE Gotcha LAST_VALUE requires careful frame specification. Without "UNBOUNDED FOLLOWING", it only sees up to the current row, making it equivalent to the current value!

## Window Frames (ROWS and RANGE)

Window frames define exactly which rows are included in the window function calculation.

### Frame Types

- **ROWS**: Physical number of rows
- **RANGE**: Logical range based on values

### Common Frame Specifications

```sql
-- Different frame specifications
SELECT salesperson,
       sale_date,
       amount,
       -- Default frame: RANGE UNBOUNDED PRECEDING
       SUM(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
       ) as running_total_default,
       
       -- Explicit ROWS frame
       SUM(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
           ROWS UNBOUNDED PRECEDING
       ) as running_total_rows,
       
       -- 3-row moving window
       AVG(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
           ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
       ) as moving_avg_3_centered,
       
       -- Current row only
       SUM(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
           ROWS CURRENT ROW
       ) as current_amount_only
FROM sales;
```

### Frame Boundary Options

|Boundary|Description|
|---|---|
|`UNBOUNDED PRECEDING`|From the first row of partition|
|`UNBOUNDED FOLLOWING`|To the last row of partition|
|`CURRENT ROW`|The current row only|
|`n PRECEDING`|n rows before current|
|`n FOLLOWING`|n rows after current|

### Practical Frame Examples

```sql
-- Sales performance metrics with different windows
SELECT salesperson,
       sale_date,
       amount,
       -- Quarter-to-date running total
       SUM(amount) OVER (
           PARTITION BY salesperson, QUARTER(sale_date)
           ORDER BY sale_date
           ROWS UNBOUNDED PRECEDING
       ) as qtd_total,
       
       -- 7-day rolling average (simulated)
       AVG(amount) OVER (
           PARTITION BY salesperson
           ORDER BY sale_date
           ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
       ) as rolling_7day_avg,
       
       -- Centered 5-period moving average
       AVG(amount) OVER (
           PARTITION BY salesperson
           ORDER BY sale_date
           ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
       ) as centered_5_period_avg
FROM sales;
```

## Advanced Window Function Patterns

### 1. Finding Gaps and Islands

```sql
-- Find consecutive days of sales
WITH sales_with_groups AS (
    SELECT sale_date,
           salesperson,
           amount,
           ROW_NUMBER() OVER (PARTITION BY salesperson ORDER BY sale_date) as rn,
           DATE_SUB(sale_date, INTERVAL ROW_NUMBER() OVER (PARTITION BY salesperson ORDER BY sale_date) DAY) as group_date
    FROM sales
)
SELECT salesperson,
       group_date,
       MIN(sale_date) as streak_start,
       MAX(sale_date) as streak_end,
       COUNT(*) as consecutive_days,
       SUM(amount) as streak_total
FROM sales_with_groups
GROUP BY salesperson, group_date
HAVING COUNT(*) > 1  -- Only show streaks of 2+ days
ORDER BY salesperson, streak_start;
```

### 2. Conditional Aggregations

```sql
-- Running totals with conditions
SELECT salesperson,
       sale_date,
       amount,
       -- Running total of sales > 1000
       SUM(CASE WHEN amount > 1000 THEN amount ELSE 0 END) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
           ROWS UNBOUNDED PRECEDING
       ) as running_large_sales,
       
       -- Count of consecutive sales above average
       COUNT(CASE WHEN amount > AVG(amount) OVER (PARTITION BY salesperson) 
                  THEN 1 END) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
           ROWS UNBOUNDED PRECEDING
       ) as above_avg_count
FROM sales;
```

### 3. Percentile Calculations

```sql
-- Percentile-based analysis
SELECT salesperson,
       amount,
       -- Percentile rank (0-1)
       PERCENT_RANK() OVER (PARTITION BY salesperson ORDER BY amount) as percentile_rank,
       
       -- Cumulative distribution (0-1)
       CUME_DIST() OVER (PARTITION BY salesperson ORDER BY amount) as cumulative_dist,
       
       -- Convert to percentages
       ROUND(PERCENT_RANK() OVER (PARTITION BY salesperson ORDER BY amount) * 100, 1) as percentile_pct,
       
       -- Median calculation using PERCENTILE_CONT (if supported)
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) OVER (PARTITION BY salesperson) as median_amount
FROM sales;
```

### 4. Time Series Analysis

```sql
-- Advanced time series patterns
SELECT salesperson,
       sale_date,
       amount,
       -- Year-over-year comparison (simulated)
       LAG(amount, 12) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
       ) as same_period_last_year,
       
       -- Seasonal decomposition (monthly averages)
       AVG(amount) OVER (
           PARTITION BY salesperson, MONTH(sale_date)
           ORDER BY sale_date
           ROWS UNBOUNDED PRECEDING
       ) as monthly_avg_to_date,
       
       -- Detect trend changes
       CASE 
           WHEN amount > LAG(amount) OVER (PARTITION BY salesperson ORDER BY sale_date)
                AND LAG(amount) OVER (PARTITION BY salesperson ORDER BY sale_date) > 
                    LAG(amount, 2) OVER (PARTITION BY salesperson ORDER BY sale_date)
           THEN 'Uptrend'
           WHEN amount < LAG(amount) OVER (PARTITION BY salesperson ORDER BY sale_date)
                AND LAG(amount) OVER (PARTITION BY salesperson ORDER BY sale_date) < 
                    LAG(amount, 2) OVER (PARTITION BY salesperson ORDER BY sale_date)
           THEN 'Downtrend'
           ELSE 'Mixed'
       END as trend_direction
FROM sales;
```

## Business Intelligence Applications

### 1. Sales Performance Dashboard

```sql
-- Comprehensive sales performance metrics
SELECT salesperson,
       DATE_FORMAT(sale_date, '%Y-%m') as month,
       SUM(amount) as monthly_sales,
       
       -- Month-over-month growth
       ROUND(
           (SUM(amount) - LAG(SUM(amount)) OVER (
               PARTITION BY salesperson 
               ORDER BY DATE_FORMAT(sale_date, '%Y-%m')
           )) * 100.0 / NULLIF(LAG(SUM(amount)) OVER (
               PARTITION BY salesperson 
               ORDER BY DATE_FORMAT(sale_date, '%Y-%m')
           ), 0),
           2
       ) as mom_growth_pct,
       
       -- Rank within month across all salespeople
       RANK() OVER (
           PARTITION BY DATE_FORMAT(sale_date, '%Y-%m') 
           ORDER BY SUM(amount) DESC
       ) as monthly_rank,
       
       -- Running annual total
       SUM(SUM(amount)) OVER (
           PARTITION BY salesperson, YEAR(sale_date) 
           ORDER BY DATE_FORMAT(sale_date, '%Y-%m')
           ROWS UNBOUNDED PRECEDING
       ) as ytd_total,
       
       -- Performance vs team average
       ROUND(
           SUM(amount) / AVG(SUM(amount)) OVER (
               PARTITION BY DATE_FORMAT(sale_date, '%Y-%m')
           ) * 100,
           1
       ) as vs_team_avg_pct
       
FROM sales
GROUP BY salesperson, DATE_FORMAT(sale_date, '%Y-%m')
ORDER BY salesperson, month;
```

### 2. Customer Cohort Analysis

```sql
-- Customer lifecycle and cohort analysis
WITH customer_first_purchase AS (
    SELECT customer_id,
           MIN(order_date) as first_purchase_date,
           DATE_FORMAT(MIN(order_date), '%Y-%m') as cohort_month
    FROM orders
    GROUP BY customer_id
),
monthly_activity AS (
    SELECT o.customer_id,
           cfp.cohort_month,
           DATE_FORMAT(o.order_date, '%Y-%m') as activity_month,
           PERIOD_DIFF(
               DATE_FORMAT(o.order_date, '%Y%m'),
               DATE_FORMAT(cfp.first_purchase_date, '%Y%m')
           ) as months_since_first_purchase,
           SUM(o.amount) as monthly_spend
    FROM orders o
    JOIN customer_first_purchase cfp ON o.customer_id = cfp.customer_id
    GROUP BY o.customer_id, cfp.cohort_month, DATE_FORMAT(o.order_date, '%Y-%m')
)
SELECT cohort_month,
       months_since_first_purchase,
       COUNT(DISTINCT customer_id) as active_customers,
       SUM(monthly_spend) as cohort_revenue,
       
       -- Retention rate
       ROUND(
           COUNT(DISTINCT customer_id) * 100.0 / FIRST_VALUE(COUNT(DISTINCT customer_id)) OVER (
               PARTITION BY cohort_month 
               ORDER BY months_since_first_purchase
               ROWS UNBOUNDED PRECEDING
           ),
           2
       ) as retention_rate
       
FROM monthly_activity
GROUP BY cohort_month, months_since_first_purchase
ORDER BY cohort_month, months_since_first_purchase;
```

### 3. Inventory and Demand Forecasting

```sql
-- Sales trend analysis for forecasting
SELECT product_id,
       sale_date,
       quantity_sold,
       
       -- 7-day moving average
       AVG(quantity_sold) OVER (
           PARTITION BY product_id 
           ORDER BY sale_date
           ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
       ) as ma_7_day,
       
       -- Exponential smoothing simulation
       0.3 * quantity_sold + 0.7 * LAG(quantity_sold) OVER (
           PARTITION BY product_id 
           ORDER BY sale_date
       ) as exp_smoothed,
       
       -- Seasonality detection (day of week pattern)
       AVG(quantity_sold) OVER (
           PARTITION BY product_id, DAYOFWEEK(sale_date)
           ORDER BY sale_date
           ROWS UNBOUNDED PRECEDING
       ) as dow_average,
       
       -- Trend analysis
       CASE 
           WHEN AVG(quantity_sold) OVER (
               PARTITION BY product_id 
               ORDER BY sale_date
               ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
           ) > AVG(quantity_sold) OVER (
               PARTITION BY product_id 
               ORDER BY sale_date
               ROWS BETWEEN 13 PRECEDING AND 7 PRECEDING
           ) THEN 'Increasing'
           WHEN AVG(quantity_sold) OVER (
               PARTITION BY product_id 
               ORDER BY sale_date
               ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
           ) < AVG(quantity_sold) OVER (
               PARTITION BY product_id 
               ORDER BY sale_date
               ROWS BETWEEN 13 PRECEDING AND 7 PRECEDING
           ) THEN 'Decreasing'
           ELSE 'Stable'
       END as demand_trend
       
FROM product_sales
WHERE sale_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
ORDER BY product_id, sale_date;
```

## Performance Optimization

### 1. Indexing for Window Functions

```sql
-- Essential indexes for window function performance
CREATE INDEX idx_sales_salesperson_date ON sales(salesperson, sale_date);
CREATE INDEX idx_sales_region_amount ON sales(region, amount DESC);
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Covering indexes for specific queries
CREATE INDEX idx_sales_covering ON sales(salesperson, sale_date, amount, region);
```

### 2. Avoiding Common Performance Pitfalls

```sql
-- SLOW: Multiple window functions with same OVER clause
SELECT salesperson,
       sale_date,
       amount,
       SUM(amount) OVER (PARTITION BY salesperson ORDER BY sale_date) as running_sum,
       AVG(amount) OVER (PARTITION BY salesperson ORDER BY sale_date) as running_avg,
       COUNT(*) OVER (PARTITION BY salesperson ORDER BY sale_date) as running_count
FROM sales;

-- FASTER: Use WINDOW clause to define once
SELECT salesperson,
       sale_date,
       amount,
       SUM(amount) OVER w as running_sum,
       AVG(amount) OVER w as running_avg,
       COUNT(*) OVER w as running_count
FROM sales
WINDOW w AS (PARTITION BY salesperson ORDER BY sale_date);
```

### 3. Limiting Window Function Scope

```sql
-- Instead of processing entire table
SELECT salesperson,
       amount,
       RANK() OVER (ORDER BY amount DESC) as overall_rank
FROM sales;

-- Limit scope when possible
SELECT salesperson,
       amount,
       RANK() OVER (ORDER BY amount DESC) as monthly_rank
FROM sales
WHERE sale_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);
```

### 4. Window Functions vs Alternatives

```sql
-- Window function approach
SELECT customer_id,
       order_date,
       amount,
       SUM(amount) OVER (PARTITION BY customer_id) as customer_total
FROM orders;

-- JOIN approach (sometimes faster for simple cases)
SELECT o.customer_id,
       o.order_date,
       o.amount,
       ct.customer_total
FROM orders o
JOIN (
    SELECT customer_id, SUM(amount) as customer_total
    FROM orders
    GROUP BY customer_id
) ct ON o.customer_id = ct.customer_id;
```

> [!tip] Performance Best Practices
> 
> 1. **Use proper indexes** on PARTITION BY and ORDER BY columns
> 2. **Define windows once** with WINDOW clause for reuse
> 3. **Limit data scope** with WHERE clauses before window functions
> 4. **Consider alternatives** for simple aggregations
> 5. **Test with realistic data sizes** to identify bottlenecks

## Common Use Cases and Solutions

### 1. Top N per Group

```sql
-- Top 3 sales by each salesperson
SELECT *
FROM (
    SELECT salesperson,
           sale_date,
           amount,
           ROW_NUMBER() OVER (
               PARTITION BY salesperson 
               ORDER BY amount DESC
           ) as rank_in_group
    FROM sales
) ranked
WHERE rank_in_group <= 3;
```

### 2. Running Differences

```sql
-- Period-over-period changes
SELECT salesperson,
       DATE_FORMAT(sale_date, '%Y-%m') as month,
       SUM(amount) as monthly_total,
       SUM(amount) - LAG(SUM(amount)) OVER (
           PARTITION BY salesperson 
           ORDER BY DATE_FORMAT(sale_date, '%Y-%m')
       ) as month_over_month_change
FROM sales
GROUP BY salesperson, DATE_FORMAT(sale_date, '%Y-%m');
```

### 3. Cumulative Percentages

```sql
-- Running percentage of total
SELECT salesperson,
       sale_date,
       amount,
       SUM(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
           ROWS UNBOUNDED PRECEDING
       ) as running_total,
       ROUND(
           SUM(amount) OVER (
               PARTITION BY salesperson 
               ORDER BY sale_date
               ROWS UNBOUNDED PRECEDING
           ) * 100.0 / SUM(amount) OVER (PARTITION BY salesperson),
           2
       ) as cumulative_percentage
FROM sales;
```

### 4. Detecting Outliers

```sql
-- Identify outliers using statistical methods
SELECT salesperson,
       sale_date,
       amount,
       AVG(amount) OVER (PARTITION BY salesperson) as avg_amount,
       STDDEV(amount) OVER (PARTITION BY salesperson) as stddev_amount,
       CASE 
           WHEN ABS(amount - AVG(amount) OVER (PARTITION BY salesperson)) > 
                2 * STDDEV(amount) OVER (PARTITION BY salesperson)
           THEN 'Outlier'
           ELSE 'Normal'
       END as outlier_status
FROM sales;
```

### 5. Session Analysis

```sql
-- Web analytics: User session identification
WITH page_views AS (
    SELECT user_id,
           page_view_time,
           LAG(page_view_time) OVER (
               PARTITION BY user_id 
               ORDER BY page_view_time
           ) as previous_view_time,
           CASE 
               WHEN TIMESTAMPDIFF(MINUTE, 
                   LAG(page_view_time) OVER (
                       PARTITION BY user_id 
                       ORDER BY page_view_time
                   ), 
                   page_view_time
               ) > 30 OR LAG(page_view_time) OVER (
                   PARTITION BY user_id 
                   ORDER BY page_view_time
               ) IS NULL
           THEN 1 ELSE 0 
           END as new_session_flag
    FROM website_logs
)
SELECT user_id,
       page_view_time,
       SUM(new_session_flag) OVER (
           PARTITION BY user_id 
           ORDER BY page_view_time
           ROWS UNBOUNDED PRECEDING
       ) as session_id
FROM page_views;
```

## Window Functions vs Alternatives

### When to Use Window Functions

✅ **Perfect for:**

- Rankings and percentiles
- Running totals and moving averages
- Period-over-period comparisons
- Keeping detail rows while adding analytics
- Complex analytical calculations

### When to Consider Alternatives

#### Simple Aggregations

```sql
-- Window function
SELECT customer_id, order_id, amount,
       SUM(amount) OVER (PARTITION BY customer_id) as total
FROM orders;

-- Simple JOIN (potentially faster)
SELECT o.customer_id, o.order_id, o.amount, t.total
FROM orders o
JOIN (SELECT customer_id, SUM(amount) as total FROM orders GROUP BY customer_id) t
ON o.customer_id = t.customer_id;
```

#### Subquery Alternative

```sql
-- Window function for existence check
SELECT customer_id, 
       CASE WHEN COUNT(*) OVER (PARTITION BY customer_id) > 5 
            THEN 'High Activity' ELSE 'Low Activity' END
FROM orders;

-- Subquery alternative
SELECT customer_id,
       CASE WHEN customer_id IN (
           SELECT customer_id FROM orders GROUP BY customer_id HAVING COUNT(*) > 5
       ) THEN 'High Activity' ELSE 'Low Activity' END
FROM orders;
```

## Troubleshooting Window Functions

### Common Issues and Solutions

#### 1. Unexpected NULL Values

```sql
-- Problem: LAG returns NULL for first row
SELECT salesperson, amount,
       LAG(amount) OVER (ORDER BY sale_date) as previous_amount
FROM sales;

-- Solution: Use default value
SELECT salesperson, amount,
       LAG(amount, 1, 0) OVER (ORDER BY sale_date) as previous_amount
FROM sales;
```

#### 2. Frame Specification Issues

```sql
-- Problem: LAST_VALUE doesn't work as expected
SELECT salesperson, amount,
       LAST_VALUE(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
       ) as last_amount  -- This gives current row value!
FROM sales;

-- Solution: Specify full frame
SELECT salesperson, amount,
       LAST_VALUE(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) as last_amount
FROM sales;
```

#### 3. Performance Problems

```sql
-- Problem: Multiple similar window calculations
SELECT customer_id,
       SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date),
       AVG(amount) OVER (PARTITION BY customer_id ORDER BY order_date),
       COUNT(*) OVER (PARTITION BY customer_id ORDER BY order_date)
FROM orders;

-- Solution: Use WINDOW clause
SELECT customer_id,
       SUM(amount) OVER w,
       AVG(amount) OVER w,
       COUNT(*) OVER w
FROM orders
WINDOW w AS (PARTITION BY customer_id ORDER BY order_date);
```

#### 4. Data Type Mismatches

```sql
-- Problem: Integer division in window function
SELECT amount,
       amount / SUM(amount) OVER () as percentage  -- Integer division!
FROM sales;

-- Solution: Cast to decimal
SELECT amount,
       amount * 100.0 / SUM(amount) OVER () as percentage
FROM sales;
```

## Practice Exercises

### Exercise 1: Basic Window Functions

```sql
-- 1. Rank employees by salary within each department
SELECT name, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
FROM employees;

-- 2. Calculate running total of sales for each salesperson
SELECT salesperson, sale_date, amount,
       SUM(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
           ROWS UNBOUNDED PRECEDING
       ) as running_total
FROM sales;

-- 3. Find the difference between each sale and the previous sale
SELECT salesperson, sale_date, amount,
       amount - LAG(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
       ) as difference_from_previous
FROM sales;
```

### Exercise 2: Advanced Applications

```sql
-- 4. Calculate 3-month moving average for each salesperson
SELECT salesperson, 
       DATE_FORMAT(sale_date, '%Y-%m') as month,
       SUM(amount) as monthly_total,
       AVG(SUM(amount)) OVER (
           PARTITION BY salesperson 
           ORDER BY DATE_FORMAT(sale_date, '%Y-%m')
           ROWS 2 PRECEDING
       ) as three_month_avg
FROM sales
GROUP BY salesperson, DATE_FORMAT(sale_date, '%Y-%m');

-- 5. Identify top 20% performers each month
SELECT *
FROM (
    SELECT salesperson,
           DATE_FORMAT(sale_date, '%Y-%m') as month,
           SUM(amount) as monthly_sales,
           NTILE(5) OVER (
               PARTITION BY DATE_FORMAT(sale_date, '%Y-%m') 
               ORDER BY SUM(amount) DESC
           ) as quintile
    FROM sales
    GROUP BY salesperson, DATE_FORMAT(sale_date, '%Y-%m')
) ranked
WHERE quintile = 1;  -- Top 20%

-- 6. Calculate year-over-year growth for each salesperson
SELECT salesperson,
       YEAR(sale_date) as year,
       SUM(amount) as annual_sales,
       LAG(SUM(amount)) OVER (
           PARTITION BY salesperson 
           ORDER BY YEAR(sale_date)
       ) as previous_year_sales,
       ROUND(
           (SUM(amount) - LAG(SUM(amount)) OVER (
               PARTITION BY salesperson 
               ORDER BY YEAR(sale_date)
           )) * 100.0 / NULLIF(LAG(SUM(amount)) OVER (
               PARTITION BY salesperson 
               ORDER BY YEAR(sale_date)
           ), 0),
           2
       ) as yoy_growth_pct
FROM sales
GROUP BY salesperson, YEAR(sale_date);
```

### Exercise 3: Complex Scenarios

```sql
-- 7. Create customer RFM analysis (Recency, Frequency, Monetary)
WITH customer_rfm AS (
    SELECT customer_id,
           DATEDIFF(CURDATE(), MAX(order_date)) as recency_days,
           COUNT(*) as frequency,
           SUM(amount) as monetary_value
    FROM orders
    GROUP BY customer_id
)
SELECT customer_id,
       recency_days,
       frequency,
       monetary_value,
       NTILE(5) OVER (ORDER BY recency_days) as recency_score,
       NTILE(5) OVER (ORDER BY frequency DESC) as frequency_score,
       NTILE(5) OVER (ORDER BY monetary_value DESC) as monetary_score
FROM customer_rfm;

-- 8. Detect sudden changes in sales patterns
SELECT salesperson,
       sale_date,
       amount,
       AVG(amount) OVER (
           PARTITION BY salesperson 
           ORDER BY sale_date
           ROWS BETWEEN 6 PRECEDING AND 1 PRECEDING
       ) as avg_previous_7,
       CASE 
           WHEN amount > 1.5 * AVG(amount) OVER (
               PARTITION BY salesperson 
               ORDER BY sale_date
               ROWS BETWEEN 6 PRECEDING AND 1 PRECEDING
           ) THEN 'Spike Up'
           WHEN amount < 0.5 * AVG(amount) OVER (
               PARTITION BY salesperson 
               ORDER BY sale_date
               ROWS BETWEEN 6 PRECEDING AND 1 PRECEDING
           ) THEN 'Spike Down'
           ELSE 'Normal'
       END as anomaly_flag
FROM sales;
```

> [!question] Challenge Exercise Create a query that identifies "streak breakers" - salespeople who had a consistent upward trend for at least 3 periods and then had a significant drop. Consider what constitutes a "significant drop" and how to detect trends.

## Real-World Implementation Examples

### 1. Financial Trading Analysis

```sql
-- Stock price technical analysis
SELECT trading_date,
       closing_price,
       -- Simple moving averages
       AVG(closing_price) OVER (
           ORDER BY trading_date
           ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
       ) as sma_20,
       AVG(closing_price) OVER (
           ORDER BY trading_date
           ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
       ) as sma_50,
       
       -- Price volatility (standard deviation)
       STDDEV(closing_price) OVER (
           ORDER BY trading_date
           ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
       ) as volatility_20,
       
       -- Relative Strength Index (simplified)
       AVG(CASE WHEN closing_price > LAG(closing_price) OVER (ORDER BY trading_date) 
                THEN closing_price - LAG(closing_price) OVER (ORDER BY trading_date) 
                ELSE 0 END) OVER (
           ORDER BY trading_date
           ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
       ) as avg_gains_14,
       
       -- Support and resistance levels
       MIN(closing_price) OVER (
           ORDER BY trading_date
           ROWS BETWEEN 51 PRECEDING AND CURRENT ROW
       ) as support_52week,
       MAX(closing_price) OVER (
           ORDER BY trading_date
           ROWS BETWEEN 51 PRECEDING AND CURRENT ROW
       ) as resistance_52week
       
FROM stock_prices
WHERE symbol = 'AAPL'
ORDER BY trading_date;
```

### 2. Marketing Campaign Analysis

```sql
-- Campaign performance and attribution
WITH campaign_conversions AS (
    SELECT customer_id,
           campaign_id,
           conversion_date,
           conversion_value,
           FIRST_VALUE(campaign_id) OVER (
               PARTITION BY customer_id 
               ORDER BY conversion_date
               ROWS UNBOUNDED PRECEDING
           ) as first_touch_campaign,
           LAST_VALUE(campaign_id) OVER (
               PARTITION BY customer_id 
               ORDER BY conversion_date
               ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
           ) as last_touch_campaign
    FROM conversions
)
SELECT campaign_id,
       COUNT(DISTINCT customer_id) as total_customers,
       SUM(conversion_value) as total_revenue,
       
       -- First-touch attribution
       COUNT(DISTINCT CASE WHEN campaign_id = first_touch_campaign 
                          THEN customer_id END) as first_touch_conversions,
       SUM(CASE WHEN campaign_id = first_touch_campaign 
               THEN conversion_value ELSE 0 END) as first_touch_revenue,
       
       -- Last-touch attribution  
       COUNT(DISTINCT CASE WHEN campaign_id = last_touch_campaign 
                          THEN customer_id END) as last_touch_conversions,
       SUM(CASE WHEN campaign_id = last_touch_campaign 
               THEN conversion_value ELSE 0 END) as last_touch_revenue
               
FROM campaign_conversions
GROUP BY campaign_id;
```

### 3. Supply Chain Optimization

```sql
-- Inventory turnover and demand forecasting
SELECT product_id,
       inventory_date,
       stock_quantity,
       daily_sales,
       
       -- Days of inventory remaining
       stock_quantity / NULLIF(
           AVG(daily_sales) OVER (
               PARTITION BY product_id 
               ORDER BY inventory_date
               ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
           ), 0
       ) as days_of_inventory,
       
       -- Inventory turnover trend
       AVG(daily_sales) OVER (
           PARTITION BY product_id 
           ORDER BY inventory_date
           ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
       ) as avg_daily_sales_30d,
       
       AVG(daily_sales) OVER (
           PARTITION BY product_id 
           ORDER BY inventory_date
           ROWS BETWEEN 59 PRECEDING AND 30 PRECEDING
       ) as avg_daily_sales_prev_30d,
       
       -- Stockout risk prediction
       CASE 
           WHEN stock_quantity / NULLIF(AVG(daily_sales) OVER (
               PARTITION BY product_id 
               ORDER BY inventory_date
               ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
           ), 0) < 7 THEN 'High Risk'
           WHEN stock_quantity / NULLIF(AVG(daily_sales) OVER (
               PARTITION BY product_id 
               ORDER BY inventory_date
               ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
           ), 0) < 14 THEN 'Medium Risk'
           ELSE 'Low Risk'
       END as stockout_risk
       
FROM inventory_levels
WHERE inventory_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY);
```

## Related Topics

- [[SQL Subqueries]] - Alternative approach for analytical queries
- [[Common Table Expressions (CTEs)]] - Readable complex query structure
- [[SQL Performance Optimization]] - Optimizing analytical queries
- [[Advanced SQL]] - Complex query patterns and techniques
- [[Data Analysis with SQL]] - Practical analytical applications
- [[Business Intelligence]] - BI reporting and dashboard queries
- [[Time Series Analysis]] - Specialized temporal data analysis
- [[Statistical Analysis with SQL]] - Statistical functions and methods
- [[Database Indexes]] - Performance optimization for analytical queries

## Summary

### Key Window Function Categories Mastered

- **Ranking Functions**: ROW_NUMBER(), RANK(), DENSE_RANK(), NTILE()
- **Aggregate Functions**: SUM(), AVG(), COUNT(), MIN(), MAX() with OVER clause
- **Value Access Functions**: LAG(), LEAD(), FIRST_VALUE(), LAST_VALUE()
- **Statistical Functions**: PERCENT_RANK(), CUME_DIST(), PERCENTILE_CONT()

### Essential Concepts

- **OVER Clause**: Defines the window specification
- **PARTITION BY**: Creates logical groups for calculations
- **ORDER BY**: Defines sorting within partitions
- **Window Frames**: ROWS and RANGE specifications for calculation boundaries
- **Frame Boundaries**: PRECEDING, FOLLOWING, CURRENT ROW options

### Advanced Patterns Learned

✅ **Running Calculations**: Cumulative sums, running averages, progressive counts  
✅ **Period Comparisons**: LAG/LEAD for period-over-period analysis  
✅ **Ranking and Percentiles**: Top N queries, quartile analysis  
✅ **Trend Analysis**: Moving averages, trend detection, anomaly identification  
✅ **Complex Analytics**: Cohort analysis, RFM scoring, session identification

### Performance Best Practices

- **Index Strategy**: Proper indexing on PARTITION BY and ORDER BY columns
- **Window Reuse**: WINDOW clause for multiple functions with same specification
- **Frame Optimization**: Careful selection of frame boundaries for performance
- **Alternative Evaluation**: When to use JOINs or subqueries instead

### Business Applications Covered

- **Sales Performance**: Rankings, territories, quota attainment
- **Financial Analysis**: Running totals, period comparisons, variance analysis
- **Customer Analytics**: Cohort analysis, lifetime value, behavior patterns
- **Inventory Management**: Demand forecasting, turnover analysis
- **Marketing Attribution**: Multi-touch attribution, campaign performance

### What You Can Do Now

- ✅ Create sophisticated analytical queries without GROUP BY limitations
- ✅ Calculate running totals, moving averages, and period comparisons
- ✅ Perform ranking and percentile analysis
- ✅ Detect trends and anomalies in time series data
- ✅ Build complex business intelligence reports
- ✅ Optimize window function performance
- ✅ Choose appropriate window functions for different analytical needs

### Next Learning Goals

- [ ] Master [[Common Table Expressions (CTEs)]] for complex hierarchical queries
- [ ] Explore [[Recursive Queries]] for tree and graph data structures
- [ ] Learn [[Advanced SQL Optimization]] techniques for analytical workloads
- [ ] Study [[Time Series Analysis]] specialized functions and patterns
- [ ] Practice [[Statistical Analysis with SQL]] for data science applications

### Modern SQL Evolution

Window functions represent modern SQL's analytical capabilities, moving beyond traditional GROUP BY limitations. They're essential for:

- **Data Science**: Statistical analysis and feature engineering
- **Business Intelligence**: Dynamic dashboards and KPI calculations
- **Financial Analysis**: Time series analysis and forecasting
- **Web Analytics**: User behavior analysis and funnel optimization

> [!tip] Mastery Path Window functions are among the most powerful features in modern SQL. Start with simple ranking and running totals, then progress to complex frame specifications and multi-dimensional analysis. Practice with real datasets to understand performance implications and business applications.

> [!note] Database Compatibility While the SQL standard defines window functions, implementation details vary:
> 
> - **PostgreSQL, SQL Server, Oracle**: Full feature support
> - **MySQL 8.0+**: Comprehensive window function support
> - **SQLite 3.25+**: Basic window function support
> - **Older databases**: May require workarounds using self-joins

---

_Tags: #SQL #WindowFunctions #AdvancedSQL #DataAnalysis #Analytics #BusinessIntelligence #Ranking #RunningTotals #TimeSeriesAnalysis #PerformanceOptimization #ModernSQL_