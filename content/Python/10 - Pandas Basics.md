---
title: Pandas Basics
tags: [python, pandas, data-science]
created: 2026-05-20
up:: [[Python MOC]]
---

# 🐼 Pandas Basics

> Pandas is the #1 Python library for data analysis. It gives you Excel-like tables (DataFrames) inside Python — but infinitely more powerful.

---

## Installation & Import

```python
pip install pandas

import pandas as pd
```

---

## The Two Core Objects

| Object | Description | Like... |
|---|---|---|
| **Series** | One column of data | A single Excel column |
| **DataFrame** | Table with rows & columns | A full Excel sheet |

---

## Series

```python
import pandas as pd

# Create a Series
sales = pd.Series([420000, 385000, 510000, 490000, 620000],
                  index=["Jan", "Feb", "Mar", "Apr", "May"])

print(sales)
# Jan    420000
# Feb    385000
# Mar    510000
# Apr    490000
# May    620000

print(sales["Mar"])         # 510000
print(sales.max())          # 620000
print(sales.mean())         # 485000.0
```

---

## Creating a DataFrame

```python
# From a dictionary
data = {
    "name": ["Beatrice", "John", "Alice", "Bob", "Carol"],
    "department": ["Engineering", "Analytics", "Engineering", "Analytics", "Management"],
    "salary": [120000, 95000, 110000, 85000, 150000],
    "years_exp": [5, 3, 4, 2, 8],
    "is_active": [True, True, True, False, True]
}

df = pd.DataFrame(data)
print(df)
```

**Output:**
```
       name   department  salary  years_exp  is_active
0  Beatrice  Engineering  120000          5       True
1      John    Analytics   95000          3       True
2     Alice  Engineering  110000          4       True
3       Bob    Analytics   85000          2      False
4     Carol   Management  150000          8       True
```

---

## First Look at Your Data

```python
df.head()           # First 5 rows
df.tail()           # Last 5 rows
df.head(3)          # First 3 rows
df.shape            # (5, 5) — rows, columns
df.columns          # Column names
df.dtypes           # Data types of each column
df.info()           # Summary: shape, dtypes, nulls
df.describe()       # Statistics: mean, std, min, max
```

---

## Selecting Data

```python
# Single column → returns Series
print(df["name"])
print(df["salary"])

# Multiple columns → returns DataFrame
print(df[["name", "salary", "department"]])

# Single row by index number
print(df.iloc[0])           # First row
print(df.iloc[-1])          # Last row
print(df.iloc[1:3])         # Rows 1 to 2

# Row by label
print(df.loc[0])            # Row with index 0
print(df.loc[0, "name"])    # Specific cell
```

---

## Filtering Rows

```python
# Single condition
high_earners = df[df["salary"] > 100000]
print(high_earners)

# Multiple conditions
senior_engineers = df[
    (df["department"] == "Engineering") &
    (df["years_exp"] >= 4)
]

# OR condition
top_or_senior = df[
    (df["salary"] > 120000) |
    (df["years_exp"] > 6)
]

# isin() — filter by list of values
target_depts = df[df["department"].isin(["Engineering", "Analytics"])]

# Active employees only
active = df[df["is_active"] == True]
```

---

## Adding & Modifying Columns

```python
# Add new column
df["annual_bonus"] = df["salary"] * 0.10
df["total_comp"] = df["salary"] + df["annual_bonus"]
df["seniority"] = df["years_exp"].apply(
    lambda x: "Senior" if x >= 5 else "Mid" if x >= 3 else "Junior"
)

print(df[["name", "salary", "annual_bonus", "total_comp", "seniority"]])
```

---

## Basic Statistics

```python
# Overall
print(df["salary"].mean())      # Average salary
print(df["salary"].median())    # Median salary
print(df["salary"].sum())       # Total payroll
print(df["salary"].min())       # Lowest
print(df["salary"].max())       # Highest
print(df["salary"].std())       # Standard deviation

# By group
dept_stats = df.groupby("department")["salary"].agg(["mean", "sum", "count"])
print(dept_stats)
```

---

## Sorting

```python
# Sort by one column
df.sort_values("salary", ascending=False)

# Sort by multiple columns
df.sort_values(["department", "salary"], ascending=[True, False])
```

---

## Real World Example — Employee Analysis

```python
import pandas as pd

# Load data (simulated)
data = {
    "name": ["Beatrice", "John", "Alice", "Bob", "Carol", "Dan", "Eve"],
    "department": ["Engineering","Analytics","Engineering","Analytics","Management","Engineering","Analytics"],
    "salary": [120000, 95000, 110000, 85000, 150000, 105000, 92000],
    "years_exp": [5, 3, 4, 2, 8, 4, 3],
    "performance": ["Excellent","Good","Excellent","Average","Excellent","Good","Good"]
}

df = pd.DataFrame(data)

# 1. Department summary
print("📊 Department Summary")
print(df.groupby("department")["salary"].agg(
    Count="count",
    Avg_Salary="mean",
    Total_Payroll="sum"
).round(0))

# 2. Top performers
print("\n⭐ Top Performers")
top = df[df["performance"] == "Excellent"][["name", "department", "salary"]]
print(top.sort_values("salary", ascending=False))

# 3. Salary bands
df["band"] = pd.cut(df["salary"],
                     bins=[0, 90000, 110000, 200000],
                     labels=["Standard", "Senior", "Executive"])
print("\n💰 Salary Bands")
print(df["band"].value_counts())
```

---

## Reading Real Files

```python
# CSV
df = pd.read_csv("data.csv")

# Excel
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# With options
df = pd.read_csv("data.csv",
    sep=",",
    encoding="utf-8",
    parse_dates=["date_column"],
    index_col="id"
)

# Save
df.to_csv("output.csv", index=False)
df.to_excel("output.xlsx", index=False)
```

---

## Practice Exercise

```python
# Bank marketing dataset analysis
import pandas as pd

df = pd.read_csv("bank_marketing.csv")

# Explore
print(df.shape)
print(df.dtypes)
print(df.describe())

# Key questions:
# 1. What is the overall subscription rate?
subscription_rate = df["y"].value_counts(normalize=True) * 100
print(subscription_rate)

# 2. Which job type has the highest subscription rate?
job_sub = df.groupby("job")["y"].apply(
    lambda x: (x == "yes").sum() / len(x) * 100
).sort_values(ascending=False)
print(job_sub)
```

---

## Previous | Next
← [[09 - Functions]] | → [[11 - Pandas Data Cleaning]]
