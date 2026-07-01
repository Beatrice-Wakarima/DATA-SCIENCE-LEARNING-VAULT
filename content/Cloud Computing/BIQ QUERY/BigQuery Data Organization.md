

### **Table Names**

- Format differs from traditional SQL databases.
    
- Full name includes **project → dataset → table** hierarchy.
    

### **Projects**

- Top‑level structure in Google Cloud.
    
- Manage users, permissions, and billing.
    
- A user can belong to multiple projects.
    
- First element in a BigQuery table name.
    

### **Datasets**

- Equivalent to schemas in SQL databases.
    
- Contain tables underneath them.
    
- Have their own permissions → users can query/join across datasets.
    
- Second element in a BigQuery table name.
    

### **Tables**

- Final element in the table name.
    
- Actual data resides here.
    

### **Regions**

- Google Cloud regions = physical data centers.
    
- Some regions contain multiple zones (e.g., Iowa has 4 zones).
    
- Two multi‑regions:
    
    - **United States** (all US data centers)
        
    - **European Union** (all EU member data centers)
        

- ![Google Cloud expands footprint with 34 global regions – IEEE ComSoc ...](https://ts1.mm.bing.net/th?id=OIP.59VYSY__Nex7mdCSvFDjqgHaEK&pid=15.1&o=7&rm=3)
    
- ![Google Cloud announces new regions, open source partnerships, Cloud Run ...](https://ts2.mm.bing.net/th?id=OIP.vfOpEX9wsYO2KHxlIzHUqAHaDt&pid=15.1&o=7&rm=3)
    

### **Cross‑Region Data**

- Dataset region is **permanent** once created.
    
- Data can be replicated/moved between regions.
    
- Queries cannot span across different regions due to physical resource allocation.