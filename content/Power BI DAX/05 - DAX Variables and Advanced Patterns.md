---
title: DAX Variables and Advanced Patterns
tags: [powerbi, dax, variables, advanced]
created: 2026-05-20
up:: [[Power BI MOC]]
---

# 🧠 DAX Variables & Advanced Patterns

> Variables transform unreadable DAX into clean, debuggable, professional code. Advanced patterns like dynamic segmentation, what-if analysis, and conditional formatting take your reports from good to exceptional.

---

## VAR / RETURN — The Game Changer

```dax
-- Without variables — nested, hard to read, recalculated multiple times
Bad Measure = 
    IF(
        DIVIDE(
            CALCULATE(SUM(Sales[Amount]), Customers[Tier] = "Gold"),
            CALCULATE(SUM(Sales[Amount]), ALL(Customers[Tier])),
            0
        ) > 0.5,
        "Dominant",
        IF(
            DIVIDE(
                CALCULATE(SUM(Sales[Amount]), Customers[Tier] = "Gold"),
                CALCULATE(SUM(Sales[Amount]), ALL(Customers[Tier])),
                0
            ) > 0.25,
            "Strong",
            "Weak"
        )
    )

-- With variables — readable, efficient, each value calculated once
Good Measure = 
    VAR GoldRevenue = 
        CALCULATE(SUM(Sales[Amount]), Customers[Tier] = "Gold")
    VAR TotalRevenue = 
        CALCULATE(SUM(Sales[Amount]), ALL(Customers[Tier]))
    VAR GoldShare = DIVIDE(GoldRevenue, TotalRevenue, 0)
    RETURN
        SWITCH(
            TRUE,
            GoldShare > 0.5,  "Dominant",
            GoldShare > 0.25, "Strong",
            "Weak"
        )
```

---

## Variables — Key Rules

```dax
-- Variables are calculated ONCE in the filter context where they're defined
-- They do NOT recalculate when used multiple times (performance win!)

-- Variables can hold scalars, tables, or booleans
Scalar Variable = 
    VAR TotalSales = SUM(Sales[Amount])       -- Scalar
    RETURN TotalSales

Table Variable = 
    VAR ActiveCustomers = 
        FILTER(Customers, Customers[Is_Active] = TRUE)  -- Table
    RETURN COUNTROWS(ActiveCustomers)

Boolean Variable = 
    VAR IsCurrentYear = 
        MAX('Date Table'[Year]) = YEAR(TODAY())         -- Boolean
    RETURN IF(IsCurrentYear, [Revenue YTD], [Total Revenue])

-- Variables capture context at definition point
-- Use this for debugging complex measures
Debug Measure = 
    VAR Step1 = SUM(Sales[Amount])
    VAR Step2 = CALCULATE(Step1, ALL(Customers[Tier]))
    VAR Step3 = DIVIDE(Step1, Step2, 0)
    -- Return any step to inspect intermediate values!
    RETURN Step3
```

---

## SWITCH — Clean Conditional Logic

```dax
-- SWITCH replaces nested IF — much cleaner

-- Value-based SWITCH
Tier Label = 
    SWITCH(
        Customers[Tier],
        "Bronze",   "🥉 Bronze",
        "Silver",   "🥈 Silver",
        "Gold",     "🥇 Gold",
        "Platinum", "💎 Platinum",
        "Unknown"   -- Default
    )

-- SWITCH(TRUE) — condition-based (most useful pattern!)
Balance Segment = 
    SWITCH(
        TRUE(),
        Customers[Balance] >= 200000, "VIP",
        Customers[Balance] >= 100000, "Premium",
        Customers[Balance] >= 50000,  "Standard",
        Customers[Balance] >= 10000,  "Basic",
        "Entry"
    )

-- Measure that changes based on slicer
Selected Metric = 
    VAR Selection = SELECTEDVALUE(Metric_Selector[Metric], "Revenue")
    RETURN
        SWITCH(
            Selection,
            "Revenue",      [Total Revenue],
            "Transactions", [Transaction Count],
            "Customers",    [Unique Customers],
            "Avg Balance",  [Average Balance],
            BLANK()
        )
```

---

## Dynamic Segmentation

```dax
-- Customer RFM Segmentation (Recency, Frequency, Monetary)

-- Recency Score (days since last purchase)
Recency Score = 
    VAR DaysSinceLastTxn = 
        DATEDIFF(
            CALCULATE(MAX(Transactions[Date])),
            TODAY(),
            DAY
        )
    RETURN
        SWITCH(
            TRUE(),
            DaysSinceLastTxn <= 30,  5,
            DaysSinceLastTxn <= 60,  4,
            DaysSinceLastTxn <= 90,  3,
            DaysSinceLastTxn <= 180, 2,
            1
        )

-- Frequency Score (number of transactions)
Frequency Score = 
    VAR TxnCount = COUNTROWS(Transactions)
    RETURN
        SWITCH(
            TRUE(),
            TxnCount >= 20, 5,
            TxnCount >= 10, 4,
            TxnCount >= 5,  3,
            TxnCount >= 2,  2,
            1
        )

-- Monetary Score (total spend)
Monetary Score = 
    VAR TotalSpend = SUM(Transactions[Amount])
    RETURN
        SWITCH(
            TRUE(),
            TotalSpend >= 500000, 5,
            TotalSpend >= 200000, 4,
            TotalSpend >= 100000, 3,
            TotalSpend >= 50000,  2,
            1
        )

-- RFM Combined Segment
RFM Segment = 
    VAR R = [Recency Score]
    VAR F = [Frequency Score]
    VAR M = [Monetary Score]
    VAR RFM = R * 100 + F * 10 + M
    RETURN
        SWITCH(
            TRUE(),
            R >= 4 && F >= 4 && M >= 4, "Champions",
            R >= 3 && F >= 3 && M >= 3, "Loyal Customers",
            R >= 4 && F <= 2,           "New Customers",
            R <= 2 && F >= 3 && M >= 3, "At Risk",
            R <= 2 && F >= 4,           "Can't Lose Them",
            R <= 1,                      "Lost",
            "Potential Loyalists"
        )
```

---

## What-If Analysis with Parameters

```dax
-- Step 1: Create a What-If Parameter in Power BI
-- Modeling → New Parameter → Name: "Growth Rate", Min: -50, Max: 100, Step: 1

-- Step 2: Use the parameter in measures
-- Power BI auto-creates: 'Growth Rate'[Growth Rate Value]

Revenue Forecast = 
    [Total Revenue] * (1 + 'Growth Rate'[Growth Rate Value] / 100)

Forecast vs Actual = 
    [Revenue Forecast] - [Total Revenue]

-- Subscription Rate Scenario
Projected Subscribers = 
    VAR CurrentContacts = COUNTROWS(Customers)
    VAR ProjectedRate = 
        [Subscription Rate] + 'Rate Uplift'[Rate Uplift Value]
    RETURN
        ROUND(CurrentContacts * ProjectedRate / 100, 0)

-- Revenue impact of different discount rates
Net Revenue (Scenario) = 
    SUMX(
        Transactions,
        Transactions[Amount] * (1 - 'Discount Rate'[Discount Rate Value] / 100)
    )
```

---

## Dynamic Titles and Labels

```dax
-- Dynamic chart title
Chart Title = 
    VAR SelectedCity = 
        IF(
            ISFILTERED(Customers[City]),
            SELECTEDVALUE(Customers[City], "Multiple Cities"),
            "All Cities"
        )
    VAR SelectedYear = 
        IF(
            ISFILTERED('Date Table'[Year]),
            FORMAT(SELECTEDVALUE('Date Table'[Year]), "0"),
            "All Years"
        )
    RETURN
        "Revenue Analysis — " & SelectedCity & " | " & SelectedYear

-- Dynamic subtitle with period comparison
Subtitle = 
    VAR CurrentRevenue = [Total Revenue]
    VAR PrevRevenue = [Revenue SPLY]
    VAR Growth = DIVIDE(CurrentRevenue - PrevRevenue, PrevRevenue, 0)
    VAR Arrow = IF(Growth >= 0, "▲", "▼")
    VAR Color = IF(Growth >= 0, "growing", "declining")
    RETURN
        "Revenue is " & Color & " " & Arrow & 
        FORMAT(ABS(Growth) * 100, "0.0") & "% vs last year"

-- KPI card subtitle
KPI Card Subtitle = 
    VAR MTDRevenue = [Revenue MTD]
    VAR Target = [Revenue Target]
    VAR Achievement = DIVIDE(MTDRevenue, Target, 0)
    RETURN
        FORMAT(Achievement, "0.0%") & " of monthly target • " &
        FORMAT(Target - MTDRevenue, "KES #,##0") & " remaining"
```

---

## Conditional Formatting Measures

```dax
-- Traffic light color (use in conditional formatting)
KPI Color = 
    VAR Achievement = DIVIDE([Total Revenue], [Revenue Target], 0)
    RETURN
        SWITCH(
            TRUE(),
            Achievement >= 1.0,  "#27AE60",   -- Green
            Achievement >= 0.8,  "#F39C12",   -- Amber
            "#E74C3C"                          -- Red
        )

-- Heatmap intensity (0-1 scale for background color)
Heatmap Value = 
    VAR CurrentValue = [Total Revenue]
    VAR MaxValue = 
        CALCULATE([Total Revenue], ALLSELECTED(Customers[City]))
    RETURN
        DIVIDE(CurrentValue, MaxValue, 0)

-- Font color based on value
Font Color = 
    IF([MoM Growth %] >= 0, "#27AE60", "#E74C3C")

-- Icon set value (for conditional formatting)
Trend Icon = 
    VAR Growth = [YoY Growth %]
    RETURN
        IF(Growth > 5, 1,       -- Up arrow icon
        IF(Growth > -5, 0,      -- Flat icon
        -1))                    -- Down arrow icon
```

---

## Error Handling Patterns

```dax
-- Safe DIVIDE — never errors on division by zero
Safe Rate = DIVIDE([Numerator], [Denominator], 0)

-- IFERROR — catch any error
Safe Calculation = 
    IFERROR(
        CALCULATE(
            DIVIDE(SUM(Sales[Amount]), COUNTROWS(Sales)),
            Sales[Status] = "Completed"
        ),
        0
    )

-- Handle blank dates
Has Transactions = 
    NOT ISBLANK(MAX(Transactions[Date]))

-- Blank guard for measures
Revenue (No Blank) = 
    VAR Result = SUM(Sales[Amount])
    RETURN IF(ISBLANK(Result), 0, Result)

-- COALESCE — return first non-blank
Best Available Value = 
    COALESCE([Actual Revenue], [Forecast Revenue], [Budget Revenue], 0)
```

---

## Selected Value Pattern

```dax
-- Get single selected value from slicer
Selected City = SELECTEDVALUE(Customers[City])

-- With default when multiple/none selected
Selected City (Default) = 
    SELECTEDVALUE(Customers[City], "All Cities")

-- Check if something is selected
City Is Filtered = ISFILTERED(Customers[City])
Single City Selected = HASONEVALUE(Customers[City])

-- Respond to slicer selection
City Context Message = 
    IF(
        HASONEVALUE(Customers[City]),
        "Showing: " & SELECTEDVALUE(Customers[City]),
        "Showing all cities (" & 
        DISTINCTCOUNT(Customers[City]) & " selected)"
    )

-- Dynamic measure based on period slicer
Period Revenue = 
    VAR Period = SELECTEDVALUE(Period_Selector[Period], "MTD")
    RETURN
        SWITCH(
            Period,
            "MTD",   [Revenue MTD],
            "QTD",   [Revenue QTD],
            "YTD",   [Revenue YTD],
            "12M",   [Rolling 12M],
            [Total Revenue]
        )
```

---

## Real World — Executive Dashboard Measures

```dax
-- ── REVENUE MEASURES ──────────────────────────────────

Total Revenue = SUM(Transactions[Amount])

Revenue Target = SUM(Targets[Monthly_Target])

Revenue vs Target = [Total Revenue] - [Revenue Target]

Achievement % = 
    VAR Rate = DIVIDE([Total Revenue], [Revenue Target], 0)
    RETURN FORMAT(Rate, "0.0%")

-- ── CUSTOMER MEASURES ─────────────────────────────────

Active Customers = 
    CALCULATE(
        DISTINCTCOUNT(Transactions[Customer_ID]),
        DATESINPERIOD(
            'Date Table'[Date],
            LASTDATE('Date Table'[Date]),
            -90, DAY
        )
    )

New Customers = 
    VAR CurrentPeriodStart = FIRSTDATE('Date Table'[Date])
    RETURN
        CALCULATE(
            DISTINCTCOUNT(Customers[Customer_ID]),
            Customers[Joined_Date] >= CurrentPeriodStart
        )

Churned Customers = 
    VAR Active90Days = [Active Customers]
    VAR ActivePrev90Days = 
        CALCULATE(
            [Active Customers],
            DATEADD('Date Table'[Date], -90, DAY)
        )
    RETURN MAXX({0, ActivePrev90Days - Active90Days}, [Value])

-- ── SUBSCRIPTION MEASURES (Bank Marketing) ────────────

Subscription Rate = 
    VAR Subscribed = 
        CALCULATE(COUNTROWS(Customers), Customers[Subscribed] = TRUE)
    VAR Total = COUNTROWS(Customers)
    RETURN DIVIDE(Subscribed, Total, 0) * 100

Best Converting Job = 
    CALCULATE(
        FIRSTNONBLANKVALUE(
            Customers[Job],
            CALCULATE(
                DIVIDE(
                    CALCULATE(COUNTROWS(Customers), Customers[Subscribed] = TRUE),
                    COUNTROWS(Customers),
                    0
                )
            )
        ),
        TOPN(1, VALUES(Customers[Job]),
            CALCULATE(
                DIVIDE(
                    CALCULATE(COUNTROWS(Customers), Customers[Subscribed] = TRUE),
                    COUNTROWS(Customers), 0
                )
            ), DESC)
    )
```

---

## Quick Reference

```dax
-- Variables
VAR Name = expression
RETURN final_expression

-- SWITCH patterns
SWITCH(value, match1, result1, match2, result2, default)
SWITCH(TRUE(), condition1, result1, condition2, result2, default)

-- Selected value
SELECTEDVALUE(Table[Column], "default")
HASONEVALUE(Table[Column])
ISFILTERED(Table[Column])

-- Error handling
DIVIDE(num, den, alternate)
IFERROR(expression, alternate)
COALESCE(val1, val2, val3)
ISBLANK(value)

-- Conditional formatting measures
Returns hex color string: "#27AE60"
Returns 0/1/-1 for icon sets
Returns 0-1 for gradient scales
```

---

## Previous | Next
← [[04 - DAX Iterator Functions]] | → [[06 - DAX Relationships and RELATED]]
