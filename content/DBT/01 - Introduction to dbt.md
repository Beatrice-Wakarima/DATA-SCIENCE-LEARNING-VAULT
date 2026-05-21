---
title: Introduction to dbt
tags: [dbt, data-engineering, sql, basics]
created: 2026-05-20
up:: [[DBT MOC]]
---

# 🔧 Introduction to dbt

> dbt (data build tool) transforms raw data in your warehouse using SQL and software engineering best practices — version control, testing, documentation, and modular code. It is the most important tool in the modern data stack.

---

## What Problem Does dbt Solve?

```
Before dbt:
  ❌ SQL transformations scattered in random .sql files
  ❌ No testing — bad data goes undetected
  ❌ No documentation — nobody knows what tables mean
  ❌ No lineage — can't trace where data comes from
  ❌ No version control — changes break things silently
  ❌ Manual execution — someone has to remember to run queries

After dbt:
  ✅ All transformations in one organised project
  ✅ Automated tests on every model
  ✅ Auto-generated documentation with lineage graphs
  ✅ Git-based version control
  ✅ Scheduled execution via Airflow or dbt Cloud
```

---

## Where dbt Fits

```
Data Sources → Extract & Load → Data Warehouse → dbt → BI Tool
(APIs, CSVs)   (Fivetran,        (Snowflake,    (Transform)  (Power BI,
               Airbyte,          BigQuery,                    Tableau)
               Python)           Postgres)
                                      ↑
                               dbt lives HERE
                         (Transform inside the warehouse)
```

dbt does the **T** in ELT. It doesn't extract or load — it transforms data that's already in your warehouse.

---

## dbt Core vs dbt Cloud

| | dbt Core | dbt Cloud |
|---|---|---|
| Cost | Free, open source | Free tier + paid |
| Interface | CLI | Web UI |
| Scheduling | Via Airflow/cron | Built-in scheduler |
| IDE | VS Code | Browser IDE |
| Docs hosting | Self-hosted | Hosted |
| Best for | Data engineers | Teams, analysts |

---

## Installation

```bash
# Install dbt Core for PostgreSQL
pip install dbt-postgres

# For other warehouses
pip install dbt-snowflake
pip install dbt-bigquery
pip install dbt-redshift
pip install dbt-databricks

# Verify
dbt --version
```

---

## The Modern Data Stack

```
┌─────────────────────────────────────────────────────────┐
│                    Modern Data Stack                    │
├─────────────┬──────────────┬───────────┬───────────────┤
│   Ingest    │   Storage    │ Transform │  Visualise    │
│             │              │           │               │
│  Fivetran   │  Snowflake   │   dbt     │   Power BI    │
│  Airbyte    │  BigQuery    │           │   Tableau     │
│  Python     │  Postgres    │           │   Metabase    │
│  Kafka      │  Redshift    │           │   Looker      │
└─────────────┴──────────────┴───────────┴───────────────┘
```

---

## dbt Project Structure

```
my_dbt_project/
│
├── dbt_project.yml          ← Project configuration
├── profiles.yml             ← Database connections
│
├── models/                  ← SQL transformation files
│   ├── staging/             ← Layer 1: Clean raw data
│   │   ├── stg_customers.sql
│   │   ├── stg_transactions.sql
│   │   └── _stg_sources.yml  ← Source definitions
│   │
│   ├── intermediate/        ← Layer 2: Business logic
│   │   ├── int_customer_orders.sql
│   │   └── int_transaction_summary.sql
│   │
│   └── marts/               ← Layer 3: Business-ready
│       ├── finance/
│       │   ├── fct_revenue.sql
│       │   └── dim_customers.sql
│       └── marketing/
│           └── fct_campaign_performance.sql
│
├── tests/                   ← Custom test SQL
│   └── assert_positive_balance.sql
│
├── macros/                  ← Reusable SQL functions
│   └── generate_surrogate_key.sql
│
├── seeds/                   ← Static CSV data
│   └── country_codes.csv
│
├── snapshots/               ← SCD Type 2 tracking
│   └── customers_snapshot.sql
│
└── docs/                    ← Documentation assets
    └── overview.md
```

---

## Key dbt Concepts

```
Model       = A SQL SELECT statement in a .sql file
              dbt builds it as a table or view

Source      = Raw table in your warehouse (not built by dbt)
              Defined in YAML, referenced with source()

Ref         = Reference to another dbt model
              {{ ref('model_name') }}

Test        = Assertion about your data
              Not null, unique, accepted values, etc.

Seed        = CSV file loaded into warehouse as a table
              Static lookup data

Snapshot    = Tracks historical changes (SCD Type 2)

Macro       = Reusable Jinja SQL function

Lineage     = Auto-generated DAG showing model dependencies
```

---

## Materialisation Types

```sql
-- View (default) — runs query every time, no storage
{{ config(materialized='view') }}
SELECT ...

-- Table — stores results, faster for BI tools
{{ config(materialized='table') }}
SELECT ...

-- Incremental — only processes new/changed rows (FAST!)
{{ config(materialized='incremental') }}
SELECT ...
{% if is_incremental() %}
WHERE created_at > (SELECT MAX(created_at) FROM {{ this }})
{% endif %}

-- Ephemeral — CTE, used in other models, never stored
{{ config(materialized='ephemeral') }}
SELECT ...
```

---

## Your First dbt Project

```bash
# Initialise new project
dbt init my_project
cd my_project

# Project structure created automatically
ls
# dbt_project.yml  models/  tests/  macros/  seeds/  snapshots/

# Test connection to database
dbt debug

# Run all models
dbt run

# Run specific model
dbt run --select stg_customers

# Run tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve      # Opens browser at localhost:8080

# Run + test in one command
dbt build
```

---

## dbt_project.yml

```yaml
# dbt_project.yml — project configuration
name: 'bank_marketing'
version: '1.0.0'
config-version: 2

profile: 'bank_marketing'   # Points to profiles.yml

# File paths
model-paths: ["models"]
seed-paths: ["seeds"]
test-paths: ["tests"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

# Default materialisation per folder
models:
  bank_marketing:
    staging:
      +materialized: view       # Staging = views (cheap)
      +schema: staging
    intermediate:
      +materialized: ephemeral  # Intermediates = CTEs
    marts:
      +materialized: table      # Marts = tables (fast for BI)
      +schema: marts
      finance:
        +materialized: table
      marketing:
        +materialized: table
```

---

## profiles.yml — Database Connection

```yaml
# ~/.dbt/profiles.yml (stored in home directory)
bank_marketing:
  target: dev
  outputs:
    
    dev:
      type: postgres
      host: localhost
      user: beatrice
      password: "{{ env_var('DB_PASSWORD') }}"   # From environment!
      port: 5432
      dbname: data_vault
      schema: dbt_dev
      threads: 4
    
    prod:
      type: postgres
      host: "{{ env_var('PROD_DB_HOST') }}"
      user: "{{ env_var('PROD_DB_USER') }}"
      password: "{{ env_var('PROD_DB_PASSWORD') }}"
      port: 5432
      dbname: data_vault
      schema: dbt_prod
      threads: 8
```

```bash
# Run against different targets
dbt run --target dev
dbt run --target prod
```

---

## The Three-Layer Architecture

```
RAW (Sources)          STAGING               MARTS
─────────────    →    ─────────────    →    ─────────────
raw.customers         stg_customers         dim_customers
raw.transactions  →   stg_transactions  →   fct_transactions
raw.products          stg_products          fct_revenue

Layer 1: Staging     Layer 2: Intermediate  Layer 3: Marts
- Clean column names  - Join models          - Business metrics
- Cast data types     - Business logic       - Ready for BI
- Filter bad rows     - Deduplication        - Aggregated
- Rename columns      - Enrichment           - Fact/Dim tables
```

---

## Practice — What to Build Next

After this intro, you will build:

1. Sources (define raw tables)
2. Staging models (clean raw data)
3. Intermediate models (business logic)
4. Mart models (BI-ready aggregations)
5. Tests (validate data quality)
6. Documentation (auto-generated)
7. Snapshots (track history)
8. dbt with Docker (production deployment)

---

## Previous | Next
← Start | → [[02 - dbt Models and Sources]]
