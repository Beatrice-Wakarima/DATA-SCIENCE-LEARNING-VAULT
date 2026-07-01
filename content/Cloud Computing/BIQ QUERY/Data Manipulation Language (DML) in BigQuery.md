

## Overview

- DML allows modification of data in BigQuery using SQL-like syntax.
    
- Statements include: **INSERT**, **UPDATE**, **DELETE**, **MERGE**, and **CREATE TABLE AS**.
    
- Useful for adjusting results or underlying tables beyond batch/stream ingestion.
    
- Reference: [Google Docs](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-manipulation-language)
    

## Performance Considerations

- Group DML statements instead of row-by-row operations.
    
- Always use a `WHERE` clause to filter affected rows.
    
- Consider **partitioning** or **clustering** datasets for efficiency.
    

## INSERT

- Adds new records to a table.
    
- Example: inserting three new customers into the `customers` dataset.
    
- Syntax:
    
    sql
    
    ```
    INSERT INTO customers (id, name, email)
    VALUES (1, 'Alice', 'alice@email.com');
    ```
    

## UPDATE

- Modifies existing records based on conditions.
    
- Can update multiple columns.
    
- Supports subqueries and joins.
    
- Example: updating a customer’s email address.
    

## DELETE

- Removes rows permanently based on conditions.
    
- Can use joins to filter deletions.
    
- Example: deleting customer with `customer_id = 3`.
    

## MERGE

- Combines **INSERT**, **UPDATE**, and **DELETE** in one operation.
    
- Requires:
    
    - Target table (e.g., `customers`)
        
    - Source table (e.g., `new_customers`)
        
    - Matching condition (e.g., `customer_id`)
        
- Example logic:
    
    - If match → update email.
        
    - If no match → insert new record.
        
- Enables complex conditional data manipulation.
    

## CREATE TABLE AS

- Creates a new table from query results.
    
- Example:
    
    sql
    
    ```
    CREATE TABLE active_customers AS
    SELECT * FROM customers
    WHERE last_active > DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY);
    ```
    
- Useful for snapshotting filtered datasets.