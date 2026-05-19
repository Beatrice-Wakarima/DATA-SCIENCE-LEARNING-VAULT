## What is DAX?

DAX or Data Analysis Expressions drive all the calculations you can perform in Power BI. DAX formulas are versatile, dynamic, and very powerful – they allow you to create new fields and tables in your model. DAX is a formula language used in Power BI, Power Pivot, and SSAS Tabular models

DAX formulas are made up of 3 core components, and this tutorial will cover each of these:

- **Syntax** – Proper DAX syntax is made up of a variety of elements, some of which are common to all formulas.
- **Functions** – DAX functions are predefined formulas that take some parameters and perform a specific calculation.
- **Context** – DAX uses context to determine which rows should be used to perform a calculation.

## Why is DAX Important in Power BI?

DAX formulas allow you to [get the most out of your data and Power BI](https://www.datacamp.com/learn/power-bi) to solve business problems efficiently.

You can perform simple calculations (such as a simple sum or average) and create most visuals without touching DAX. For example, if you wanted to create a simple chart showing total profit, you could drag the profit field onto the _Values_ section of the chart, and it would perform a sum of the rows in that field. However, there are two cases where it would be better to create a DAX formula:

1. If you wanted to re-use a formula in multiple places, such as in multiple charts or as an expression in other DAX formulas. In this case, using a DAX formula would make your report more efficient and easier to change in the future since you would only need to change a single formula rather than changing many individual formulas in each place they are used.
2. If you wanted to create complex or customized formulas where just a simple `SUM` or `AVERAGE` would not be sufficient for the business problem you were trying to solve.

## Where are DAX Formulas Used in Power BI?

There are three ways you can use DAX formulas in Power BI:

1. **Calculated Tables** - These calculations will add an additional table to the report based on a formula. 
2. **Calculated Columns** - These calculations will add an additional column to a table based on a formula. These columns are treated like any other field in the table.
3. **Measures** - These calculations will add a summary or aggregated measure to a table based on a formula. 

The main difference between these three calculation types is their context (more on this later) and the outputs they produce. 

To add any one of these types of calculations to a model, navigate to the _Modeling_ tab of the ribbon. Here, you will find three choices for adding a new measure, calculated column, or table. Alternatively, you can right-click a table in the _Fields_ pane and get the option to add a new measure or calculated column in the drop-down menu. 

![Power BI Drop-down Menu](https://images.datacamp.com/image/upload/v1650528217/image3_b0e06e0339.png)

## How to Write a DAX Formula

DAX formulas are intuitive and easy to read. This makes it easy to understand the basics of DAX so you can start writing your own formulas relatively quickly. Let’s go over the building blocks of proper DAX syntax. 

![Dax Formula Composition Infographic](https://images.datacamp.com/image/upload/v1650528217/image1_668ee17b1b.png)

1. The name of the measure or calculated column
2. The equal-to operator (“=”) indicates the start of the formula
3. A DAX function
4. Opening (and closing) parentheses (“()”)
5. Column and/or table references
6. Note that each subsequent parameter in a function is separated by a comma (“,”)

DAX functions can also be nested inside each other to perform multiple operations efficiently. This can save a lot of time when writing DAX formulas. For example, it is often useful to have multiple nested `IF` statements or to use the `IFERROR` function to wrap around another function so that any errors in the formula are represented by the value you specify. 

Some of the most common DAX functions used in reports are:

1. Simple calculations: `COUNT`, `DISTINCTCOUNT`, `SUM`, `AVERAGE`, `MIN`, `MAX`.
2. `SUMMARISE`: Returns a table typically used to further apply aggregations over different groupings.
3. `CALCULATE`: Performs an aggregation along with one or more filters. When you specify more than one filter, the function will perform the calculation where all filters are _true_.
4. `IF`: Based on a logical condition, it will return a different value if it is _true_ or _false_. This is similar to the `CASE WHEN` operation in SQL.
5. `IFERROR`: Looks for any errors for an inner function and returns a specified result
6. `ISBLANK`: This function checks if the rows in a column are blank and returns true or false. It is useful in conjunction with other functions like IF.
7. `EOMONTH`: Returns the last day of the month of a given date (column reference in a date format) for as many months in the past or the future.
8. `DATEDIFF`: returns the difference between two dates (both as column references in date formats) in days, months, quarters, years, etc.

## Understanding Context in DAX Formulas

DAX formulas in Power BI are dynamic and change according to the context in which they were created. It’s important to understand how contexts work in DAX, as it can help save you a lot of headaches when you run into confusing errors in your formulas. 

There are two main types of context in DAX: _row context_ and _filter context_.

### Row context

This refers to just “the current row” across all columns of a table and extends to all columns in related tables. This type of context lets the DAX formula know which rows to use for a specific formula.

Here is an example of a formula for a calculated column that has a row context:

`Cost Price Per Unit = financials[COGS] / financials[Units Sold]`

![Power BI Calculated Column Screen Shot](https://images.datacamp.com/image/upload/v1650528217/image2_6394427663.png)

In this example, the `Cost Price Per Unit` is calculated on a row-by-row basis. This means that DAX needs to know the current row as it proceeds through the dataset, making the calculation and populating the new column with the result.

Row context is implicit in calculated columns. This is because the calculations performed in calculated columns are done on a row-by-row basis; thus, the row context is defined by default. However, this is not the case in measures since the aggregations are applied for all rows in a table. These calculations do not need to have any knowledge of a current row since all rows are aggregated together. 

As an example of a measure, consider the following DAX formula:

`Profit margin = SUM ( financials[Profit] ) / SUM ( financials[Sales] )`

In this case, the entire `Profit` column is summed to produce a single number, and this is divided by the sum of the entire `Sales` column. DAX does not need to know the current row since it performs an aggregation. Thus, this measure has no row context.

To explicitly define a row context in a measure, you need to use a special function called an iterator. Examples of iterator functions are `SUMX`, `AVERAGEX`, and `COUNTX`. These functions will first perform a calculation on a row-by-row basis and then perform the final aggregation on the result (i.e., sum, average, count, etc.). In this way, the row context is defined explicitly by using these iterators.

Let’s take a look at an example of an iterator function in action:

`Average Cost Per Unit = AVERAGEX ( financials, financials[COGS] / financials[Units Sold] )`

This example performs two calculations: first, the expression is evaluated on a row-by-row basis, and then the result is applied to the `AVERAGE` function. An alternative way of reaching this same result is to first create the calculated column `Cost Price Per Unit` as we did above and then create a separate `AVERAGE` measure for that column. However, knowing when to use these iterator functions can make your reports more efficient and use less memory, as you can effectively perform two calculations using just a single formula.

### Filter context 

Filter context is applied on top of a row context and refers to a subset of rows or columns that are specified as filters in the report. Filters can be applied in a few ways:

- Directly in a DAX formula
- Using the filters pane
- Using a slicer visual
- Through the fields that make up a visual (such as the rows and columns in a matrix)

A good example of adding a filter context to a `DAX` formula is using the `CALCULATE` function, which allows you to add one or more filter parameters to the measure. In the example below, we create a profit margin measure filtered for the USA only:

`USA Profit Margin = CALCULATE ( SUM ( financials[Profit] ) / SUM ( financials[Sales] ),  financials[Country] = "United States of America")`

## Common Challenges and Beginner Mistakes in DAX

When learning DAX, beginners often encounter common pitfalls that can make understanding and debugging formulas more challenging. Here are some of the issues and tips to address them:

**1. Confusing row and filter contexts**: Many beginners struggle with distinguishing between row and filter contexts. Remember that row context refers to operations performed row-by-row (e.g., calculated columns). In contrast, filter context applies additional filters to calculations (e.g., slicers or filters in a report). **Tip**: Use iterator functions like `SUMX` or `AVERAGEX` to explicitly define row contexts in measures.

**2. Overusing calculated columns**: While calculated columns are useful, they can often be replaced by measures, which are more memory-efficient and dynamic. Creating unnecessary calculated columns can bloat your data model. **Tip**: Use measures whenever possible, as they are calculated on the fly, and do not permanently increase the size of your data model.

**3. Neglecting proper naming conventions**: Poorly named measures or calculated columns can quickly become confusing in complex reports. **Tip**: Adopt consistent and descriptive naming conventions to organize your DAX formulas.

**4. Ignoring performance optimization**: DAX formulas can become slow with large datasets if not optimized. Overcomplicated formulas or excessive use of nested functions may lead to performance issues. **Tip**: Use tools like DAX Studio to analyze and optimize your formulas, and consider simplifying calculations where possible.

## Best Practices for Optimizing DAX Formulas

To improve the performance of DAX formulas, especially in large datasets, follow these best practices:

|Best practice|Description|
|---|---|
|Use measures over calculated columns|Measures are dynamic and calculated on demand, consuming less memory than calculated columns.|
|Avoid nested iterations|Minimize the use of complex nested functions (e.g., `SUMX`, `AVERAGEX`) to prevent performance bottlenecks.|
|Filter early|Apply filters at the data source or in DAX formulas to reduce the number of rows processed.|
|Leverage variables|Use VAR to store intermediate results and avoid redundant calculations within a formula.|
|Simplify relationships|Ensure the data model has clear relationships and appropriately indexed tables for faster processing.|
|Optimize cardinality|Reduce the number of unique values in columns used for filtering or joining to enhance performance.|
up:: [[Power BI MOC]]
