---
title: DAX for Executive Dashboards
tags: [powerbi, dax, dashboards, executive, advanced]
created: 2026-05-20
up:: [[Power BI MOC]]
---

# 📊 DAX for Executive Dashboards

> This note brings everything together — the complete set of DAX patterns for building production-grade executive dashboards. Every measure here is designed to be dropped directly into a real report.

---

## The Executive Dashboard Framework

```
Every executive dashboard needs these 4 layers:

1. SUMMARY    — Top-line KPIs at a glance (cards)
2. TREND      — How performance is changing over time (line charts)
3. BREAKDOWN  — Performance by dimension (bar/matrix)
4. DETAIL     — Drill-through for investigation (tables)
```

---

## Layer 1 — Summary KPIs (Card Visuals)

```dax
-- ── REVENUE CARD ──────────────────────────────────────

Card Revenue = [Total Revenue]

Card Revenue Subtitle = 
    VAR YoY = [Revenue YoY %]
    VAR Arrow = IF(YoY >= 0, "▲", "▼")
    VAR Color = IF(YoY >= 0, "vs last year", "vs last year")
    RETURN Arrow & " " & FORMAT(ABS(YoY), "0.0") & "% " & Color

-- ── TARGET ACHIEVEMENT CARD ───────────────────────────

Target Achievement = 
    FORMAT(
        DIVIDE([Total Revenue], [Revenue Target], 0) * 100,
        "0.0"
    ) & "% of target"

Card Color Revenue = 
    VAR Ach = DIVIDE([Total Revenue], [Revenue Target], 0)
    RETURN
        SWITCH(TRUE(),
            Ach >= 1.0, "#27AE60",
            Ach >= 0.9, "#F39C12",
            "#E74C3C"
        )

-- ── CUSTOMER CARD ─────────────────────────────────────

Card Active Customers = [Active Customers]

Card Customer Subtitle = 
    VAR New = [New Customers MTD]
    VAR Churned = [Churned Customers]
    RETURN
        "+" & FORMAT(New, "#,##0") & " new | " &
        "-" & FORMAT(Churned, "#,##0") & " churned"

-- ── CONVERSION CARD (Bank Marketing) ─────────────────

Card Conversion Rate = 
    FORMAT([Conversion Rate %], "0.0") & "%"

Card Conversion Subtitle = 
    VAR Vs = [Conversion Rate %] - 11.5
    VAR Arrow = IF(Vs >= 0, "▲", "▼")
    RETURN
        Arrow & " " & FORMAT(ABS(Vs), "0.0") & "pp vs benchmark (11.5%)"

-- ── PORTFOLIO CARD ────────────────────────────────────

Card Portfolio = 
    "KES " & FORMAT([Total Portfolio Value] / 1000000, "0.0") & "M"

Card Portfolio Subtitle = 
    VAR Growth = [Portfolio Growth]
    VAR Pct = DIVIDE([Portfolio Growth], 
        [Total Portfolio Value] - [Portfolio Growth], 0) * 100
    RETURN
        IF(Growth >= 0, "▲ ", "▼ ") &
        FORMAT(ABS(Pct), "0.0") & "% since last period"
```

---

## Layer 2 — Trend Measures (Line Charts)

```dax
-- ── MULTI-METRIC TREND (use with field parameter) ─────

Selected Trend Metric = 
    VAR Selection = 
        SELECTEDVALUE(Metric_Selector[Metric_Name], "Revenue")
    RETURN
        SWITCH(
            Selection,
            "Revenue",          [Total Revenue],
            "Transactions",     [Transaction Count],
            "Active Customers", [Active Customers],
            "Conversion Rate",  [Conversion Rate %],
            "Avg Balance",      [Average Balance],
            [Total Revenue]
        )

-- ── ROLLING AVERAGES ──────────────────────────────────

Revenue 3M Rolling Avg = 
    CALCULATE(
        AVERAGEX(
            DATESINPERIOD(
                'Date Table'[Date],
                LASTDATE('Date Table'[Date]),
                -3, MONTH
            ),
            [Total Revenue]
        )
    )

Revenue 12M Rolling = 
    CALCULATE(
        SUM(Transactions[Amount]),
        DATESINPERIOD(
            'Date Table'[Date],
            LASTDATE('Date Table'[Date]),
            -12, MONTH
        )
    )

-- ── FORECAST LINE ─────────────────────────────────────

Revenue Forecast = 
    VAR CurrentMonth = MAX('Date Table'[Month Number])
    VAR CurrentYear = MAX('Date Table'[Year])
    VAR IsCurrentOrFuture = 
        (CurrentYear = YEAR(TODAY()) && CurrentMonth >= MONTH(TODAY())) ||
        CurrentYear > YEAR(TODAY())
    VAR HistoricalAvg = 
        CALCULATE(
            AVERAGE(Monthly_Revenue[Revenue]),
            FILTER(
                Monthly_Revenue,
                Monthly_Revenue[Year] < YEAR(TODAY())
            )
        )
    VAR GrowthFactor = 1 + [Revenue YoY %] / 100
    RETURN
        IF(IsCurrentOrFuture, HistoricalAvg * GrowthFactor, BLANK())

-- Show actual only for past, forecast for future
Revenue Actual or Forecast = 
    IF(
        MAX('Date Table'[Date]) <= TODAY(),
        [Total Revenue],
        [Revenue Forecast]
    )
```

---

## Layer 3 — Breakdown Measures (Bar/Matrix)

```dax
-- ── CONTRIBUTION TO TOTAL ─────────────────────────────

Revenue Share % = 
    DIVIDE(
        [Total Revenue],
        CALCULATE([Total Revenue], ALLSELECTED(Customers[City])),
        0
    ) * 100

-- ── SEGMENT COMPARISON ────────────────────────────────

Above Average Revenue Flag = 
    VAR OverallAvg = 
        CALCULATE([Total Revenue], ALL(Customers[Tier]))
    RETURN
        IF([Total Revenue] > OverallAvg, "Above Average", "Below Average")

-- ── WATERFALL CHART MEASURES ──────────────────────────

Waterfall Base = 
    CALCULATE(
        SUM(Transactions[Amount]),
        'Date Table'[Year] = YEAR(TODAY()) - 1
    )

Waterfall Change = [Total Revenue] - [Waterfall Base]

Waterfall End = 
    [Waterfall Base] + [Waterfall Change]

-- ── PARETO (80/20) ────────────────────────────────────

Cumulative Revenue % = 
    VAR CurrentCustomerRevenue = [Total Revenue]
    VAR TotalRevenue = CALCULATE([Total Revenue], ALL(Customers))
    VAR CustomersWithLessRevenue = 
        CALCULATE(
            SUM(Customers[Customer_Revenue]),
            FILTER(
                ALL(Customers),
                [Total Revenue] >= CurrentCustomerRevenue
            )
        )
    RETURN
        DIVIDE(CustomersWithLessRevenue, TotalRevenue, 0) * 100

Pareto Label = 
    IF(
        [Cumulative Revenue %] <= 80,
        "Top 80% Revenue",
        "Remaining 20%"
    )
```

---

## Layer 4 — Detail Drill-Through

```dax
-- ── DRILL-THROUGH MEASURES ────────────────────────────

-- Full customer summary for drill-through page
Customer Detail - Transactions = 
    CALCULATE(COUNTROWS(Transactions))

Customer Detail - Revenue = 
    CALCULATE(SUM(Transactions[Amount]))

Customer Detail - Last Activity = 
    FORMAT(
        CALCULATE(MAX(Transactions[Date])),
        "DD MMM YYYY"
    )

Customer Detail - Days Inactive = 
    DATEDIFF(
        CALCULATE(MAX(Transactions[Date])),
        TODAY(),
        DAY
    )

Customer Detail - Risk Level = 
    VAR DaysInactive = [Customer Detail - Days Inactive]
    VAR Balance = MAX(Customers[Balance])
    RETURN
        SWITCH(
            TRUE(),
            DaysInactive > 180 && Balance < 10000, "🔴 High Risk",
            DaysInactive > 90,                      "🟡 Medium Risk",
            "🟢 Low Risk"
        )
```

---

## Complete Bank Marketing Dashboard

```dax
-- ── HOMEPAGE METRICS ──────────────────────────────────

-- Total Contacts KPI
KPI Total Contacts = 
    FORMAT(COUNTROWS(Customers), "#,##0")

-- Conversion Rate KPI  
KPI Conversion Rate = 
    FORMAT([Conversion Rate %], "0.0") & "%"

-- Best Performing Job
KPI Best Job = 
    VAR TopJob = 
        TOPN(1, VALUES(Customers[Job]), [Conversion Rate %], DESC)
    RETURN MAXX(TopJob, Customers[Job])

-- Best Performing Month
KPI Best Month = 
    VAR BestM = 
        TOPN(1, VALUES(Customers[Month]), [Conversion Rate %], DESC)
    RETURN MAXX(BestM, Customers[Month])

-- Campaign Efficiency
KPI Efficiency = 
    FORMAT(
        DIVIDE(
            [Total Revenue],
            DIVIDE(SUM(Customers[Call_Duration_Secs]), 3600, 0),
            0
        ),
        "KES #,##0"
    ) & " per hour of calls"

-- ── TREND ANALYSIS ────────────────────────────────────

Monthly Subscription Trend = 
    CALCULATE(
        DIVIDE(
            CALCULATE(COUNTROWS(Customers), Customers[Subscribed] = TRUE),
            COUNTROWS(Customers),
            0
        ) * 100
    )

3M Subscription Trend = 
    CALCULATE(
        AVERAGEX(
            DATESINPERIOD(
                'Date Table'[Date],
                LASTDATE('Date Table'[Date]),
                -3, MONTH
            ),
            [Monthly Subscription Trend]
        )
    )

-- ── SEGMENT ANALYSIS ──────────────────────────────────

Balance Segment Conversion = 
    VAR SegmentTotal = COUNTROWS(Customers)
    VAR SegmentSubscribed = 
        CALCULATE(COUNTROWS(Customers), Customers[Subscribed] = TRUE)
    RETURN
        DIVIDE(SegmentSubscribed, SegmentTotal, 0) * 100

Job Tier Index = 
    DIVIDE(
        [Conversion Rate %],
        CALCULATE([Conversion Rate %], ALL(Customers[Job])),
        0
    )
    -- > 1.0 = above average, < 1.0 = below average

-- ── TOOLTIPS ──────────────────────────────────────────

Tooltip Details = 
    VAR Contacts = COUNTROWS(Customers)
    VAR Subscribed = 
        CALCULATE(COUNTROWS(Customers), Customers[Subscribed] = TRUE)
    VAR Rate = DIVIDE(Subscribed, Contacts, 0) * 100
    VAR AvgBalance = FORMAT(AVERAGE(Customers[Balance]), "KES #,##0")
    VAR AvgDuration = FORMAT(
        DIVIDE(AVERAGE(Customers[Call_Duration_Secs]), 60, 0),
        "0.0"
    ) & " mins"
    RETURN
        "Contacts: " & FORMAT(Contacts, "#,##0") & UNICHAR(10) &
        "Subscribed: " & FORMAT(Subscribed, "#,##0") & UNICHAR(10) &
        "Rate: " & FORMAT(Rate, "0.0") & "%" & UNICHAR(10) &
        "Avg Balance: " & AvgBalance & UNICHAR(10) &
        "Avg Call: " & AvgDuration
```

---

## Performance Optimisation

```dax
-- ✅ Use variables — calculated once, referenced many times
-- ✅ Filter before iterating — FILTER(Table, condition) then SUMX
-- ✅ Avoid CALCULATE inside SUMX unless needed for context transition
-- ✅ Use DIVIDE instead of / (handles zero division)
-- ✅ Use COUNTROWS instead of COUNTX where possible
-- ✅ Avoid bidirectional relationships — use CROSSFILTER when needed
-- ✅ Measure dependencies — build simple measures, compose complex ones
-- ✅ Hide unused columns from the model (reduce memory)

-- Measure composition (build simple then compose)
Revenue = SUM(Transactions[Amount])                     -- Simple
Revenue YoY = [Revenue] - [Revenue SPLY]                -- Composed
Revenue YoY % = DIVIDE([Revenue YoY], [Revenue SPLY])   -- Composed from composed
```

---

## DAX Studio — Performance Testing

```
DAX Studio (free tool) helps you:
  - See how long measures take to execute
  - View query plans
  - Find which columns are being scanned
  - Identify slow measures before they reach production

To use:
  1. Download DAX Studio from daxstudio.org
  2. Connect to your Power BI Desktop file
  3. Run: EVALUATE {[Your Slow Measure]}
  4. Check "Server Timings" tab for performance breakdown
```

---

## Quick Reference — Dashboard Patterns

```dax
-- Card KPI
[Measure]
FORMAT([Measure], "KES #,##0")
FORMAT([Measure], "0.0") & "%"

-- Subtitle with trend
IF(Growth>=0,"▲","▼") & FORMAT(ABS(Growth),"0.0") & "%"

-- Color coding
IF(value>=target,"#27AE60","#E74C3C")
SWITCH(TRUE(), v>1, "green", v>0.8, "amber", "red")

-- Dynamic title
"Revenue — " & SELECTEDVALUE(Table[Column], "All")

-- Contribution
DIVIDE([Measure], CALCULATE([Measure], ALLSELECTED(Table)))

-- % of total
DIVIDE([Revenue], CALCULATE([Revenue], ALL(Customers[City]))) * 100

-- Ranking
RANKX(ALL(Customers[City]), [Revenue], , DESC, Dense)

-- Tooltip multiline
"Line1" & UNICHAR(10) & "Line2" & UNICHAR(10) & "Line3"
```

---

## Previous | Next
← [[07 - DAX KPI and Financial Measures]] | → [[Power BI MOC]]
