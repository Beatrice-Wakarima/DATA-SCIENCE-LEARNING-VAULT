---
title: Functions
tags: [python, basics]
created: 2026-05-20
up:: [[Python MOC]]
---

# ⚙️ Functions

> A function is a reusable block of code. Write once, use many times. Core to clean, professional Python.

---

## Creating a Function

```python
# Define
def greet():
    print("Hello, Beatrice!")

# Call
greet()             # Hello, Beatrice!
greet()             # Hello, Beatrice!  (reusable!)
```

---

## Functions with Parameters

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Beatrice")   # Hello, Beatrice!
greet("John")       # Hello, John!
```

---

## Functions with Return Values

```python
def add(a, b):
    return a + b

result = add(10, 20)
print(result)           # 30

# Return multiple values
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([5, 2, 8, 1, 9])
print(low, high)        # 1 9
```

---

## Default Parameters

```python
def create_account(name, account_type="Savings", balance=0):
    return {
        "name": name,
        "type": account_type,
        "balance": balance
    }

# Use defaults
acc1 = create_account("Beatrice")
print(acc1)     # {'name': 'Beatrice', 'type': 'Savings', 'balance': 0}

# Override defaults
acc2 = create_account("John", "Current", 50000)
print(acc2)     # {'name': 'John', 'type': 'Current', 'balance': 50000}
```

---

## Keyword Arguments

```python
def profile(name, age, city, role):
    print(f"{name} | {age} | {city} | {role}")

# Positional
profile("Beatrice", 28, "Nairobi", "Data Scientist")

# Keyword — order doesn't matter!
profile(role="Data Scientist", name="Beatrice", city="Nairobi", age=28)
```

---

## *args — Variable Number of Arguments

```python
def total_sales(*amounts):
    return sum(amounts)

print(total_sales(1000, 2000, 3000))        # 6000
print(total_sales(500, 750, 1200, 900))     # 3350
```

---

## **kwargs — Variable Keyword Arguments

```python
def create_record(**fields):
    for key, value in fields.items():
        print(f"{key}: {value}")

create_record(name="Beatrice", role="Data Scientist", city="Nairobi")
# name: Beatrice
# role: Data Scientist
# city: Nairobi
```

---

## Docstrings — Documenting Functions

```python
def calculate_roi(revenue, cost):
    """
    Calculate Return on Investment (ROI).
    
    Args:
        revenue (float): Total revenue generated
        cost (float): Total cost incurred
    
    Returns:
        float: ROI as a percentage
    
    Example:
        >>> calculate_roi(150000, 100000)
        50.0
    """
    return ((revenue - cost) / cost) * 100

print(calculate_roi(150000, 100000))    # 50.0
help(calculate_roi)                     # Shows the docstring
```

---

## Lambda Functions (Anonymous)

```python
# Normal function
def square(x):
    return x ** 2

# Lambda — one liner
square = lambda x: x ** 2
print(square(5))        # 25

# Common use — sorting
customers = [
    {"name": "Alice", "balance": 95000},
    {"name": "Bob", "balance": 12000},
    {"name": "Carol", "balance": 230000}
]

# Sort by balance
sorted_customers = sorted(customers, key=lambda c: c["balance"], reverse=True)
for c in sorted_customers:
    print(f"{c['name']:10}: KES {c['balance']:,}")
```

---

## Real World Example — Data Pipeline Functions

```python
def load_data(filepath):
    """Simulate loading CSV data"""
    return [
        {"name": "Beatrice", "salary": 120000, "dept": "Engineering"},
        {"name": "John", "salary": 95000, "dept": "Analytics"},
        {"name": "Alice", "salary": 110000, "dept": "Engineering"},
        {"name": "Bob", "salary": 85000, "dept": "Analytics"}
    ]

def filter_by_dept(data, department):
    """Filter records by department"""
    return [r for r in data if r["dept"] == department]

def calculate_avg_salary(data):
    """Calculate average salary"""
    if not data:
        return 0
    return sum(r["salary"] for r in data) / len(data)

def generate_report(data, dept):
    """Generate department salary report"""
    dept_data = filter_by_dept(data, dept)
    avg = calculate_avg_salary(dept_data)
    
    print(f"\n📊 {dept} Department Report")
    print("-" * 40)
    for emp in dept_data:
        print(f"  {emp['name']:10}: KES {emp['salary']:,}")
    print(f"  {'Average':10}: KES {avg:,.0f}")

# Run pipeline
data = load_data("employees.csv")
generate_report(data, "Engineering")
generate_report(data, "Analytics")
```

---

## Practice Exercise

```python
# Build a simple KPI calculator
def calculate_kpis(revenue, cost, units, target):
    """Calculate business KPIs"""
    gross_profit = revenue - cost
    profit_margin = (gross_profit / revenue) * 100
    avg_sale = revenue / units
    target_achievement = (revenue / target) * 100
    
    return {
        "gross_profit": gross_profit,
        "profit_margin": profit_margin,
        "avg_sale_value": avg_sale,
        "target_achievement": target_achievement
    }

def display_kpis(kpis):
    """Display KPIs in formatted table"""
    print("\n📈 KPI Dashboard")
    print("=" * 35)
    print(f"Gross Profit:      KES {kpis['gross_profit']:>10,.0f}")
    print(f"Profit Margin:         {kpis['profit_margin']:>9.1f}%")
    print(f"Avg Sale Value:    KES {kpis['avg_sale_value']:>10,.0f}")
    print(f"Target Achievement:    {kpis['target_achievement']:>9.1f}%")

# Use the functions
kpis = calculate_kpis(
    revenue=850000,
    cost=520000,
    units=1700,
    target=800000
)
display_kpis(kpis)
```

---

## Previous | Next
← [[08 - Loops]] | → [[10 - Pandas Basics]]
