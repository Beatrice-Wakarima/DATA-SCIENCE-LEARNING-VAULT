# 🔄 transform

**Script:** `scripts/transform.py`  
**Role:** Step 2 of 3 — `raw.*` → `int.*` → `analytics.*` → `presentation.*`  
**Parent:** [[SPAERO_REVENUE_ANALYSIS]]  
**Tags:** #script #transform #elt #sql

---

## Purpose

Runs 36 SQL blocks in sequence, each in its own transaction. Builds the full 3-layer analytical model from the raw ingested data. Stops immediately on any failure — no partial deployments.

---

## Execution Flow

```
run_pipeline()
    │
    └── for each block in TRANSFORMATION_BLOCKS (36 total)
            engine.begin()              ← isolated transaction
            conn.execute(block['sql'])  ← deploy the object
            ✔ log success / ✘ sys.exit(1)
```

---

## Block Structure — 36 Blocks

```
Block 01      → Extensions & schemas (uuid-ossp, int, analytics, presentation)

Blocks 02–03  → DROP + CREATE int.stg_customers
Blocks 04–05  → DROP + CREATE int.stg_sales
Blocks 06–07  → DROP + CREATE int.stg_revenue_targets
Blocks 08–09  → DROP + CREATE int.stg_cash_flow
Blocks 10–11  → DROP + CREATE int.stg_employees

Block 12      → analytics.dim_customers
Block 13      → analytics.dim_products
Block 14      → analytics.dim_date

Block 15      → analytics.mart_annual_performance
Block 16      → analytics.mart_monthly_sales
Block 17      → analytics.mart_customer_sales
Block 18      → analytics.mart_product_sales
Block 19      → analytics.mart_product_cashflow

Blocks 20–22  → presentation.* Executive Overview (3 views)
Blocks 23–26  → presentation.* Customer Analytics (4 views)
Blocks 27–30  → presentation.* Product Analytics (4 views)
Blocks 31–34  → presentation.* Revenue Forecast (4 views)
Blocks 35–37  → presentation.* Capital Budgeting (3 views)  ← wait, counted above
Blocks 20–36  → presentation.* Employee Analytics (4 views)
```

> [!NOTE]
> Staging views are split into DROP + CREATE blocks (2 blocks per view) because `CREATE OR REPLACE VIEW` cannot reorder or rename existing columns — Postgres rejects it. DROP CASCADE then CREATE is the safe pattern.

---

## Layer-by-Layer Reference

### Layer 1 — Staging (`int.*`)

Purpose: Type-cast raw columns, add derived date fields, clean strings.

| View | Notable Logic |
|---|---|
| `int.stg_sales` | Adds `order_year`, `order_month`, `order_quarter`, `calculated_profit = revenue - cogs` |
| `int.stg_customers` | `UPPER(TRIM(segment))` — normalises casing |
| `int.stg_employees` | `"tenure_(years)"` must be double-quoted — parentheses are special chars |

```sql
-- stg_employees tenure column — always quote it
"tenure_(years)"::NUMERIC(5,2) AS tenure_years
```

### Layer 2 — Dimensions (`analytics.dim_*`)

Purpose: Surrogate keys, deduplication, reference data.

| Table | Key Type | Dedup Logic |
|---|---|---|
| `dim_customers` | `uuid_generate_v5` on `customer_id` | `ROW_NUMBER() OVER (PARTITION BY customer_id)` |
| `dim_products` | `uuid_generate_v5` on `product_id` | `DISTINCT` + window avg |
| `dim_date` | `YYYYMMDD` integer | `generate_series` 2015–2035 |

```sql
-- Fiscal year logic (starts July 1)
CASE WHEN EXTRACT(MONTH FROM d) >= 7
     THEN EXTRACT(YEAR FROM d)::INT + 1
     ELSE EXTRACT(YEAR FROM d)::INT
END AS fiscal_year
```

### Layer 3 — Marts (`analytics.mart_*`)

Purpose: Pre-aggregated facts, ready for Power BI import.

| Mart | Grain | Key Metric |
|---|---|---|
| `mart_annual_performance` | Year | Revenue vs target, margin %, YoY |
| `mart_monthly_sales` | Month | Monthly revenue, YTD cumulative |
| `mart_customer_sales` | Customer | Total orders, AOV, lifetime value |
| `mart_product_sales` | Product | Units, revenue, avg prices |
| `mart_product_cashflow` | Project × Period | DCF, cumulative cashflow |

> [!IMPORTANT]
> `target_achievement_pct` and `gross_margin_pct` are stored as **percentage numbers** (e.g. `107.27`, `38.01`) — not decimals (0.38). Use `AVERAGE` not `SUM` in Power BI KPI cards.

### Layer 4 — Presentation (`presentation.*`)

17 views — one per Power BI visual group. See [[powerbi_guide]] for full mapping.

---

## Known SQL Gotchas

### 1. ROUND with FLOAT fails
```sql
-- ✘ Fails — Postgres ROUND() only takes NUMERIC
ROUND(REGR_SLOPE(revenue, year), 0)

-- ✔ Works — cast to NUMERIC first
ROUND(REGR_SLOPE(revenue::FLOAT, year::FLOAT)::NUMERIC, 0)
```

### 2. POWER() with mixed types fails
```sql
-- ✘ Fails — FLOAT and NUMERIC conflict
POWER(actual_revenue::FLOAT / base_revenue, 1.0 / n)

-- ✔ Works — use LN/EXP on pure NUMERIC
EXP(LN(actual_revenue::NUMERIC / base_revenue::NUMERIC) / n::NUMERIC)
```

### 3. month_abbr not in stg_sales
```sql
-- ✘ Fails — column doesn't exist in int.stg_sales
month_abbr

-- ✔ Works — derive it from order_month integer
TRIM(TO_CHAR(TO_DATE(order_month::TEXT, 'MM'), 'Mon')) AS month_abbr
```

### 4. CREATE OR REPLACE VIEW can't reorder columns
```sql
-- ✘ Fails if column order changed
CREATE OR REPLACE VIEW int.stg_sales AS ...

-- ✔ Works — always split into two blocks
DROP VIEW IF EXISTS int.stg_sales CASCADE;
CREATE VIEW int.stg_sales AS ...
```

### 5. DROP CASCADE in same transaction loses the view
```sql
-- ✘ Fails — DROP and CREATE in one transaction: CREATE sees nothing
BEGIN;
DROP VIEW IF EXISTS int.stg_customers CASCADE;
CREATE VIEW int.stg_customers AS ...  -- relation does not exist
COMMIT;

-- ✔ Works — separate transactions (separate blocks in pipeline)
-- Block N:   DROP VIEW IF EXISTS int.stg_customers CASCADE;
-- Block N+1: CREATE VIEW int.stg_customers AS ...
```

---

## Re-run Behaviour

| Object | DDL | On Re-run |
|---|---|---|
| `int.*` views | DROP CASCADE + CREATE | Dropped and rebuilt |
| `analytics.dim_*` | DROP TABLE CASCADE + CREATE TABLE | Dropped and rebuilt |
| `analytics.mart_*` | DROP TABLE CASCADE + CREATE TABLE | Dropped and rebuilt |
| `presentation.*` | CREATE OR REPLACE VIEW | Replaced in place |

---

## Related

- [[SPAERO_REVENUE_ANALYSIS]] — Parent project note
- [[extract_load]] — Previous step, populates `raw.*`
- [[inspect_views]] — Next step, validates all objects
- [[powerbi_guide]] — Consumes `presentation.*` views
