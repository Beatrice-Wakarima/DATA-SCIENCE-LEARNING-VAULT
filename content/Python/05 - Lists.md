---
title: Lists
tags: [python, basics]
created: 2026-05-20
up:: [[Python MOC]]
---

# 📋 Lists

> A list stores multiple items in a single variable. It's the most used data structure in Python data science work.

---

## Creating Lists

```python
# Empty list
empty = []

# List of strings
fruits = ["apple", "banana", "mango"]

# List of numbers
scores = [85, 92, 78, 95, 88]

# Mixed types (allowed but uncommon)
mixed = ["Beatrice", 28, True, 95000.0]

# List of lists (2D — like a table!)
table = [
    ["Name", "Age", "City"],
    ["Beatrice", 28, "Nairobi"],
    ["John", 32, "Mombasa"]
]
```

---

## Accessing Items (Indexing)

```python
fruits = ["apple", "banana", "mango", "orange", "grape"]
#           0         1         2        3          4
#          -5        -4        -3       -2         -1

print(fruits[0])        # apple  (first)
print(fruits[-1])       # grape  (last)
print(fruits[2])        # mango
print(fruits[-2])       # orange
```

---

## Slicing Lists

```python
scores = [85, 92, 78, 95, 88, 72, 90]

print(scores[0:3])      # [85, 92, 78]  — first 3
print(scores[2:5])      # [78, 95, 88]
print(scores[:3])       # [85, 92, 78]  — up to index 3
print(scores[3:])       # [95, 88, 72, 90] — from index 3
print(scores[::2])      # [85, 78, 88, 90] — every 2nd
print(scores[::-1])     # [90, 72, 88, 95, 78, 92, 85] — reversed
```

---

## Modifying Lists

```python
cities = ["Nairobi", "Mombasa", "Kisumu"]

# Change an item
cities[1] = "Nakuru"
print(cities)           # ['Nairobi', 'Nakuru', 'Kisumu']

# Add items
cities.append("Eldoret")           # Add to end
cities.insert(1, "Thika")          # Insert at index 1
cities.extend(["Nyeri", "Malindi"]) # Add multiple

# Remove items
cities.remove("Thika")             # Remove by value
cities.pop()                       # Remove last item
cities.pop(0)                      # Remove by index
del cities[0]                      # Delete by index
```

---

## List Methods

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5]

print(len(numbers))         # 9    — count items
print(sum(numbers))         # 36   — total
print(max(numbers))         # 9    — highest
print(min(numbers))         # 1    — lowest
print(numbers.count(1))     # 2    — count occurrences of 1
print(numbers.index(5))     # 4    — first index of 5

numbers.sort()              # Sort ascending [1,1,2,3,4,5,5,6,9]
numbers.sort(reverse=True)  # Sort descending
numbers.reverse()           # Reverse order

sorted_nums = sorted(numbers)       # Returns new sorted list
```

---

## Checking Membership

```python
fruits = ["apple", "banana", "mango"]

print("mango" in fruits)        # True
print("grape" in fruits)        # False
print("grape" not in fruits)    # True
```

---

## Real World Example — Sales Data

```python
# Monthly sales figures (KES thousands)
monthly_sales = [420, 385, 510, 490, 620, 580, 450, 730, 695, 810, 750, 920]
months = ["Jan","Feb","Mar","Apr","May","Jun",
          "Jul","Aug","Sep","Oct","Nov","Dec"]

total = sum(monthly_sales)
average = total / len(monthly_sales)
best_month = months[monthly_sales.index(max(monthly_sales))]
worst_month = months[monthly_sales.index(min(monthly_sales))]

print(f"Total Sales:    KES {total:,}K")
print(f"Monthly Avg:    KES {average:,.1f}K")
print(f"Best Month:     {best_month} (KES {max(monthly_sales):,}K)")
print(f"Worst Month:    {worst_month} (KES {min(monthly_sales):,}K)")
print(f"Q4 Sales:       KES {sum(monthly_sales[-3:]):,}K")
```

**Output:**
```
Total Sales:    KES 7,360K
Monthly Avg:    KES 613.3K
Best Month:     Dec (KES 920K)
Worst Month:    Feb (KES 385K)
Q4 Sales:       KES 2,480K
```

---

## List Comprehension (Powerful Shortcut!)

```python
# Normal way
squares = []
for n in range(1, 6):
    squares.append(n ** 2)

# List comprehension — one line!
squares = [n ** 2 for n in range(1, 6)]
print(squares)      # [1, 4, 9, 16, 25]

# With condition
even_squares = [n ** 2 for n in range(1, 11) if n % 2 == 0]
print(even_squares) # [4, 16, 36, 64, 100]

# Clean a list of names
raw_names = ["  beatrice ", "JOHN  ", " alice"]
clean = [name.strip().title() for name in raw_names]
print(clean)        # ['Beatrice', 'John', 'Alice']
```

---

## Practice Exercise

```python
# Bank customer balances
balances = [45230, 12800, 98500, 3200, 67400, 23100, 150000, 8900]

# Tasks:
# 1. Find total deposits
# 2. Find average balance
# 3. Find premium customers (balance > 50000)
# 4. Sort from highest to lowest

total = sum(balances)
average = total / len(balances)
premium = [b for b in balances if b > 50000]
sorted_balances = sorted(balances, reverse=True)

print(f"Total Deposits: KES {total:,}")
print(f"Average Balance: KES {average:,.2f}")
print(f"Premium Customers: {len(premium)}")
print(f"Top 3 Balances: {sorted_balances[:3]}")
```

---

## Previous | Next
← [[04 - Numbers and Operators]] | → [[06 - Dictionaries]]
