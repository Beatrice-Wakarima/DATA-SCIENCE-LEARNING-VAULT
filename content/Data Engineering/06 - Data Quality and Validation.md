---
title: Data Quality and Validation
tags: [data-engineering, data-quality, testing, validation]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# ✅ Data Quality & Validation

> Bad data is worse than no data — it leads to wrong decisions made with false confidence. Data quality checks at every pipeline stage catch issues before they reach executives and ML models.

---

## The Cost of Bad Data

```
Without quality checks:
  Bad data flows into warehouse
  dbt builds broken metrics on bad data
  Power BI shows wrong numbers
  CFO makes budget decision on wrong numbers
  Company loses KES 10M

With quality checks:
  Pipeline detects bad data at source
  Alert sent immediately
  Engineer fixes before dashboard updates
  Correct numbers reach CFO
```

---

## The Data Quality Framework

```python
# src/quality/quality_framework.py
import pandas as pd
import logging
from dataclasses import dataclass
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)

@dataclass
class QualityCheck:
    """Define a single quality check"""
    name: str
    description: str
    severity: str           # 'error' | 'warning'
    check_fn: Callable
    threshold: Optional[float] = None

@dataclass
class CheckResult:
    """Result of a quality check"""
    check_name: str
    passed: bool
    value: Any
    message: str
    severity: str

class DataQualityValidator:
    """Run quality checks on a DataFrame"""

    def __init__(self, df: pd.DataFrame, source_name: str):
        self.df = df
        self.source_name = source_name
        self.results: list[CheckResult] = []

    def check_row_count(self, min_rows: int = 1,
                        max_rows: int = None,
                        severity: str = "error") -> "DataQualityValidator":
        count = len(self.df)
        passed = count >= min_rows
        if max_rows:
            passed = passed and count <= max_rows

        self.results.append(CheckResult(
            check_name="row_count",
            passed=passed,
            value=count,
            message=f"Row count: {count:,} (min: {min_rows:,})",
            severity=severity
        ))
        return self

    def check_not_null(self, columns: list,
                       severity: str = "error") -> "DataQualityValidator":
        for col in columns:
            if col not in self.df.columns:
                self.results.append(CheckResult(
                    check_name=f"not_null_{col}",
                    passed=False,
                    value=None,
                    message=f"Column '{col}' does not exist",
                    severity="error"
                ))
                continue

            null_count = self.df[col].isnull().sum()
            null_pct = null_count / len(self.df) * 100

            self.results.append(CheckResult(
                check_name=f"not_null_{col}",
                passed=null_count == 0,
                value=null_count,
                message=f"'{col}': {null_count:,} nulls ({null_pct:.1f}%)",
                severity=severity
            ))
        return self

    def check_unique(self, columns: list,
                     severity: str = "error") -> "DataQualityValidator":
        for col in columns:
            dupes = self.df[col].duplicated().sum()
            self.results.append(CheckResult(
                check_name=f"unique_{col}",
                passed=dupes == 0,
                value=dupes,
                message=f"'{col}': {dupes:,} duplicates",
                severity=severity
            ))
        return self

    def check_accepted_values(self, column: str,
                               values: list,
                               severity: str = "error") -> "DataQualityValidator":
        if column not in self.df.columns:
            return self
        invalid = ~self.df[column].isin(values)
        invalid_count = invalid.sum()
        self.results.append(CheckResult(
            check_name=f"accepted_values_{column}",
            passed=invalid_count == 0,
            value=invalid_count,
            message=f"'{column}': {invalid_count:,} invalid values. "
                   f"Sample: {self.df[column][invalid].unique()[:5].tolist()}",
            severity=severity
        ))
        return self

    def check_range(self, column: str,
                    min_val=None, max_val=None,
                    severity: str = "error") -> "DataQualityValidator":
        if column not in self.df.columns:
            return self
        series = pd.to_numeric(self.df[column], errors="coerce")
        violations = pd.Series([False] * len(series))

        if min_val is not None:
            violations |= series < min_val
        if max_val is not None:
            violations |= series > max_val

        violations |= series.isna()
        count = violations.sum()

        self.results.append(CheckResult(
            check_name=f"range_{column}",
            passed=count == 0,
            value=count,
            message=f"'{column}': {count:,} out-of-range values "
                   f"[{min_val}, {max_val}]",
            severity=severity
        ))
        return self

    def check_regex(self, column: str, pattern: str,
                    severity: str = "warning") -> "DataQualityValidator":
        if column not in self.df.columns:
            return self
        non_null = self.df[column].dropna()
        invalid = ~non_null.str.match(pattern)
        count = invalid.sum()
        self.results.append(CheckResult(
            check_name=f"regex_{column}",
            passed=count == 0,
            value=count,
            message=f"'{column}': {count:,} values don't match pattern",
            severity=severity
        ))
        return self

    def check_freshness(self, column: str,
                        max_hours: int = 24,
                        severity: str = "error") -> "DataQualityValidator":
        if column not in self.df.columns:
            return self
        max_ts = pd.to_datetime(self.df[column]).max()
        hours_old = (pd.Timestamp.now() - max_ts).total_seconds() / 3600

        self.results.append(CheckResult(
            check_name=f"freshness_{column}",
            passed=hours_old <= max_hours,
            value=round(hours_old, 1),
            message=f"Data is {hours_old:.1f}h old (max: {max_hours}h)",
            severity=severity
        ))
        return self

    def check_custom(self, name: str, condition: pd.Series,
                     description: str,
                     severity: str = "error") -> "DataQualityValidator":
        violations = (~condition).sum()
        self.results.append(CheckResult(
            check_name=name,
            passed=violations == 0,
            value=violations,
            message=f"{description}: {violations:,} violations",
            severity=severity
        ))
        return self

    def validate(self, raise_on_error: bool = True) -> dict:
        """Run all checks and return summary"""
        passed = [r for r in self.results if r.passed]
        warnings = [r for r in self.results
                    if not r.passed and r.severity == "warning"]
        errors = [r for r in self.results
                  if not r.passed and r.severity == "error"]

        # Log results
        for r in self.results:
            status = "✅" if r.passed else ("⚠️" if r.severity == "warning" else "❌")
            logger.info(f"{status} [{r.check_name}] {r.message}")

        summary = {
            "source": self.source_name,
            "total_checks": len(self.results),
            "passed": len(passed),
            "warnings": len(warnings),
            "errors": len(errors),
            "results": [vars(r) for r in self.results]
        }

        if errors and raise_on_error:
            error_names = [r.check_name for r in errors]
            raise ValueError(
                f"Data quality FAILED for {self.source_name}. "
                f"Failed checks: {error_names}"
            )

        return summary
```

---

## Bank Marketing Quality Checks

```python
# src/quality/bank_marketing_checks.py

def validate_bank_marketing(df: pd.DataFrame) -> dict:
    """Run all quality checks for bank marketing data"""

    return (
        DataQualityValidator(df, "bank_marketing")

        # Volume checks
        .check_row_count(min_rows=1000)

        # Null checks on critical columns
        .check_not_null(["age", "job", "balance", "y"])
        .check_not_null(["marital", "education"], severity="warning")

        # Range checks
        .check_range("age", min_val=18, max_val=95)
        .check_range("balance", min_val=-50000, max_val=200000,
                     severity="warning")
        .check_range("campaign", min_val=1, max_val=50)

        # Value checks
        .check_accepted_values("marital",
            ["single", "married", "divorced", "unknown"])
        .check_accepted_values("y", ["yes", "no"])
        .check_accepted_values("contact",
            ["cellular", "telephone", "unknown"])

        # Business logic checks
        .check_custom(
            "subscription_rate_reasonable",
            (df["y"] == "yes").mean() > 0.01,
            "Subscription rate > 1%"
        )
        .check_custom(
            "positive_call_duration_for_contacts",
            ~((df["duration"] == 0) & (df["y"] == "yes")),
            "No subscriptions with 0-second calls"
        )

        .validate(raise_on_error=True)
    )


# Usage in pipeline
df = pd.read_csv("data/bank_marketing.csv", sep=";")
quality_report = validate_bank_marketing(df)
print(f"Passed {quality_report['passed']}/{quality_report['total_checks']} checks")
```

---

## SQL-Based Quality Checks

```sql
-- Run after dbt models — validate the warehouse directly

-- 1. No duplicate customer IDs in dimension
SELECT customer_id, COUNT(*) AS cnt
FROM silver.bank_customers
GROUP BY customer_id
HAVING COUNT(*) > 1;
-- Expected: 0 rows

-- 2. Subscription rate sanity check
SELECT
    ROUND(100.0 * SUM(CASE WHEN subscribed THEN 1 ELSE 0 END)
          / COUNT(*), 2) AS subscription_rate
FROM silver.bank_customers;
-- Expected: between 5% and 20%

-- 3. Age distribution check
SELECT
    MIN(age) AS min_age,
    MAX(age) AS max_age,
    AVG(age) AS avg_age
FROM silver.bank_customers;
-- Expected: min 18, max 95, avg around 40

-- 4. All job values are valid
SELECT DISTINCT job FROM silver.bank_customers
WHERE job NOT IN (
    'admin', 'technician', 'management', 'blue-collar',
    'services', 'retired', 'self-employed', 'entrepreneur',
    'housemaid', 'student', 'unemployed', 'unknown'
);
-- Expected: 0 rows

-- 5. Revenue reconciliation — mart matches silver
SELECT
    ABS(
        (SELECT SUM(total_revenue) FROM gold.campaign_performance)
        -
        (SELECT COUNT(*) FROM silver.bank_customers)
    ) AS discrepancy;
-- Expected: 0

-- 6. Data freshness
SELECT
    MAX(processed_at)                           AS last_load,
    NOW() - MAX(processed_at)                  AS data_lag,
    CASE
        WHEN NOW() - MAX(processed_at) > INTERVAL '2 days'
        THEN 'STALE' ELSE 'FRESH'
    END                                         AS freshness_status
FROM silver.bank_customers;
```

---

## Great Expectations Integration

```python
# pip install great_expectations
import great_expectations as gx

context = gx.get_context()

# Define expectations
validator = context.sources.pandas_default.read_csv("bank_marketing.csv")

validator.expect_column_to_exist("age")
validator.expect_column_values_to_not_be_null("age")
validator.expect_column_values_to_be_between("age", min_value=18, max_value=95)
validator.expect_column_values_to_be_in_set("y", ["yes", "no"])
validator.expect_column_unique_value_count_to_be_between("job", min_value=5)

# Run and get results
results = validator.validate()
print(results.success)          # True/False
print(results.statistics)       # Summary stats
```

---

## Quality Dashboard in Power BI

```sql
-- Create quality metrics table for Power BI
CREATE TABLE quality_run_log (
    id              BIGSERIAL PRIMARY KEY,
    run_date        DATE,
    pipeline_name   VARCHAR(100),
    source_name     VARCHAR(100),
    check_name      VARCHAR(100),
    passed          BOOLEAN,
    check_value     DECIMAL,
    message         TEXT,
    severity        VARCHAR(20),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Query for Power BI dashboard
SELECT
    run_date,
    pipeline_name,
    COUNT(*) FILTER (WHERE passed = TRUE)   AS checks_passed,
    COUNT(*) FILTER (WHERE passed = FALSE
        AND severity = 'error')             AS errors,
    COUNT(*) FILTER (WHERE passed = FALSE
        AND severity = 'warning')           AS warnings,
    ROUND(100.0 * COUNT(*) FILTER (WHERE passed = TRUE)
          / COUNT(*), 1)                    AS pass_rate
FROM quality_run_log
WHERE run_date >= CURRENT_DATE - 30
GROUP BY run_date, pipeline_name
ORDER BY run_date DESC;
```

---

## Quick Reference

```python
# DataQualityValidator chaining
validator = (
    DataQualityValidator(df, "source_name")
    .check_row_count(min_rows=100)
    .check_not_null(["col1", "col2"])
    .check_unique(["id_col"])
    .check_accepted_values("status", ["active", "inactive"])
    .check_range("age", min_val=0, max_val=120)
    .check_regex("email", r"^[\w\.-]+@[\w\.-]+\.\w+$")
    .check_freshness("updated_at", max_hours=24)
    .validate(raise_on_error=True)
)

# Quality dimensions
Completeness  → not_null, row_count
Uniqueness    → unique, deduplication
Validity      → accepted_values, range, regex
Timeliness    → freshness, recency
Accuracy      → reconciliation, cross-system checks
Consistency   → format checks, referential integrity
```

---

## Previous | Next
← [[05 - Data Warehouse Design]] | → [[07 - Streaming with Kafka]]
