

## Databases

- Traditional relational storage → row-column tables.
    
- Ideal for day-to-day operations.
    
- **Cloud SQL** provides managed relational database services.
    

## Global Scale Needs

- Multiple branches accessing databases simultaneously requires scalability.
    
- **Cloud Spanner** → fully managed relational database with unlimited scale.
    
- Supports multiple concurrent read/write operations.
    
- Combines relational consistency with scalability of unstructured systems.
    

## Data Warehousing

- Designed for repeated operations over large datasets.
    
- Collects, sorts, and collates data for analysis.
    
- Optimized for **reading and querying**, not writing.
    
- Central hub for analytics across multiple sources.
    

## BigQuery

- Fully managed, serverless data warehouse.
    
- Performs complex queries across massive datasets.
    
- Scales automatically with workload.
    
- Integrated with **Looker** for BI dashboards and interactive visualizations.
    

## Data Lakes

- Centralized storage for structured, semi-structured, and unstructured data.
    
- Store raw data without categorization.
    
- Highly flexible, capable of handling petabytes from diverse sources (social media, mobile devices, transactions).
    
- Enable big data analytics and machine learning.
    
- **BigLake** integrates BigQuery with data lakes for unified analytics.
    

## Retail Example

- **Cloud SQL** → transactional data (inventory, sales).
    
- **Cloud Spanner** → global-scale relational operations.
    
- **BigQuery + Looker** → analytics and dashboards.
    
- **BigLake** → unified repository for diverse data sources.