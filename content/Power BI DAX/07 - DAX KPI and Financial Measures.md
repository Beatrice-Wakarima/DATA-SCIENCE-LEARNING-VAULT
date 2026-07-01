---
title: DAX KPI and Financial Measures
tags: [powerbi, dax, kpi, finance, business-intelligence]
created: 2026-05-20
up:: [[Power BI MOC]]
---

# 💰 DAX KPI & Financial Measures

> This note is the practical engine of your Power BI work. Every KPI, financial ratio, and business metric you'll need — built with clean, production-grade DAX patterns.

---

## Revenue KPIs

```dax
-- ── CORE REVENUE ──────────────────────────────────────

Total Revenue = SUM(Transactions[Amount])

Gross Profit = [Total Revenue] - SUM(Costs[Amount])

Gross Profit Margin % = 
    DIVIDE([Gross Profit], [Total Revenue], 0) * 100

Net Revenue = 
    SUMX(
        Transactions,
        Transactions[Amount] * (1 - Transactions[Discount_Pct])
    )

Revenue Per Transaction = 
    DIVIDE([Total Revenue], COUNTROWS(Transactions), 0)

Revenue Per Customer = 
    DIVIDE(
        [Total Revenue],
        DISTINCTCOUNT(Transactions[Customer_ID]),
        0
    )

-- ── GROWTH METRICS ────────────────────────────────────

Revenue YoY = [Total Revenue] - [Revenue SPLY]

Revenue YoY % = 
    DIVIDE([Revenue YoY], [Revenue SPLY], 0) * 100

Revenue MoM % = 
    DIVIDE(
        [Total Revenue] - [Revenue Prev Month],
        [Revenue Prev Month],
        0
    ) * 100

Revenue CAGR = 
    VAR StartRevenue = 
        CALCULATE(
            SUM(Transactions[Amount]),
            'Date Table'[Year] = MIN('Date Table'[Year])
        )
    VAR EndRevenue = 
        CALCULATE(
            SUM(Transactions[Amount]),
            'Date Table'[Year] = MAX('Date Table'[Year])
        )
    VAR Years = MAX('Date Table'[Year]) - MIN('Date Table'[Year])
    RETURN
        (POWER(DIVIDE(EndRevenue, StartRevenue, 0), 1/Years) - 1) * 100
```

---

## Customer KPIs

```dax
-- ── CUSTOMER METRICS ──────────────────────────────────

Total Customers = COUNTROWS(Customers)

Active Customers = 
    CALCULATE(
        DISTINCTCOUNT(Transactions[Customer_ID]),
        DATESINPERIOD(
            'Date Table'[Date],
            LASTDATE('Date Table'[Date]),
            -90, DAY
        )
    )

New Customers MTD = 
    CALCULATE(
        COUNTROWS(Customers),
        DATESMTD('Date Table'[Date]),
        Customers[Joined_Date] >= STARTOFMONTH(LASTDATE('Date Table'[Date]))
    )

Customer Lifetime Value (CLV) = 
    VAR AvgRevPerCustomer = 
        DIVIDE([Total Revenue], DISTINCTCOUNT(Transactions[Customer_ID]), 0)
    VAR AvgLifespanYears = 
        AVERAGEX(
            VALUES(Customers[Customer_ID]),
            DATEDIFF(
                CALCULATE(MIN(Transactions[Date])),
                CALCULATE(MAX(Transactions[Date])),
                YEAR
            ) + 1
        )
    RETURN AvgRevPerCustomer * AvgLifespanYears

Customer Acquisition Cost (CAC) = 
    DIVIDE(
        SUM(Marketing[Spend]),
        [New Customers MTD],
        0
    )

CLV to CAC Ratio = 
    DIVIDE([Customer Lifetime Value (CLV)], [Customer Acquisition Cost (CAC)], 0)

-- Churn Rate
Churned Customers = 
    VAR ActiveThis = [Active Customers]
    VAR ActiveLast = 
        CALCULATE(
            [Active Customers],
            DATEADD('Date Table'[Date], -1, MONTH)
        )
    RETURN MAXX({0, ActiveLast - ActiveThis}, [Value])

Churn Rate % = 
    DIVIDE([Churned Customers], [Active Customers], 0) * 100

Net Promoter Impact = 
    [Total Revenue] * (1 - [Churn Rate %] / 100)
```

---

## Campaign & Conversion KPIs

```dax
-- ── BANK MARKETING CAMPAIGN METRICS ──────────────────

Total Contacts = COUNTROWS(Customers)

Subscriptions = 
    CALCULATE(
        COUNTROWS(Customers),
        Customers[Subscribed] = TRUE
    )

Non-Subscriptions = [Total Contacts] - [Subscriptions]

Conversion Rate % = 
    DIVIDE([Subscriptions], [Total Contacts], 0) * 100

Conversion Rate vs Benchmark = 
    [Conversion Rate %] - 11.5    -- Industry benchmark 11.5%

Cost Per Contact = 
    DIVIDE(SUM(Campaign[Total_Cost]), [Total Contacts], 0)

Cost Per Subscription = 
    DIVIDE(SUM(Campaign[Total_Cost]), [Subscriptions], 0)

Revenue Per Subscription = 
    DIVIDE([Total Revenue], [Subscriptions], 0)

Campaign ROI % = 
    VAR Revenue = [Subscriptions] * 5000        -- Avg subscription value
    VAR Cost = SUM(Campaign[Total_Cost])
    RETURN DIVIDE(Revenue - Cost, Cost, 0) * 100

Best Channel = 
    VAR BestContact = 
        TOPN(
            1,
            VALUES(Customers[Contact]),
            [Conversion Rate %],
            DESC
        )
    RETURN MAXX(BestContact, Customers[Contact])
```

---

## Balance & Portfolio KPIs

```dax
-- ── PORTFOLIO METRICS ─────────────────────────────────

Total Portfolio Value = SUM(Customers[Balance])

Average Balance = AVERAGE(Customers[Balance])

Median Balance = 
    PERCENTILE.INC(Customers[Balance], 0.5)

Balance Concentration (Top 20% share) = 
    VAR Top20Pct = 
        CALCULATE(
            SUM(Customers[Balance]),
            TOPN(
                ROUNDUP(COUNTROWS(Customers) * 0.2, 0),
                Customers,
                Customers[Balance],
                DESC
            )
        )
    RETURN DIVIDE(Top20Pct, [Total Portfolio Value], 0) * 100

Portfolio Growth = 
    [Total Portfolio Value] - 
    CALCULATE(
        SUM(Customers[Balance]),
        SAMEPERIODLASTYEAR('Date Table'[Date])
    )

At-Risk Portfolio = 
    CALCULATE(
        SUM(Customers[Balance]),
        Customers[Balance] < 1000,
        Customers[Is_Active] = FALSE
    )
```

---

## Operational KPIs

```dax
-- ── EFFICIENCY METRICS ────────────────────────────────

Avg Call Duration (mins) = 
    DIVIDE(AVERAGE(Customers[Call_Duration_Secs]), 60, 0)

Total Call Time (hours) = 
    DIVIDE(SUM(Customers[Call_Duration_Secs]), 3600, 0)

Revenue Per Call Minute = 
    DIVIDE(
        [Total Revenue],
        DIVIDE(SUM(Customers[Call_Duration_Secs]), 60, 0),
        0
    )

Contacts Per Day = 
    DIVIDE(
        [Total Contacts],
        DISTINCTCOUNT('Date Table'[Date]),
        0
    )

-- Efficiency score
Agent Efficiency Score = 
    VAR ConversionWeight = [Conversion Rate %] * 0.6
    VAR DurationWeight = 
        IF(
            [Avg Call Duration (mins)] <= 5,
            40,
            MAXX({0, 40 - ([Avg Call Duration (mins)] - 5) * 4}, [Value])
        )
    RETURN ConversionWeight + DurationWeight
```

---

## Financial Ratios

```dax
-- ── FINANCIAL ANALYSIS ────────────────────────────────

Return on Investment (ROI) = 
    DIVIDE(
        [Gross Profit],
        SUM(Costs[Investment]),
        0
    ) * 100

Payback Period (months) = 
    DIVIDE(
        SUM(Costs[Investment]),
        [Gross Profit] / 12,
        0
    )

Break-Even Volume = 
    DIVIDE(
        SUM(Costs[Fixed_Costs]),
        [Revenue Per Transaction] - AVERAGE(Costs[Variable_Cost_Per_Unit]),
        0
    )

Operating Leverage = 
    DIVIDE(
        [Gross Profit Margin %],
        [Net Profit Margin %],
        0
    )

-- Budget variance
Budget Variance = [Total Revenue] - [Budget Revenue]

Budget Variance % = 
    DIVIDE([Budget Variance], [Budget Revenue], 0) * 100

Forecast Accuracy % = 
    100 - ABS([Budget Variance %])
```

---

## Composite KPI Cards

```dax
-- ── COMPOSITE MEASURES FOR CARDS ──────────────────────

-- Health Score (0-100)
Business Health Score = 
    VAR ConversionScore = 
        DIVIDE([Conversion Rate %], 20, 0) * 25    -- Max 25 points
    VAR GrowthScore = 
        IF([Revenue YoY %] > 0,
            MIN(25, [Revenue YoY %]),
            0)                                      -- Max 25 points
    VAR RetentionScore = 
        (1 - [Churn Rate %] / 100) * 25            -- Max 25 points
    VAR PortfolioScore = 
        MIN(25, [Average Balance] / 10000)          -- Max 25 points
    RETURN
        ConversionScore + GrowthScore + RetentionScore + PortfolioScore

-- Executive Summary Line
Executive Summary = 
    VAR Revenue = FORMAT([Total Revenue], "KES #,##0")
    VAR Growth = FORMAT([Revenue YoY %], "+0.0;-0.0") & "%"
    VAR Customers = FORMAT([Active Customers], "#,##0")
    VAR ConvRate = FORMAT([Conversion Rate %], "0.0") & "%"
    RETURN
        Revenue & " revenue (" & Growth & " YoY) | " &
        Customers & " active customers | " &
        ConvRate & " conversion rate"

-- KPI Status
KPI Status = 
    VAR Achievement = DIVIDE([Total Revenue], [Revenue Target], 0)
    RETURN
        SWITCH(
            TRUE(),
            Achievement >= 1.10, "🚀 Exceptional",
            Achievement >= 1.00, "✅ On Target",
            Achievement >= 0.90, "⚠️ Near Target",
            Achievement >= 0.75, "🔴 Below Target",
            "🚨 Critical"
        )
```

---

## Dashboard Measure Table

```
Organise all measures in a dedicated hidden table:

Create an empty table: _Measures
Move all measures there
Hide the table from Report view (keep in model)

Benefits:
  ✅ All measures in one place
  ✅ Cleaner field list
  ✅ Easier maintenance
  ✅ No confusion with data tables
```

---

## Quick Reference — KPI Formulas

```dax
-- Revenue
Total Revenue = SUM(Table[Amount])
YoY Growth % = DIVIDE([Rev] - [Rev SPLY], [Rev SPLY], 0) * 100
MoM Growth % = DIVIDE([Rev] - [Rev Prev Month], [Rev Prev Month], 0) * 100

-- Customers
Active = CALCULATE(DISTINCTCOUNT(Txn[CustID]), last 90 days)
CLV = Avg Revenue Per Customer × Avg Lifespan
Churn Rate % = Churned / Active * 100

-- Campaign
Conversion % = DIVIDE(Subscribed, Total, 0) * 100
ROI % = DIVIDE(Revenue - Cost, Cost, 0) * 100
Cost Per Conversion = DIVIDE(Total Cost, Conversions, 0)

-- Portfolio
Total Portfolio = SUM(Customers[Balance])
Concentration = Top 20% Balance / Total * 100

-- Financial
Gross Margin % = DIVIDE(Gross Profit, Revenue, 0) * 100
ROI = DIVIDE(Profit, Investment, 0) * 100
Budget Variance % = DIVIDE(Actual - Budget, Budget, 0) * 100
```

---

## Previous | Next
← [[06 - DAX Relationships and RELATED]] | → [[08 - DAX for Executive Dashboards]]
