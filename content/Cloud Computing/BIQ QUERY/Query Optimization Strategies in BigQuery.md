

## Three Rules of Thumb

- Reduce the amount of data processed.
    
- Optimize operations within the query.
    
- Reduce the query output as much as possible.
    
- Reference: [BigQuery Performance Best Practices](https://cloud.google.com/bigquery/docs/best-practices-performance-compute#use-bi-engine)
    

## Reducing Data Scanned

- Select only the columns you need.
    
- Apply `WHERE` filters early in the query.
    
- Use **CTEs** to filter subsets before final joins.
    
- Smaller datasets → faster queries.
    

## Optimizing Joins

- Limit data before the join step.
    
- Prefer joining on **INT64** keys for efficiency.
    
- Fewer possible combinations → faster joins.
    

## Optimizing WHERE Clause

- Use efficient data types: **BOOLEAN, INTEGER, FLOAT, DATE**.
    
- Avoid filtering on **STRING** or **BYTES** when possible.
    
- Example:
    
    - Less efficient: `WHERE product_name = 'shoes'`
        
    - More efficient: `WHERE product_id = 101`
        

## ORDER BY Optimizations

- `ORDER BY` can be costly on large datasets.
    
- Avoid using `ORDER BY` inside CTEs.
    
- Place `ORDER BY` in the **outermost query**.
    
- Trade-off: adding extra columns may be cheaper than sorting large intermediate results.
    

## EXISTS vs COUNT

- **COUNT** aggregates all rows even after condition is met.
    
- **EXISTS** stops scanning once a match is found.
    
- More efficient for existence checks.
    
- Example:
    
    sql
    
    ```
    SELECT EXISTS (
      SELECT 1 FROM customers WHERE customer_id = 3
    );
    ```
    

## Other Optimization Methods

- Use **approximate aggregate functions** (e.g., `APPROX_COUNT_DISTINCT`).
    
- Filter queries by **date partitions** to reduce scanned data.
    
- Partitioning and clustering improve performance on large tables.