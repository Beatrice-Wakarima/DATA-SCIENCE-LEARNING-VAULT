#  ETL Data Pipeline Documentation: Revenue Analysis Platform

**Author:** Beatrice Builds
**Target Environment:** Dockerized PostgreSQL Warehouse (v18-alpine)

## 1. Process Overview

### Architecture Diagram

The platform utilizes a structured **Medallion Architecture** to move data from unstructured files to optimized business models.

Code snippet

```
graph TD
    subgraph Local File System
        Excel[ data/*.xlsx Files]
    end

    subgraph Docker Container Environment
        ETL[etl_runner: Python 3.11-slim]
        DB[(postgres_warehouse: Postgres 18)]
    end

    Excel -->|Volume Mount: ./data| ETL
    ETL -->|1. Ingest: to_sql| Bronze[(raw schema)]
    Bronze -->|2. Clean: VIEW| Silver[(staging schema)]
    Silver -->|3. Model: CREATE TABLE| Gold[(analytics schema)]
    Gold -->|4. Consume: Port 5439| PBI[Power BI / pgAdmin Client]

    style Excel fill:#f9f,stroke:#333,stroke-width:2px
    style ETL fill:#bbf,stroke:#333,stroke-width:2px
    style DB fill:#bfb,stroke:#333,stroke-width:2px
```

### Narrative Workflow

1. **Extraction:** A Python ingestion engine (`etl_runner`) uses `glob` to dynamically scan the local mounted `./data` directory for modern Excel files.
    
2. **Loading (Bronze):** Dataframes are batched and directly streamed into a dedicated `raw` isolation schema inside PostgreSQL with idempotent `replace` execution rules.
    
3. **Transformation (Silver):** Raw tables are sanitized through database views within the `staging` schema to enforce strict lowercase `snake_case` properties, handle null anomalies, and normalize text casing.
    
4. **Modeling (Gold):** Cleaned entities are materialized physically into the `analytics` core schema as fully keyed Dimension and Fact tables, optimized for star-schema analytical tooling.
    

### Platform Stakeholders

- **Data Engineering:** Beatrice Builds (Pipeline author, system architect)
    
- **Business Consumers:** Executive Leadership, Revenue Operations Team, Finance Managers
    
- **Downstream Systems:** Power BI Financial Analytics Dashboards
    

## 🗃️ 2. Data Source Inventory

|**File Name**|**Ingestion Frequency**|**Format**|**Target Table Name**|**Data Ownership**|
|---|---|---|---|---|
|`Capital_Budgeting.xlsx`|Ad-hoc / Monthly|`.xlsx` (OpenPyXL)|`raw.capital_budgeting_cash_flow`|Corporate Finance|
|`Employee_Fact.xlsx`|Monthly|`.xlsx` (OpenPyXL)|`raw.employee_fact_sheet1`|Human Resources|
|`revenue_targets.xlsx`|Quarterly|`.xlsx` (OpenPyXL)|`raw.revenue_targets_revenue_targets`|RevOps Operations|
|`spaero_sales.xlsx`|Daily / Weekly|`.xlsx` (OpenPyXL)|`raw.spaero_sales_sales_fact`<br><br>  <br><br>`raw.spaero_sales_customer_dim`|Global Sales Admin|

## 🗺️ 3. Schema Mapping & Transformation Rules

### Target Entity: `analytics.dim_customers`

This dimension merges, normalizes, and materializes customer identity mappings from the raw sales source ledger.

|**Source Column (raw.spaero_sales_customer_dim)**|**Target Column (analytics.dim_customers)**|**Target Data Type**|**Transformation & Validation Rules Applied**|
|---|---|---|---|
|`customer_id`|`customer_key`|`VARCHAR`|**Primary Key.** Handles null values via `COALESCE(field, 'UNKNOWN')`.|
|`customer_name`|`customer_name`|`VARCHAR`|Applies `UPPER(TRIM(field))` to remove accidental double-spacing and enforce uniformity.|
|`segment`|`customer_segment`|`VARCHAR`|Applies `INITCAP(TRIM(field))` to convert text blocks to standard Title Case formatting.|
|`country`|`country`|`VARCHAR`|Cleaned via Title Case (`INITCAP`). Trims leading/trailing whitespace.|
|`city`|`city`|`VARCHAR`|Cleaned via Title Case (`INITCAP`). Trims leading/trailing whitespace.|
|`postal_code`|`postal_code`|`VARCHAR`|Replaces null or unpopulated codes with `'N/A'`.|
|`region`|`business_region`|`VARCHAR`|Remapped field identifier. Cleaned via standard Title Case string parsing.|

SQL

```
-- Target DDL Schema Generation Blueprint
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;

CREATE OR REPLACE VIEW staging.stg_customers AS 
SELECT 
    COALESCE(customer_id::VARCHAR, 'UNKNOWN') AS customer_key,
    UPPER(TRIM(customer_name)) AS customer_name,
    INITCAP(TRIM(segment)) AS customer_segment,
    INITCAP(TRIM(country)) AS country,
    INITCAP(TRIM(city)) AS city,
    COALESCE(postal_code::VARCHAR, 'N/A') AS postal_code,
    INITCAP(TRIM(region)) AS business_region
FROM raw.spaero_sales_customer_dim
WHERE customer_id IS NOT NULL;
```

## 🚨 4. Error Handling & Validation Queries

### Ingestion Safety Guardrails

- **Connection Debugging Gateway:** Built directly into the script to mask production passwords while revealing connection parameters (`DB_HOST`, `DB_PORT`) to logs before running operations.
    
- **Terminal Flushing:** Leverages `sys.stdout.flush()` inside execution blocks to bypass Docker container logging latencies, ensuring real-time log outputs in case of operational failure.
    
- **Exception Isolation:** Individual workbooks are captured inside `try/except` loop blocks. If one file breaks due to structure decay, the pipeline logs the specific error and proceeds cleanly to parse the next asset.
    

### Data Validation Scripts

SQL

```
-- Validation 1: Integrity Key Duplication Audit
SELECT customer_key, COUNT(*) 
FROM analytics.dim_customers 
GROUP BY customer_key 
HAVING COUNT(*) > 1;

-- Validation 2: Medallion Row Count Synchronization Test
SELECT 
    (SELECT COUNT(*) FROM raw.spaero_sales_customer_dim WHERE customer_id IS NOT NULL) AS raw_count,
    (SELECT COUNT(*) FROM analytics.dim_customers) AS production_count;
```

## 🚀 5. Deployment & Configuration Guide

### Environment Configuration Variables (`.env`)

The pipeline runs on an isolated development sandbox. Secret files should stay strictly localized and out of Git repositories.

Ini, TOML

```
# Database Core Target Credentials
DB_USER=dev_analytics_user
DB_PASSWORD=local_dev_only_password_123!
DB_NAME=revenue_warehouse
DB_PORT=5439
DB_HOST=postgres_warehouse
```

### Infrastructure Configuration Blueprint (`docker-compose.yml`)

YAML

```
version: '3.8'

services:
  postgres_warehouse:
    image: postgres:18-alpine
    container_name: postgres_warehouse
    environment:
      POSTGRES_USER: ${DB_USER:-dev_analytics_user}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-local_dev_only_password_123!}
      POSTGRES_DB: ${DB_NAME:-revenue_warehouse}
    ports:
      - "${DB_PORT:-5439}:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - analytics_network

  etl_runner:
    build: .
    container_name: etl_runner
    environment:
      - DB_USER=${DB_USER:-dev_analytics_user}
      - DB_PASSWORD=${DB_PASSWORD:-local_dev_only_password_123!}
      - DB_NAME=${DB_NAME:-revenue_warehouse}
      - DB_HOST=postgres_warehouse
      - DB_PORT=5432
    volumes:
      - ./data:/app/data
      - ./scripts:/app/scripts
    depends_on:
      - postgres_warehouse
    networks:
      - analytics_network

volumes:
  pgdata:

networks:
  analytics_network:
    driver: bridge
```

### Orchestration Commands

Bash

```
# Force a hard reset to destroy stale artifacts and rebuild environment networks
docker-compose down -v

# Fire up the stack, trigger runtime compilation, and stream execution pipelines
docker-compose up --build
```

## 📊 6. Monitoring & Reporting Gateway

### Pipeline Performance Benchmarks

- **Connection Probe:** `< 1.0s` verification step.
    
- **Ingestion Throughput:** Successfully processed 4 workbooks containing **7,700+ rows** in under 5.0 seconds.
    
- **Database Driver Connectivity:** Utilizing native SQLAlchemy mapping to `psycopg2` binaries inside the slim-Debian runtime layer.
    

### Target Reporting Integration

- **pgAdmin Administration Connection Point:** `localhost` mapped to External Port `5439`. (Bypasses local default database port conflicts).
    
- **Power BI Gateway Routing:** Point the native desktop connector to `localhost:5439` targeting database name `revenue_warehouse`. Primary keys declared in the `analytics` schema will cleanly translate as direct data relationships inside the model dashboard canvas.