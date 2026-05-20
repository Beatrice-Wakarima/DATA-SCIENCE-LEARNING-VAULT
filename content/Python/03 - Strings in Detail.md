---
title: Strings in Detail
tags: [python, basics]
created: 2026-05-20
up:: [[Python MOC]]
---

# 🔤 Strings in Detail

> Strings are sequences of characters. Mastering strings is essential for data cleaning and manipulation.

---

## Creating Strings

```python
single = 'Hello'
double = "Hello"
multiline = """
This is a
multiline string
"""
```

---

## String Operations

### Concatenation (Joining)
```python
first = "Beatrice"
last = "Wakarima"
full = first + " " + last
print(full)                     # Beatrice Wakarima
```

### Repetition
```python
line = "-" * 30
print(line)                     # ------------------------------
```

### Length
```python
name = "Beatrice"
print(len(name))                # 8
```

---

## F-Strings (Most Used in Data Science)

```python
name = "Beatrice"
role = "Data Scientist"
salary = 120000

# f-string — put f before the quote
print(f"Name: {name}")
print(f"Role: {role}")
print(f"Salary: ${salary:,}")           # $ 120,000
print(f"Tax (16%): ${salary * 0.16:,.2f}")
```

**Output:**
```
Name: Beatrice
Role: Data Scientist
Salary: $120,000
Tax (16%): $19,200.00
```

---

## String Methods

```python
text = "  hello world  "

# Case
print(text.upper())             # HELLO WORLD
print(text.lower())             # hello world
print(text.title())             # Hello World
print(text.capitalize())        # Hello world

# Cleaning
print(text.strip())             # "hello world" (removes spaces)
print(text.lstrip())            # "hello world  " (left only)
print(text.rstrip())            # "  hello world" (right only)

# Replacing
print(text.replace("world", "Beatrice"))  # hello Beatrice

# Splitting
csv_row = "Beatrice,28,Nairobi,Data Scientist"
print(csv_row.split(","))
# ['Beatrice', '28', 'Nairobi', 'Data Scientist']

# Checking
print("hello".startswith("he"))     # True
print("hello".endswith("lo"))       # True
print("hello".contains("ell"))      # True
```

---

## String Indexing & Slicing

```python
name = "Beatrice"
#        01234567

# Single character
print(name[0])          # B  (first)
print(name[-1])         # e  (last)
print(name[3])          # t

# Slicing [start:end:step]
print(name[0:4])        # Beat
print(name[4:])         # rice
print(name[:4])         # Beat
print(name[::2])        # Barc  (every 2nd character)
print(name[::-1])       # ecirtaeB  (reversed)
```

---

## Real World Data Example

```python
# Cleaning messy data — common in data engineering!
raw_name = "  beatrice wakarima  "
raw_salary = "120,000"
raw_date = "2026-05-20"

# Clean name
clean_name = raw_name.strip().title()
print(clean_name)               # Beatrice Wakarima

# Clean salary — remove comma, convert to int
clean_salary = int(raw_salary.replace(",", ""))
print(clean_salary)             # 120000

# Split date
year, month, day = raw_date.split("-")
print(f"Year: {year}, Month: {month}, Day: {day}")
# Year: 2026, Month: 05, Day: 20
```

---

## Practice Exercise

```python
# You have this messy customer data
raw = "  john DOE | nairobi | 45230.75  "

# Tasks:
# 1. Strip whitespace
# 2. Split by "|"
# 3. Clean each value
# 4. Print a formatted summary

parts = raw.strip().split("|")
name = parts[0].strip().title()
city = parts[1].strip().title()
balance = float(parts[2].strip())

print(f"Customer: {name}")
print(f"City: {city}")
print(f"Balance: ${balance:,.2f}")
```

---

## Previous | Next
← [[02 - Variables and Data Types]] | → [[04 - Numbers and Operators]]
