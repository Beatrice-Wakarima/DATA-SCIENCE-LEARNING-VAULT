# 📥 extract_load

**Script:** `scripts/extract_load.py`  
**Role:** Step 1 of 3 — Extract Excel files → Load into `raw.*`  
**Parent:** [[SPAERO_REVENUE_ANALYSIS]]  
**Tags:** #script #extract #load #raw

---

## Purpose

Scans `data/*.xlsx`, reads every sheet, and loads each into a dedicated table in the `raw` schema. Fully idempotent — safe to re-run any number of times without duplicating data.

---

## Execution Flow

```
ingest_all_excel_files()
    │
    ├── test_connection()          ← probe DB before doing any work
    ├── ensure_metadata_table()    ← create raw.ingestion_log if not exists
    │
    └── for each .xlsx in data/
            process_workbook()
                │
                └── for each sheet
                        sanitize_columns()     ← snake_case all column names
                        validate_dataframe()   ← skip empty / all-null sheets
                        load_dataframe()       ← TRUNCATE if exists, then append
                        log_ingestion()        ← record to raw.ingestion_log
```

---

## Idempotent Load Pattern

```python
if table_exists(engine, clean_table_name):
    TRUNCATE TABLE raw."<table>"    # wipe stale rows
    run_mode = "full_refresh"
else:
    run_mode = "initial_load"       # first run

df.to_sql(..., if_exists="append")  # always appends into empty table
```

> [!WARNING]
> Never change `if_exists="append"` to `"replace"` — that would drop and recreate the table schema on every run, breaking downstream views.

---

## Column Sanitization Rules

`clean_string()` converts column names to snake_case:

| Input | Output |
|---|---|
| `Order Date` | `order_date` |
| `Units Sold` | `units_sold` |
| `Tenure (Years)` | `tenure_(years)_` → quoted in SQL as `"tenure_(years)"` |
| `Discount/Premium Band` | `discount_premium_band` |

> [!NOTE]
> Parentheses survive sanitization but become special characters. Always quote them in SQL: `"tenure_(years)"::NUMERIC`

---

## Raw Table Mapping

| Source File | Sheet | Raw Table |
|---|---|---|
| `spaero_sales.xlsx` | `Sales_Fact` | `raw.spaero_sales_sales_fact` |
| `spaero_sales.xlsx` | `Customer_Dim` | `raw.spaero_sales_customer_dim` |
| `revenue_targets.xlsx` | `Revenue Targets` | `raw.revenue_targets_revenue_targets` |
| `Capital_Budgeting.xlsx` | `Cash Flow` | `raw.capital_budgeting_cash_flow` |
| `Employee_Fact.xlsx` | `Sheet1` | `raw.employee_fact_sheet1` |

---

## Ingestion Log

```sql
-- Check last run
SELECT file_name, sheet_name, table_name, row_count, run_mode, ingested_at
FROM raw.ingestion_log
ORDER BY ingested_at DESC
LIMIT 10;

-- Check all runs for a specific table
SELECT * FROM raw.ingestion_log
WHERE table_name = 'spaero_sales_sales_fact'
ORDER BY ingested_at DESC;
```

---

## Expected Output

```
[INFO] Found 4 source workbook(s) for ingestion.
[INFO]    ↺  Truncated raw.spaero_sales_sales_fact (full refresh).
[INFO]    ✔  raw.spaero_sales_sales_fact  (6,320 rows)  [full_refresh]
[INFO]    ✔  raw.spaero_sales_customer_dim  (141 rows)  [full_refresh]
[INFO]    ✔  raw.revenue_targets_revenue_targets  (7 rows)  [full_refresh]
[INFO]    ✔  raw.capital_budgeting_cash_flow  (N rows)  [full_refresh]
[INFO]    ✔  raw.employee_fact_sheet1  (N rows)  [full_refresh]
[INFO]  Extract & Load pipeline complete.
```

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `No Excel files found in data/` | `data/` folder empty or wrong path | Check files are in `data/` not project root |
| `Connection failed` | Wrong `DB_HOST` or port | Check `.env` — `DB_HOST=postgres_warehouse`, `DB_PORT=5432` |
| `Validation warning: entirely null columns` | Excel sheet has blank columns | Safe to ignore — data still loads |

---

## Related

- [[SPAERO_REVENUE_ANALYSIS]] — Parent project note
- [[transform]] — Next step, reads from `raw.*`
- [[docker_setup]] — How this script runs inside Docker
