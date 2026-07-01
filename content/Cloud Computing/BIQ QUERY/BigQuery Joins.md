

## Overview

- Joins combine multiple datasets for analysis.
    
- BigQuery supports familiar SQL join types: inner, left, right, full outer, and cross.
    
- Syntax is similar to other relational databases.
    

## Real-Life Examples

- **Inner Join** → customers with orders only.
    
- **Left Join** → all customers, even without orders.
    
- **Right Join** → all orders, even without customer IDs.
    
- **Full Outer Join** → all customers + all orders, matched or not.
    
- **Cross Join** → every customer paired with every order.
    

## INNER JOIN

- Combines rows where values match in both tables.
    
- Ideal for correlated data points.
    
- Example: `customers JOIN sales_data ON customer_id`.
    
- `INNER` keyword is optional.
    

## LEFT JOIN

- Returns all rows from the left table.
    
- Non-matching rows show `NULL` values.
    
- Example: customers with no orders still appear.
    

## RIGHT JOIN

- Returns all rows from the right table.
    
- Non-matching rows show `NULL` values.
    
- Example: orders without a customer ID.
    

## FULL OUTER JOIN

- Combines left and right join results.
    
- Captures unmatched customers and unmatched orders.
    
- Useful for comprehensive analysis.
    

## CROSS JOIN

- Cartesian product: every row from one table joined to every row in another.
    
- Example: 10 customers × 10 orders = 100 rows.
    
- Often used with `UNNEST`.
    

## Joins with UNNEST

- Cross joins help flatten arrays.
    
- Example: unnesting payment methods per customer.