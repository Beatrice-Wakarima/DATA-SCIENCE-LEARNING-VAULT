

## 📌 Purpose

- **Data Marts** → Clean, accessible models at the end of the ELT pipeline.
    
- **Snapshot Models** → Track changes over time that marts alone cannot capture.
    

## 🛠️ Data Marts Overview

- Reduce SQL repetition by storing logic as code.
    
- Provide stakeholder‑friendly tables for analysis.
    
- Business reasons: clarity, accessibility, and performance.
    

## 📊 Looker E‑commerce Marts

- **Customers Mart** → One row per customer.
    
    - Answers: _Who are our customers?_ _What are they purchasing?_
        
- **Products Mart** → One row per product.
    
    - Answers: _What is our revenue and profit?_
        

## 🔗 Mart Construction

- Join multiple staging models together.
    
- Refine SQL logic outside dbt first.
    
- Paste verified SQL into dbt model files.
    
- Replace table names with `ref()` calls.
    
- Add YAML documentation + tests.
    
- Run and validate build.
    

## ⏳ Snapshot Models

- Marts show current state but **overwrite history**.
    
- Example: Orders staging model tracks latest status only.
    
- Problem: Cannot measure time between _Processing → Returned_.
    
- Solution: Create snapshot model to record changes over time.
    

## 📝 Snapshot Implementation

1. Create new file → start with Jinja syntax:
    
    Code
    
    ```
    {% snapshot orders_snapshot %}
    ...
    {% endsnapshot %}
    ```
    
2. Configure snapshot settings (unique key, strategy, updated_at).
    
3. Run with `dbt snapshot` (not `dbt run`).
    
4. Schedule snapshots in dbt Cloud or orchestration tool for controlled timing.
    

## 📐 Best Practices

- Refine complex SQL outside dbt before implementation.
    
- Use `ref()` consistently for maintainability.
    
- Document marts and snapshots in YAML.
    
- Apply tests (unique, not_null, relationships).
    
- Schedule snapshots to capture incremental changes reliably.
    
- Reference: [dbt snapshots docs](https://docs.getdbt.com/docs/build/snapshots)