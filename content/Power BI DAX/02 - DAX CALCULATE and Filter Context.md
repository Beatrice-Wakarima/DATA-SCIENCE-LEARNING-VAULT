---
title: DAX CALCULATE and Filter Context
tags: [powerbi, dax, calculate, filter-context]
created: 2026-05-20
up:: [[Power BI MOC]]
---

# 🎛️ CALCULATE & Filter Context

> CALCULATE is the most important function in DAX. It is the engine behind every advanced calculation. Understanding it completely is the difference between basic and expert Power BI.

---

## What CALCULATE Does

```dax
CALCULATE(expression, filter1, filter2, ...)

-- It does TWO things:
-- 1. Evaluates an expression
-- 2. In a MODIFIED filter context
```

```dax
-- Without CALCULATE — affected by ALL visual filters
Total Sales = SUM(Sales[Amount])

-- With CALCULATE — you control exactly what's filtered
Gold Sales = 
    CALCULATE(
        SUM(Sales[Amount]),
        Customers[Tier] = "Gold"    -- Override/add filter
    )
-- Returns Gold sales regardless of what tier slicer says!
```

---

## How CALCULATE Modifies Context

```dax
-- Step 1: Power BI creates filter context from visuals/slicers
-- Step 2: CALCULATE takes that context
-- Step 3: Modifies it with your filters
-- Step 4: Evaluates the expression in the new context

-- Example: Matrix with Month on rows, City on columns
-- Cell: May 2026 | Nairobi
-- Original filter context: Month=May, City=Nairobi

Gold Nairobi May Sales = 
    CALCULATE(
        SUM(Sales[Amount]),
        Customers[Tier] = "Gold"    -- Adds Tier=Gold to context
        -- Month and City filters from visual still apply!
    )
-- Result: Gold customer sales in Nairobi in May 2026
```

---

## CALCULATE with Multiple Filters

```dax
-- Multiple filters are AND conditions
Premium Active Customers = 
    CALCULATE(
        COUNTROWS(Customers),
        Customers[Tier] = "Platinum",
        Customers[Is_Active] = TRUE,
        Customers[Balance] > 100000
    )

-- Using FILTER for complex conditions
High Value Recent = 
    CALCULATE(
        SUM(Transactions[Amount]),
        FILTER(
            Transactions,
            Transactions[Amount] > 50000 &&
            Transactions[Date] >= DATE(2026, 1, 1)
        )
    )
```

---

## ALL — Remove Filters

```dax
-- ALL removes filters from a table or columns
-- Useful for calculating totals and percentages

% of Total = 
    DIVIDE(
        SUM(Sales[Amount]),
        CALCULATE(SUM(Sales[Amount]), ALL(Sales))
    ) * 100

-- ALL on specific columns (keep other filters)
% of City Total = 
    DIVIDE(
        SUM(Sales[Amount]),
        CALCULATE(
            SUM(Sales[Amount]),
            ALL(Customers[Tier])    -- Remove tier filter only
            -- City filter from visual still applies
        )
    ) * 100

-- ALLEXCEPT — remove all filters EXCEPT specified columns
City Total = 
    CALCULATE(
        SUM(Sales[Amount]),
        ALLEXCEPT(Customers, Customers[City])
        -- Keep city filter, remove everything else
    )
```

---

## ALLSELECTED — Respect Slicers

```dax
-- ALLSELECTED keeps the user's slicer selections
-- but removes row/column header filters

-- Scenario: User selects "Nairobi" in City slicer
-- Matrix has Tier on rows

% of Slicer Selection = 
    DIVIDE(
        SUM(Sales[Amount]),
        CALCULATE(
            SUM(Sales[Amount]),
            ALLSELECTED(Customers)   -- Uses slicer filters only
            -- Removes Tier filter from rows
        )
    ) * 100

-- Each tier row shows: that tier's % of all Nairobi sales
-- If user changes slicer, percentages update accordingly
```

---

## Real World Examples

### Sales vs Target
```dax
Sales vs Target = 
    [Total Revenue] - [Revenue Target]

Achievement % = 
    DIVIDE([Total Revenue], [Revenue Target], 0) * 100

Above Target = 
    CALCULATE(
        COUNTROWS(Salespeople),
        [Achievement %] >= 100
    )
```

### Market Share
```dax
Market Share % = 
    DIVIDE(
        SUM(Sales[Amount]),
        CALCULATE(SUM(Sales[Amount]), ALL(Products[Category]))
    ) * 100
```

### Subscription Analysis
```dax
-- Bank marketing: conversion rate vs overall rate
Local Conversion Rate = 
    DIVIDE(
        CALCULATE(
            COUNTROWS(Customers),
            Customers[Subscribed] = TRUE
        ),
        COUNTROWS(Customers),
        0
    ) * 100

Overall Conversion Rate = 
    CALCULATE(
        DIVIDE(
            CALCULATE(
                COUNTROWS(Customers),
                Customers[Subscribed] = TRUE
            ),
            COUNTROWS(Customers),
            0
        ) * 100,
        ALL(Customers)      -- Remove all visual filters
    )

Conversion vs Overall = 
    [Local Conversion Rate] - [Overall Conversion Rate]
```

---

## KEEPFILTERS — Add Without Overriding

```dax
-- Normal CALCULATE overrides existing filters on same column
-- KEEPFILTERS intersects with existing filters instead

-- Without KEEPFILTERS — always returns Gold sales
-- even if user selects Silver in slicer
Gold Sales = 
    CALCULATE(
        SUM(Sales[Amount]),
        Customers[Tier] = "Gold"    -- Overrides slicer
    )

-- With KEEPFILTERS — returns nothing if slicer says Silver
Gold Sales (Filtered) = 
    CALCULATE(
        SUM(Sales[Amount]),
        KEEPFILTERS(Customers[Tier] = "Gold")
        -- Intersects: Gold AND whatever slicer says
    )
```

---

## REMOVEFILTERS

```dax
-- Explicit way to remove filters (same as ALL but clearer)
Grand Total = 
    CALCULATE(
        SUM(Sales[Amount]),
        REMOVEFILTERS(Sales)    -- Remove all filters on Sales
    )

-- Remove specific column filters
Tier Total = 
    CALCULATE(
        SUM(Sales[Amount]),
        REMOVEFILTERS(Customers[Tier])
    )
```

---

## Variables in CALCULATE

```dax
-- Always use variables for complex CALCULATE
Subscription Uplift = 
    VAR LocalRate = 
        DIVIDE(
            CALCULATE(COUNTROWS(Customers), Customers[Subscribed] = TRUE),
            COUNTROWS(Customers),
            0
        )
    VAR GlobalRate = 
        CALCULATE(
            DIVIDE(
                CALCULATE(COUNTROWS(Customers), Customers[Subscribed] = TRUE),
                COUNTROWS(Customers),
                0
            ),
            ALL(Customers)
        )
    RETURN
        LocalRate - GlobalRate
```

---

## Common CALCULATE Mistakes

```dax
-- ❌ WRONG: Comparing measure inside FILTER
Wrong Measure = 
    CALCULATE(
        SUM(Sales[Amount]),
        FILTER(Customers, [Total Revenue] > 100000)  -- Slow! Row-by-row
    )

-- ✅ BETTER: Use column value
Better Measure = 
    CALCULATE(
        SUM(Sales[Amount]),
        Customers[Balance] > 100000    -- Uses column directly
    )

-- ❌ WRONG: Using CALCULATE when not needed
Simple Sum = CALCULATE(SUM(Sales[Amount]))  -- Pointless CALCULATE

-- ✅ CORRECT: Just use SUM directly
Simple Sum = SUM(Sales[Amount])

-- ❌ WRONG: Forgetting ALL for % of total
Wrong Pct = DIVIDE(SUM(Sales[Amount]), SUM(Sales[Amount])) * 100
-- Always returns 100%!

-- ✅ CORRECT: Remove filters for denominator
Correct Pct = 
    DIVIDE(
        SUM(Sales[Amount]),
        CALCULATE(SUM(Sales[Amount]), ALL(Sales))
    ) * 100
```

---

## CALCULATE Cheat Sheet

```dax
-- Basic CALCULATE
CALCULATE(expression, filter)

-- Multiple filters (AND)
CALCULATE(expr, filter1, filter2)

-- Remove all filters
CALCULATE(expr, ALL(Table))

-- Remove specific column filters
CALCULATE(expr, ALL(Table[Column]))

-- Keep only slicer filters
CALCULATE(expr, ALLSELECTED(Table))

-- Keep other filters, remove all except one column
CALCULATE(expr, ALLEXCEPT(Table, Table[Column]))

-- Add filter without overriding
CALCULATE(expr, KEEPFILTERS(condition))

-- Complex filter
CALCULATE(expr, FILTER(Table, complex_condition))
```

---

## Previous | Next
← [[01 - Introduction to DAX]] | → [[03 - DAX Time Intelligence]]
