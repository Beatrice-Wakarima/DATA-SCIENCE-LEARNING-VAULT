
## Project Summary

Built a complete end-to-end ELT data pipeline and multi-page Power BI dashboard for a fictional aerospace company (Spaero), covering Finance, Sales, HR, and Capital Investment analytics across 7 years of data.

The project demonstrates the full data engineering lifecycle — from raw Excel ingestion through a structured analytical model to a production-ready Power BI dashboard — containerised with Docker for reproducibility and portability.

---

## The Problem

Finance and Sales data lived in four separate Excel workbooks with no unified reporting layer. Leadership had no single view of:

- Whether revenue targets were being hit year over year
- Which customers and products were driving profitability
- How capital investment projects were performing against expected returns
- How workforce tenure and department structure looked across the organisation

The goal was to build a pipeline that ingested all four sources, transformed them into a clean analytical model, and surfaced the answers in an interactive dashboard.

---

## What I Built

### Data Pipeline (Python + PostgreSQL + Docker)

Designed and implemented a three-layer ELT architecture:

**Raw layer** — Excel files ingested into PostgreSQL using pandas and SQLAlchemy. Every run is fully idempotent — raw tables are truncated before reload so no duplicates accumulate across pipeline runs.

**Staging layer** — Five typed, sanitised SQL views (`int.*`) that cast raw columns to correct data types, derive date dimensions (year, month, quarter), normalise string casing, and compute calculated fields like `calculated_profit = revenue - cogs`.

**Analytics layer** — Eight materialised tables including three dimension tables (`dim_customers`, `dim_products`, `dim_date`) with UUIDv5 surrogate keys, and five pre-aggregated mart tables covering annual performance, monthly sales, customer lifetime value, product metrics, and discounted cash flows.

**Presentation layer** — Twenty-two SQL views designed specifically for Power BI consumption, one per visual group across six dashboard pages. Each view includes only the columns Power BI needs, with metrics stored at display precision (percentages as `38.01` not `0.38`) to simplify DAX.

The pipeline runs as a Docker Compose setup — a PostgreSQL 15 container holds the warehouse, and a Python 3.11 container runs the three scripts in sequence (`extract_load.py → transform.py → inspect_views.py`) then exits cleanly with code 0. The entire warehouse rebuilds from scratch on every run across 36 SQL blocks, each in its own transaction so failures halt cleanly without partial deployments.

### Power BI Dashboard (6 pages)

**Executive Overview** — KPI cards for revenue, profit, gross margin and target attainment. Monthly revenue and profit trend chart with quarterly grouping. Revenue split by customer segment with year slicer cross-filtering all visuals.

**Customer Analytics** — Top customers ranked by revenue with average order value, profit margin and active years. Filled map showing revenue concentration by country. RFM (Recency, Frequency, Monetary) scatter plot segmenting 130 customers into Champions, Loyal, At Risk and Lost cohorts.

**Product Analytics** — Revenue KPI cards per product responding to year slicer via DAX CALCULATE measures. Line chart showing revenue trajectory per product 2015–2021. Product × segment matrix and a pricing comparison chart showing actual selling price vs target price vs manufacturing cost, revealing that all four products were consistently sold at a premium above target.

**Revenue Forecast** — Annual actual vs target bar chart with On/Below Target status. Year-over-year growth and CAGR line chart. Three-year forward projection using linear regression (`REGR_SLOPE`/`REGR_INTERCEPT`) delivered through a UNION of actuals and projected rows. Monthly seasonality index showing December as the strongest month at ~9.5% of annual revenue.

**Capital Budgeting** — Waterfall chart showing project cash flow schedule. Cumulative cash flow line identifying the break-even point. NPV, payback period and profitability index KPI cards. Sensitivity matrix showing NPV for both projects (TC25147 and ZB95486) across seven discount rates from 3% to 15%, with conditional formatting highlighting positive/negative NPV zones.

**Employee Analytics** — Headcount, average tenure and senior staff ratio KPI cards. Clustered bar by department. Tenure distribution stacked bar. Hiring cohort chart showing recruitment waves by year. Drill-through to a hidden Employee Roster page filtered by department, triggered from the department bar chart.

---

## Technical Challenges Solved

**Idempotent loading** — The original design used `if_exists="append"` which duplicated rows on every re-run. Solved with a truncate-then-append pattern that checks table existence before loading, making every run a clean full refresh regardless of how many times it runs.

**Postgres type conflicts** — Multiple SQL blocks failed because `ROUND()` in PostgreSQL only accepts `NUMERIC`, not `FLOAT`. `REGR_SLOPE()` and `POWER()` return `FLOAT`. Solved by casting intermediate results to `NUMERIC` before passing to `ROUND()`, and replacing `POWER()` in the CAGR calculation with an `LN`/`EXP` pattern that operates entirely on `NUMERIC` types.

**View column immutability** — `CREATE OR REPLACE VIEW` in PostgreSQL cannot reorder or rename existing columns. When the staging views needed a new `order_quarter` column, the pipeline failed. Solved by splitting each staging block into two separate transactions — `DROP VIEW IF EXISTS ... CASCADE` followed by `CREATE VIEW` — ensuring the old definition is fully gone before the new one is created.

**Cross-filter isolation** — The segment donut on the Executive Overview page did not respond to the year slicer because `vw_exec_segment_summary` had no year column. Solved by adding `order_year AS year` to the view and creating a Many-to-One relationship from `vw_exec_kpi_scorecard.performance_year` to `vw_exec_segment_summary.year`, making `vw_exec_kpi_scorecard` the year hub for all fact views.

**Docker port collision** — Local PostgreSQL 18 occupied port 5432 on the host. The pipeline was reading `DB_PORT` from `.env` (set to the host port) and using it as the internal Docker connection port, causing connection refused errors. Solved by separating internal (`DB_PORT=5432`) and host (`DB_HOST_PORT=5439`) port configuration.

---

## Key Findings from the Data

- **FB71015 dominates** — one product accounts for 57.7% of total revenue ($437M of $757M) and has the strongest margin profile
- **Government segment drives the business** — 55.75% of revenue from 72 customers, far outpacing Enterprise (18.27%) and Channel Partners (14.71%)
- **2021 cost spike** — manufacturing prices jumped 20–30% above any prior year across all products, visible in the pricing waterfall
- **Both capital projects are viable** — TC25147 NPV of $11.27M, ZB95486 NPV of $12.29M at their assigned discount rates; both remain positive at 12% but turn negative at 15%
- **Strong revenue growth** — CAGR of approximately 19% from 2015 to 2021, with 2021 showing the strongest single-year performance at $179.6M

---

## Stack

|Component|Technology|
|---|---|
|Pipeline language|Python 3.11|
|Database|PostgreSQL 15|
|Data processing|pandas, openpyxl|
|DB connector|SQLAlchemy, psycopg2|
|Containerisation|Docker, Docker Compose|
|Dashboard|Microsoft Power BI Desktop|
|Version control|Git, GitHub|
|Documentation|Obsidian|

---

## What I Would Add Next

- **Data quality gate** — row-level validation (no negative revenue, no future dates, profit reconciliation) before data enters the analytics layer
- **Schema drift detection** — column contract checks that halt the pipeline if the source Excel files change structure
- **Failure alerting** — email notification when any pipeline block fails
- **Integration tests** — pytest suite validating row counts, business rules and view existence after every run
- **Incremental loading** — watermark-based loading for when data volume grows beyond full-refresh feasibility

---

_Source code and documentation available on GitHub._