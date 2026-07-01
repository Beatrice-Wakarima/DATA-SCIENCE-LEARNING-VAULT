
**Type:** End-to-End ELT + Power BI Dashboard  

**Stack:** Python · PostgreSQL · Docker · Power BI  

**Status:** #active  

**Last Updated:** 2026-06-03

  ## Project Map

  

```

Excel Files → extract_load.py → raw.* → transform.py → int.* → analytics.* → presentation.* → Power BI

```

  

```dataview

table file.mtime as "Last Modified"

from "SPAERO"

sort file.mtime desc

```

  

---

  

## 📁 Folder Structure

  

```

REVENUE ANALYSIS/

├── data/                        ← Source Excel files (git-ignored)

│   ├── Capital_Budgeting.xlsx

│   ├── Employee_Fact.xlsx

│   ├── revenue_targets.xlsx

│   └── spaero_sales.xlsx

├── scripts/

│   ├── extract_load.py          ← Step 1: Excel → raw.*

│   ├── transform.py             ← Step 2: raw.* → int.* → analytics.* → presentation.*

│   └── inspect_views.py        ← Step 3: Validate all 28 objects

├── .env                         ← Credentials (never commit)

├── .env.example                 ← Template

├── .gitignore

├── docker-compose.yml

├── Dockerfile

└── requirements.txt

```

  

---

## ⚙️ Environment Setup

  ### `.env` file (copy from `.env.example`)

  

```env

DB_USER=spaero_user

DB_PASSWORD=your_strong_password

DB_HOST=postgres_warehouse

DB_PORT=5432

DB_NAME=spaero_dw

DB_HOST_PORT=5439

```

  

> [!WARNING]

> Never commit `.env` to version control. It is in `.gitignore`.

  

### Python dependencies (`requirements.txt`)

  

```

pandas==2.2.2

openpyxl==3.1.2

sqlalchemy==2.0.30

psycopg2-binary==2.9.9

python-dotenv==1.0.1

```

  

---

  

## 🐳 Docker Setup

  

### `docker-compose.yml` — Two services

  

| Service | Image | Role |

|---|---|---|

| `postgres_warehouse` | `postgres:15-alpine` | Data warehouse, exposed on `DB_HOST_PORT` |

| `elt_pipeline` | Custom Python image | Runs all 3 scripts in sequence, then exits |

  

Both services share `spaero_network` (bridge) so `elt_pipeline` resolves `postgres_warehouse` by hostname.

  

```yaml

# Port mapping — host:container

ports:

  - "${DB_HOST_PORT:-5439}:5432"

```

  

> [!NOTE]

> Local Postgres 18 runs on `5432`. Docker Postgres 15 is mapped to `5439` to avoid port collision. Inside Docker, containers always communicate on `5432`.

  

### `Dockerfile` — Pipeline image

  

```dockerfile

FROM python:3.11-slim

# installs libpq-dev + gcc for psycopg2

# copies requirements.txt, scripts/

CMD ["sh", "-c", "python extract_load.py && python transform.py && python inspect_views.py"]

```

  

### Run Commands

  

```bash

# First time

cp .env.example .env          # fill in credentials

docker compose up --build     # build + start everything

  

# Every refresh (after new Excel files dropped into data/)

docker compose run --rm elt_pipeline

  

# Rebuild after code changes

docker compose down

docker compose up --build

  

# Nuke everything (corrupted cache fix)

docker system prune -af

docker compose up --build

```

  

---

  

## 📥 Step 1 – Extract & Load (`extract_load.py`)

  

### What it does

Scans `data/*.xlsx` → reads every sheet → loads into `raw.*` schema.

  

### Key design: Truncate-then-Append (Idempotent)

  

```python

if table_exists(engine, clean_table_name):

    TRUNCATE TABLE raw."<table>"   # wipe stale rows

    run_mode = "full_refresh"

else:

    run_mode = "initial_load"

  

df.to_sql(..., if_exists="append")  # always appends to empty table

```

  

> [!IMPORTANT]

> Using `if_exists="append"` without TRUNCATE would duplicate rows on every re-run. The truncate-first pattern makes every run idempotent.

  

### Naming Convention

  

`{workbook_name}_{sheet_name}` → sanitized to snake_case

  

| Source File | Sheet | Raw Table |

|---|---|---|

| `spaero_sales.xlsx` | `Sales_Fact` | `raw.spaero_sales_sales_fact` |

| `spaero_sales.xlsx` | `Customer_Dim` | `raw.spaero_sales_customer_dim` |

| `revenue_targets.xlsx` | `Revenue Targets` | `raw.revenue_targets_revenue_targets` |

| `Capital_Budgeting.xlsx` | `Cash Flow` | `raw.capital_budgeting_cash_flow` |

| `Employee_Fact.xlsx` | `Sheet1` | `raw.employee_fact_sheet1` |

  

### Ingestion Log

  

```sql

SELECT * FROM raw.ingestion_log ORDER BY ingested_at DESC;

```

  

---

  

## 🔄 Step 2 – Transform (`transform.py`)

  

### Architecture – 3-Layer ELT

  

```

raw.*  (append-only, exact copy of Excel)

  ↓ DROP VIEW CASCADE + CREATE VIEW

int.*  (typed, sanitised staging views)

  ↓ DROP TABLE CASCADE + CREATE TABLE

analytics.*  (UUIDv5 dims + pre-aggregated marts)

  ↓ CREATE OR REPLACE VIEW

presentation.*  (Power BI ready, one view per visual)

```

  

### Block Count: 36 blocks total

  

| Layer | Objects | Type |

|---|---|---|

| Schema init | 1 | Extension + schemas |

| `int.*` staging | 10 | DROP + CREATE VIEW (split per table) |

| `analytics.dim_*` | 3 | DROP TABLE CASCADE + CREATE TABLE |

| `analytics.mart_*` | 5 | DROP TABLE CASCADE + CREATE TABLE |

| `presentation.*` | 17 | CREATE OR REPLACE VIEW |

  

> [!TIP]

> Each block runs in its own transaction. A failure stops at that block without rolling back already-deployed objects.

  

### Staging Layer (`int.*`)

  

| View | Source Table | Key Columns Added |

|---|---|---|

| `int.stg_customers` | `raw.spaero_sales_customer_dim` | segment uppercased |

| `int.stg_sales` | `raw.spaero_sales_sales_fact` | `order_year`, `order_month`, `order_quarter`, `calculated_profit` |

| `int.stg_revenue_targets` | `raw.revenue_targets_revenue_targets` | `target_year` |

| `int.stg_cash_flow` | `raw.capital_budgeting_cash_flow` | `cashflow_year` |

| `int.stg_employees` | `raw.employee_fact_sheet1` | `"tenure_(years)"` quoted — special chars |

  

> [!WARNING]

> `tenure_(years)` must be quoted in SQL: `"tenure_(years)"::NUMERIC(5,2)` — the parentheses are special characters.

  

### Dimension Layer (`analytics.dim_*`)

  

| Table | Key | Source |

|---|---|---|

| `analytics.dim_customers` | `uuid_generate_v5` on `customer_id` | `int.stg_customers` |

| `analytics.dim_products` | `uuid_generate_v5` on `product_id` | `int.stg_sales` |

| `analytics.dim_date` | `YYYYMMDD` integer | `generate_series` 2015–2035 |

  

### Mart Layer (`analytics.mart_*`)

  

| Table | Grain | Key Metrics |

|---|---|---|

| `mart_annual_performance` | 1 row per year | revenue, profit, cogs, target, margin % |

| `mart_monthly_sales` | 1 row per month | monthly revenue, YTD cumulative |

| `mart_customer_sales` | 1 row per customer | total orders, AOV, RFM inputs |

| `mart_product_sales` | 1 row per product | units, revenue, margin, avg prices |

| `mart_product_cashflow` | 1 row per project-period | DCF, cumulative cashflow, NPV inputs |

  

> [!NOTE]

> `target_achievement_pct` and `gross_margin_pct` are stored as **percentage values** (e.g. `107.27`, `38.01`) — not decimals. Use `AVERAGE` not `SUM` in Power BI cards.

  

### Presentation Layer (`presentation.*`) — 17 views

  

#### Page 1 · Executive Overview

| View | Answers |

|---|---|

| `vw_exec_kpi_scorecard` | Revenue vs target, YoY growth, margin per year |

| `vw_exec_monthly_trend` | Monthly revenue/profit, YTD, quarter grouping |

| `vw_exec_segment_summary` | Revenue by segment **with `year` column** for cross-filtering |

  

#### Page 2 · Customer Analytics

| View | Answers |

|---|---|

| `vw_customer_performance` | Top customers by revenue, AOV, active years |

| `vw_customer_yearly_revenue` | Customer revenue trend year by year |

| `vw_customer_country_summary` | Revenue by country + segment (map visual) |

| `vw_customer_rfm` | Champions / Loyal / At Risk / Lost segmentation |

  

#### Page 3 · Product Analytics

| View | Answers |

|---|---|

| `vw_product_performance` | Revenue, margin per product |

| `vw_product_monthly_trend` | Product revenue over time |

| `vw_product_segment_matrix` | Product × segment cross-tab |

| `vw_product_pricing` | Actual vs target vs mfg price per year |

  

#### Page 4 · Revenue Forecast

| View | Answers |

|---|---|

| `vw_revenue_actual_vs_target` | Hit/miss per year |

| `vw_revenue_growth` | YoY % + CAGR (uses `LN`/`EXP` — not `POWER`) |

| `vw_revenue_forecast_linear` | 3-year linear regression projection |

| `vw_revenue_seasonality` | Monthly share of annual revenue (seasonal index) |

  

#### Page 5 · Capital Budgeting

| View | Answers |

|---|---|

| `vw_capex_cashflow_schedule` | Cash flow timeline per project |

| `vw_capex_project_summary` | NPV, payback period, profitability index |

| `vw_capex_sensitivity` | NPV at 7 discount rates (3%–15%) |

  

#### Page 6 · Employee

| View | Answers |

|---|---|

| `vw_employee_dept_summary` | Headcount, senior %, avg tenure by dept |

| `vw_employee_tenure_distribution` | Tenure band histogram |

| `vw_employee_hiring_cohort` | Hires by year and department |

| `vw_employee_roster` | Full roster for drill-through |

  

---

  

## 🔍 Step 3 – Inspect (`inspect_views.py`)

  

### Run modes

  

```bash

# All 28 objects — full validation

docker compose run --rm elt_pipeline python inspect_views.py

  

# One dashboard page group

docker compose run --rm elt_pipeline python inspect_views.py --group "customer"

docker compose run --rm elt_pipeline python inspect_views.py --group "capital"

docker compose run --rm elt_pipeline python inspect_views.py --group "employee"

  

# One specific view

docker compose run --rm elt_pipeline python inspect_views.py --view presentation.vw_customer_rfm

```

  

### Expected row counts (healthy pipeline)

  

| View | Expected Rows |

|---|---|

| `raw.spaero_sales_sales_fact` | 6,320 |

| `raw.spaero_sales_customer_dim` | 141 |

| `raw.revenue_targets_revenue_targets` | 7 |

| `int.stg_sales` | 6,320 |

| `int.stg_customers` | 130 (after dedup) |

| `analytics.mart_annual_performance` | 7 (2015–2021) |

| `analytics.mart_monthly_sales` | 84 |

| `analytics.mart_customer_sales` | 130 |

| `analytics.mart_product_sales` | 4 |

  

---

  

## 📊 Power BI Setup

  

### Connection

  

| Setting | Value |

|---|---|

| Server | `localhost` |

| Port | `5439` (or your `DB_HOST_PORT`) |

| Database | `DB_NAME` from `.env` |

| Schema | `presentation` |

| Mode | Import |

  

### Data Model Relationships

  

```

vw_exec_kpi_scorecard.performance_year (1)

    → vw_exec_segment_summary.year         (M)  ← fixes segment donut cross-filter

    → vw_exec_monthly_trend.order_year     (M)

    → vw_revenue_actual_vs_target.year     (M)

    → vw_revenue_growth.year               (M)

    → vw_customer_yearly_revenue.year      (M)

    → vw_product_monthly_trend.order_year  (M)

    → vw_product_segment_matrix.year       (M)

  

vw_customer_performance.customer_id (1)

    → vw_customer_yearly_revenue.customer_id (M)

  

vw_product_performance.product_id (1)

    → vw_product_monthly_trend.product_id  (M)

    → vw_product_segment_matrix.product_id (M)

    → vw_product_pricing.product_id        (M)

  

vw_capex_project_summary.product_id (1)

    → vw_capex_cashflow_schedule.product_id (M)

    → vw_capex_sensitivity.product_id       (M)

```

  

### Key DAX Measures

  

```dax

Total Revenue = SUM(vw_exec_kpi_scorecard[actual_revenue])

Total Profit  = SUM(vw_exec_kpi_scorecard[actual_profit])

  

Gross Margin % =

DIVIDE(

    SUM(vw_exec_kpi_scorecard[actual_profit]),

    SUM(vw_exec_kpi_scorecard[actual_revenue])

) * 100

  

Target Achievement % =

AVERAGE(vw_exec_kpi_scorecard[target_achievement_pct])

  

Total Headcount  = COUNTROWS(vw_employee_roster)

Avg Tenure       = AVERAGE(vw_employee_roster[tenure_years])

  

Senior % =

DIVIDE(

    COUNTROWS(FILTER(vw_employee_roster, vw_employee_roster[seniority_level] = "Senior")),

    COUNTROWS(vw_employee_roster)

) * 100

  

Total NPV            = SUM(vw_capex_project_summary[npv])

Profitability Index  = AVERAGE(vw_capex_project_summary[profitability_index])

```

  

### Cross-Filter Fix (segment donut)

  

> [!TIP]

> Click chart → Format ribbon → **Edit interactions** → click **filter icon** (funnel) on the donut. Do this for every slicer on every page.

  

---

  

## 🐛 Bugs Fixed & Lessons Learned

  

| # | Error | Root Cause | Fix |

|---|---|---|---|

| 1 | `tenure_years_` does not exist | `clean_string()` converts `(` and `)` to `_` in column name | Quote the raw column: `"tenure_(years)"` |

| 2 | `ROUND(double precision, integer)` | Postgres `ROUND()` only accepts `NUMERIC`, not `FLOAT` | Cast to `NUMERIC` before `ROUND`: `(expr)::NUMERIC` |

| 3 | `POWER()` type conflict in CAGR | Mixed `FLOAT` and `NUMERIC` args | Replace with `LN`/`EXP` pattern on pure `NUMERIC` |

| 4 | `month_abbr` does not exist | Column only exists in mart, not in `int.stg_sales` | Derive inline: `TO_CHAR(TO_DATE(order_month::TEXT, 'MM'), 'Mon')` |

| 5 | Segment donut not cross-filtering | `vw_exec_segment_summary` had no `year` column | Added `order_year AS year` and Power BI relationship |

| 6 | `cannot change name of view column` | `CREATE OR REPLACE VIEW` can't reorder/rename columns | Split into `DROP VIEW CASCADE` + `CREATE VIEW` |

| 7 | `relation int.stg_customers does not exist` | `DROP CASCADE` in same transaction drops and loses the view | Split DROP and CREATE into separate blocks/transactions |

| 8 | Docker `parent snapshot does not exist` | Corrupted Docker build cache | `docker system prune -af` then `docker compose up --build` |

| 9 | `DB_PORT=5439` breaks internal connection | Scripts used `DB_PORT` for internal Docker connection | Keep `DB_PORT=5432` internal, use `DB_HOST_PORT=5439` for host mapping |

| 10 | Duplicate rows on re-run | `if_exists="append"` stacks rows each run | TRUNCATE table before append — idempotent load pattern |

  

---

  

## 🔁 Full Refresh Sequence

  

```

1. Drop new/updated Excel files into data/

2. docker compose run --rm elt_pipeline

3. Power BI Desktop → Home → Refresh

```

  

### What happens to each layer on re-run

  

| Layer | Operation | Result |

|---|---|---|

| `raw.*` tables | TRUNCATE → append | Fresh rows, no duplicates |

| `int.*` views | DROP CASCADE → CREATE | Rebuilt with new column definitions |

| `analytics.dim_*` | DROP TABLE CASCADE → CREATE TABLE | Fully rebuilt |

| `analytics.mart_*` | DROP TABLE CASCADE → CREATE TABLE | Fully rebuilt |

| `presentation.*` | CREATE OR REPLACE VIEW | Replaced in place |

  

---

  

## 📈 Data Profile

  

| Metric | Value |

|---|---|

| Date range | 2015-01-02 → 2021-12-30 |

| Total revenue | ~$757M |

| Total profit | ~$243M |

| Total orders | 6,320 |

| Customers | 130 |

| Products | 4 (AD58008, FB71015, JK95673, LO84601) |

| Segments | Government, Enterprise, Channel Partners, Midmarket |

| Countries | 30+ |

| Employees | varies by dept |

| Capital projects | 2 (ZB95486, TC25147) |

  

---

  

## 🔗 Related Notes

  

- [[extract_load]] — Extract & Load script walkthrough

- [[transform]] — Full transformation block reference  

- [[inspect_views]] — Validation script reference

- [[powerbi_guide]] — Visual-by-visual Power BI setup

- [[docker_setup]] — Docker architecture and troubleshooting

  

---

  

## 📌 Tags

  

#project #elt #postgresql #powerbi #docker #python #dataengineering #finance #sales