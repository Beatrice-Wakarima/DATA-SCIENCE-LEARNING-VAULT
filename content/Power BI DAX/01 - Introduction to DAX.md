---
title: Introduction to DAX
tags: [powerbi, dax, basics]
created: 2026-05-20
up:: [[Power BI MOC]]
---

# 📐 Introduction to DAX

> DAX (Data Analysis Expressions) is the formula language of Power BI, Power Pivot, and Analysis Services. It is what separates basic Power BI users from professionals who can answer any business question with data.

---

## What is DAX?

DAX is used to create:
- **Measures** — calculations that respond to filters (e.g. Total Sales)
- **Calculated Columns** — new columns added to a table
- **Calculated Tables** — new tables generated from existing data

```
DAX is NOT like Excel formulas:
  Excel:  =SUM(A1:A10)          — works on a range
  DAX:    Total Sales = SUM(Sales[Amount])  — works on a column
  
DAX is context-aware:
  The same measure gives different results in different contexts
  (by month, by region, by product — automatically)
```

---

## Measures vs Calculated Columns

```
MEASURE                          CALCULATED COLUMN
──────────────────               ──────────────────────────────
Calculated at query time         Calculated at data refresh
Lives in the model, not a table  Lives in a table as a new column
Responds to filters/slicers      Fixed — doesn't change with filters
Uses filter context              Uses row context
Stored as formula only           Stored as data (uses memory)
e.g. Total Sales = SUM(...)      e.g. Full Name = [First] & " " & [Last]
```

---

## Your First Measure

```dax
-- Simple aggregation
Total Sales = SUM(Sales[Amount])

-- With filter
Gold Customer Sales = 
    CALCULATE(
        SUM(Sales[Amount]),
        Customers[Tier] = "Gold"
    )

-- Count rows
Total Transactions = COUNTROWS(Transactions)

-- Average
Average Balance = AVERAGE(Customers[Balance])

-- Conditional count
Active Customers = 
    COUNTROWS(
        FILTER(Customers, Customers[Is_Active] = TRUE)
    )
```

---

## Two Types of Context

### Filter Context — What's Visible
```
When you put a slicer on "City = Nairobi":
  Filter context restricts which rows DAX sees
  Measures automatically recalculate for visible rows only
  
  Total Sales = SUM(Sales[Amount])
  → Without filter: KES 4,500,000
  → With City = Nairobi filter: KES 1,200,000
```

### Row Context — Current Row
```
When Power BI calculates a calculated column:
  DAX processes each row one at a time
  
  Customers[Bonus] = Customers[Salary] * 0.10
  → Row 1: 120,000 * 0.10 = 12,000
  → Row 2: 95,000 * 0.10 = 9,500
  → Row 3: 110,000 * 0.10 = 11,000
```

---

## The DAX Calculation Engine

```
Report Visual
     ↓
Filter Context (slicers, visual filters, row/column headers)
     ↓
DAX Engine evaluates measure in that context
     ↓
Result displayed in visual

Example:
  Matrix visual with Month on rows, Tier on columns
  Cell "May 2026 | Gold" has filter context:
    Month = May 2026  AND  Tier = Gold
  
  Total Sales measure returns sales for Gold customers in May 2026
```

---

## DAX Syntax Rules

```dax
-- Table names use single quotes if they contain spaces
Sales[Amount]               -- Column reference: Table[Column]
'Sales Data'[Amount]        -- Spaces in table name: quotes required
[Total Sales]               -- Measure reference: [MeasureName]

-- DAX is case-insensitive
SUM(sales[amount]) = SUM(Sales[Amount])

-- String literals use double quotes
WHERE Country = "Kenya"

-- Comments
// Single line comment
/* Multi-line 
   comment */

-- Line breaks don't matter
Total Sales = 
    CALCULATE(
        SUM(Sales[Amount]),
        DateTable[Year] = 2026
    )
```

---

## Data Types

```dax
-- Integer
Order Count = COUNTROWS(Orders)

-- Decimal
Tax Rate = 0.16

-- Text
Status = "Active"

-- Boolean
Is Premium = TRUE()
Has Purchases = [Total Transactions] > 0

-- Date
Today = TODAY()
This Month Start = DATE(YEAR(TODAY()), MONTH(TODAY()), 1)

-- Blank (NULL equivalent)
No Value = BLANK()
Safe Divide = DIVIDE([Sales], [Costs], BLANK())  -- BLANK if error
```

---

## The Most Important DAX Functions

```dax
-- AGGREGATION
SUM(Table[Column])
AVERAGE(Table[Column])
MIN(Table[Column])
MAX(Table[Column])
COUNT(Table[Column])        -- Counts non-blanks
COUNTA(Table[Column])       -- Counts non-blanks (any type)
COUNTROWS(Table)            -- Counts rows
DISTINCTCOUNT(Table[Column]) -- Count unique values

-- FILTER
CALCULATE(expression, filter1, filter2, ...)  -- The most important function!
FILTER(Table, condition)    -- Returns filtered table
ALL(Table)                  -- Remove all filters
ALLEXCEPT(Table, col)       -- Remove all except specified filters
ALLSELECTED(Table)          -- Keep slicer filters only

-- LOGICAL
IF(condition, true_result, false_result)
SWITCH(expression, value1, result1, value2, result2, ..., else)
AND(cond1, cond2)  or  cond1 && cond2
OR(cond1, cond2)   or  cond1 || cond2
NOT(condition)
ISNULL(value)
ISBLANK(value)
COALESCE(value1, value2, ...)  -- First non-blank

-- TEXT
CONCATENATE(text1, text2)  or  text1 & text2
LEFT(text, n)
RIGHT(text, n)
MID(text, start, length)
LEN(text)
UPPER(text) / LOWER(text)
TRIM(text)
REPLACE(text, start, length, new_text)
SUBSTITUTE(text, old, new)
FORMAT(value, "format_string")

-- DATE
TODAY()  /  NOW()
DATE(year, month, day)
YEAR(date) / MONTH(date) / DAY(date)
DATEDIFF(start, end, MONTH)
DATEADD(dates, n, period)
EOMONTH(date, 0)            -- End of current month
WEEKDAY(date, 2)            -- Day of week (1=Mon)

-- MATH
DIVIDE(numerator, denominator, alternate)  -- Safe division
ROUND(number, decimals)
ABS(number)
POWER(number, exponent)
SQRT(number)
MOD(number, divisor)
```

---

## Writing Your First Measures

```dax
-- ── BASIC MEASURES ──────────────────────────────────────

Total Revenue = SUM(Transactions[Amount])

Transaction Count = COUNTROWS(Transactions)

Average Transaction = AVERAGE(Transactions[Amount])

Unique Customers = DISTINCTCOUNT(Transactions[Customer_ID])

-- ── CONDITIONAL MEASURES ────────────────────────────────

Subscription Rate % = 
    DIVIDE(
        COUNTROWS(FILTER(Customers, Customers[Subscribed] = TRUE)),
        COUNTROWS(Customers),
        0
    ) * 100

High Value Customers = 
    COUNTROWS(
        FILTER(Customers, Customers[Balance] > 100000)
    )

-- ── FORMATTED OUTPUT ────────────────────────────────────

Revenue (Formatted) = 
    "KES " & FORMAT([Total Revenue], "#,##0")

Subscription Rate (Formatted) = 
    FORMAT([Subscription Rate %], "0.0") & "%"
```

---

## Where to Write DAX

```
1. New Measure:
   Home tab → New Measure
   OR right-click a table → New Measure
   
2. Quick Measure:
   Home tab → Quick Measure (wizard-based)
   
3. Calculated Column:
   Right-click table header → New Column
   
4. Calculated Table:
   Modeling tab → New Table

5. DAX formula bar:
   Appears at top when measure/column selected
   IntelliSense helps with function names and columns
```

---

## Debugging DAX

```dax
-- Check intermediate values with a table visual
-- Drag measure to a table to see row-by-row values

-- Use variables to break complex formulas into steps
Revenue Per Customer = 
    VAR TotalRevenue = SUM(Transactions[Amount])
    VAR CustomerCount = DISTINCTCOUNT(Transactions[Customer_ID])
    VAR Result = DIVIDE(TotalRevenue, CustomerCount, 0)
    RETURN Result

-- Add a "debug measure" to check what CALCULATE is seeing
Debug Filter Context = 
    CONCATENATE(
        "Rows visible: ",
        COUNTROWS(Customers)
    )
```

---

## Quick Reference

```dax
-- Basic measures
Total = SUM(Table[Column])
Count = COUNTROWS(Table)
Avg = AVERAGE(Table[Column])
Max = MAX(Table[Column])
Unique = DISTINCTCOUNT(Table[Column])

-- Context modification
CALCULATE([Measure], filter)
ALL(Table)              -- Remove filters
FILTER(Table, condition) -- Custom filter

-- Safe operations
DIVIDE(num, den, 0)     -- Divide safely
COALESCE(val, default)  -- Handle blanks
IF(cond, yes, no)       -- Conditional

-- Format
FORMAT(value, "#,##0")         -- Number with commas
FORMAT(value, "0.00%")         -- Percentage
FORMAT(date, "MMM YYYY")       -- Date format
```

---

## Previous | Next
← Start | → [[02 - DAX CALCULATE and Filter Context]]
