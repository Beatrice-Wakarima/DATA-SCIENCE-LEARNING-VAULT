---
title: NumPy
tags: [python, numpy, data-science]
created: 2026-05-20
up:: [[Python MOC]]
---

# 🔢 NumPy

> NumPy (Numerical Python) is the foundation of all data science in Python. It powers Pandas, Scikit-learn, and TensorFlow under the hood. Fast, efficient array operations.

---

## Installation & Import

```python
pip install numpy

import numpy as np
```

---

## NumPy Array vs Python List

```python
import numpy as np

# Python list — slow for math
py_list = [1, 2, 3, 4, 5]
py_list * 2                 # [1,2,3,4,5,1,2,3,4,5] — repeats!

# NumPy array — fast, math-friendly
np_array = np.array([1, 2, 3, 4, 5])
np_array * 2                # [2, 4, 6, 8, 10] — multiplies each element!
```

---

## Creating Arrays

```python
# From list
arr = np.array([1, 2, 3, 4, 5])

# Zeros and ones
zeros = np.zeros(5)             # [0. 0. 0. 0. 0.]
ones = np.ones(5)               # [1. 1. 1. 1. 1.]
full = np.full(5, 10)           # [10 10 10 10 10]

# Range
arr = np.arange(0, 10, 2)      # [0 2 4 6 8]
arr = np.linspace(0, 1, 5)     # [0.   0.25  0.5   0.75  1.  ]

# Random
np.random.seed(42)              # For reproducibility
rand = np.random.rand(5)        # 5 random floats 0-1
rand_int = np.random.randint(1, 100, 5)  # 5 random ints

# 2D Arrays (matrices)
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])
```

---

## Array Properties

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

print(arr.shape)        # (2, 3) — 2 rows, 3 columns
print(arr.ndim)         # 2 — number of dimensions
print(arr.size)         # 6 — total elements
print(arr.dtype)        # int64 — data type
```

---

## Array Operations (Vectorized)

```python
a = np.array([10, 20, 30, 40, 50])
b = np.array([1, 2, 3, 4, 5])

# Math operations — applied to EVERY element
print(a + b)        # [11 22 33 44 55]
print(a - b)        # [ 9 18 27 36 45]
print(a * b)        # [ 10  40  90 160 250]
print(a / b)        # [10. 10. 10. 10. 10.]
print(a ** 2)       # [ 100  400  900 1600 2500]
print(np.sqrt(a))   # [3.16 4.47 5.47 6.32 7.07]

# Scalar operations
salaries = np.array([120000, 95000, 110000, 85000])
print(salaries * 1.10)      # 10% raise for everyone!
print(salaries - 10000)     # Deduct tax from everyone
```

---

## Statistical Functions

```python
data = np.array([85, 92, 78, 95, 88, 72, 90, 88, 85, 91])

print(np.mean(data))        # 86.4  — average
print(np.median(data))      # 88.0  — middle value
print(np.std(data))         # 6.56  — standard deviation
print(np.var(data))         # 43.04 — variance
print(np.min(data))         # 72
print(np.max(data))         # 95
print(np.sum(data))         # 864
print(np.percentile(data, 25))   # 25th percentile
print(np.percentile(data, 75))   # 75th percentile
print(np.corrcoef(data, data))   # Correlation matrix
```

---

## Indexing & Slicing

```python
arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90])

# Same as lists
print(arr[0])           # 10
print(arr[-1])          # 90
print(arr[2:5])         # [30 40 50]
print(arr[::2])         # [10 30 50 70 90]

# 2D indexing
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

print(matrix[0, 0])     # 1  — row 0, col 0
print(matrix[1, 2])     # 6  — row 1, col 2
print(matrix[:, 1])     # [2 5 8] — entire column 1
print(matrix[0, :])     # [1 2 3] — entire row 0
print(matrix[0:2, 1:3]) # [[2 3] [5 6]] — sub-matrix
```

---

## Boolean Indexing (Filtering)

```python
salaries = np.array([120000, 95000, 110000, 85000, 150000, 72000])

# Filter
high = salaries[salaries > 100000]
print(high)             # [120000 110000 150000]

# Multiple conditions
mid_range = salaries[(salaries >= 90000) & (salaries <= 120000)]
print(mid_range)        # [120000 95000 110000]

# Where — conditional replacement
adjusted = np.where(salaries < 90000, salaries * 1.15, salaries)
print(adjusted)         # Low salaries get 15% raise
```

---

## Reshaping Arrays

```python
arr = np.arange(12)             # [0 1 2 3 4 5 6 7 8 9 10 11]

# Reshape
matrix = arr.reshape(3, 4)      # 3 rows, 4 cols
matrix = arr.reshape(4, 3)      # 4 rows, 3 cols
matrix = arr.reshape(2, 2, 3)   # 3D array!

# Flatten
flat = matrix.flatten()         # Back to 1D

# Transpose
print(matrix.T)                 # Flip rows and columns
```

---

## Real World Example — Sales Analysis

```python
import numpy as np

# Monthly sales data (12 months, 3 regions)
np.random.seed(42)
sales = np.array([
    [420, 385, 510, 490, 620, 580, 450, 730, 695, 810, 750, 920],  # Nairobi
    [210, 195, 280, 245, 310, 290, 225, 365, 348, 405, 375, 460],  # Mombasa
    [150, 140, 200, 175, 220, 208, 161, 261, 249, 290, 268, 329]   # Kisumu
])

regions = ["Nairobi", "Mombasa", "Kisumu"]
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

print("📊 Regional Sales Analysis (KES Thousands)")
print("=" * 50)

for i, region in enumerate(regions):
    region_sales = sales[i]
    print(f"\n{region}:")
    print(f"  Total:    KES {np.sum(region_sales):,}K")
    print(f"  Average:  KES {np.mean(region_sales):,.1f}K")
    print(f"  Best:     {months[np.argmax(region_sales)]} (KES {np.max(region_sales):,}K)")
    print(f"  Worst:    {months[np.argmin(region_sales)]} (KES {np.min(region_sales):,}K)")
    print(f"  Growth:   {((region_sales[-1] - region_sales[0]) / region_sales[0] * 100):.1f}%")

# Overall
print(f"\n📈 Overall:")
print(f"  Total Revenue: KES {np.sum(sales):,}K")
print(f"  Monthly Total: {np.sum(sales, axis=0)}")     # Sum each month across regions
print(f"  Region Total:  {np.sum(sales, axis=1)}")     # Sum each region across months
```

---

## NumPy vs Pandas

| Use NumPy when... | Use Pandas when... |
|---|---|
| Pure numerical computation | Mixed data types |
| Matrix operations (ML) | Named columns matter |
| Speed is critical | Data cleaning |
| Under the hood of ML models | Reading CSV/Excel |

---

## Practice Exercise

```python
import numpy as np

# Customer credit scores
scores = np.array([720, 650, 810, 580, 695, 720, 760, 640, 810, 590,
                   700, 730, 680, 810, 620, 750, 690, 720, 580, 800])

# Analysis
print(f"Total customers: {len(scores)}")
print(f"Average score:   {np.mean(scores):.1f}")
print(f"Median score:    {np.median(scores):.1f}")
print(f"Std deviation:   {np.std(scores):.1f}")

# Segmentation
excellent = np.sum(scores >= 750)
good = np.sum((scores >= 650) & (scores < 750))
fair = np.sum((scores >= 580) & (scores < 650))
poor = np.sum(scores < 580)

print(f"\nExcellent (750+): {excellent} customers")
print(f"Good (650-749):   {good} customers")
print(f"Fair (580-649):   {fair} customers")
print(f"Poor (<580):      {poor} customers")
```

---

## Previous | Next
← [[11 - Pandas Data Cleaning]] | → [[13 - Matplotlib and Seaborn]]
