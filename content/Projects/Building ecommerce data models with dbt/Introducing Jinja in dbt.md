

## 🎬 Overview

Jinja is a Pythonic templating language that dbt uses to make SQL dynamic, reusable, and less repetitive. You’ve already been using it without realizing — every `{{ source() }}` call is Jinja!

## 📖 Three Languages in dbt

- **SQL** → transformations
    
- **YAML** → documentation
    
- **Jinja** → templating
    

## 📝 Types of Jinja

- **Statements** → `{% ... %}` (control flow, variables, macros)
    
- **Expressions** → `{{ ... }}` (evaluate and insert values)
    
- **Comments** → `{# ... #}` (ignored by compiler)
    

Example:

sql

```
-- Jinja statement
{% set country = 'Australia' %}

-- Jinja expression
SELECT * 
FROM {{ source('ecommerce', 'customers') }}
WHERE country = '{{ country }}'
```

## ⚙️ Set Statement

Creates a variable for reuse. Helpful for clarity when filtering or repeating logic.

sql

```
{% set country = 'Australia' %}

SELECT *
FROM {{ ref('stg_customers') }}
WHERE country = '{{ country }}'
```

## 🔍 Compile with dbt

Use `dbt compile` to check what Jinja generates:

- Outputs compiled SQL in terminal (if single model specified).
    
- Creates a `target/` folder with compiled files for inspection.
    

bash

```
dbt compile --select stg_customers
```

## 🚀 Next Steps

- Explore **loops** and **conditionals** in Jinja.
    
- Build **macros** for reusable SQL snippets.
    
- Add **tests** that leverage Jinja expressions.