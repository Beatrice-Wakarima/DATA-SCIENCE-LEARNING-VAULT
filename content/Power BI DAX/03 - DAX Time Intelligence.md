---
title: DAX Time Intelligence
tags: [powerbi, dax, time-intelligence, dates]
created: 2026-05-20
up:: [[Power BI MOC]]
---

# 📅 DAX Time Intelligence

> Time intelligence is DAX's superpower. With a proper date table, you can compare periods, calculate running totals, show growth rates, and build any date-based KPI your stakeholders need.

---

## The Date Table — Non-Negotiable

```
Time intelligence functions REQUIRE a dedicated date table.
Without it, functions like SAMEPERIODLASTYEAR won't work.

Rules for a date table:
  ✅ One row per calendar day
  ✅ No missing dates
  ✅ Marked as a Date Table in Power BI
  ✅ Covers the full range of your data
```

---

## Create a Date Table in DAX

```dax
Date Table = 
ADDCOLUMNS(
    CALENDAR(DATE(2020, 1, 1), DATE(2030, 12, 31)),
    "Year",             YEAR([Date]),
    "Month Number",     MONTH([Date]),
    "Month Name",       FORMAT([Date], "MMMM"),
    "Month Short",      FORMAT([Date], "MMM"),
    "Quarter",          "Q" & ROUNDUP(MONTH([Date]) / 3, 0),
    "Quarter Number",   ROUNDUP(MONTH([Date]) / 3, 0),
    "Week Number",      WEEKNUM([Date], 2),
    "Day of Week",      WEEKDAY([Date], 2),
    "Day Name",         FORMAT([Date], "dddd"),
    "Day Short",        FORMAT([Date], "ddd"),
    "Is Weekend",       IF(WEEKDAY([Date], 2) >= 6, TRUE, FALSE),
    "Year-Month",       FORMAT([Date], "YYYY-MM"),
    "Year-Quarter",     YEAR([Date]) & " Q" & ROUNDUP(MONTH([Date])/3,0),
    "Month-Year",       FORMAT([Date], "MMM YYYY"),
    "Day of Month",     DAY([Date]),
    "Day of Year",      DATEDIFF(DATE(YEAR([Date]),1,1), [Date], DAY) + 1,
    "Is Current Month", IF(
                            YEAR([Date]) = YEAR(TODAY()) &&
                            MONTH([Date]) = MONTH(TODAY()),
                            TRUE, FALSE
                        ),
    "Is Current Year",  IF(YEAR([Date]) = YEAR(TODAY()), TRUE, FALSE),
    "Fiscal Year",      IF(MONTH([Date]) >= 7,
                            YEAR([Date]) + 1,
                            YEAR([Date])),
    "Fiscal Quarter",   SWITCH(
                            ROUNDUP(MOD(MONTH([Date]) - 7 + 12, 12) / 3, 0),
                            0, 4,
                            ROUNDUP(MOD(MONTH([Date]) - 7 + 12, 12) / 3, 0)
                        )
)
```

```dax
-- Mark as Date Table in Power BI:
-- Right-click table → Mark as Date Table → Select the Date column
```

---

## Year-to-Date (YTD)

```dax
-- Revenue YTD
Revenue YTD = 
    TOTALYTD(
        SUM(Transactions[Amount]),
        'Date Table'[Date]
    )

-- Manual approach (more control)
Revenue YTD Manual = 
    CALCULATE(
        SUM(Transactions[Amount]),
        DATESYTD('Date Table'[Date])
    )

-- With custom year end (e.g. fiscal year ends June 30)
Revenue FYTD = 
    TOTALYTD(
        SUM(Transactions[Amount]),
        'Date Table'[Date],
        "06-30"             -- Fiscal year end date
    )

-- Previous Year YTD (for comparison)
Revenue PYTD = 
    CALCULATE(
        [Revenue YTD],
        SAMEPERIODLASTYEAR('Date Table'[Date])
    )

-- YTD Growth
YTD Growth % = 
    DIVIDE(
        [Revenue YTD] - [Revenue PYTD],
        [Revenue PYTD],
        0
    ) * 100
```

---

## Quarter-to-Date and Month-to-Date

```dax
-- Quarter to Date
Revenue QTD = 
    TOTALQTD(
        SUM(Transactions[Amount]),
        'Date Table'[Date]
    )

-- Month to Date
Revenue MTD = 
    TOTALMTD(
        SUM(Transactions[Amount]),
        'Date Table'[Date]
    )

-- Previous Month to Date
Revenue PMTD = 
    CALCULATE(
        [Revenue MTD],
        DATEADD('Date Table'[Date], -1, MONTH)
    )

-- MTD vs PMTD
MTD Growth % = 
    DIVIDE(
        [Revenue MTD] - [Revenue PMTD],
        [Revenue PMTD],
        0
    ) * 100
```

---

## Same Period Last Year (SPLY)

```dax
-- Revenue same period last year
Revenue SPLY = 
    CALCULATE(
        SUM(Transactions[Amount]),
        SAMEPERIODLASTYEAR('Date Table'[Date])
    )

-- Year-over-Year growth
YoY Growth = [Total Revenue] - [Revenue SPLY]

YoY Growth % = 
    DIVIDE(
        [Total Revenue] - [Revenue SPLY],
        [Revenue SPLY],
        0
    ) * 100

-- YoY Growth Label for visuals
YoY Label = 
    VAR Growth = [YoY Growth %]
    VAR Arrow = IF(Growth >= 0, "▲", "▼")
    RETURN
        Arrow & " " & FORMAT(ABS(Growth), "0.0") & "%"
```

---

## DATEADD — Shift by Any Period

```dax
-- Previous month
Revenue Prev Month = 
    CALCULATE(
        SUM(Transactions[Amount]),
        DATEADD('Date Table'[Date], -1, MONTH)
    )

-- Previous quarter
Revenue Prev Quarter = 
    CALCULATE(
        SUM(Transactions[Amount]),
        DATEADD('Date Table'[Date], -1, QUARTER)
    )

-- Same period 2 years ago
Revenue 2 Years Ago = 
    CALCULATE(
        SUM(Transactions[Amount]),
        DATEADD('Date Table'[Date], -2, YEAR)
    )

-- Next month forecast period
Next Month Revenue = 
    CALCULATE(
        SUM(Transactions[Amount]),
        DATEADD('Date Table'[Date], 1, MONTH)
    )
```

---

## Month-over-Month (MoM) Comparison

```dax
-- MoM Change
MoM Change = 
    [Total Revenue] - [Revenue Prev Month]

-- MoM %
MoM Growth % = 
    DIVIDE(
        [Total Revenue] - [Revenue Prev Month],
        [Revenue Prev Month],
        0
    ) * 100

-- Rolling 3-Month Average
Rolling 3M Avg = 
    CALCULATE(
        AVERAGEX(
            DATESINPERIOD(
                'Date Table'[Date],
                LASTDATE('Date Table'[Date]),
                -3,
                MONTH
            ),
            [Total Revenue]
        )
    )

-- Rolling 12-Month Total
Rolling 12M = 
    CALCULATE(
        SUM(Transactions[Amount]),
        DATESINPERIOD(
            'Date Table'[Date],
            LASTDATE('Date Table'[Date]),
            -12,
            MONTH
        )
    )
```

---

## Running Totals (Cumulative)

```dax
-- Cumulative Revenue (all time)
Cumulative Revenue = 
    CALCULATE(
        SUM(Transactions[Amount]),
        FILTER(
            ALL('Date Table'),
            'Date Table'[Date] <= MAX('Date Table'[Date])
        )
    )

-- Cumulative within current year only
Cumulative Revenue YTD = 
    CALCULATE(
        SUM(Transactions[Amount]),
        FILTER(
            ALL('Date Table'),
            'Date Table'[Date] <= MAX('Date Table'[Date]) &&
            'Date Table'[Year] = MAX('Date Table'[Year])
        )
    )
```

---

## Last N Days / Weeks / Months

```dax
-- Last 30 days
Revenue Last 30 Days = 
    CALCULATE(
        SUM(Transactions[Amount]),
        DATESINPERIOD(
            'Date Table'[Date],
            TODAY(),
            -30,
            DAY
        )
    )

-- Last 7 days
Revenue Last 7 Days = 
    CALCULATE(
        SUM(Transactions[Amount]),
        LASTDATE('Date Table'[Date]) - 6 <= 'Date Table'[Date]
    )

-- Last 12 months
Revenue Last 12M = 
    CALCULATE(
        SUM(Transactions[Amount]),
        DATESINPERIOD(
            'Date Table'[Date],
            LASTDATE('Date Table'[Date]),
            -12,
            MONTH
        )
    )
```

---

## Dynamic Period Labels

```dax
-- Show "Current Month" or actual month name
Period Label = 
    IF(
        MAX('Date Table'[Is Current Month]),
        "Current Month (" & FORMAT(TODAY(), "MMM YYYY") & ")",
        MAX('Date Table'[Month-Year])
    )

-- Days remaining in month
Days Remaining in Month = 
    EOMONTH(TODAY(), 0) - TODAY()

-- Days since last transaction
Days Since Last Transaction = 
    DATEDIFF(
        MAX(Transactions[Date]),
        TODAY(),
        DAY
    )
```

---

## Real World — Bank Marketing Time Analysis

```dax
-- Monthly subscription count
Monthly Subscriptions = 
    CALCULATE(
        COUNTROWS(Customers),
        Customers[Subscribed] = TRUE
    )

-- YTD subscriptions
Subscriptions YTD = 
    TOTALYTD(
        CALCULATE(COUNTROWS(Customers), Customers[Subscribed] = TRUE),
        'Date Table'[Date]
    )

-- Subscription rate this month vs last month
Subscription Rate = 
    DIVIDE(
        CALCULATE(COUNTROWS(Customers), Customers[Subscribed] = TRUE),
        COUNTROWS(Customers),
        0
    ) * 100

Subscription Rate Prev Month = 
    CALCULATE(
        [Subscription Rate],
        DATEADD('Date Table'[Date], -1, MONTH)
    )

Subscription Rate Change = 
    [Subscription Rate] - [Subscription Rate Prev Month]

-- Campaign call duration trends
Avg Call Duration MTD = 
    TOTALMTD(
        AVERAGE(Customers[Call_Duration_Secs]),
        'Date Table'[Date]
    )
```

---

## Time Intelligence Quick Reference

```dax
-- YTD / QTD / MTD
TOTALYTD(expr, dates)
TOTALQTD(expr, dates)
TOTALMTD(expr, dates)
DATESYTD(dates)
DATESQTD(dates)
DATESMTD(dates)

-- Period shift
SAMEPERIODLASTYEAR(dates)
DATEADD(dates, n, period)        -- n can be negative
PARALLELPERIOD(dates, n, period) -- Full period shift

-- Period ranges
DATESINPERIOD(dates, last_date, n, period)
DATESBETWEEN(dates, start, end)

-- Period helpers
FIRSTDATE(dates)
LASTDATE(dates)
STARTOFMONTH(dates)
ENDOFMONTH(dates)
STARTOFQUARTER(dates)
ENDOFQUARTER(dates)
STARTOFYEAR(dates)
ENDOFYEAR(dates)

-- Total functions
TOTALYTD(expr, dates, [filter], [year_end])
TOTALQTD(expr, dates, [filter])
TOTALMTD(expr, dates, [filter])
```

---

## Previous | Next
← [[02 - DAX CALCULATE and Filter Context]] | → [[04 - DAX Iterator Functions]]
