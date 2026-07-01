

### **Simple Queries**

- Syntax similar to other SQL databases.
    
- Core SQL commands (SELECT, WHERE, GROUP BY, etc.) apply.
    
- Differences arise from GoogleSQL functions and datatypes.
    

### **Running Queries**

- Options for execution:
    
    - Google BigQuery Studio (Cloud Console)
        
    - Client libraries (Python, Java, etc.)
        
    - Command line (gcloud CLI)
        
    - Pandas functions → DataFrames
        

### **Table Name Formatting**

- Full format: `project.dataset.table`.
    
- If querying within default project → `dataset.table` is sufficient.
    

### **GoogleSQL**

- BigQuery’s dialect of SQL.
    
- Core SQL elements remain.
    
- Differences:
    
    - Specific functions
        
    - Datatypes (e.g., integers/floats are base‑64 encoded)
        

### **Datasets: Olist E‑Commerce**

- Source: [Kaggle Olist Brazilian E‑Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
    
- Modified for course use.
    
- Four main tables:
    
    - **Products** → product details (photos, weight, category)
        
    - **Orders** → order‑id, nested order‑items (product/seller IDs, price)
        
    - **Order Details** → order/customer IDs, status, timestamps for delivery stages
        
    - **Payments** → payment type, installments, value
        

### **Aggregations & Joins**

- Core components of analytical queries:
    
    1. Aggregation function (e.g., `COUNT`)
        
    2. Left dataset in join (e.g., `order_details`)
        
    3. Right dataset in join (e.g., `orders`)
        
    4. Join condition (`ON` or `USING`)
        
    5. Group By condition (e.g., `customer_id`)