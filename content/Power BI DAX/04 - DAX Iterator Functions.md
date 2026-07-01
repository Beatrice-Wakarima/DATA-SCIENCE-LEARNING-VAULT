---
title: DAX Iterator Functions (X Functions)
tags: [powerbi, dax, iterators, sumx, averagex]
created: 2026-05-20
up:: [[Power BI MOC]]
---

# 🔄 DAX Iterator Functions (X Functions)

> Iterator functions loop through every row of a table, evaluate an expression per row, then aggregate the results. They are the most powerful and flexible DAX functions — essential for complex business calculations.

---

## The X Function Pattern

```dax
-- Regular aggregation — works on a single column
Total Revenue = SUM(Transactions[Amount])

-- Iterator — calculates per row then aggregates
Revenue After Tax = 
    SUMX(
        Transactions,                           -- Table to iterate
        Transactions[Amount] * (1 - 0.16)      -- Expression per row
    )

-- SUMX loops through each row:
--   Row 1: 45000 * 0.84 = 37800
--   Row 2: 12000 * 0.84 = 10080
--   Row 3: 98000 * 0.84 = 82320
--   Result: 37800 + 10080 + 82320 = 130200
```

---

## SUMX — Row-by-Row Sum

```dax
-- Revenue with tax deducted
Net Revenue = 
    SUMX(
        Transactions,
        Transactions[Amount] * (1 - 'Tax Rates'[Rate])
    )

-- Total order value (quantity × unit price per row)
Total Order Value = 
    SUMX(
        Orders,
        Orders[Quantity] * Orders[Unit_Price]
    )

-- Discounted revenue
Discounted Revenue = 
    SUMX(
        Sales,
        Sales[Amount] * (1 - Sales[Discount_Pct])
    )

-- With related table (lookup values while iterating)
Revenue with Margin = 
    SUMX(
        Sales,
        Sales[Amount] * RELATED(Products[Margin_Pct])
    )
```

---

## AVERAGEX — Row-by-Row Average

```dax
-- Average revenue per customer (using RELATED)
Avg Revenue Per Customer = 
    AVERAGEX(
        Customers,
        CALCULATE(SUM(Transactions[Amount]))
    )

-- Average basket value (total / count per transaction)
Avg Basket Value = 
    AVERAGEX(
        VALUES(Transactions[Transaction_ID]),
        CALCULATE(SUM(Order_Lines[Line_Total]))
    )

-- Average call duration for subscribed customers only
Avg Call Duration Subscribers = 
    AVERAGEX(
        FILTER(Customers, Customers[Subscribed] = TRUE),
        Customers[Call_Duration_Secs]
    )

-- Weighted average (price × volume / total volume)
Weighted Avg Price = 
    DIVIDE(
        SUMX(Sales, Sales[Unit_Price] * Sales[Quantity]),
        SUM(Sales[Quantity]),
        0
    )
```

---

## COUNTX — Row-by-Row Count

```dax
-- Count rows where condition is true
High Value Transactions = 
    COUNTX(
        FILTER(Transactions, Transactions[Amount] > 50000),
        Transactions[Transaction_ID]
    )

-- Count customers with at least one transaction
Active Customers = 
    COUNTX(
        VALUES(Transactions[Customer_ID]),
        Transactions[Customer_ID]
    )

-- Equivalent to COUNTROWS + FILTER (COUNTROWS is usually faster)
High Value Count = 
    COUNTROWS(FILTER(Transactions, Transactions[Amount] > 50000))
```

---

## MAXX and MINX — Row-by-Row Max/Min

```dax
-- Max single transaction per customer group
Largest Transaction = 
    MAXX(
        Transactions,
        Transactions[Amount]
    )

-- Most profitable product per category
Best Margin Product = 
    MAXX(
        Products,
        Products[Margin_Pct]
    )

-- Customer with highest lifetime value
Top Customer Value = 
    MAXX(
        VALUES(Customers[Customer_ID]),
        CALCULATE(SUM(Transactions[Amount]))
    )

-- Most recent transaction date
Latest Transaction = 
    MAXX(
        Transactions,
        Transactions[Date]
    )
```

---

## RANKX — Ranking

```dax
-- Rank customers by total revenue (1 = highest)
Customer Revenue Rank = 
    RANKX(
        ALL(Customers),                         -- Rank over all customers
        CALCULATE(SUM(Transactions[Amount])),   -- Metric to rank by
        ,                                       -- Empty = use current value
        DESC,                                   -- Descending (highest = 1)
        Dense                                   -- Dense = no gaps in ranks
    )

-- Rank products within category
Product Rank in Category = 
    RANKX(
        ALLSELECTED(Products),
        [Total Revenue],
        ,
        DESC,
        Dense
    )

-- Rank months by revenue
Month Rank = 
    RANKX(
        ALL('Date Table'[Month-Year]),
        [Total Revenue],
        ,
        DESC,
        Dense
    )

-- Top N filter (use in visual filter)
Is Top 10 Customer = 
    [Customer Revenue Rank] <= 10
```

---

## FILTER — Filter a Table

```dax
-- FILTER returns a table, used inside other functions

-- Revenue from active Gold customers
Active Gold Revenue = 
    CALCULATE(
        SUM(Transactions[Amount]),
        FILTER(
            Customers,
            Customers[Tier] = "Gold" &&
            Customers[Is_Active] = TRUE
        )
    )

-- Transactions over KES 100,000
Large Transactions = 
    SUMX(
        FILTER(
            Transactions,
            Transactions[Amount] > 100000
        ),
        Transactions[Amount]
    )

-- Multi-condition filter
High Value Young Subscribers = 
    COUNTROWS(
        FILTER(
            Customers,
            Customers[Balance] > 50000 &&
            Customers[Age] < 35 &&
            Customers[Subscribed] = TRUE
        )
    )
```

---

## GENERATE and GENERATEALL

```dax
-- GENERATE — cross join two tables (row context passes through)
Customer Transaction Pairs = 
    GENERATE(
        Customers,
        FILTER(
            Transactions,
            Transactions[Customer_ID] = Customers[Customer_ID]
        )
    )
```

---

## ADDCOLUMNS — Extend a Table

```dax
-- Add calculated columns to a virtual table
Customer Summary = 
    ADDCOLUMNS(
        Customers,
        "Total Transactions",
            CALCULATE(COUNTROWS(Transactions)),
        "Total Revenue",
            CALCULATE(SUM(Transactions[Amount])),
        "Avg Transaction",
            CALCULATE(AVERAGE(Transactions[Amount])),
        "Last Transaction",
            CALCULATE(MAX(Transactions[Date]))
    )

-- Use in SUMX for complex calculations
Revenue Score = 
    SUMX(
        ADDCOLUMNS(
            VALUES(Customers[Customer_ID]),
            "Revenue",      CALCULATE(SUM(Transactions[Amount])),
            "Tenure",       DATEDIFF(MIN(Customers[Joined_Date]), TODAY(), YEAR)
        ),
        [Revenue] * [Tenure]
    )
```

---

## TOPN — Get Top N Rows

```dax
-- Top 5 customers by revenue
Top 5 Revenue = 
    SUMX(
        TOPN(
            5,
            VALUES(Customers[Customer_ID]),
            CALCULATE(SUM(Transactions[Amount])),
            DESC
        ),
        CALCULATE(SUM(Transactions[Amount]))
    )

-- Top 10% of customers
Top Decile Revenue = 
    VAR CustomerCount = DISTINCTCOUNT(Transactions[Customer_ID])
    VAR Top10PctCount = ROUNDUP(CustomerCount * 0.1, 0)
    RETURN
        SUMX(
            TOPN(
                Top10PctCount,
                VALUES(Customers[Customer_ID]),
                CALCULATE(SUM(Transactions[Amount])),
                DESC
            ),
            CALCULATE(SUM(Transactions[Amount]))
        )
```

---

## Real World — Bank Marketing Iterators

```dax
-- Weighted average balance by job type
Weighted Avg Balance = 
    DIVIDE(
        SUMX(
            Customers,
            Customers[Balance] * Customers[Campaign_Contacts]
        ),
        SUM(Customers[Campaign_Contacts]),
        0
    )

-- Revenue contribution score
Customer Score = 
    SUMX(
        Customers,
        (Customers[Balance] * 0.4) +
        (Customers[Call_Duration_Secs] / 60 * 0.3) +
        (IF(Customers[Subscribed], 100, 0) * 0.3)
    )

-- Average revenue per subscribed customer
Revenue Per Subscriber = 
    AVERAGEX(
        FILTER(Customers, Customers[Subscribed] = TRUE),
        CALCULATE(SUM(Transactions[Amount]))
    )

-- ROI: subscription value / campaign cost per segment
Campaign ROI = 
    SUMX(
        VALUES(Customers[Job]),
        VAR SegmentSubscribers = 
            CALCULATE(
                COUNTROWS(Customers),
                Customers[Subscribed] = TRUE
            )
        VAR SegmentContacts = CALCULATE(COUNTROWS(Customers))
        VAR SegmentCost = SegmentContacts * 50     -- KES 50 per call
        VAR SegmentRevenue = SegmentSubscribers * 5000
        RETURN
            DIVIDE(SegmentRevenue - SegmentCost, SegmentCost, 0)
    )
```

---

## Variables in Iterators

```dax
-- Always use variables inside iterators for clarity
Complex Score = 
    SUMX(
        Customers,
        VAR Balance = Customers[Balance]
        VAR Age = Customers[Age]
        VAR Duration = Customers[Call_Duration_Secs]
        VAR Subscribed = Customers[Subscribed]

        VAR BalanceScore = SWITCH(
            TRUE,
            Balance > 100000, 5,
            Balance > 50000,  4,
            Balance > 10000,  3,
            Balance > 1000,   2,
            1
        )

        VAR EngagementScore = 
            IF(Duration > 300, 3,
            IF(Duration > 120, 2, 1))

        VAR SubscriptionBonus = IF(Subscribed, 10, 0)

        RETURN
            BalanceScore * 0.5 +
            EngagementScore * 0.3 +
            SubscriptionBonus * 0.2
    )
```

---

## Iterator Performance Tips

```dax
-- ✅ Use CALCULATE instead of SUMX when possible (much faster)
Fast = SUM(Sales[Amount])                    -- Best
Also Fast = CALCULATE(SUM(Sales[Amount]))    -- Good
Slow = SUMX(Sales, Sales[Amount])            -- Avoid if SUM works

-- ✅ Filter BEFORE iterating (reduce rows)
Better = SUMX(
    FILTER(Customers, Customers[Is_Active] = TRUE),  -- Filter first
    CALCULATE(SUM(Transactions[Amount]))
)

-- ✅ Use CALCULATE inside SUMX for context transition
Correct = SUMX(
    VALUES(Customers[Customer_ID]),
    CALCULATE(SUM(Transactions[Amount]))    -- CALCULATE needed here!
)

-- ❌ Never nest SUMX in SUMX unnecessarily
-- ❌ Never use iterators on huge tables without filtering first
```

---

## Quick Reference

```dax
SUMX(table, expression)         -- Sum expression per row
AVERAGEX(table, expression)     -- Average expression per row
COUNTX(table, expression)       -- Count non-blank per row
MAXX(table, expression)         -- Max expression per row
MINX(table, expression)         -- Min expression per row
RANKX(table, expression, , order, ties) -- Rank
FILTER(table, condition)        -- Filter rows
TOPN(n, table, expression, order) -- Top N rows
ADDCOLUMNS(table, name, expr, ...) -- Add virtual columns
GENERATE(table1, table2)        -- Cross join tables
```

---

## Previous | Next
← [[03 - DAX Time Intelligence]] | → [[05 - DAX Variables and Advanced Patterns]]
