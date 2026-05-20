---
title: Dictionaries
tags: [python, basics]
created: 2026-05-20
up:: [[Python MOC]]
---

# 📖 Dictionaries

> A dictionary stores data as key-value pairs — like a real dictionary where a word (key) has a definition (value). Essential for working with JSON and APIs.

---

## Creating Dictionaries

```python
# Empty dictionary
empty = {}

# Customer record
customer = {
    "name": "Beatrice Wakarima",
    "age": 28,
    "city": "Nairobi",
    "balance": 95000.50,
    "is_premium": True
}
```

---

## Accessing Values

```python
customer = {
    "name": "Beatrice",
    "age": 28,
    "city": "Nairobi"
}

# By key
print(customer["name"])             # Beatrice
print(customer["age"])              # 28

# Using .get() — safer (no error if key missing)
print(customer.get("city"))         # Nairobi
print(customer.get("email"))        # None
print(customer.get("email", "N/A")) # N/A (default value)
```

---

## Modifying Dictionaries

```python
customer = {"name": "Beatrice", "age": 28}

# Add new key
customer["email"] = "beatrice@gmail.com"
customer["city"] = "Nairobi"

# Update existing key
customer["age"] = 29

# Update multiple at once
customer.update({"age": 30, "salary": 120000})

# Remove keys
del customer["age"]                 # Delete specific key
removed = customer.pop("city")      # Remove and return value
customer.clear()                    # Remove all keys
```

---

## Dictionary Methods

```python
employee = {
    "name": "Beatrice",
    "role": "Data Scientist",
    "department": "Engineering",
    "salary": 120000
}

print(employee.keys())      # dict_keys(['name', 'role', 'department', 'salary'])
print(employee.values())    # dict_values(['Beatrice', 'Data Scientist', ...])
print(employee.items())     # dict_items([('name', 'Beatrice'), ...])

print(len(employee))        # 4
print("name" in employee)   # True
print("age" in employee)    # False
```

---

## Nested Dictionaries

```python
# Like a database record!
employees = {
    "E001": {
        "name": "Beatrice Wakarima",
        "role": "Data Scientist",
        "salary": 120000,
        "skills": ["Python", "SQL", "Power BI"]
    },
    "E002": {
        "name": "John Doe",
        "role": "Data Engineer",
        "salary": 110000,
        "skills": ["Python", "Airflow", "Kafka"]
    }
}

# Access nested data
print(employees["E001"]["name"])            # Beatrice Wakarima
print(employees["E001"]["skills"][0])       # Python
print(employees["E002"]["salary"])          # 110000
```

---

## Real World Example — API Response (JSON-like)

```python
# This is what API data looks like in Python
api_response = {
    "status": "success",
    "total_records": 3,
    "data": [
        {"id": 1, "name": "Beatrice", "balance": 95000, "tier": "Gold"},
        {"id": 2, "name": "John", "balance": 12000, "tier": "Silver"},
        {"id": 3, "name": "Alice", "balance": 230000, "tier": "Platinum"}
    ]
}

# Extract information
print(f"Status: {api_response['status']}")
print(f"Records: {api_response['total_records']}")

# Loop through data
for customer in api_response["data"]:
    print(f"{customer['name']:10} | {customer['tier']:8} | KES {customer['balance']:,}")
```

**Output:**
```
Status: success
Records: 3
Beatrice   | Gold     | KES 95,000
John       | Silver   | KES 12,000
Alice      | Platinum | KES 230,000
```

---

## Dictionary Comprehension

```python
# Normal way
squares = {}
for n in range(1, 6):
    squares[n] = n ** 2

# Dictionary comprehension
squares = {n: n ** 2 for n in range(1, 6)}
print(squares)      # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Filter — only premium customers
customers = {"Alice": 95000, "Bob": 12000, "Carol": 230000, "Dan": 8000}
premium = {name: bal for name, bal in customers.items() if bal > 50000}
print(premium)      # {'Alice': 95000, 'Carol': 230000}
```

---

## Practice Exercise

```python
# Build a simple student grade tracker
students = {
    "Alice": [85, 92, 78, 95],
    "Bob": [70, 65, 80, 75],
    "Carol": [95, 98, 92, 97],
    "Dan": [60, 55, 70, 65]
}

# Calculate average for each student
for name, grades in students.items():
    avg = sum(grades) / len(grades)
    grade = "A" if avg >= 90 else "B" if avg >= 75 else "C"
    print(f"{name:8} | Avg: {avg:.1f} | Grade: {grade}")
```

---

## Previous | Next
← [[05 - Lists]] | → [[07 - Conditionals]]
