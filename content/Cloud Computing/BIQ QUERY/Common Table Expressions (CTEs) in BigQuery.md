

### **Definition**

- Named temporary result sets within a query.
    
- Enhance readability and usability.
    
- Exist only within the scope of the query where defined.
    

### **CTEs vs Subqueries**

- **Subqueries** → nested queries, harder to maintain.
    
- **CTEs** → modular, reusable, improve readability.
    
- Example: `WITH cte_name AS (...) SELECT ... FROM cte_name`.
    

### **Writing CTEs**

- Step 1: Use `WITH` clause to define CTE name and structure.
    
- Step 2: Reference the CTE in the main query.
    
- Scope limited to the query block.
    

### **Multiple CTEs**

- Use `WITH` once, then define multiple CTEs separated by commas.
    
- Each CTE begins with `cte_name AS (...)`.
    
- Later CTEs can reference earlier ones.
    

### **Filtering Data**

- Efficient way to filter and organize subsets before querying.
    
- Example: `filtered_data` CTE returns only rows meeting conditions.
    
- Main query runs on fewer rows → faster performance.
    

### **Optimizing Queries**

- Precompute complex logic or repetitive subqueries.
    
- Store aggregated values in a CTE.
    
- Reduces redundant calculations → improves query speed.
    

### **Joining Data**

- Define intermediate results of joins in CTEs.
    
- Reference them in the final query.
    
- Makes queries more concise and easier to follow.
    

### **Cheat Sheet**

- **WITH clause** → define CTEs.
    
- **Scope** → limited to query.
    
- **Multiple CTEs** → modular, can reference each other.
    
- **Use cases** → filtering, optimization, joins.