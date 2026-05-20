---
title: Numbers and Operators
tags: [python, basics]
created: 2026-05-20
up:: [[Python MOC]]
---

# 🔢 Numbers and Operators

> Python handles numbers effortlessly. Understanding operators is fundamental for data calculations.

---

## Arithmetic Operators

```python
a = 20
b = 6

print(a + b)        # 26  — Addition
print(a - b)        # 14  — Subtraction
print(a * b)        # 120 — Multiplication
print(a / b)        # 3.333... — Division (always float)
print(a // b)       # 3   — Floor division (whole number)
print(a % b)        # 2   — Modulus (remainder)
print(a ** b)       # 64000000 — Exponent (power)
```

---

## Comparison Operators

```python
x = 10
y = 20

print(x == y)       # False — Equal to
print(x != y)       # True  — Not equal
print(x > y)        # False — Greater than
print(x < y)        # True  — Less than
print(x >= y)       # False — Greater or equal
print(x <= y)       # True  — Less or equal
```

---

## Assignment Operators

```python
score = 100

score += 10     # score = score + 10 = 110
score -= 5      # score = score - 5  = 105
score *= 2      # score = score * 2  = 210
score /= 3      # score = score / 3  = 70.0
score //= 2     # score = score // 2 = 35.0
score **= 2     # score = score ** 2 = 1225.0

print(score)    # 1225.0
```

---

## Useful Math Functions

```python
import math

# Built-in (no import needed)
print(abs(-15))             # 15   — absolute value
print(round(3.14159, 2))    # 3.14 — round to 2 decimals
print(max(10, 20, 30))      # 30
print(min(10, 20, 30))      # 10
print(sum([1, 2, 3, 4]))    # 10
print(pow(2, 8))            # 256

# Math module
print(math.sqrt(144))       # 12.0 — square root
print(math.pi)              # 3.14159...
print(math.ceil(4.2))       # 5    — round up
print(math.floor(4.9))      # 4    — round down
print(math.log(100, 10))    # 2.0  — logarithm
```

---

## Real World Example — Sales Calculations

```python
# Monthly sales report
revenue = 450000
cost = 280000
tax_rate = 0.16
units_sold = 1500

# Calculations
gross_profit = revenue - cost
tax = revenue * tax_rate
net_profit = gross_profit - tax
profit_margin = (net_profit / revenue) * 100
avg_sale = revenue / units_sold

print(f"Revenue:        ${revenue:>12,.2f}")
print(f"Cost:           ${cost:>12,.2f}")
print(f"Gross Profit:   ${gross_profit:>12,.2f}")
print(f"Tax (16%):      ${tax:>12,.2f}")
print(f"Net Profit:     ${net_profit:>12,.2f}")
print(f"Profit Margin:  {profit_margin:>11.1f}%")
print(f"Avg Sale Value: ${avg_sale:>12,.2f}")
```

**Output:**
```
Revenue:          $450,000.00
Cost:             $280,000.00
Gross Profit:     $170,000.00
Tax (16%):         $72,000.00
Net Profit:        $98,000.00
Profit Margin:          21.8%
Avg Sale Value:       $300.00
```

---

## Operator Precedence (BODMAS)

```python
# Python follows BODMAS/PEMDAS
result = 2 + 3 * 4          # 14 (not 20!) — * before +
result = (2 + 3) * 4        # 20 — brackets first
result = 2 ** 3 ** 2        # 512 — right to left for **
result = 10 / 2 + 3 * 4    # 17.0
```

---

## Practice Exercise — KPI Dashboard

```python
# Calculate KPIs for a bank marketing campaign
total_contacts = 45211
successful_conversions = 5289
campaign_cost = 250000
revenue_per_conversion = 1200

# Calculate
conversion_rate = (successful_conversions / total_contacts) * 100
total_revenue = successful_conversions * revenue_per_conversion
roi = ((total_revenue - campaign_cost) / campaign_cost) * 100
cost_per_conversion = campaign_cost / successful_conversions

print(f"Conversion Rate:      {conversion_rate:.2f}%")
print(f"Total Revenue:        ${total_revenue:,.2f}")
print(f"ROI:                  {roi:.1f}%")
print(f"Cost per Conversion:  ${cost_per_conversion:.2f}")
```

---

## Previous | Next
← [[03 - Strings in Detail]] | → [[05 - Lists]]
