

## 📌 Purpose

Ensure every column in your DuckDB staging models is properly described, so dbt docs can generate clear, searchable metadata for onboarding and analysis.

## 📂 Steps

### 1. Open schema.yml

Each staging model should have a `schema.yml` file where you define sources, models, and column descriptions.

yaml

```
version: 2

models:
  - name: stg_orders
    description: "Staging model for raw orders data"
    columns:
      - name: order_id
        description: "Unique identifier for each order"
      - name: customer_id
        description: "Foreign key linking to customers table"
      - name: order_date
        description: "Date when the order was placed"
      - name: total_amount
        description: "Total monetary value of the order"
```

### 2. Run dbt docs generate

This compiles your project and builds the documentation site.

bash

```
dbt docs generate
```

### 3. View dbt docs

Spin up the docs site locally to visualize your column descriptions.

bash

```
dbt docs serve
```

This opens a browser window where you can explore models, sources, and column metadata.

### 4. Iterate descriptions

- Keep descriptions concise but clear.
    
- Use consistent phrasing across models.
    
- Add business context (e.g., “Revenue in USD after discounts”).
    

## 🔗 Connections

- Backlink to **Staging Models Note**
    
- Backlink to **Transformation Logic Note**
    
- Backlink to **Consumption Layer / Power BI Note**
    

## 🚀 Next Steps

- Add **tests** (unique, not null, accepted values) alongside column descriptions.
    
- Document **sources** with freshness checks.
    
- Expand with **macros** for reusable documentation patterns.