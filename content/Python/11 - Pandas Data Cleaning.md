---
title: Pandas Data Cleaning
tags: [python, pandas, data-science, data-engineering]
created: 2026-05-20
up:: [[Python MOC]]
---

# 🧹 Pandas Data Cleaning

> Real-world data is messy. Data cleaning is 80% of a data scientist's job. Master this and you're halfway there.

---

## The Messy Data Problem

```python
import pandas as pd

# This is what real data looks like
data = {
    "name": ["Beatrice", "  john  ", "ALICE", None, "Bob", "carol"],
    "age": [28, 35, None, 25, -5, 200],
    "salary": [120000, "95,000", 110000, 85000, None, 92000],
    "email": ["b@gmail.com", "invalid-email", "a@gmail.com", "b2@gmail.com", None, "c@gmail.com"],
    "join_date": ["2021-03-15", "2020/07/22", "March 10, 2019", "2022-01-05", "2023-06-30", None],
    "department": ["Engineering", "analytics", "Engineering", "ANALYTICS", "Engineering", None]
}

df = pd.DataFrame(data)
```

---

## Step 1 — Assess the Mess

```python
# Overview
print(df.info())
print(df.describe())

# Missing values
print(df.isnull().sum())            # Count nulls per column
print(df.isnull().sum() / len(df) * 100)  # % missing

# Duplicates
print(df.duplicated().sum())        # Count duplicate rows
print(df[df.duplicated()])          # Show duplicates
```

---

## Step 2 — Handle Missing Values

```python
# Check nulls
print(df.isnull())

# Option 1 — Drop rows with any null
df_clean = df.dropna()

# Option 2 — Drop rows where SPECIFIC columns are null
df_clean = df.dropna(subset=["name", "salary"])

# Option 3 — Fill with a value
df["age"].fillna(df["age"].median(), inplace=True)
df["salary"].fillna(0, inplace=True)
df["department"].fillna("Unknown", inplace=True)

# Option 4 — Forward fill (use previous value)
df["salary"].fillna(method="ffill", inplace=True)

# Option 5 — Fill with mean/median/mode
df["age"].fillna(df["age"].mean(), inplace=True)
df["department"].fillna(df["department"].mode()[0], inplace=True)
```

---

## Step 3 — Fix Data Types

```python
# Check types
print(df.dtypes)

# String to number (remove commas first)
df["salary"] = df["salary"].astype(str).str.replace(",", "").astype(float)

# String to datetime
df["join_date"] = pd.to_datetime(df["join_date"], errors="coerce")

# Number to string
df["id"] = df["id"].astype(str)

# Boolean
df["is_active"] = df["is_active"].astype(bool)
```

---

## Step 4 — Clean String Columns

```python
# Clean name column
df["name"] = df["name"].str.strip()         # Remove spaces
df["name"] = df["name"].str.title()         # Title Case
df["department"] = df["department"].str.lower()  # lowercase
df["email"] = df["email"].str.lower().str.strip()

# Remove special characters
df["name"] = df["name"].str.replace(r"[^a-zA-Z\s]", "", regex=True)

# Standardize department names
dept_map = {
    "engineering": "Engineering",
    "analytics": "Analytics",
    "management": "Management"
}
df["department"] = df["department"].map(dept_map)
```

---

## Step 5 — Handle Outliers

```python
# Find outliers using IQR
Q1 = df["age"].quantile(0.25)
Q3 = df["age"].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

print(f"Valid age range: {lower} to {upper}")

# Remove outliers
df = df[(df["age"] >= lower) & (df["age"] <= upper)]

# Or cap them (Winsorization)
df["age"] = df["age"].clip(lower=18, upper=65)
df["salary"] = df["salary"].clip(lower=0)
```

---

## Step 6 — Remove Duplicates

```python
# Check
print(df.duplicated().sum())

# Drop exact duplicates
df = df.drop_duplicates()

# Drop duplicates based on specific columns
df = df.drop_duplicates(subset=["name", "email"], keep="first")
```

---

## Step 7 — Validate & Fix Values

```python
# Validate email (basic check)
df["valid_email"] = df["email"].str.contains(r"^[\w\.-]+@[\w\.-]+\.\w+$", regex=True)

# Validate age range
df = df[(df["age"] >= 18) & (df["age"] <= 65)]

# Fix date column
df["join_date"] = pd.to_datetime(df["join_date"], errors="coerce")
df["join_year"] = df["join_date"].dt.year
df["join_month"] = df["join_date"].dt.month

# Replace unexpected values
df["department"].replace("Enginnering", "Engineering", inplace=True)  # Fix typo
```

---

## Full Cleaning Pipeline

```python
import pandas as pd

def clean_employee_data(filepath):
    """Complete data cleaning pipeline for employee data"""
    
    # Load
    df = pd.read_csv(filepath)
    print(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # 1. Remove duplicates
    df = df.drop_duplicates()
    
    # 2. Clean strings
    df["name"] = df["name"].str.strip().str.title()
    df["department"] = df["department"].str.strip().str.title()
    df["email"] = df["email"].str.strip().str.lower()
    
    # 3. Fix salary column
    df["salary"] = df["salary"].astype(str)\
                               .str.replace(",", "")\
                               .str.replace("KES", "")\
                               .str.strip()
    df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
    
    # 4. Handle missing values
    df["salary"].fillna(df["salary"].median(), inplace=True)
    df["department"].fillna("Unknown", inplace=True)
    df.dropna(subset=["name", "email"], inplace=True)
    
    # 5. Fix dates
    df["join_date"] = pd.to_datetime(df["join_date"], errors="coerce")
    
    # 6. Remove outliers
    df = df[(df["salary"] > 0) & (df["salary"] < 1000000)]
    
    # 7. Add derived columns
    df["tenure_years"] = (pd.Timestamp.now() - df["join_date"]).dt.days / 365
    
    print(f"Cleaned: {df.shape[0]} rows remaining")
    return df

# Run pipeline
df_clean = clean_employee_data("employees.csv")
df_clean.to_csv("employees_clean.csv", index=False)
print("✅ Clean data saved!")
```

---

## Quick Reference Cheatsheet

```python
# Missing values
df.isnull().sum()               # Count nulls
df.dropna()                     # Drop null rows
df.fillna(value)                # Fill nulls
df.fillna(method="ffill")       # Forward fill

# Duplicates
df.duplicated().sum()           # Count duplicates
df.drop_duplicates()            # Remove duplicates

# Data types
df.dtypes                       # Check types
df["col"].astype(int)           # Convert type
pd.to_datetime(df["date"])      # Convert to datetime
pd.to_numeric(df["num"])        # Convert to number

# Strings
df["col"].str.strip()           # Remove whitespace
df["col"].str.lower()           # Lowercase
df["col"].str.replace("a","b")  # Replace
df["col"].str.contains("pattern") # Check pattern

# Outliers
df["col"].clip(lower=0, upper=100)  # Cap values
df["col"].quantile([0.25, 0.75])    # Quartiles
```

---

## Previous | Next
← [[10 - Pandas Basics]] | → [[12 - NumPy]]
