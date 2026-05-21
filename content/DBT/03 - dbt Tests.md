---
title: dbt Tests
tags: [dbt, testing, data-quality]
created: 2026-05-20
up:: [[DBT MOC]]
---

# ✅ dbt Tests

> dbt tests are automated assertions about your data. They catch data quality issues before they reach Power BI dashboards or executive reports. Every production dbt project must have tests.

---

## Why Test Your Data?

```
Without tests:           With tests:
  Bad data → BI tool       Bad data → dbt test FAILS → alert sent
  Dashboard shows wrong    Data engineer fixes issue
  numbers                  Clean data reaches dashboard
  Executive makes bad      Executive makes good decisions
  decisions
```

---

## Two Types of Tests

```
1. Generic tests  — Built-in, configured in YAML
2. Singular tests — Custom SQL you write
```

---

## Generic Tests — YAML Configuration

```yaml
# models/staging/_stg_models.yml
version: 2

models:
  - name: stg_bank_marketing
    description: "Cleaned bank marketing campaign data"
    
    columns:
      - name: age
        description: "Customer age in years"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 18
              max_value: 95

      - name: job
        description: "Customer job type"
        tests:
          - not_null
          - accepted_values:
              values:
                - 'admin'
                - 'technician'
                - 'management'
                - 'blue-collar'
                - 'services'
                - 'retired'
                - 'self-employed'
                - 'entrepreneur'
                - 'housemaid'
                - 'student'
                - 'unemployed'
                - 'unknown'

      - name: balance
        description: "Customer bank balance in EUR"
        tests:
          - not_null

      - name: subscribed
        description: "Whether customer subscribed to term deposit"
        tests:
          - not_null
          - accepted_values:
              values: [true, false]

  - name: stg_customers
    description: "Cleaned customer dimension"
    
    columns:
      - name: customer_id
        description: "Primary key"
        tests:
          - unique
          - not_null
      
      - name: email
        description: "Customer email address"
        tests:
          - unique
          - not_null
      
      - name: tier
        tests:
          - accepted_values:
              values: ['bronze', 'silver', 'gold', 'platinum']
      
      - name: balance
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0

  - name: stg_transactions
    columns:
      - name: transaction_id
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - not_null
          - relationships:             # Referential integrity!
              to: ref('stg_customers')
              field: customer_id
      - name: amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              inclusive: false         # Must be > 0, not >= 0
```

---

## The 4 Built-in Generic Tests

```yaml
# 1. unique — no duplicate values
- unique

# 2. not_null — no null values
- not_null

# 3. accepted_values — only specific values allowed
- accepted_values:
    values: ['bronze', 'silver', 'gold', 'platinum']

# 4. relationships — foreign key integrity
- relationships:
    to: ref('stg_customers')
    field: customer_id
```

---

## Singular Tests — Custom SQL

```sql
-- tests/assert_positive_balances.sql
-- Returns rows that FAIL the test (should return 0 rows)

SELECT
    customer_id,
    balance
FROM {{ ref('stg_customers') }}
WHERE balance < 0
```

```sql
-- tests/assert_subscription_rate_reasonable.sql
-- Subscription rate should be between 1% and 50%

WITH stats AS (
    SELECT
        COUNT(*) AS total,
        SUM(CASE WHEN subscribed THEN 1 ELSE 0 END) AS subscribed_count,
        ROUND(
            100.0 * SUM(CASE WHEN subscribed THEN 1 ELSE 0 END) / COUNT(*),
            2
        ) AS subscription_rate
    FROM {{ ref('stg_bank_marketing') }}
)
SELECT *
FROM stats
WHERE subscription_rate < 1
   OR subscription_rate > 50
-- Returns rows if rate is outside expected range (fails test)
```

```sql
-- tests/assert_no_future_transactions.sql
-- Transactions should not be in the future

SELECT
    transaction_id,
    created_at
FROM {{ ref('stg_transactions') }}
WHERE created_at > NOW()
```

```sql
-- tests/assert_revenue_matches_transactions.sql
-- Monthly revenue in mart should match raw transaction sum

WITH mart_revenue AS (
    SELECT SUM(total_revenue) AS mart_total
    FROM {{ ref('fct_monthly_revenue') }}
),
raw_revenue AS (
    SELECT SUM(amount) AS raw_total
    FROM {{ ref('stg_transactions') }}
)
SELECT
    mart_total,
    raw_total,
    ABS(mart_total - raw_total) AS discrepancy
FROM mart_revenue, raw_revenue
WHERE ABS(mart_total - raw_total) > 0.01    -- Tolerance for rounding
```

---

## Source Freshness Tests

```yaml
# models/staging/_sources.yml
sources:
  - name: raw
    schema: bronze
    tables:
      - name: transactions
        loaded_at_field: loaded_at        # Column tracking load time
        freshness:
          warn_after:
            count: 6
            period: hour                  # Warn if no data for 6 hours
          error_after:
            count: 12
            period: hour                  # Error if no data for 12 hours

      - name: customers
        loaded_at_field: updated_at
        freshness:
          warn_after: {count: 24, period: hour}
          error_after: {count: 48, period: hour}
```

```bash
# Check source freshness
dbt source freshness
```

---

## dbt-utils — Extended Tests

```bash
# Install dbt-utils
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: [">=1.0.0", "<2.0.0"]

dbt deps   # Install packages
```

```yaml
# Available dbt_utils tests
columns:
  - name: created_at
    tests:
      - dbt_utils.not_null_proportion:
          at_least: 0.95              # 95% must be non-null

      - dbt_utils.accepted_range:
          min_value: 0
          max_value: 1000000
          inclusive: true

  - name: customer_id
    tests:
      - dbt_utils.not_empty_string
      - dbt_utils.expression_is_true:
          expression: "> 0"
```

---

## Model-Level Tests

```yaml
# Test at the model level (not column level)
models:
  - name: fct_monthly_revenue
    tests:
      # No duplicate month + city combinations
      - unique:
          column_name: "month || city"
      
      # Custom expression test
      - dbt_utils.expression_is_true:
          expression: "total_revenue >= 0"
          name: revenue_is_non_negative
```

---

## Running Tests

```bash
# Run all tests
dbt test

# Test specific model
dbt test --select stg_customers

# Test specific model and downstream
dbt test --select stg_customers+

# Test by type
dbt test --select test_type:generic
dbt test --select test_type:singular

# Test by tag
dbt test --select tag:critical

# Run build (models + tests together)
dbt build

# Build specific model with its tests
dbt build --select stg_customers
```

---

## Test Severity — Warn vs Error

```yaml
columns:
  - name: email
    tests:
      - not_null:
          severity: error        # FAILS the run (default)

  - name: phone
    tests:
      - not_null:
          severity: warn         # WARNS but continues run

  - name: balance
    tests:
      - dbt_utils.accepted_range:
          min_value: 0
          severity: warn
          config:
            limit: 100           # Only show first 100 failures
```

---

## Real World — Complete Test Suite

```yaml
# models/marts/_mart_models.yml
version: 2

models:
  - name: fct_monthly_revenue
    description: "Monthly revenue aggregated by city and tier"
    tests:
      - dbt_utils.recency:
          datepart: month
          field: month
          interval: 1             # Data should be within last month
    
    columns:
      - name: month
        tests:
          - not_null
      
      - name: city
        tests:
          - not_null
      
      - name: total_revenue
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              severity: error
      
      - name: unique_customers
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0

  - name: dim_customers
    description: "Customer dimension with enriched attributes"
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      
      - name: tier
        tests:
          - not_null
          - accepted_values:
              values: ['bronze', 'silver', 'gold', 'platinum']
      
      - name: lifetime_value
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```

---

## CI/CD — Tests in Pipeline

```bash
# .github/workflows/dbt_ci.yml
# (or run in Airflow)

# On every pull request:
dbt deps                          # Install packages
dbt debug                         # Test connection
dbt source freshness              # Check source data
dbt build --select state:modified+  # Build + test changed models

# On production deploy:
dbt build --target prod           # Full run with tests
```

---

## Quick Reference

```bash
# Run tests
dbt test                          # All tests
dbt test --select model_name      # Specific model
dbt test --select tag:critical    # By tag
dbt source freshness              # Source freshness

# Test types in YAML
- unique
- not_null
- accepted_values:
    values: [...]
- relationships:
    to: ref('model')
    field: column

# Singular test
-- tests/my_test.sql
SELECT * FROM {{ ref('model') }}
WHERE condition_that_should_be_false
```

---

## Previous | Next
← [[02 - dbt Models and Sources]] | → [[04 - dbt Documentation]]
