---
title: Introduction to Data Engineering
tags: [data-engineering, basics]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# ⚙️ Introduction to Data Engineering

> Data Engineering is the discipline of designing, building, and maintaining the infrastructure and systems that collect, store, process, and serve data at scale. Without data engineers, there is no data science.

---

## What Does a Data Engineer Do?

```
Raw Data Sources           Data Engineer Builds          Consumers
────────────────    →    ──────────────────────    →    ─────────────
APIs                     Pipelines (ETL/ELT)           Data Scientists
Databases                Data Warehouses               Analysts
CSV Files                Data Lakes                    Power BI
IoT Sensors              Streaming Systems             ML Models
Web Events               Data Quality Checks           Executives
```

A data engineer's job:
- **Collect** data from diverse sources
- **Move** it reliably to storage
- **Transform** it into usable formats
- **Serve** it to downstream consumers
- **Monitor** everything for failures

---

## Data Engineer vs Data Scientist vs Analyst

| Role | Builds | Uses | Tools |
|---|---|---|---|
| **Data Engineer** | Pipelines, warehouses | SQL, Python, Docker | Airflow, dbt, Kafka |
| **Data Scientist** | ML models, statistics | Python, R | Scikit-learn, TensorFlow |
| **Data Analyst** | Reports, dashboards | SQL, Excel | Power BI, Tableau |

---

## The Modern Data Stack

```
┌──────────────────────────────────────────────────────────────┐
│                    Modern Data Stack                         │
├───────────┬───────────┬────────────┬────────────┬───────────┤
│  Sources  │  Ingest   │  Storage   │ Transform  │   Serve   │
│           │           │            │            │           │
│  APIs     │ Fivetran  │ Snowflake  │   dbt      │ Power BI  │
│  DBs      │ Airbyte   │ BigQuery   │            │ Tableau   │
│  Files    │ Python    │ Postgres   │            │ FastAPI   │
│  Streams  │ Kafka     │ S3/GCS     │            │ ML Models │
└───────────┴───────────┴────────────┴────────────┴───────────┘
```

---

## ETL vs ELT

```
ETL (Extract → Transform → Load)    ELT (Extract → Load → Transform)
────────────────────────────────    ────────────────────────────────
Extract from source                 Extract from source
Transform OUTSIDE warehouse         Load RAW into warehouse
Load transformed data               Transform INSIDE warehouse with SQL

Used when:                          Used when:
- Legacy systems                    - Cloud warehouses (Snowflake, BQ)
- Sensitive data (transform         - Large data volumes
  before storage)                   - Modern stack with dbt
- Limited warehouse compute         - Fast iteration needed
```

---

## Data Pipeline Patterns

### Batch Processing
```
Schedule: Every hour / daily / weekly
Process: Large chunks of historical data
Tools: Python, Airflow, dbt, Spark
Example: Daily sales report at 6 AM
```

### Stream Processing
```
Schedule: Continuous / real-time
Process: Individual events as they arrive
Tools: Kafka, Flink, Spark Streaming
Example: Fraud detection on transactions
```

### Micro-batch
```
Schedule: Every few minutes
Process: Small batches frequently
Tools: Airflow, Python
Example: Near-real-time dashboard updates
```

---

## Data Architecture Patterns

### Medallion Architecture (Most Common)
```
BRONZE              SILVER              GOLD
──────────          ──────────          ──────────
Raw data            Cleaned data        Business-ready
As-is from          Validated           Aggregated
source              Typed               Joined
No transforms       Deduplicated        KPI-ready

→ Loaded by         → Built by          → Built by
  Python/Fivetran     dbt staging         dbt marts
```

### Lambda Architecture
```
Batch Layer   → Historical accuracy (slow, complete)
Speed Layer   → Real-time approximation (fast, incomplete)
Serving Layer → Combines both for queries
```

### Kappa Architecture
```
Everything treated as a stream
Single processing layer (Kafka + Flink)
Simpler than Lambda but requires stream expertise
```

---

## Core Data Engineering Skills

```
Foundation:
  ✅ SQL (advanced — window functions, CTEs)
  ✅ Python (pandas, requests, SQLAlchemy)
  ✅ Linux command line
  ✅ Git / version control

Storage:
  ✅ Relational DBs (PostgreSQL, MySQL)
  ✅ Cloud warehouses (Snowflake, BigQuery)
  ✅ Object storage (S3, GCS)
  ✅ Data formats (Parquet, Avro, JSON, CSV)

Processing:
  ✅ dbt (SQL transformations)
  ✅ Apache Airflow (orchestration)
  ✅ Apache Spark / PySpark (big data)
  ✅ Kafka (streaming)

Infrastructure:
  ✅ Docker (containerisation)
  ✅ Cloud (AWS, GCP, Azure basics)
  ✅ CI/CD basics
```

---

## Data Formats — When to Use What

| Format | Size | Speed | Human-readable | Use when |
|---|---|---|---|---|
| **CSV** | Large | Slow | ✅ Yes | Interchange, Excel |
| **JSON** | Large | Slow | ✅ Yes | APIs, semi-structured |
| **Parquet** | Small | Fast | ❌ No | Analytics, warehouses |
| **Avro** | Small | Fast | ❌ No | Kafka, streaming |
| **ORC** | Small | Fast | ❌ No | Hive, Spark |

```python
import pandas as pd

# CSV — large, slow, universal
df.to_csv("data.csv", index=False)
df = pd.read_csv("data.csv")

# Parquet — compressed, fast, columnar (use for analytics!)
df.to_parquet("data.parquet", compression="snappy")
df = pd.read_parquet("data.parquet")

# JSON — flexible, API responses
df.to_json("data.json", orient="records")
df = pd.read_json("data.json")
```

---

## Data Quality Dimensions

```
Completeness   — Are all expected records present? No nulls?
Accuracy       — Is the data correct? Matches reality?
Consistency    — Same format across all records?
Timeliness     — Is the data fresh? Updated on schedule?
Uniqueness     — No duplicate records?
Validity       — Values within expected ranges/formats?

Example checks:
  ✅ Row count > 0 (completeness)
  ✅ No nulls in critical columns (completeness)
  ✅ Emails match pattern (validity)
  ✅ Ages between 18-100 (validity)
  ✅ No duplicate IDs (uniqueness)
  ✅ Data loaded within last 24h (timeliness)
  ✅ Totals match across systems (accuracy)
```

---

## Data Pipeline Lifecycle

```
1. EXTRACT    → Pull data from sources (APIs, DBs, files)
2. VALIDATE   → Check data quality at source
3. LOAD       → Store raw data (Bronze layer)
4. TRANSFORM  → Clean, enrich, aggregate (Silver → Gold)
5. TEST       → Validate transformed data
6. SERVE      → Make available to consumers
7. MONITOR    → Alert on failures, data drift
8. DOCUMENT   → Keep data catalogue updated
```

---

## What You'll Build in This Series

```
Note 01: Introduction (this note)
Note 02: Data Sources & Extraction
Note 03: Loading Data (Batch)
Note 04: Pipeline Orchestration with Airflow
Note 05: Data Warehouse Design
Note 06: Data Quality & Validation
Note 07: Streaming with Kafka
Note 08: End-to-End Pipeline Project (Bank Marketing)
Note 09: Monitoring & Alerting
Note 10: Cloud Data Engineering
```

Everything builds toward **Note 08** — a complete production pipeline for the Bank Marketing dataset using Python + PostgreSQL + dbt + Airflow + Docker.

---

## Previous | Next
← Start | → [[02 - Data Sources and Extraction]]
