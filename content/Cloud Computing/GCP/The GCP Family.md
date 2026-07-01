

## Storage Cousins

- **Cloud Storage** → efficient storage for files and objects.
    
- **Cloud SQL** → relational database for structured tabular data.
    

## Non-Relational Data

- Some data (e.g., org charts, hierarchical trees) cannot be stored efficiently in tables.
    
- This is **non-relational data**, which doesn’t fit the row-column model.
    

## Bigtable

- Handles both tabular and non-relational data.
    
- Optimized for large operational and analytical workloads.
    
- Provides low latency and high throughput.
    
- Ideal for IoT, finance, and ad tech applications.
    

## App Engine vs Cloud Functions

- **App Engine** → designed for full-fledged web applications with UI and complex backend logic.
    
- **Cloud Functions** → best for single-purpose, event-driven functions.
    
    - Example: triggered by document upload.
        
    - Charged per request → cost-efficient for sporadic usage.
        

## Serverless Computing

- Both App Engine and Cloud Functions are serverless.
    
- Analogy: ordering coffee at a café instead of brewing it yourself.
    
- GCP manages servers behind the scenes; you only pay for what you consume.
    

## Containers

- Applications packaged with dependencies into portable “containers.”
    
- Ensures consistent behavior across environments (local, test, cloud).
    
- Lightweight compared to virtual machines.
    
- Up to 20 containers can run on one computer.
    

## Virtual Machines vs Containers

- **Virtual Machines (VMs)** → full OS environment, ideal for specific software needs.
    
- **Containers** → lightweight, only essential components included.
    
- Containers are faster to deploy and more resource-efficient.
    

## Containerized Applications

- Example: online shopping platform.
    
    - Containers for user authentication, product listings, payment processing, etc.
        
- Each container provides a microservice.
    

## Microservices

- Break large applications into smaller, independent units.
    
- Benefits:
    
    - Easier development and scalability.
        
    - Fault isolation → one container failing doesn’t affect others.
        
- Example: scaling only the search container during high demand.