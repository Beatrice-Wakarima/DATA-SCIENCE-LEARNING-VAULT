

### **Definition**

- Also called analytic functions.
    
- Perform calculations over a dynamic set of rows (“window”).
    
- Enable running totals, moving averages, ranks, and contextual analysis.
    

### **Purpose**

- Reveal hidden patterns across data ranges.
    
- Work like a magnifying glass: focus on specific rows while considering dataset context.
    
- Example: sum of current row + prior two rows.
    

### **Use Cases**

- Trends and time‑series analysis.
    
- Moving averages.
    
- Ranking items within groups.
    
- Outlier detection. 🔗 Reference: [Guide to advanced SQL window functions](https://towardsdatascience.com/a-guide-to-advanced-sql-window-functions-f63f2642cbf9)
    

### **Structure: PARTITION & ORDER BY**

- Syntax: `function() OVER (PARTITION BY ... ORDER BY ...)`.
    
- **PARTITION BY** → groups rows (e.g., by `customer_id`).
    
- **ORDER BY** → defines sequence (e.g., by `order_date`).
    
- Example: sequential row numbers per customer’s orders.
    

### **RANK & PERCENT_RANK**

- **RANK()** → ordinal rank within window.
    
- **PERCENT_RANK()** → percentile rank (percentage below current row).
    
- Example: rank products by number of photos.
    

### **LAG & LEAD**

- **LAG()** → value from previous row.
    
- **LEAD()** → value from next row.
    
- Example: compare current row with prior/next values.
    

### **RANGE BETWEEN & CURRENT ROW**

- Defines flexible window frames relative to current row.
    
- Example: sum of item price for current + 2 preceding rows.
    
- Options: bounded (specific rows) or unbounded (all before/after).
    

### **QUALIFY**

- Filters results based on window function output.
    
- Example: return only rows with rank ≤ 3.
    
- Acts like `WHERE` but for window conditions (not aggregates).
    

### **Cheat Sheet**

- **RANK / PERCENT_RANK** → ranking
    
- **LAG / LEAD** → previous/next values
    
- **RANGE BETWEEN** → flexible frames
    
- **QUALIFY** → filter by window condition