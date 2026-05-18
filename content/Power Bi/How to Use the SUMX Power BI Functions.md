## What is the SUMX Function in Power BI?

The SUMX function in Power BI is a powerful DAX function used to calculate the sum of an expression that is calculated for each row in a table. This function is important because it allows for more complex calculations than a simple sum.

Keep our [DAX cheat sheet](https://www.datacamp.com/cheat-sheet/dax-cheat-sheet) on hand for a quick reference on many of the most useful DAX functions you will encounter.

![image2.png](https://media.datacamp.com/legacy/v1706706531/image2_32a0881618.png)

The syntax of the SUMX function is

`SUMX(Table, Expression)`

- **Table:** The table or table expression over which the function iterates.
- **Expression:** The expression that is evaluated for each row of the table. This expression often involves data from columns in the table.

SUMX is particularly useful when you must perform calculations that depend on individual row values before summing up the results. For example, calculating total sales by multiplying the quantity and price for each transaction or applying different discount rates per product before summing up the total discounted sales. It offers flexibility and precision in your calculations, making it a pretty important function to learn about.

## How SUMX Works in Power BI

Here's a breakdown of how the SUMX function works under the hood:

- When SUMX is called, it iterates over the rows of the specified table one by one. For each row, it temporarily establishes a row context, which is a kind of environment where the current row’s values are directly accessible.
- In this row context, the function evaluates the expression provided in its second argument. The expression typically involves one or more other column values from the current row. As the function iterates through the table, it recalculates this expression for each row based on that row's data.
- As SUMX processes each row, it aggregates the results, keeping a running total. Power BI uses DAX's in-memory analytics engine (VertiPaq), which is optimized for calculations like this one.
- After iterating through all rows, SUMX finalizes the aggregated total, which is the sum of the individual results computed for each row. This final value is then returned as the output of the function.

### Understanding Contexts

In Power BI, context is crucial for understanding how DAX functions like SUMX operate. Context determines how the values in data models are calculated and displayed. Check out our [introduction to DAX](https://www.datacamp.com/courses/introduction-to-dax-in-power-bi) course, where we discuss [contexts](https://campus.datacamp.com/courses/introduction-to-dax-in-power-bi/context-in-dax-formulas?ex=1) in more detail. With the SUMX function, there are two main types of context to consider: row context and filter context.

#### Row context

Row context refers to the environment where DAX formulas evaluate each row of a table. When you are within a row context, you can directly reference columns of the table, and DAX formulas will use the value from the current row in calculations.

When you use SUMX, it creates and leverages row context for its operation. For each row in the specified table, SUMX evaluates the given expression in the context of that particular row.

#### Filter context

Filter context is a set of filters applied to data in a Power BI report, such as filters from visuals, slicers, and report-level filters. This context determines which data points are considered in calculations.

Although SUMX operates within row context for its row-by-row calculations, these calculations are still subject to the overall filter context of the report or visual. This means that the rows iterated by SUMX are those that meet the criteria defined by the current filter context.

#### Interaction between contexts in SUMX

When using SUMX, the function respects both the row context and the filter context. The table over which SUMX iterates is shaped by the filter context, while the calculation for each row is done in the row context.

You can use a measure within SUMX. In this case, a **context transition** occurs, where the row context is temporarily transformed into an equivalent filter context to evaluate the measure for each row.

## SUMX Best Practices

When using the SUMX function in Power BI, consider a few of these best practices:

- **Ensure your data model is well-structured** before applying SUMX. Properly defined relationships and model schema are crucial for accurate and optimized Power BI reports.
- **SUMX is not supported in DirectQuery mode** when used in calculated columns or row-level security rules.
- **Keep the expressions used within SUMX as simple and efficient** as possible. Avoid overly complex calculations that slow down performance, especially with large datasets.
- **Be mindful of context transition** and how it can affect the results of your function.
- **SUMX considers numbers only.** Blanks, logical values, and text are ignored.

## SUMX vs Other Functions

Some functions are similar to SUMX, and knowing which function to use and when can be a little confusing. Let’s break down two functions that cause the most confusion.

### SUMX vs SUM

SUM is used to calculate the sum of a column in a table and has the following syntax:

`SUM(Column)`

SUMX iterates over each row to evaluate an expression, while SUM directly aggregates values from a single column. This means that SUMX can handle more complex calculations involving multiple columns.

However, the iterative nature of SUMX makes it more resource-intensive, especially with large datasets, compared to SUM. Remember this if you’re working with a large data model, and stick to SUM for simple summations.

### SUMX vs CALCULATE

CALCULATE modifies the filter context on a calculation and is one of the most powerful functions in DAX. This is the syntax for the CALCULATE function:

`CALCULATE(Expression, Filter1, Filter2,...)`

CALCULATE is ideal for scenarios where you must perform calculations under different filter conditions than those currently applied to the report or model. On the other hand, SUMX is for row-level calculations followed by an aggregation.

In complex scenarios, we can use CALCULATE with other functions, like SUMX. For example, you might use CALCULATE to define a specific filter context within which SUMX performs its row-level calculations and aggregation.

## Implementing SUMX in Power BI: Step-by-Step Guide

Using the Power BI sample data (available when you install Power BI Desktop), we will demonstrate how to use the SUMX function and how to combine SUMX with some other useful DAX functions.

Here is a snapshot of our data showing monthly sales for different products across various segments and countries.

![image4.png](https://media.datacamp.com/legacy/v1706706654/image4_a346413d8e.png)

### Step 1: Creating a measure using SUMX

Here is a classic example of the power of SUMX. We want to use the number of units sold, the price per unit, and the value of any discounts given to calculate the total sales value.

`SUMX(Sales, (Sales[Units Sold] * Sales[Sale Price])-Sales[Discounts])`

Here is a table showing the result of our SUMX function. As you can see, total sales can also have a filter context applied–in this case, we filter by Year and Product.

![image1.png](https://media.datacamp.com/legacy/v1706706708/image1_bdd2444d98.png)

### Step 2: Applying filters to SUMX

We could use filters with the SUMX function in two ways: with FILTER or CALCULATE.

**FILTER** is used to apply specific filters to a table or expression within SUMX. It allows more granular control over the rows that SUMX iterates over.

`SUMX(FILTER(Sales, Sales[Discount Band] = "High"), Sales[Units Sold])`

**CALCULATE** modifies the filter context for the SUMX function, allowing for complex conditional aggregations.

`SUMX(Sales, CALCULATE(SUM(Sales[Units Sold]), Sales[Year] = 2020))`

### Step 3: Combining SUMX with other functions

#### ALL and ALLEXCEPT

These functions are used to remove filters from a table or all tables except specified ones. They are often used within CALCULATE and in combination with SUMX to perform calculations over an unfiltered dataset.

`SUMX(ALL(Sales), Sales[Sale Price] * Sales[Units Sold])`

#### VALUES

VALUES returns a one-column table of unique values from a column. You can combine it with SUMX for calculations that require iterating over unique values.

`SUMX(VALUES(Sales[Country]), [Total Sales])`

#### AVERAGEX, MINX, and MAXX

These are other iterative functions similar to SUMX but used to calculate average, minimum, or maximum values, respectively. They can be nested or used alongside SUMX.

`AVERAGEX(Customers, SUMX(RELATEDTABLE(Sales), Sales[Units Sold]))`

#### IF and SWITCH

Logical functions like IF and SWITCH can be used within SUMX to perform conditional calculations.

`SUMX(Sales, IF(Sales[Country] = "Mexico", Sales[Units Sold], 0))`

#### USERELATIONSHIP

USERELATIONSHIP specifies a particular relationship to be used in a calculation. It is especially useful when multiple relationships exist between tables.

`SUMX(CALCULATETABLE(Sales, USERELATIONSHIP(Date[Date], Sales[Date])), Sales[Units Sold])`