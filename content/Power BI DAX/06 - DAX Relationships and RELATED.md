---
title: DAX Relationships and RELATED
tags: [powerbi, dax, relationships, related, lookupvalue]
created: 2026-05-20
up:: [[Power BI MOC]]
---

# 🔗 DAX Relationships & RELATED

> Understanding relationships is the foundation of the data model. RELATED, RELATEDTABLE, LOOKUPVALUE, and USERELATIONSHIP let you navigate between tables and pull values across relationships — the DAX equivalent of SQL JOINs.

---

## Power BI Relationships

```
Relationships connect tables on matching keys:

Customers (1) ──────── (many) Transactions
  Customer_ID              Customer_ID
  
  One customer → many transactions
  Filter flows from Customers → Transactions
  (Many side inherits filters from One side)
```

### Relationship Properties

```
Cardinality:
  One-to-Many (1:*)    — most common
  One-to-One (1:1)     — lookup/dimension tables
  Many-to-Many (*.*)   — requires bridge table

Cross-filter direction:
  Single     — filter flows one way (standard, fastest)
  Both       — filter flows both ways (use carefully)

Active vs Inactive:
  Active     — used automatically by DAX
  Inactive   — must be activated with USERELATIONSHIP
```

---

## RELATED — Lookup from Many to One

```dax
-- RELATED looks up a value from the ONE side of a relationship
-- Used in CALCULATED COLUMNS (row context required)

-- In Transactions table — get customer tier from Customers table
Transactions[Customer Tier] = 
    RELATED(Customers[Tier])

-- Get customer city for each transaction
Transactions[Customer City] = 
    RELATED(Customers[City])

-- Get product price from Products table
Order_Lines[Unit Price] = 
    RELATED(Products[Price])

-- Calculate margin in calculated column
Order_Lines[Line Margin] = 
    Order_Lines[Revenue] - 
    (Order_Lines[Quantity] * RELATED(Products[Cost]))
```

---

## RELATED in Measures (with SUMX)

```dax
-- RELATED works inside SUMX because SUMX creates row context

Revenue by Tier = 
    SUMX(
        Transactions,
        IF(
            RELATED(Customers[Tier]) = "Gold",
            Transactions[Amount],
            0
        )
    )

-- Weight transactions by customer balance
Weighted Revenue = 
    SUMX(
        Transactions,
        Transactions[Amount] * RELATED(Customers[Balance]) / 1000000
    )

-- Discount based on product category
Discounted Revenue = 
    SUMX(
        Order_Lines,
        Order_Lines[Revenue] * 
        (1 - RELATED(Products[Category_Discount_Pct]))
    )
```

---

## RELATEDTABLE — From One to Many

```dax
-- RELATEDTABLE returns the related MANY-side rows
-- Used in calculated columns on the ONE side

-- In Customers table — count their transactions
Customers[Transaction Count] = 
    COUNTROWS(RELATEDTABLE(Transactions))

-- Sum of all customer transactions
Customers[Lifetime Value] = 
    SUMX(
        RELATEDTABLE(Transactions),
        Transactions[Amount]
    )

-- Last transaction date
Customers[Last Transaction] = 
    MAXX(
        RELATEDTABLE(Transactions),
        Transactions[Date]
    )

-- Has any transaction over KES 100,000?
Customers[Has Large Transaction] = 
    COUNTROWS(
        FILTER(
            RELATEDTABLE(Transactions),
            Transactions[Amount] > 100000
        )
    ) > 0
```

---

## LOOKUPVALUE — No Relationship Required

```dax
-- LOOKUPVALUE finds a value without needing a formal relationship
-- Like VLOOKUP in Excel

LOOKUPVALUE(
    result_column,          -- Column to return
    search_column,          -- Column to search in
    search_value,           -- Value to match
    [search_column2, search_value2, ...],  -- Optional extra conditions
    [alternate_result]      -- If not found
)

-- Get customer name for a transaction
Transaction[Customer Name] = 
    LOOKUPVALUE(
        Customers[Name],
        Customers[Customer_ID],
        Transactions[Customer_ID]
    )

-- Multi-condition lookup
Sales[Product Price] = 
    LOOKUPVALUE(
        Price_List[Price],
        Price_List[Product_ID],  Sales[Product_ID],
        Price_List[Year],        YEAR(Sales[Date]),
        0                        -- Default if not found
    )

-- Use in measures with SELECTEDVALUE
Selected Customer Name = 
    LOOKUPVALUE(
        Customers[Name],
        Customers[Customer_ID],
        SELECTEDVALUE(Customers[Customer_ID])
    )
```

---

## USERELATIONSHIP — Activate Inactive Relationships

```dax
-- Scenario: Date table connected to both Order_Date and Ship_Date
-- Only one relationship can be active at a time
-- Use USERELATIONSHIP to activate the inactive one

Revenue by Ship Date = 
    CALCULATE(
        SUM(Orders[Revenue]),
        USERELATIONSHIP(Orders[Ship_Date], 'Date Table'[Date])
    )

Revenue by Order Date = 
    CALCULATE(
        SUM(Orders[Revenue]),
        USERELATIONSHIP(Orders[Order_Date], 'Date Table'[Date])
    )

-- Common pattern: Sales by different date types
Orders YTD (Ship Date) = 
    CALCULATE(
        TOTALYTD(SUM(Orders[Revenue]), 'Date Table'[Date]),
        USERELATIONSHIP(Orders[Ship_Date], 'Date Table'[Date])
    )
```

---

## CROSSFILTER — Control Filter Direction

```dax
-- Override bidirectional filtering for a specific calculation
-- Useful when you need both directions but want to control it

-- Count customers who have matching transactions
-- (requires filter to flow from Transactions to Customers)
Customers With Purchases = 
    CALCULATE(
        DISTINCTCOUNT(Customers[Customer_ID]),
        CROSSFILTER(Customers[Customer_ID], Transactions[Customer_ID], BOTH)
    )
```

---

## Role-Playing Dimensions

```dax
-- One date table, multiple relationships (one active, others inactive)
-- Common pattern for Order Date, Ship Date, Return Date

-- Measure using active relationship (Order Date — active)
Revenue by Order Date = SUM(Orders[Amount])

-- Measure using inactive relationship (Ship Date)
Revenue by Ship Date = 
    CALCULATE(
        SUM(Orders[Amount]),
        USERELATIONSHIP(Orders[Ship_Date], 'Date Table'[Date])
    )

-- YTD by Ship Date
Revenue YTD by Ship = 
    CALCULATE(
        TOTALYTD(SUM(Orders[Amount]), 'Date Table'[Date]),
        USERELATIONSHIP(Orders[Ship_Date], 'Date Table'[Date])
    )
```

---

## Many-to-Many Relationships

```dax
-- Scenario: Customers can have multiple products
--           Products can belong to multiple customers
-- Solution: Bridge table Customer_Products

-- Revenue via bridge table
Revenue via Bridge = 
    CALCULATE(
        SUM(Sales[Amount]),
        TREATAS(
            VALUES(Customer_Products[Customer_ID]),
            Sales[Customer_ID]
        )
    )

-- TREATAS — treat a table as if it has a specific relationship
-- Powerful for virtual relationships
```

---

## Real World — Bank Marketing Model

```dax
-- Model: Customers ←→ Campaigns ←→ Date Table

-- Subscription rate by job using RELATED
Subscription Rate by Job = 
    VAR JobCustomers = COUNTROWS(Customers)
    VAR Subscribed = 
        CALCULATE(COUNTROWS(Customers), Customers[Subscribed] = TRUE)
    RETURN DIVIDE(Subscribed, JobCustomers, 0) * 100

-- Balance segment using LOOKUPVALUE (no relationship needed)
Balance Tier Label = 
    LOOKUPVALUE(
        Tier_Thresholds[Tier_Label],
        Tier_Thresholds[Min_Balance], 
            MAXX(
                FILTER(
                    Tier_Thresholds,
                    Tier_Thresholds[Min_Balance] <= Customers[Balance]
                ),
                Tier_Thresholds[Min_Balance]
            )
    )

-- Get campaign month using RELATED (in transaction calculated column)
Campaign[Month Number] = 
    RELATED('Date Table'[Month Number])

Campaign[Is Weekday] = 
    NOT RELATED('Date Table'[Is Weekend])

-- Revenue from customers subscribed in a specific month
Revenue from Month Subscribers = 
    CALCULATE(
        SUM(Transactions[Amount]),
        USERELATIONSHIP(
            Customers[Subscription_Date],
            'Date Table'[Date]
        ),
        FILTER(
            ALL('Date Table'),
            'Date Table'[Month Number] = 
                SELECTEDVALUE('Date Table'[Month Number])
        )
    )
```

---

## Relationship Best Practices

```
Model design:
  ✅ Star schema — fact table in centre, dimensions around it
  ✅ Single direction relationships (default)
  ✅ Integer keys (faster than strings)
  ✅ Mark date table as Date Table
  ❌ Avoid bidirectional unless necessary (circular filters)
  ❌ Avoid many-to-many without bridge table

DAX:
  ✅ Use RELATED in calculated columns (row context)
  ✅ Use CALCULATE + FILTER for complex cross-table filters
  ✅ Use LOOKUPVALUE when no relationship exists
  ✅ Use USERELATIONSHIP for role-playing dimensions
  ❌ Never use RELATED in measures without SUMX/AVERAGEX
```

---

## Quick Reference

```dax
-- RELATED: many side → one side (in calc column or SUMX)
Table[Column] = RELATED(OtherTable[Column])

-- RELATEDTABLE: one side → many side (in calc column)
COUNTROWS(RELATEDTABLE(ManyTable))

-- LOOKUPVALUE: no relationship needed
LOOKUPVALUE(result_col, search_col, search_val, [default])

-- USERELATIONSHIP: activate inactive relationship
CALCULATE(expr, USERELATIONSHIP(Table1[Col], Table2[Col]))

-- CROSSFILTER: change filter direction
CALCULATE(expr, CROSSFILTER(col1, col2, BOTH))

-- TREATAS: virtual relationship
CALCULATE(expr, TREATAS(table, target_col))
```

---

## Previous | Next
← [[05 - DAX Variables and Advanced Patterns]] | → [[07 - DAX KPI and Financial Measures]]
