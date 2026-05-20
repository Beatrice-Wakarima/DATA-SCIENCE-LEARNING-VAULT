---
title: Loops (for and while)
tags: [python, basics]
created: 2026-05-20
up:: [[Python MOC]]
---

# 🔁 Loops

> Loops repeat a block of code. Essential for processing datasets, iterating through records, and automation.

---

## for Loop

```python
# Loop through a list
fruits = ["apple", "banana", "mango"]

for fruit in fruits:
    print(fruit)
# apple
# banana
# mango
```

---

## range() with for

```python
# range(stop)
for i in range(5):
    print(i)            # 0 1 2 3 4

# range(start, stop)
for i in range(1, 6):
    print(i)            # 1 2 3 4 5

# range(start, stop, step)
for i in range(0, 20, 5):
    print(i)            # 0 5 10 15

# Count backwards
for i in range(10, 0, -1):
    print(i)            # 10 9 8 7 6 5 4 3 2 1
```

---

## enumerate() — Loop with Index

```python
months = ["Jan", "Feb", "Mar", "Apr", "May"]

for index, month in enumerate(months):
    print(f"{index + 1}. {month}")

# Output:
# 1. Jan
# 2. Feb
# 3. Mar
# 4. Apr
# 5. May
```

---

## zip() — Loop Two Lists Together

```python
months = ["Jan", "Feb", "Mar", "Apr"]
sales = [420000, 385000, 510000, 490000]

for month, amount in zip(months, sales):
    print(f"{month}: KES {amount:,}")

# Jan: KES 420,000
# Feb: KES 385,000
# Mar: KES 510,000
# Apr: KES 490,000
```

---

## while Loop

```python
# Repeat while condition is True
count = 0

while count < 5:
    print(f"Count: {count}")
    count += 1          # Important! Increment or infinite loop

# Count: 0
# Count: 1
# ...
# Count: 4
```

---

## break and continue

```python
# break — exit loop early
for num in range(10):
    if num == 5:
        break
    print(num)          # 0 1 2 3 4

# continue — skip current iteration
for num in range(10):
    if num % 2 == 0:    # Skip even numbers
        continue
    print(num)          # 1 3 5 7 9
```

---

## Loop Through Dictionary

```python
employee = {
    "name": "Beatrice",
    "role": "Data Scientist", 
    "salary": 120000,
    "city": "Nairobi"
}

# Keys only
for key in employee:
    print(key)

# Values only
for value in employee.values():
    print(value)

# Keys and values
for key, value in employee.items():
    print(f"{key:10}: {value}")
```

---

## Real World Example — Processing a Dataset

```python
# Sales transactions dataset
transactions = [
    {"id": "T001", "product": "Laptop", "amount": 85000, "region": "Nairobi"},
    {"id": "T002", "product": "Phone", "amount": 45000, "region": "Mombasa"},
    {"id": "T003", "product": "Laptop", "amount": 85000, "region": "Nairobi"},
    {"id": "T004", "product": "Tablet", "amount": 35000, "region": "Kisumu"},
    {"id": "T005", "product": "Phone", "amount": 45000, "region": "Nairobi"},
]

# Calculate totals by product
product_totals = {}

for txn in transactions:
    product = txn["product"]
    amount = txn["amount"]
    
    if product in product_totals:
        product_totals[product] += amount
    else:
        product_totals[product] = amount

# Display results
print("Sales by Product:")
print("-" * 30)
for product, total in product_totals.items():
    print(f"{product:10}: KES {total:>10,}")
```

**Output:**
```
Sales by Product:
------------------------------
Laptop    : KES     170,000
Phone     : KES      90,000
Tablet    : KES      35,000
```

---

## Nested Loops — Processing 2D Data

```python
# A simple multiplication table
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i*j}")
    print()         # blank line between groups

# Processing a table of data
data = [
    ["Beatrice", 85, 92, 78],
    ["John", 70, 65, 80],
    ["Alice", 95, 98, 92]
]

for row in data:
    name = row[0]
    grades = row[1:]
    avg = sum(grades) / len(grades)
    print(f"{name:10}: {avg:.1f}")
```

---

## Practice Exercise

```python
# ATM withdrawal simulation
balance = 150000
withdrawals = [20000, 50000, 15000, 80000, 10000]

print(f"Starting balance: KES {balance:,}")
print("-" * 40)

for i, amount in enumerate(withdrawals, 1):
    if amount > balance:
        print(f"Withdrawal {i}: KES {amount:,} — INSUFFICIENT FUNDS ❌")
    else:
        balance -= amount
        print(f"Withdrawal {i}: KES {amount:,} — Approved ✅ | Balance: KES {balance:,}")

print("-" * 40)
print(f"Final balance: KES {balance:,}")
```

---

## Previous | Next
← [[07 - Conditionals]] | → [[09 - Functions]]
