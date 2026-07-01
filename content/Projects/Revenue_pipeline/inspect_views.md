# 🔍 inspect_views

**Script:** `scripts/inspect_views.py`  
**Role:** Step 3 of 3 — Validate all views and row counts after transform  
**Parent:** [[SPAERO_REVENUE_ANALYSIS]]  
**Tags:** #script #validation #inspection

---

## Purpose

Queries every object across all three analytical layers and prints row counts + 5-row previews. Confirms the pipeline deployed cleanly before opening Power BI.

---

## Run Modes

```bash
# Full inspection — all 28 objects across all layers
docker compose run --rm elt_pipeline python inspect_views.py

# One dashboard page group (partial match on group name)
docker compose run --rm elt_pipeline python inspect_views.py --group "staging"
docker compose run --rm elt_pipeline python inspect_views.py --group "customer"
docker compose run --rm elt_pipeline python inspect_views.py --group "product"
docker compose run --rm elt_pipeline python inspect_views.py --group "capital"
docker compose run --rm elt_pipeline python inspect_views.py --group "employee"
docker compose run --rm elt_pipeline python inspect_views.py --group "forecast"
docker compose run --rm elt_pipeline python inspect_views.py --group "executive"

# Single specific view
docker compose run --rm elt_pipeline python inspect_views.py --view presentation.vw_customer_rfm
docker compose run --rm elt_pipeline python inspect_views.py --view analytics.mart_annual_performance
docker compose run --rm elt_pipeline python inspect_views.py --view int.stg_employees
```

---

## View Groups Inspected

| Group | Views |
|---|---|
| INT STAGING LAYER | `stg_customers`, `stg_sales`, `stg_revenue_targets`, `stg_cash_flow`, `stg_employees` |
| ANALYTICS DIMS & MARTS | All 3 dims + 5 marts |
| PAGE 1 · Executive Overview | 3 views |
| PAGE 2 · Customer Analytics | 4 views |
| PAGE 3 · Product Analytics | 4 views |
| PAGE 4 · Revenue Forecast | 4 views |
| PAGE 5 · Capital Budgeting | 3 views |
| PAGE 6 · Employee Analytics | 4 views |

---

## Expected Row Counts

| Object | Expected |
|---|---|
| `int.stg_sales` | 6,320 |
| `int.stg_customers` | 130 |
| `int.stg_revenue_targets` | 7 |
| `analytics.dim_date` | 7,671 (2015–2035) |
| `analytics.mart_annual_performance` | 7 (2015–2021) |
| `analytics.mart_monthly_sales` | 84 |
| `analytics.mart_customer_sales` | 130 |
| `analytics.mart_product_sales` | 4 |
| `presentation.vw_revenue_seasonality` | 12 |
| `presentation.vw_capex_sensitivity` | 14 (2 projects × 7 rates) |
| `presentation.vw_capex_project_summary` | 2 |

> [!TIP]
> If any view returns 0 rows or errors, the corresponding `transform.py` block failed silently or the upstream staging view was dropped. Re-run `docker compose run --rm elt_pipeline` and check the logs.

---

## Sample Output

```
════════════════════════════════════════════════════════════════════════════════
   SPAERO DATA WAREHOUSE – FULL LAYER INSPECTION
════════════════════════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  INT STAGING LAYER  (int.*)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ➔  int.stg_sales
  ──────────────────────────────────────────────────────────────────────────────
  Rows: 6320   |   Columns: 17
  Columns: ['order_id', 'order_date', 'order_year', ...]
  ...
```

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `relation does not exist` | Transform block failed or never ran | Re-run `docker compose run --rm elt_pipeline` |
| `View returned empty recordset` | Raw table empty — extract failed | Check `docker logs spaero_elt` |
| `Failed to fetch structural view details` | DB connection error | Check `.env` credentials and port |

---

## Related

- [[SPAERO_REVENUE_ANALYSIS]] — Parent project note
- [[transform]] — Previous step, creates all objects being inspected
- [[powerbi_guide]] — Next step after clean inspection
