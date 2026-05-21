---
title: dbt Documentation
tags: [dbt, documentation, lineage]
created: 2026-05-20
up:: [[DBT MOC]]
---

# 📚 dbt Documentation

> dbt auto-generates a documentation website with your data lineage graph, model descriptions, column definitions, and test results. It's the living data dictionary your team actually uses.

---

## Why dbt Docs?

```
Traditional documentation:
  ❌ Written in Confluence — immediately outdated
  ❌ No one reads it
  ❌ No lineage — can't see where data comes from
  ❌ No test status

dbt docs:
  ✅ Generated from your actual code — always accurate
  ✅ Visual lineage graph (DAG)
  ✅ Column-level descriptions
  ✅ Test pass/fail status
  ✅ Source definitions
  ✅ Searchable
```

---

## Adding Descriptions to Models

```yaml
# models/staging/_stg_models.yml
version: 2

models:
  - name: stg_bank_marketing
    description: |
      Cleaned and standardised bank marketing campaign data.
      Source: Portuguese bank telemarketing campaign data (May 2008 - November 2010).
      
      Each row represents one phone contact with a customer.
      The target variable `subscribed` indicates if the customer
      signed up for a term deposit.
    
    columns:
      - name: age
        description: "Customer age in years. Range: 18-95."
      
      - name: job
        description: |
          Customer occupation category. 
          Standardised to lowercase. 
          Values: admin, technician, management, blue-collar, services,
          retired, self-employed, entrepreneur, housemaid, student,
          unemployed, unknown.
      
      - name: balance
        description: "Average yearly balance in euros. Can be negative (overdraft)."
      
      - name: balance_segment
        description: |
          Derived segmentation based on balance.
          - high: balance > 10,000
          - medium: balance 1,000–10,000
          - low: balance 0–1,000
          - negative: balance < 0
      
      - name: subscribed
        description: "TRUE if customer subscribed to term deposit. Target variable for ML models."
      
      - name: call_duration_seconds
        description: "Duration of last contact in seconds. Note: duration=0 means no contact was made."
```

---

## Descriptions in dbt_project.yml Level

```yaml
# models/marts/finance/_finance_models.yml
version: 2

models:
  - name: fct_monthly_revenue
    description: |
      ## Monthly Revenue Fact Table
      
      Aggregated revenue metrics by month, city, and customer tier.
      
      **Grain:** One row per month × city × tier combination.
      
      **Key Metrics:**
      - `total_revenue`: Sum of all transaction amounts
      - `unique_customers`: Distinct customers who transacted
      - `mom_growth_pct`: Month-over-month revenue growth %
      
      **Refresh:** Daily at 06:00 EAT via Airflow
      
      **Owner:** Beatrice Wakarima (Data Engineering)
      
      **Used by:** Executive Revenue Dashboard (Power BI)
    
    columns:
      - name: month
        description: "First day of the month. e.g., 2026-05-01 represents May 2026."
      
      - name: total_revenue
        description: "Sum of all transaction amounts for the month in KES."
      
      - name: mom_growth_pct
        description: |
          Month-over-month revenue growth as a percentage.
          Positive = growth, negative = decline.
          NULL for first month (no prior month to compare).
      
      - name: cumulative_revenue
        description: "Running total of revenue from beginning of dataset."
```

---

## Docs Blocks — Reusable Descriptions

```markdown
<!-- docs/descriptions.md -->
{% docs balance_description %}
Average yearly bank balance in euros.

- Positive values indicate savings
- Negative values indicate overdraft
- Values are cleaned and validated (nulls removed, extreme outliers flagged)

Source: Core Banking System (CBS) — refreshed daily.
{% enddocs %}

{% docs age_segment_description %}
Customer age segmentation derived from age field:
- **young**: 18-29 years
- **middle**: 30-49 years  
- **senior**: 50+ years
{% enddocs %}

{% docs subscription_rate_description %}
Percentage of contacted customers who subscribed to a term deposit.
Formula: (subscribed_count / total_contacted) × 100
{% enddocs %}
```

```yaml
# Reference in YAML
columns:
  - name: balance
    description: "{{ doc('balance_description') }}"
  
  - name: age_segment
    description: "{{ doc('age_segment_description') }}"
```

---

## Source Documentation

```yaml
# models/staging/_sources.yml
version: 2

sources:
  - name: raw
    description: |
      Raw data loaded by Python ETL pipelines.
      All tables in the `bronze` schema.
      Data is loaded as-is with minimal transformation.
    
    database: data_vault
    schema: bronze
    
    tables:
      - name: bank_marketing
        description: |
          Raw bank marketing campaign dataset.
          
          **Original source:** UCI Machine Learning Repository
          **Time period:** May 2008 - November 2010
          **Institution:** Portuguese banking institution
          **Campaigns:** 17 total campaigns
          
          Contains 45,211 records with 17 columns.
        
        columns:
          - name: age
            description: "Customer age (integer)"
          - name: job
            description: "Job type (raw text, may contain mixed case)"
          - name: y
            description: "Target: 'yes' or 'no' — did customer subscribe?"
      
      - name: customers
        description: "Customer master data from CRM system"
        columns:
          - name: id
            description: "Unique customer identifier"
          - name: balance
            description: "Current account balance in KES"
```

---

## Generating and Viewing Docs

```bash
# Generate documentation
dbt docs generate

# This creates:
# target/catalog.json   — Column types from warehouse
# target/manifest.json  — Model metadata, tests, lineage

# Serve docs locally
dbt docs serve
# Opens browser at http://localhost:8080

# Serve on specific port
dbt docs serve --port 9000
```

---

## The Lineage Graph

The docs site includes an interactive DAG showing:

```
raw.bank_marketing (source)
        ↓
stg_bank_marketing
        ↓
int_customer_segments
        ↓
fct_campaign_performance  ←── dim_customers
        ↓
(Power BI Dashboard)
```

You can:
- Click any node to see its description and columns
- See which models are upstream/downstream
- Filter by tags or model type
- Search across all models

---

## Exposures — Document BI Dashboards

```yaml
# models/exposures.yml
version: 2

exposures:
  - name: executive_revenue_dashboard
    type: dashboard
    maturity: production
    url: https://app.powerbi.com/groups/.../reports/...
    description: |
      Executive revenue dashboard showing monthly KPIs.
      Used by CEO, CFO, and regional managers.
    
    depends_on:
      - ref('fct_monthly_revenue')
      - ref('dim_customers')
    
    owner:
      name: Beatrice Wakarima
      email: beatrice@gmail.com
  
  - name: campaign_analysis_report
    type: analysis
    maturity: development
    description: "Bank marketing campaign performance analysis"
    
    depends_on:
      - ref('fct_campaign_performance')
    
    owner:
      name: Beatrice Wakarima
      email: beatrice@gmail.com
  
  - name: customer_360_api
    type: application
    maturity: production
    url: https://api.beatricebuilds.com/customers
    description: "FastAPI endpoint serving customer profiles"
    
    depends_on:
      - ref('dim_customers')
```

---

## Metrics (dbt Semantic Layer)

```yaml
# models/metrics.yml
version: 2

metrics:
  - name: total_revenue
    label: "Total Revenue"
    model: ref('fct_monthly_revenue')
    description: "Sum of all transaction revenue in KES"
    
    type: sum
    sql: total_revenue
    
    timestamp: month
    time_grains: [month, quarter, year]
    
    dimensions:
      - city
      - tier

  - name: subscription_rate
    label: "Subscription Rate %"
    model: ref('fct_campaign_performance')
    description: "Percentage of contacts who subscribed"
    
    type: derived
    sql: "{{ metric('subscriptions') }} / {{ metric('total_contacts') }} * 100"
```

---

## Documentation Best Practices

```yaml
# ✅ Document every model
models:
  - name: fct_monthly_revenue
    description: "At least one sentence describing purpose and grain"

# ✅ Document primary keys and important columns
columns:
  - name: customer_id
    description: "Surrogate key. Unique per customer."
    tests:
      - unique
      - not_null

# ✅ Use docs blocks for long descriptions
description: "{{ doc('long_description_block') }}"

# ✅ Document the grain of fact tables
description: "Grain: one row per customer per month."

# ✅ Mention the owner and refresh schedule
description: |
  Owner: Beatrice Wakarima
  Refresh: Daily at 06:00 EAT
  Used by: Revenue Dashboard (Power BI)

# ✅ Document derived columns
- name: balance_segment
  description: |
    Derived from balance:
    - high: > 10,000
    - medium: 1,000–10,000
    - low: 0–1,000
    - negative: < 0
```

---

## Quick Reference

```bash
# Generate docs
dbt docs generate

# View docs
dbt docs serve

# What's in the docs:
# - Model descriptions
# - Column descriptions + types
# - Test status
# - Lineage graph (DAG)
# - Source definitions
# - Exposure documentation
# - Metric definitions
```

---

## Previous | Next
← [[03 - dbt Tests]] | → [[05 - dbt Macros and Jinja]]
