**Tool:** Microsoft Power BI Desktop  
**Role:** Dashboard layer — connects to `presentation.*` views  
**Parent:** [[SPAERO_REVENUE_ANALYSIS]]  
**Tags:** #powerbi #dashboard #visualisation

---

## Connection Settings

| Setting | Value |
|---|---|
| Connector | PostgreSQL |
| Server | `localhost` |
| Port | `5439` (your `DB_HOST_PORT` from `.env`) |
| Database | your `DB_NAME` from `.env` |
| Schema | `presentation` |
| Data Connectivity | Import |

> [!NOTE]
> Import mode loads data into Power BI's in-memory engine. Click **Home → Refresh** after every pipeline re-run to pull fresh data.

---

## Views to Import

Import **only** the `presentation` schema — never `int` or `analytics` directly.

```
vw_exec_kpi_scorecard          vw_revenue_actual_vs_target
vw_exec_monthly_trend          vw_revenue_growth
vw_exec_segment_summary        vw_revenue_forecast_linear
vw_customer_performance        vw_revenue_seasonality
vw_customer_yearly_revenue     vw_capex_cashflow_schedule
vw_customer_country_summary    vw_capex_project_summary
vw_customer_rfm                vw_capex_sensitivity
vw_product_performance         vw_employee_dept_summary
vw_product_monthly_trend       vw_employee_tenure_distribution
vw_product_segment_matrix      vw_employee_hiring_cohort
vw_product_pricing             vw_employee_roster
```

---

## Data Model — Relationships

Set in **Model View → Manage Relationships**.  
All: Many-to-One, Single direction.

```
vw_exec_kpi_scorecard.performance_year  ──1:M──►  vw_exec_segment_summary.year
vw_exec_kpi_scorecard.performance_year  ──1:M──►  vw_exec_monthly_trend.order_year
vw_exec_kpi_scorecard.performance_year  ──1:M──►  vw_revenue_actual_vs_target.performance_year
vw_exec_kpi_scorecard.performance_year  ──1:M──►  vw_revenue_growth.year
vw_exec_kpi_scorecard.performance_year  ──1:M──►  vw_customer_yearly_revenue.year
vw_exec_kpi_scorecard.performance_year  ──1:M──►  vw_product_monthly_trend.order_year
vw_exec_kpi_scorecard.performance_year  ──1:M──►  vw_product_segment_matrix.year

vw_customer_performance.customer_id     ──1:M──►  vw_customer_yearly_revenue.customer_id

vw_product_performance.product_id       ──1:M──►  vw_product_monthly_trend.product_id
vw_product_performance.product_id       ──1:M──►  vw_product_segment_matrix.product_id
vw_product_performance.product_id       ──1:M──►  vw_product_pricing.product_id

vw_capex_project_summary.product_id     ──1:M──►  vw_capex_cashflow_schedule.product_id
vw_capex_project_summary.product_id     ──1:M──►  vw_capex_sensitivity.product_id
```

---

## Column Formatting

| Column pattern | Format |
|---|---|
| `*_revenue`, `*_profit`, `*_cogs`, `npv`, `cashflow` | Currency, 2 dp |
| `*_pct`, `margin_pct`, `yoy_*`, `cagr_*` | Percentage, 2 dp — already stored as % (e.g. 38.01) |
| `target_achievement_pct` | Percentage, 1 dp — use `AVERAGE` not `SUM` |
| `tenure_years`, `avg_tenure_years` | Decimal, 1 dp |
| `profitability_index` | Decimal, 3 dp |
| `rfm_total`, `r_score`, `f_score`, `m_score` | Whole number |

---

## DAX Measures

Create in a dedicated `_Measures` table (Home → Enter Data → blank table).

```dax
// Revenue & Profit
Total Revenue =
    SUM(vw_exec_kpi_scorecard[actual_revenue])

Total Profit =
    SUM(vw_exec_kpi_scorecard[actual_profit])

Gross Margin % =
    DIVIDE(
        SUM(vw_exec_kpi_scorecard[actual_profit]),
        SUM(vw_exec_kpi_scorecard[actual_revenue])
    ) * 100

// Target
Target Achievement % =
    AVERAGE(vw_exec_kpi_scorecard[target_achievement_pct])

Revenue vs Target =
    SUM(vw_exec_kpi_scorecard[target_variance])

YoY Revenue Growth % =
    AVERAGE(vw_exec_kpi_scorecard[yoy_revenue_growth_pct])

// Forecast
CAGR % =
    AVERAGE(vw_revenue_growth[cagr_from_base_pct])

// Capital Budgeting
Total NPV =
    SUM(vw_capex_project_summary[npv])

Profitability Index =
    AVERAGE(vw_capex_project_summary[profitability_index])

// Employee
Total Headcount =
    COUNTROWS(vw_employee_roster)

Avg Tenure =
    AVERAGE(vw_employee_roster[tenure_years])

Senior % =
    DIVIDE(
        COUNTROWS(
            FILTER(vw_employee_roster, vw_employee_roster[seniority_level] = "Senior")
        ),
        COUNTROWS(vw_employee_roster)
    ) * 100
```

---

## Page 1 · Executive Overview

| # | Visual | Type | Fields |
|---|---|---|---|
| 1 | Year slicer | Slicer | `vw_exec_kpi_scorecard[performance_year]` — dropdown |
| 2 | Total Revenue | Card | `[Total Revenue]` |
| 3 | Total Profit | Card | `[Total Profit]` |
| 4 | Target Achievement | Card | `[Target Achievement %]` |
| 5 | Revenue vs Target | Card | `[Revenue vs Target]` — red/green conditional colour |
| 6 | Monthly trend | Column + Line | Axis: `month_start` / Column: `monthly_revenue` / Line: `monthly_profit` |
| 7 | Segment split | Donut | Legend: `segment` / Values: `total_revenue` from `vw_exec_segment_summary` |

> [!TIP]
> Segment donut cross-filter fix: Format ribbon → Edit interactions → click **filter icon** (funnel) on the donut from both the year slicer and the trend chart.

---

## Page 2 · Customer Analytics

| # | Visual | Type | Fields |
|---|---|---|---|
| 1 | Segment slicer | Slicer | `vw_customer_performance[customer_segment]` |
| 2 | Year slicer | Slicer | `vw_customer_yearly_revenue[year]` |
| 3 | Top customers | Table | `customer_id`, `country`, `total_revenue`, `profit_margin_pct`, `avg_order_value`, `active_years` |
| 4 | Revenue map | Filled Map | Location: `country` / Size: `total_revenue` |
| 5 | RFM scatter | Scatter | X: `frequency` / Y: `monetary` / Size: `rfm_total` / Legend: `rfm_segment` |
| 6 | RFM segments | Bar | Axis: `rfm_segment` / Values: `COUNT(customer_id)` |

---

## Page 3 · Product Analytics

| # | Visual | Type | Fields |
|---|---|---|---|
| 1 | Year slicer | Slicer | `vw_product_monthly_trend[order_year]` |
| 2 | Product KPIs | Card ×4 | `total_revenue` filtered per `product_id` |
| 3 | Revenue trend | Line | Axis: `month_start` / Lines: `revenue` per `product_id` |
| 4 | Segment matrix | Matrix | Rows: `product_id` / Columns: `segment` / Values: `revenue` |
| 5 | Pricing bars | Clustered Bar | `avg_actual_unit_price`, `avg_target_price`, `avg_mfg_price` per `product_id` |

---

## Page 4 · Revenue Forecast

| # | Visual | Type | Fields |
|---|---|---|---|
| 1 | Actual vs target | Column + Line | Bar: `actual_revenue` / Line: `targeted_revenue` / Axis: `performance_year` |
| 2 | Target status | Card | `[Target Achievement %]` — green ≥100%, red <100% |
| 3 | Forecast line | Line | Axis: `year` / Values: `actual_revenue` + `projected_revenue` / Legend: `record_type` |
| 4 | Growth line | Line | Axis: `year` / Values: `yoy_revenue_growth_pct`, `cagr_from_base_pct` |
| 5 | Seasonality | Column | Axis: `month_abbr` / Values: `avg_month_share_pct` |

---

## Page 5 · Capital Budgeting

| # | Visual | Type | Fields |
|---|---|---|---|
| 1 | Project slicer | Slicer | `vw_capex_project_summary[product_id]` |
| 2 | NPV | Card | `[Total NPV]` — green if positive |
| 3 | Payback period | Card | `payback_period` |
| 4 | Profitability Index | Card | `[Profitability Index]` — >1.0 = viable |
| 5 | Cash flow | Waterfall | Category: `cashflow_date` / Y: `operational_cashflow` |
| 6 | Cumulative | Line | Axis: `cashflow_date` / Values: `cumulative_cashflow` |
| 7 | Sensitivity | Matrix | Rows: `product_id` / Columns: `discount_rate` / Values: `npv` |

> [!TIP]
> Sensitivity matrix: select NPV values → Conditional formatting → Background colour → value > 0 green scale, value < 0 red scale.

---

## Page 6 · Employee Analytics

| # | Visual | Type | Fields |
|---|---|---|---|
| 1 | Headcount | Card | `[Total Headcount]` |
| 2 | Avg Tenure | Card | `[Avg Tenure]` |
| 3 | Senior % | Card | `[Senior %]` |
| 4 | Dept headcount | Clustered Bar | Axis: `department` / Values: `headcount`, `senior_count` |
| 5 | Tenure dist | Stacked Bar | Axis: `department` / Legend: `tenure_band` / Values: `headcount` |
| 6 | Hiring cohort | Stacked Column | Axis: `hire_year` / Legend: `department` / Values: `hires` |
| 7 | Roster | Table | `employee_name`, `department`, `tenure_years`, `seniority_level` — drill-through target |

**Set up drill-through on roster table:**
1. Select the roster table visual
2. Visualizations pane → **Drill through** section
3. Drag `department` into the drill-through field
4. Right-click any dept bar → Drill through → Employee Roster

---

## Cross-Filter Setup (all pages)

1. Click a visual → **Format** ribbon → **Edit interactions**
2. Set **filter icon** (funnel) on every visual that should respond
3. Avoid highlight icon — it dims instead of filters

| Page | Source | Must filter |
|---|---|---|
| Executive | Year slicer | Donut, monthly trend |
| Executive | Segment donut | Monthly trend |
| Customer | Segment slicer | Map, RFM scatter, table |
| Customer | Year slicer | All customer visuals |
| Product | Year slicer | All product visuals |
| CapEx | Project slicer | Waterfall, cumulative line, sensitivity |

---

## Refresh Workflow

```bash
# 1. Drop updated Excel into data/
# 2. Re-run pipeline
docker compose run --rm elt_pipeline
# 3. Power BI Desktop → Home → Refresh
```

---

## Related

- [[SPAERO_REVENUE_ANALYSIS]] — Parent project note
- [[transform]] — Creates presentation.* views consumed here
- [[inspect_views]] — Validate before refreshing
