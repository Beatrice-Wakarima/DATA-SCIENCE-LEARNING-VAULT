---
title: dbt Macros and Jinja
tags: [dbt, macros, jinja, advanced]
created: 2026-05-20
up:: [[DBT MOC]]
---

# 🧩 dbt Macros & Jinja

> Macros are reusable SQL functions written in Jinja — Python's templating language. They eliminate repetition, enforce consistency, and make your dbt project DRY (Don't Repeat Yourself).

---

## What is Jinja?

```sql
-- Jinja adds logic to SQL using {{ }}, {% %}, {# #}

{{ expression }}        -- Output a value
{% statement %}         -- Logic (if, for, set)
{# comment #}           -- Comment (not in output)

-- Example
SELECT
    customer_id,
    {{ 'balance' }}     -- outputs: balance
FROM customers
{% if is_incremental() %}
WHERE created_at > (SELECT MAX(created_at) FROM {{ this }})
{% endif %}
```

---

## Built-in Jinja Variables

```sql
-- {{ this }} — reference the current model
SELECT * FROM {{ this }}

-- {{ model }} — current model metadata
-- {{ model.name }} — model name
-- {{ model.schema }} — model schema

-- {{ target }} — current target (dev/prod)
-- {{ target.name }} — 'dev' or 'prod'
-- {{ target.schema }} — target schema
-- {{ target.type }} — 'postgres', 'snowflake', etc.

-- {{ run_started_at }} — when dbt run started
-- {{ invocation_id }} — unique run ID

-- Example: different logic per environment
{% if target.name == 'prod' %}
    WHERE created_at >= '2020-01-01'
{% else %}
    WHERE created_at >= '2025-01-01'  -- Smaller dataset for dev
{% endif %}
```

---

## dbt Variables

```yaml
# dbt_project.yml — define variables
vars:
  start_date: '2020-01-01'
  days_back: 30
  environment: 'dev'
  subscription_min_rate: 5.0
```

```sql
-- Use variables in models
SELECT *
FROM {{ ref('stg_transactions') }}
WHERE created_at >= '{{ var("start_date") }}'

-- With default value
WHERE created_at >= '{{ var("start_date", "2020-01-01") }}'
```

```bash
# Override variables at runtime
dbt run --vars '{"start_date": "2026-01-01", "days_back": 7}'
dbt run --vars '{"environment": "prod"}'
```

---

## Your First Macro

```sql
-- macros/cents_to_shillings.sql
-- Convert cents to KES shillings

{% macro cents_to_shillings(column_name) %}
    ROUND({{ column_name }} / 100.0, 2)
{% endmacro %}
```

```sql
-- Use it in a model
SELECT
    customer_id,
    {{ cents_to_shillings('balance_cents') }} AS balance_kes,
    {{ cents_to_shillings('transaction_amount_cents') }} AS amount_kes
FROM raw_transactions
```

---

## Useful Macro Patterns

### Surrogate Key
```sql
-- macros/generate_surrogate_key.sql
{% macro generate_surrogate_key(field_list) %}
    MD5(
        CAST(CONCAT_WS('|',
            {% for field in field_list %}
                COALESCE(CAST({{ field }} AS VARCHAR), '')
                {% if not loop.last %}, {% endif %}
            {% endfor %}
        ) AS VARCHAR)
    )
{% endmacro %}
```

```sql
-- Use in a model
SELECT
    {{ generate_surrogate_key(['customer_id', 'month']) }} AS pk,
    customer_id,
    month,
    revenue
FROM monthly_stats
```

### Current Timestamp
```sql
-- macros/current_timestamp.sql
{% macro current_timestamp() %}
    CAST(NOW() AT TIME ZONE 'Africa/Nairobi' AS TIMESTAMP)
{% endmacro %}
```

### Safe Divide
```sql
-- macros/safe_divide.sql
{% macro safe_divide(numerator, denominator) %}
    CASE
        WHEN {{ denominator }} = 0 OR {{ denominator }} IS NULL
        THEN NULL
        ELSE ROUND(CAST({{ numerator }} AS DECIMAL) / {{ denominator }}, 4)
    END
{% endmacro %}
```

```sql
-- Use it
SELECT
    {{ safe_divide('subscriptions', 'total_contacts') }} AS conversion_rate,
    {{ safe_divide('revenue', 'num_customers') }} AS revenue_per_customer
FROM campaign_stats
```

### Date Spine (Generate date series)
```sql
-- macros/date_spine.sql
{% macro date_spine(start_date, end_date) %}
    SELECT
        GENERATE_SERIES(
            '{{ start_date }}'::DATE,
            '{{ end_date }}'::DATE,
            '1 day'::INTERVAL
        )::DATE AS date_day
{% endmacro %}
```

---

## Conditional Logic in Models

```sql
-- models/marts/fct_campaign_performance.sql
{{
    config(
        materialized='incremental' if target.name == 'prod' else 'table'
    )
}}

WITH base AS (
    SELECT * FROM {{ ref('stg_bank_marketing') }}
    
    -- Load less data in dev
    {% if target.name != 'prod' %}
    LIMIT 5000
    {% endif %}
),

campaign_stats AS (
    SELECT
        job,
        education,
        marital,
        balance_segment,
        age_segment,
        COUNT(*)                                            AS total_contacts,
        SUM(CASE WHEN subscribed THEN 1 ELSE 0 END)        AS subscriptions,
        {{ safe_divide('SUM(CASE WHEN subscribed THEN 1 ELSE 0 END)', 'COUNT(*)') }}
            AS conversion_rate,
        ROUND(AVG(balance), 2)                             AS avg_balance,
        ROUND(AVG(call_duration_seconds), 0)               AS avg_call_duration,
        {{ current_timestamp() }}                          AS updated_at
    FROM base
    GROUP BY 1, 2, 3, 4, 5
)

SELECT * FROM campaign_stats
```

---

## For Loops in Macros

```sql
-- macros/union_tables.sql
-- Union multiple tables with the same structure

{% macro union_tables(tables) %}
    {% for table in tables %}
        SELECT *, '{{ table }}' AS source_table
        FROM {{ ref(table) }}
        {% if not loop.last %} UNION ALL {% endif %}
    {% endfor %}
{% endmacro %}
```

```sql
-- Use it
{{ union_tables([
    'stg_transactions_2024',
    'stg_transactions_2025',
    'stg_transactions_2026'
]) }}
```

### Generate Columns Dynamically
```sql
-- macros/pivot_values.sql
{% macro pivot_values(column, values) %}
    {% for value in values %}
        SUM(CASE WHEN {{ column }} = '{{ value }}'
            THEN 1 ELSE 0 END) AS {{ value | replace(' ', '_') | lower }}_count
        {% if not loop.last %},{% endif %}
    {% endfor %}
{% endmacro %}
```

```sql
-- Pivot job types automatically
SELECT
    month,
    {{ pivot_values('job', [
        'admin', 'technician', 'management',
        'blue-collar', 'services', 'retired'
    ]) }}
FROM {{ ref('stg_bank_marketing') }}
GROUP BY month
```

---

## Pre and Post Hooks

```sql
-- Run SQL before/after model materialisation
{{
    config(
        materialized='table',
        pre_hook=[
            "DROP TABLE IF EXISTS {{ this }}_backup",
            "CREATE TABLE IF NOT EXISTS {{ this }}_backup AS SELECT * FROM {{ this }}"
        ],
        post_hook=[
            "GRANT SELECT ON {{ this }} TO bi_reader",
            "GRANT SELECT ON {{ this }} TO reporting_user",
            "ANALYZE {{ this }}"    -- Update table statistics
        ]
    )
}}

SELECT * FROM {{ ref('stg_customers') }}
```

---

## Custom Schema Macro

```sql
-- macros/generate_schema_name.sql
-- Control how dbt names schemas in different environments

{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    
    {%- if target.name == 'prod' -%}
        -- Production: use exact schema names
        {%- if custom_schema_name is none -%}
            {{ default_schema }}
        {%- else -%}
            {{ custom_schema_name | trim }}
        {%- endif -%}
    
    {%- else -%}
        -- Development: prefix with username to avoid conflicts
        {%- if custom_schema_name is none -%}
            {{ default_schema }}
        {%- else -%}
            {{ default_schema }}_{{ custom_schema_name | trim }}
        {%- endif -%}
    
    {%- endif -%}
{%- endmacro %}
```

---

## Packages — Pre-built Macros

```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: [">=1.0.0", "<2.0.0"]
  
  - package: dbt-labs/codegen
    version: [">=0.12.0", "<1.0.0"]
  
  - package: calogica/dbt_expectations
    version: [">=0.10.0", "<1.0.0"]
```

```bash
# Install packages
dbt deps
```

```sql
-- dbt_utils macros you'll use daily:
{{ dbt_utils.generate_surrogate_key(['customer_id', 'month']) }}
{{ dbt_utils.star(from=ref('stg_customers'), except=['loaded_at']) }}
{{ dbt_utils.pivot('job', ['admin','technician','management']) }}
{{ dbt_utils.date_spine(datepart='day', start_date="'2026-01-01'", end_date="'2026-12-31'") }}
```

---

## codegen — Auto-Generate YAML

```bash
# Auto-generate model YAML from existing table
dbt run-operation codegen.generate_model_yaml \
  --args '{"model_names": ["stg_customers", "stg_transactions"]}'

# Auto-generate source YAML from database schema
dbt run-operation codegen.generate_source \
  --args '{"schema_name": "bronze"}'
```

---

## Macro Best Practices

```sql
-- ✅ Document your macros
{#
  Macro: safe_divide
  Purpose: Divide two values safely, returning NULL instead of error
  Args:
    numerator (str): The dividend column or expression
    denominator (str): The divisor column or expression
  Returns: DECIMAL or NULL
  Example: {{ safe_divide('revenue', 'customers') }}
#}
{% macro safe_divide(numerator, denominator) %}
    CASE WHEN {{ denominator }} = 0 THEN NULL
         ELSE {{ numerator }}::DECIMAL / {{ denominator }}
    END
{% endmacro %}

-- ✅ Use default arguments
{% macro limit_in_dev(n=1000) %}
    {% if target.name != 'prod' %}
    LIMIT {{ n }}
    {% endif %}
{% endmacro %}

-- ✅ Keep macros focused (one thing each)
-- ❌ Don't build 200-line macros
```

---

## Quick Reference

```sql
-- Jinja syntax
{{ value }}             -- Output expression
{% if condition %}      -- Conditional
{% for item in list %}  -- Loop
{% set x = value %}     -- Set variable
{# comment #}           -- Comment

-- dbt variables
{{ var('my_var') }}
{{ var('my_var', 'default') }}

-- dbt built-ins
{{ this }}              -- Current model
{{ target.name }}       -- dev/prod
{{ ref('model') }}      -- Reference model
{{ source('src','tbl')}} -- Reference source

-- Define macro
{% macro name(arg1, arg2='default') %}
    SQL using {{ arg1 }} and {{ arg2 }}
{% endmacro %}

-- Call macro
{{ macro_name(column, optional_arg) }}
```

---

## Previous | Next
← [[04 - dbt Documentation]] | → [[06 - dbt Snapshots and Seeds]]
