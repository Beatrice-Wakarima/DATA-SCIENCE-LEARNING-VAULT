

## 🛠️ Project Initialization

- Installed dbt in IDE.
    
- Initialized project: `looker_ecommerce`.
    
- Auto‑generated directory structure.
    
- Verified setup with `dbt debug`.
    

## 📊 Data Sources

### 🏢 Distribution Centers

- **Rows:** 10
    
- **Columns:** ID, name, latitude, longitude
    
- **Nature:** Small, static dataset
    
- **Decision:** Load with `dbt seed` (one‑time file).
    

### 📦 Orders

- **Rows:** 125,000
    
- **Columns:** 9 (order ID, user ID, status, timestamps, items, etc.)
    
- **Nature:** Large, dynamic dataset
    
- **Decision:** Load with `dbt source` (live database connection).
    
- **Database:** DuckDB
    

## 📂 Directory Structure

- **Seeds** → `distribution_centers.csv`
    
- **Models** → SQL + YAML files for staging and transformations
    
- **Sources** → YAML files documenting raw sources
    

## 📝 Documentation

- **Source YAML** → documents raw sources (e.g., `orders`).
    
- **Model YAML** → documents staging models.
    
- Ensures lineage, clarity, and onboarding readiness.
    

## ⚙️ dbt Subcommands Recap

- `dbt init` → initialize project
    
- `dbt seed` → load static CSVs
    
- `dbt source` → connect live datasets
    
- `dbt debug` → verify environment
    
- `dbt run` → execute models
    
- `dbt test` → validate transformations
    
- `dbt docs generate` → build documentation site
    

## 📐 Style Guide

- Follow dbt naming conventions.
    
- Consistent folder and file naming.
    
- Modular SQL models for clarity.
    
- YAML documentation aligned with dbt best practices.
    
- Reference: [dbt best practices](https://docs.getdbt.com/best-practices)