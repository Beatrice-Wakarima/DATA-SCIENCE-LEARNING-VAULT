 

### **Introduction**

- Designed for large datasets → faster, resource‑efficient approximations.
    
- Categories:
    
    - Approximate aggregations
        
    - String/array manipulation
        
    - Logical operations
        

### **ARRAY_CONCAT_AGG**

- Merges multiple arrays into one aggregated array.
    
- Example: combine `order_items` arrays into a single `all_items` array.
    
- Simplifies handling of grouped array data.
    

### **STRING_AGG**

- Concatenates strings into one string.
    
- Optional delimiter for separation.
    
- Example: customer IDs separated by commas with delivery dates.
    

### **APPROX_COUNT_DISTINCT**

- Estimates distinct counts quickly.
    
- Useful for massive datasets where exact counts are expensive.
    
- Example: approximate distinct `order_id` count grouped by `customer_id`.
    

### **APPROX_QUANTILES**

- Estimates quantiles for numeric columns.
    
- Performance advantage over exact percentile functions.
    
- Example: approximate quartiles (4 bins) for product categories.
    

### **APPROX_TOP_COUNT**

- Identifies top K elements by frequency.
    
- Probabilistic → efficient for large datasets.
    
- Example: top 3 customers by product category.
    

### **APPROX_TOP_SUM**

- Finds top K elements and aggregates their sum.
    
- Arguments: category, numeric column (e.g., price), K.
    
- Example: top 3 items per seller with total sales.
    

### **LOGICAL_AND / LOGICAL_OR**

- Aggregate boolean logic across grouped data.
    
- **LOGICAL_AND** → true if all conditions true.
    
- **LOGICAL_OR** → true if at least one condition true.
    
- Example: check if all orders shipped vs at least one shipped.
    

### **Cheat Sheet**

- **ARRAY_CONCAT_AGG** → merge arrays
    
- **STRING_AGG** → concatenate strings
    
- **APPROX_COUNT_DISTINCT** → fast distinct counts
    
- **APPROX_QUANTILES** → approximate percentiles
    
- **APPROX_TOP_COUNT** → top K by frequency
    
- **APPROX_TOP_SUM** → top K by sum
    
- **LOGICAL_AND / OR** → boolean aggregation