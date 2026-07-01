---
title: DAX Cheat Sheet and Interview Prep
tags: [powerbi, dax, cheatsheet, interview]
created: 2026-05-20
up:: [[Power BI MOC]]
---

# 🎯 DAX Cheat Sheet & Interview Prep

> Everything you need for DAX interviews and day-to-day reference. Every function, every pattern, every common question — in one place.

---

## Interview Q&A

**Q: What is DAX?**
A: Data Analysis Expressions — a formula language used in Power BI, Power Pivot, and Analysis Services to create calculated columns, measures, and tables.

**Q: What is the difference between a measure and a calculated column?**
A:
- **Measure**: calculated at query time, responds to filters, stored as a formula only, uses filter context
- **Calculated Column**: calculated at data refresh, stored as data (uses memory), uses row context, fixed value

**Q: What is filter context and row context?**
A:
- **Filter context**: which rows are visible, created by slicers/visuals/CALCULATE. Measures respond to it automatically
- **Row context**: the current row being processed, created by calculated columns and iterator functions (SUMX, AVERAGEX)

**Q: What does CALCULATE do?**
A: Evaluates an expression in a modified filter context. It is the most important DAX function — it lets you override, add, or remove filters on any calculation.

**Q: What is the difference between ALL, ALLSELECTED, and ALLEXCEPT?**
A:
- `ALL(Table)` — removes ALL filters from a table/column
- `ALLSELECTED(Table)` — removes row/column header filters but keeps slicer selections
- `ALLEXCEPT(Table, col)` — removes all filters EXCEPT the specified columns

**Q: When would you use SUMX instead of SUM?**
A: Use SUMX when the calculation requires row-by-row evaluation — for example, multiplying two columns together (`SUMX(Sales, Sales[Qty] * Sales[Price])`). Use SUM when simply summing a single column.

**Q: What is context transition?**
A: When CALCULATE is used inside an iterator (like SUMX), it converts the current row context into a filter context. This allows measures to be evaluated per row.

```dax
-- Context transition example
Revenue Per Customer = 
    SUMX(
        VALUES(Customers[ID]),
        CALCULATE(SUM(Transactions[Amount]))  -- CALCULATE causes context transition
        -- Each iteration: row context (Customer ID) → filter context
    )
```

**Q: What is a date table and why is it required?**
A: A dedicated table with one row per calendar day, marked as a Date Table in Power BI. Required for time intelligence functions like TOTALYTD, SAMEPERIODLASTYEAR, and DATEADD to work correctly.

**Q: What is the difference between RELATED and LOOKUPVALUE?**
A:
- `RELATED` — requires a formal relationship in the model, used in calculated columns
- `LOOKUPVALUE` — works without a relationship, like VLOOKUP, can match on multiple conditions

**Q: How do you handle division by zero in DAX?**
A: Use `DIVIDE(numerator, denominator, alternate_result)` — returns the alternate (default 0 or BLANK()) when denominator is zero, instead of erroring.

**Q: What is USERELATIONSHIP used for?**
A: Activates an inactive relationship for a specific calculation. Common for role-playing dimensions — e.g. a date table with relationships to both Order_Date and Ship_Date, where only one can be active at a time.

---

## Complete Function Reference

### Aggregation
```dax
SUM(Table[Column])                          -- Sum numbers
SUMX(Table, expression)                     -- Sum per row
AVERAGE(Table[Column])                      -- Average
AVERAGEX(Table, expression)                 -- Average per row
MIN(Table[Column])                          -- Minimum value
MINX(Table, expression)                     -- Min per row
MAX(Table[Column])                          -- Maximum value
MAXX(Table, expression)                     -- Max per row
COUNT(Table[Column])                        -- Count non-blank numbers
COUNTA(Table[Column])                       -- Count non-blank (any type)
COUNTROWS(Table)                            -- Count rows
COUNTBLANK(Table[Column])                   -- Count blank values
DISTINCTCOUNT(Table[Column])                -- Count unique values
COUNTX(Table, expression)                   -- Count non-blank per row
```

### Filter Functions
```dax
CALCULATE(expression, [filter1, filter2, ...])
FILTER(Table, condition)                    -- Returns filtered table
ALL(Table or Column)                        -- Remove all filters
ALLEXCEPT(Table, col1, col2)               -- Remove all except specified
ALLSELECTED(Table)                          -- Keep slicer filters only
REMOVEFILTERS(Table or Column)              -- Explicit filter removal
KEEPFILTERS(filter)                         -- Intersect with existing filter
CROSSFILTER(col1, col2, direction)          -- Override relationship direction
USERELATIONSHIP(col1, col2)                -- Activate inactive relationship
```

### Logical Functions
```dax
IF(condition, true_result, false_result)
IFERROR(expression, alternate)
SWITCH(expression, val1, res1, val2, res2, default)
SWITCH(TRUE(), cond1, res1, cond2, res2, default)
AND(cond1, cond2)     -- or &&
OR(cond1, cond2)      -- or ||
NOT(condition)
ISNULL(value)
ISBLANK(value)
ISFILTERED(column)
HASONEVALUE(column)
ISEMPTY(table)
COALESCE(val1, val2, val3)                  -- First non-blank
```

### Text Functions
```dax
CONCATENATE(text1, text2)   -- or text1 & text2
CONCAT(val1, val2, ...)
CONCATENATEX(table, expression, delimiter)
LEFT(text, n)
RIGHT(text, n)
MID(text, start, length)
LEN(text)
UPPER(text) / LOWER(text)
PROPER(text)
TRIM(text)
SUBSTITUTE(text, old, new, [instance])
REPLACE(text, start, length, new_text)
FORMAT(value, format_string)
VALUE(text)                                 -- Text to number
TEXT(value, format)                         -- Number to text
FIND(find_text, within_text, [start])
SEARCH(find_text, within_text, [start])     -- Case insensitive
CONTAINS(text, search_text)
EXACT(text1, text2)                         -- Case sensitive compare
UNICHAR(number)                             -- Unicode character
REPT(text, n)                               -- Repeat text
```

### Date & Time
```dax
TODAY()
NOW()
DATE(year, month, day)
DATEVALUE(text)
TIME(hour, minute, second)
YEAR(date) / MONTH(date) / DAY(date)
HOUR(time) / MINUTE(time) / SECOND(time)
WEEKDAY(date, return_type)
WEEKNUM(date, return_type)
EOMONTH(date, months)                       -- End of month
DATEDIFF(start, end, interval)
DATEADD(dates, n, interval)
FORMAT(date, format_string)
CALENDAR(start, end)
CALENDARAUTO()
```

### Time Intelligence
```dax
TOTALYTD(expr, dates, [filter], [year_end])
TOTALQTD(expr, dates, [filter])
TOTALMTD(expr, dates, [filter])
DATESYTD(dates, [year_end])
DATESQTD(dates)
DATESMTD(dates)
SAMEPERIODLASTYEAR(dates)
DATEADD(dates, n, interval)
PARALLELPERIOD(dates, n, interval)
DATESINPERIOD(dates, last_date, n, interval)
DATESBETWEEN(dates, start, end)
FIRSTDATE(dates) / LASTDATE(dates)
STARTOFMONTH(dates) / ENDOFMONTH(dates)
STARTOFQUARTER(dates) / ENDOFQUARTER(dates)
STARTOFYEAR(dates) / ENDOFYEAR(dates)
PREVIOUSDAY(dates) / NEXTDAY(dates)
PREVIOUSMONTH(dates) / NEXTMONTH(dates)
PREVIOUSQUARTER(dates) / NEXTQUARTER(dates)
PREVIOUSYEAR(dates) / NEXTYEAR(dates)
```

### Table Functions
```dax
FILTER(Table, condition)
ALL(Table or Column)
VALUES(Table or Column)                     -- Unique values, includes blanks
DISTINCT(Table or Column)                   -- Unique values, excludes blanks
SELECTCOLUMNS(Table, name, expression, ...)
ADDCOLUMNS(Table, name, expression, ...)
SUMMARIZE(Table, group_col, ..., name, expr)
SUMMARIZECOLUMNS(col, ..., name, expr)
GROUPBY(Table, col, name, expr)
UNION(Table1, Table2, ...)
INTERSECT(Table1, Table2)
EXCEPT(Table1, Table2)
CROSSJOIN(Table1, Table2)
GENERATE(Table1, Table2)
TOPN(n, Table, expression, order)
SAMPLE(n, Table, expression)
ROW(name, expression, ...)                  -- Single row table
DATATABLE(...)                              -- Static inline table
TREATAS(table, target_column, ...)
NATURALLEFTOUTERJOIN(Table1, Table2)
NATURALINNERJOIN(Table1, Table2)
```

### Relationship
```dax
RELATED(OtherTable[Column])
RELATEDTABLE(Table)
LOOKUPVALUE(result_col, search_col, value, [default])
USERELATIONSHIP(col1, col2)
CROSSFILTER(col1, col2, direction)
TREATAS(table, target_col)
```

### Math
```dax
DIVIDE(numerator, denominator, [alternate])
ABS(number)
ROUND(number, decimals)
ROUNDUP(number, decimals)
ROUNDDOWN(number, decimals)
CEILING(number, significance)
FLOOR(number, significance)
INT(number)
TRUNC(number, decimals)
MOD(number, divisor)
POWER(number, exponent)
SQRT(number)
EXP(number)
LOG(number, base)
LN(number)
SIGN(number)
RAND() / RANDBETWEEN(low, high)
PI()
```

### Statistical
```dax
MEDIAN(column)
MEDIANX(table, expression)
PERCENTILE.INC(column, k)
PERCENTILE.EXC(column, k)
PERCENTILEXINC(table, expression, k)
STDEV.P(column)
STDEV.S(column)
STDEVX.P(table, expression)
VAR.P(column) / VAR.S(column)
```

### Information
```dax
SELECTEDVALUE(column, [default])
HASONEVALUE(column)
HASONEFILTER(column)
ISFILTERED(column)
ISCROSSFILTERED(column)
ISEMPTY(table)
ISINSCOPE(column)
CONTAINS(table, col, value, ...)
CONTAINSROW(table, row)
EARLIER(column, [n])
EARLIEST(column)
USERNAME()
USERPRINCIPALNAME()
```

---

## Common DAX Patterns Quick Cards

```dax
-- % of Total
DIVIDE([Measure], CALCULATE([Measure], ALL(Table))) * 100

-- % of Filtered Total
DIVIDE([Measure], CALCULATE([Measure], ALLSELECTED(Table))) * 100

-- YoY Growth %
DIVIDE([Revenue] - [Revenue SPLY], [Revenue SPLY], 0) * 100

-- Running Total
CALCULATE([Measure],
    FILTER(ALL('Date Table'),
    'Date Table'[Date] <= MAX('Date Table'[Date])))

-- Top N filter
RANKX(ALL(Table[Column]), [Measure], , DESC, Dense) <= N

-- Dynamic segmentation
SWITCH(TRUE(),
    value >= threshold3, "High",
    value >= threshold2, "Medium",
    value >= threshold1, "Low",
    "Very Low")

-- Conditional color
IF([Measure] >= [Target], "#27AE60", "#E74C3C")

-- Safe period comparison
VAR Current = [Revenue]
VAR Prior = [Revenue SPLY]
RETURN IF(ISBLANK(Prior), BLANK(), DIVIDE(Current-Prior, Prior, 0)*100)

-- Customer with max value
CALCULATE(
    FIRSTNONBLANKVALUE(Table[Name], CALCULATE([Measure])),
    TOPN(1, Table, [Measure], DESC)
)
```

---

## Format Strings Reference

```dax
FORMAT(12345.678, "#,##0")           -- 12,346
FORMAT(12345.678, "#,##0.00")        -- 12,345.68
FORMAT(0.1567, "0.0%")              -- 15.7%
FORMAT(0.1567, "0.00%")             -- 15.67%
FORMAT(12345, "KES #,##0")          -- KES 12,345
FORMAT(DATE(2026,5,20), "DD/MM/YYYY") -- 20/05/2026
FORMAT(DATE(2026,5,20), "MMM YYYY")   -- May 2026
FORMAT(DATE(2026,5,20), "MMMM")       -- May
FORMAT(DATE(2026,5,20), "dddd")       -- Wednesday
FORMAT(1234567, "0.0,,M")            -- 1.2M
FORMAT(1234567890, "0.0,,,B")        -- 1.2B
```

---

## Previous | Next
← [[08 - DAX for Executive Dashboards]] | → [[Power BI MOC]]
