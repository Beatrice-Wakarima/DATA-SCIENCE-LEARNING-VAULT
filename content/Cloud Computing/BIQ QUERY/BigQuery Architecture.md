

### **Columnar Data**

- Stores data in a column‑oriented format.
    
- Each column indexed separately → faster read‑intensive workflows.
    
- Queries only scan required columns, not entire rows.
    
- **Metaphor:** Car factory parts stored individually. 🔗 Reference: [Column‑oriented databases](https://www.primarydigit.com/blog/-a-brief-introduction-to-column-oriented-databases)
    

### **Capacitor**

- Introduced in 2016 for semi‑structured data.
    
- Each column stored in a separate Capacitor file.
    
- Highly compressed → faster queries.
    
- **Metaphor:** Organized warehouse of car parts.
    

### **Colossus**

- Google’s distributed file system.
    
- Handles replication, recovery, distributed management.
    
- Each data center has its own Colossus cluster.
    
- **Metaphor:** Assembly line workers distributing tasks.
    

### **Jupiter**

- Connects storage ↔ compute.
    
- Transfers terabytes at petabit bandwidth/sec.
    
- Equivalent to 100,000 servers at 10 GB/s.
    
- **Metaphor:** Robotics moving parts quickly.
    

### **Dremel**

- Query execution engine.
    
- Splits queries into logical levels for efficiency.
    
- **Metaphor:** Assembly line order ensuring effective car assembly.
    

### **Borg**

- Cluster management system with thousands of CPU cores.
    
- Allocates resources, routes around failures.
    
- **Metaphor:** Factory foreperson keeping operations smooth.
    

### **Execution Tree**

- Hierarchical query execution: root → mixers → leaves.
    
- Root reads metadata, mixers optimize, leaves execute.
    
- Leaf nodes pull data from Colossus, apply filters, aggregate.
    
- Slots calculated per query complexity → parallelization.
    

### **Categorized Architecture**

- **Storage:** Capacitor, Colossus
    
- **Compute:** Jupiter, Borg
    
- **Execution:** Dremel (engine, mixers, leaves, slots, tree) 🔗 Reference: [BigQuery Architecture Guide](https://panoply.io/data-warehouse-guide/bigquery-architecture/)