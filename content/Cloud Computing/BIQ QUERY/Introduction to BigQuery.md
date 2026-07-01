

### **Overview**

- Enterprise-scale data warehouse launched in 2012
    
- Built on Google’s internal tools for storage, analytics, and compute
    
- Enables querying of terabytes/petabytes with SQL
    

### **Unique Features**

- OLAP (online analytical processing) system
    
- Separates compute from storage
    
- Serverless → Google manages resources automatically
    

### **Compute vs Storage**

- Storage and compute clusters are independent
    
- Resources allocated dynamically per query
    
- Analogy: renting shared kitchen space vs owning a full kitchen
    

🔗 Reference: [Google Cloud Storage Overview](https://cloud.google.com/bigquery/docs/storage_overview)

### **Snowflake Comparison**

- Snowflake: multi-cloud (AWS, Azure, GCP)
    
- Popular for BI apps with dynamic querying
    
- Sized compute tiers + serverless
    
- BigQuery: Google Cloud only, auto-scales compute per query
    

### **Redshift Comparison**

- Redshift: AWS-native, supports serverless + dedicated clusters
    
- Strong for real-time dashboards
    
- BigQuery: optimized for scheduled analytical reporting
    

### **Traditional SQL vs BigQuery**

- MySQL/PostgreSQL → OLTP (transactional: inserts, updates, deletes)
    
- Compute + storage tightly coupled
    
- BigQuery → OLAP, distributed queries, separated compute/storage
    

### **Use Cases**

- Scheduled reports (daily sales, quarterly analytics)
    
- Complex queries for presentations
    
- Ad-hoc discovery (marketing analytics, raw data exploration)