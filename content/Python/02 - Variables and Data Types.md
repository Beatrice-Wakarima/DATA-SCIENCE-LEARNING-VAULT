---
title: Variables and Data Types
tags: [python, basics]
created: 2026-05-20
up:: [[Python MOC]]
---

# 📦 Variables and Data Types

> A variable is a container for storing data. Python automatically detects the data type — no need to declare it.

---

## Creating Variables

```python
name = "Beatrice"        # String
age = 28                 # Integer
salary = 95000.50        # Float
is_employed = True       # Boolean
```

- No `var`, `let`, or `int` needed — just assign with `=`
- Variable names are **case sensitive**: `Name` ≠ `name`

---

## The 4 Main Data Types

### 1. String (str) — Text
```python
first_name = "Beatrice"
last_name = 'Wakarima'          # single or double quotes both work
full_name = "Beatrice Wakarima"

print(type(first_name))         # <class 'str'>
```

### 2. Integer (int) — Whole Numbers
```python
age = 28
employees = 500
year = 2026

print(type(age))                # <class 'int'>
```

### 3. Float — Decimal Numbers
```python
salary = 95000.50
tax_rate = 0.16
pi = 3.14159

print(type(salary))             # <class 'float'>
```

### 4. Boolean (bool) — True or False
```python
is_employed = True
has_degree = True
is_retired = False

print(type(is_employed))        # <class 'bool'>
```

---

## Checking Data Types

```python
name = "Beatrice"
age = 28
salary = 95000.50

print(type(name))               # <class 'str'>
print(type(age))                # <class 'int'>
print(type(salary))             # <class 'float'>
```

---

## Converting Between Types

```python
# String to Integer
age_str = "28"
age_int = int(age_str)
print(age_int + 2)              # 30

# Integer to String
score = 95
score_str = str(score)
print("Your score: " + score_str)   # Your score: 95

# String to Float
price = float("99.99")
print(price)                    # 99.99

# Float to Integer (drops decimals)
pi = 3.14159
print(int(pi))                  # 3
```

---

## Multiple Assignment

```python
# Assign same value to multiple variables
x = y = z = 0

# Assign different values in one line
name, age, city = "Beatrice", 28, "Nairobi"
print(name)     # Beatrice
print(age)      # 28
print(city)     # Nairobi
```

---

## Naming Rules

| Rule                                | Example                |
| ----------------------------------- | ---------------------- |
| ✅ Use letters, numbers, underscores | `my_variable`, `data1` |
| ✅ Start with letter or underscore   | `_name`, `name`        |
| ❌ Cannot start with number          | ~~`1name`~~            |
| ❌ No spaces                         | ~~`my variable`~~      |
| ❌ No special characters             | ~~`my-var`~~           |

---

## Real World Example

```python
# Employee record
employee_name = "Beatrice Wakarima"
department = "Data Engineering"
salary = 120000.00
is_active = True
years_of_experience = 5

print(employee_name)
print(f"Department: {department}")
print(f"Salary: ${salary:,.2f}")
print(f"Active: {is_active}")
```

**Output:**
```
Beatrice Wakarima
Department: Data Engineering
Salary: $120,000.00
Active: True
```

---

## Practice Exercise

Create variables for a dataset row:
```python
# Create variables for a bank customer
customer_id = 1001
customer_name = "John Doe"
account_balance = 45230.75
is_premium = True
credit_score = 720

# Print a summary
print(f"Customer: {customer_name}")
print(f"Balance: ${account_balance:,.2f}")
print(f"Premium: {is_premium}")
```

---

## Previous | Next
← [[01 - Introduction to Python]] | → [[03 - Strings in Detail]]
