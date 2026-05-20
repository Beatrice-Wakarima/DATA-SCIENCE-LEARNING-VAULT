---
title: Conditionals (if, elif, else)
tags: [python, basics]
created: 2026-05-20
up:: [[Python MOC]]
---

# 🔀 Conditionals

> Conditionals let your program make decisions — "if this, do that, otherwise do something else."

---

## Basic if Statement

```python
balance = 95000

if balance > 50000:
    print("Premium customer")
```

---

## if / else

```python
age = 20

if age >= 18:
    print("Adult — can open account")
else:
    print("Minor — needs guardian")
```

---

## if / elif / else

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score: {score} → Grade: {grade}")   # Score: 85 → Grade: B
```

---

## Comparison & Logical Operators

```python
age = 28
salary = 95000
has_degree = True

# and — both must be True
if age >= 25 and salary >= 80000:
    print("Eligible for premium loan")

# or — at least one must be True
if age < 18 or age > 65:
    print("Not in working age range")

# not — reverses True/False
if not has_degree:
    print("Degree required")
else:
    print("Qualification met")
```

---

## Real World Example — Customer Segmentation

```python
def segment_customer(balance, transactions, age):
    """Segment bank customers based on profile"""
    
    if balance >= 100000 and transactions >= 20:
        segment = "Platinum"
        benefit = "Dedicated relationship manager"
    elif balance >= 50000 or transactions >= 15:
        segment = "Gold"
        benefit = "Priority banking"
    elif balance >= 10000:
        segment = "Silver"
        benefit = "Standard benefits"
    else:
        segment = "Bronze"
        benefit = "Basic banking"
    
    return segment, benefit

# Test it
customers = [
    ("Beatrice", 150000, 25, 28),
    ("John", 45000, 18, 35),
    ("Alice", 8000, 5, 22),
    ("Bob", 250000, 30, 45)
]

print(f"{'Name':10} {'Balance':>12} {'Segment':10} {'Benefit'}")
print("-" * 60)
for name, balance, txns, age in customers:
    seg, benefit = segment_customer(balance, txns, age)
    print(f"{name:10} KES {balance:>8,} {seg:10} {benefit}")
```

**Output:**
```
Name       Balance      Segment    Benefit
------------------------------------------------------------
Beatrice   KES  150,000 Platinum   Dedicated relationship manager
John       KES   45,000 Gold       Priority banking
Alice      KES    8,000 Bronze     Basic banking
Bob        KES  250,000 Platinum   Dedicated relationship manager
```

---

## Ternary Operator (One-line if/else)

```python
# Normal
if balance > 50000:
    status = "Premium"
else:
    status = "Standard"

# One-liner
status = "Premium" if balance > 50000 else "Standard"
print(status)
```

---

## Nested Conditionals

```python
loan_amount = 500000
credit_score = 720
has_collateral = True

if credit_score >= 700:
    if has_collateral:
        if loan_amount <= 1000000:
            print("Loan approved ✅")
        else:
            print("Loan amount too high ❌")
    else:
        print("Collateral required ❌")
else:
    print("Credit score too low ❌")
```

---

## Practice Exercise

```python
# Build a loan eligibility checker
def check_loan_eligibility(age, income, credit_score, employment):
    
    # Age check
    if age < 18 or age > 65:
        return "Ineligible", "Age must be 18-65"
    
    # Income check
    if income < 30000:
        return "Ineligible", "Minimum income KES 30,000"
    
    # Credit score
    if credit_score < 600:
        return "Ineligible", "Credit score too low"
    
    # Employment
    if employment not in ["employed", "self-employed"]:
        return "Ineligible", "Must be employed"
    
    # All checks passed
    max_loan = income * 5
    return "Eligible", f"Maximum loan: KES {max_loan:,}"

# Test
result, message = check_loan_eligibility(28, 95000, 720, "employed")
print(f"Status: {result}")
print(f"Detail: {message}")
```

---

## Previous | Next
← [[06 - Dictionaries]] | → [[08 - Loops]]
