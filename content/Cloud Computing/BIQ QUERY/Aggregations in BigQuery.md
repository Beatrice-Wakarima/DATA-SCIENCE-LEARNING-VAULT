

### **Definition**

- Operations that summarize large datasets into concise results.
    
- Essential for trend analysis, pattern recognition, and decision‑making.
    
- BigQuery’s scalability, columnar storage, and distributed processing make it ideal for aggregations.
    

### **GROUP BY & ORDER BY**

- **GROUP BY** → organizes data into groups.
    
- **ORDER BY** → sorts results (e.g., descending by total cost).
    
- Example: group sales by `order_id` and calculate totals.
    

### **COUNT**

- Counts rows returned by query.
    
- Example: count records per category in product dataset.
    
- Useful for dataset size and distribution analysis.
    

### **SUM & AVG**

- **SUM** → total of numeric values.
    
- **AVG** → average of numeric values.
    
- Example: total and average sales per category.
    

### **MIN & MAX**

- **MIN** → lowest value in group.
    
- **MAX** → highest value in group.
    
- Example: min/max photo counts in `ecomm_products`.
    
- Useful for range analysis and identifying outliers.
    

### **COUNTIF**

- Conditional count based on criteria.
    
- Example: `COUNTIF(cost > 500)` → number of records per category with cost > $500.
    
- Valuable for frequency analysis of specific conditions.
    

### **HAVING**

- Filters grouped data based on aggregate conditions.
    
- Example: categories with average item price > $75.
    
- Acts like `WHERE` but for aggregated results.
    

### **ANY_VALUE**

- Returns an arbitrary value from grouped data.
    
- Useful when non‑aggregated columns are needed in grouped queries.
    
- Example: arbitrary product category from each group.
    
- Can combine with `HAVING` to return min/max values from another column.
    

### **Cheat Sheet**

- **COUNT** → row counts
    
- **SUM / AVG** → totals & averages
    
- **MIN / MAX** → boundaries & outliers
    
- **COUNTIF** → conditional counts
    
- **GROUP BY / ORDER BY** → organize & sort
    
- **HAVING** → filter aggregated results
    
- **ANY_VALUE** → arbitrary non‑aggregated values