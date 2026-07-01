

## 📌 Purpose

Layer user‑defined descriptions and data tests on top of models to ensure clarity, governance, and trust in analytics workflows.

## 📂 User‑Defined Descriptions

- Documentation is critical for **understanding, maintaining, and collaborating** on code.
    
- dbt uses **YAML files** for descriptions.
    
- YAML can document: models, sources, seeds, and tests.
    
- Store YAML in the **same directory** as the asset.
    
- Best practice: name YAML files similar to the asset (e.g., `looker_models.yml`).
    

## 🛠️ Model YAML Structure

- **Version**: Always set to `2` (latest schema format).
    
- **Keyword**: `models` for documenting models; `sources` for documenting sources.
    
- **Indentation**:
    
    - Model names → 2 spaces + dash + name.
        
    - Column names → 4 spaces.
        
- Document both **models** and **columns**.
    

## ⚙️ dbt Data Tests

### 🔑 Unique Test

- Ensures no duplicate values in a column.
    
- Commonly applied to primary keys.
    

### 🔑 Not Null Test

- Ensures no null values in a column.
    
- Ignores empty strings.
    
- Often paired with `unique` for primary keys.
    

### 🔑 Accepted Values Test

- Restricts column values to a predefined list.
    
- Guards against **data drift**.
    

### 🔑 Relationships Test

- dbt’s version of foreign keys.
    
- Ensures values in one column exist in another table’s column.
    
- Validates upstream → downstream propagation.
    

## 📊 Repository Example

Code

```
/models
  users_staging.sql
  users_staging.yml   # docs + tests
/sources
  sources.yml         # source docs
```

## 📐 Best Practices

- Align YAML naming with asset names.
    
- Apply `unique` + `not_null` to primary keys.
    
- Use `accepted_values` for categorical fields.
    
- Use `relationships` for foreign key integrity.
    
- Reference: [dbt best practices](https://docs.getdbt.com/best-practices)