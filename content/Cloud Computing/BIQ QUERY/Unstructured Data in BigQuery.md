

### **Why It Matters**

- Common in BigQuery for complex row‑level structures.
    
- Example: customer record with multiple email addresses.
    

### **ARRAYs**

- Ordered lists of zero or more elements (like Python lists).
    
- Access via functions or square brackets (`array[0]` = first element).
    
- Example: construct array from subquery, access second value with `[1]`.
    

### **STRUCTs**

- Flexible structures (like Python dicts or JSON).
    
- Can contain single values, key‑value pairs, or nested ARRAYs/STRUCTs.
    
- Must remain consistent across column values.
    
- Access keys with dot notation (`struct.key`).
    

### **ARRAY Functions**

- `ARRAY_LENGTH(array)` → number of elements.
    
- `ARRAY_CONCAT(array1, array2)` → join arrays together.
    

### **UNNEST**

- Flattens ARRAYs into rows.
    
- Example: ARRAY of two emails → two rows.
    

### **UNNEST with STRUCTs**

- STRUCTs inside ARRAYs can be flattened.
    
- Example: column `skills` with ARRAY of STRUCTs.
    
- Use `UNNEST` in `FROM`, then dot notation in `SELECT` to extract values.
    

### **SEARCH**

- Flexible function to query across any data type.
    
- Especially useful for unstructured data.
    
- Syntax: `SEARCH(data, query)` → returns boolean.
    
- Example: check if any email in STRUCT ends with `gmail.com`.
    

### **Cheat Sheet**

- **ARRAY** → ordered list, indexed access, concat, length.
    
- **STRUCT** → key‑value, nested flexibility, dot notation.
    
- **UNNEST** → flatten arrays/structs into rows.
    
- **SEARCH** → query across arrays/structs for terms.