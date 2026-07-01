

### **Methods of Loading Data**

- **BigQuery Studio (UI)**
    
- **bq command line tools**
    
- **LOAD DATA SQL command**
    
- Note: excludes streaming ingestion & external tools (covered separately).
    

### **BigQuery Studio**

- Upload files from local computer or Google Cloud Storage.
    
- Supported formats: Avro, CSV, JSON, ORC, Parquet.
    
- Must specify **project → dataset → table**.
    
- Schema can be defined via JSON or UI; otherwise auto‑detected.
    

### **bq Command Line Tools**

- Import files from local machine or Google Cloud Storage.
    
- Default project prompted automatically.
    
- URI points to GCS object.
    
- Optional flags for fine‑grained control (e.g., `--format=CSV`, `--autodetect`). 🔗 Reference: [bq command line tool](https://cloud.google.com/bigquery/docs/bq-command-line-tool#loading_data)
    

### **LOAD DATA SQL**

- Load data stored in Google Cloud Storage directly into BigQuery tables.
    
- Syntax: `LOAD DATA INTO dataset.table FROM FILES (...)`.
    
- Arguments:
    
    - URIs (array of GCS files with same schema)
        
    - File format (CSV, JSON, etc.)
        
    - CSV‑specific options (e.g., skip header row)
        
- Many additional arguments for formatting and special use cases.
    

### **Data Ingestion Considerations**

- Local file loading limited to **100 MB**.
    
- LOAD DATA cannot be used for local files (only GCS).
    
- Studio and CLI methods share similar limitations. 🔗 Reference: [BigQuery quotas](https://cloud.google.com/bigquery/quotas#load_jobs)