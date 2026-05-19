## What is the DAX SUMMARIZE() Function?

The DAX `SUMMARIZE()` function takes your data and groups it based on the columns you choose. Then, it calculates totals or other summaries for each group.

For example, suppose you have a big list of sales data with information about products, regions, and sales amounts. Here, you can use `SUMMARIZE()` to group all that data by product or region and see the total sales for each group. 

You'll come across DAX in several Microsoft tools, such as:

- [Power BI](https://www.datacamp.com/courses/introduction-to-power-bi) (it's super popular for business analytics)
- [Excel](https://www.datacamp.com/courses/introduction-to-excel), specifically in Power Pivot
- [SQL Server Analysis Services](https://www.datacamp.com/tracks/sql-server-developer) (SSAS) 

Once you understand `SUMMARIZE()`, you can organize your data efficiently by creating better reports and digging deeper into your data for valuable insights. So, next time you're working with a large dataset and need to make sense of it quickly, use the `SUMMARIZE()` function.

## DAX SUMMARIZE() and Data Grouping

Here’s how the `SUMMARIZE()` function creates summary tables based on specified columns and aggregations:

```none
SUMMARIZE (<table>, <groupBy_columnName>[, <groupBy_columnName>]…[, <name>, <expression>]…)
```

In the above syntax:

- `table` is the source table for your data.
    
- `groupBy_columnName` is the column(s) you want to group by.
    
- `name` is the name for your new calculated column.
    
- `expression` is the calculation you want to perform.
    

You can use `SUMMARIZE()` with any table or column in your dataset, which makes it very versatile.

### Basic grouping

Let's look at a simple example of basic grouping with `SUMMARIZE()`.

First, import the data set into Power BI. To do so, go to the Home tab > Get Data. Select the option corresponding to your saved file from the dropdown menu and load it. In this example, I have a dataset with columns for Year, Product, and SalesAmount. I’ll now import this to Power BI.

![A table in Power BI that needs to be aggregated with DAX SUMMARIZE()](https://media.datacamp.com/cms/google/ad_4nxe411oe0yvvdqsdt4ggt0rpftidnkxxt9ppdvuv2m7grnwrd1xbu9nafnxqse6xrzueqk_xoo7grbrslhxh0b3hmznafula50slosq7uo2gety62gb62xwtm2soi1pdkitgzfuuntfewwj2be9lwr0tycdv.png)

A table named sales. Image by Author.  
  

Once the data is imported, go to the Modeling tab > New table. Then, enter the following formula to group by the Year column and aggregate the Total Sales.

	`SummaryTable = 	SUMMARIZE( 	    sales, 	    sales[Year], 	    "Total Sales", SUM(sales[SalesAmount]) 	)`

[](https://app.datacamp.com/workspace)

![Formula bar in Power BI using the SUMMARIZE() function](https://media.datacamp.com/cms/google/ad_4nxebsrybnddeqaphpjkg2rzvswjgkezt-wuyoihvukctm5rj86f7kvyhjrttmikvqepo1rdxz353b6vukmm5kq1z2xagxys4t9g-6_temkclx1f1mqggc5v3rxiud-rmmuos2lli-ymt3qxial34jldkaw1s.png)

Formula bar. Image by Author.  
  

In this formula:

- `SummarizedTable` creates a new table.
    
- `SUMMARIZE(` begins grouping and summarizing data.
    
- `SalesData,` is the source table.
    
- `SalesData[Year],` groups by the Year column.
    
- `"Total Sales", SUM(SalesData[SalesAmount])` creates a new column called Total Sales that sums up SalesAmount for each year.
    

![Summarized the total sales using DAX SUMMARIZE() function in Power BI](https://media.datacamp.com/cms/google/ad_4nxcq0bw_y41kmwfjl2vfvxanqa6auo2vznr_ugl-dkmbpwqpfzdre120dyjtj-hthi6vt4ijfzb0wo0sftzaybzvwalaokhhv19jl6vj6aod6vi4ptkqn5np0efjv56hcknrey3d85xi0q4omza88unxagqp.png)

Summarized results. Image by Author.  
  

Here, the `SUMMARIZE()` function creates a summary table by grouping the data by Year and calculates the Total Sales by summing the SalesAmount for each year.

### Multiple grouping

`SUMMARIZE()` can also handle more complex groupings. Let’s understand this with an example. Here, I have a dataset here with columns for Year, Product, Region, and SalesAmount.

![Sales data table in Power BI](https://media.datacamp.com/cms/google/ad_4nxcmz0m0ryyjh6e97ymlmwtstmseuvvebh-f7lju5di0p6vjhrpndm49rubfcfeic2owgwevagnvbxmblp-5pjo61he2nojfcsfzmw6rgpksdrjcaziq7jruptk4k-fsuqjkagif1a1rfmnroljvfr5xdji.png)

A table named sales_data. Image by Author.  
  

Here, I’m grouping by Year and Region to calculate the Total Sales for each combination.

	`SummarizedTable = 	SUMMARIZE( 	    sales_data, 	    sales_data[Year], 	    sales_data[Region], 	    "Total Sales", SUM(sales_data[SalesAmount]) 	)`

[](https://app.datacamp.com/workspace)

In this formula: 

- `sales_data` is the table where your data is stored.
    
- `sales_data[Year]` is the first column to be grouped by Year.
    
- `sales_data[Region]` is the second column to be grouped by Region.
    
- `"Total Sales"` is the custom column name for the sum of sales.
    
- `SUM(SalesData[SalesAmount])` sums up the sales for each group.
    

![Using the DAX SUMMARIZE() function in Power BI](https://media.datacamp.com/cms/google/ad_4nxcsgvctbbsllq2lltpy4shskbbrqp5gnghnkzcb7q9zsmq-brscnxljvlewiufznqlraijzkpkgcwb_eswf9rbljdj4bntq9wnwpddnpwa6y2k8nawxvks5oluiaakxgpaudgt0vw7uqicqcu-z-duigtem.png)

Summarized multiple columns. Image by Author.  
  

Here, multiple grouping helped us visualize sales trends by both Region and Year. The North and East regions display growth from 2021 to 2023. The South had high sales in 2022, while the West only has data for 2022-2023. 

## Advanced Techniques with DAX SUMMARIZE()

While `SUMMARIZE()` is helpful, you can combine it with other DAX functions to try even more sophisticated data analysis capabilities. So, let's explore some examples to see how advanced techniques can leverage `SUMMARIZE()` for complex aggregations and summaries.

### Using SUMMARIZE() with ROLLUP()

The `ROLLUP()` feature within `SUMMARIZE()` adds subtotal rows to your summary tables to show subtotals across different grouping levels and provide more detailed hierarchical summaries. If you work in the finance field or any relevant analysis role, this would be particularly useful for performing multi-level aggregations.

1. Add the `ROLLUP()` keyword after your grouping columns in `SUMMARIZE()`.
    
2. Specify which columns should be included in the `ROLLUP()` calculation.
    

```none
SUMMARIZE(<table>, <groupBy_columnName>[, <groupBy_columnName>]…[, ROLLUP(<groupBy_columnName>[,< groupBy_columnName>…])][, <name>, <expression>]…)
```

For example, this dataset shows the Sales and Quantity of each Product in a particular Region. Now, I have to find the sales summary by Region and Product, with subtotals and totals.

![DAX SUMMARIZE() used with ROLLUP() in Power BI](https://media.datacamp.com/cms/google/ad_4nxfjlfzesbo7lvsqr0cfizyapw8wfjdbzg5ccbkfe-pq1arp_qczwuol_pq4-uywqeimwnlvxir0jbh5pvfsyovlpjegskai3jkqcdwhvefoa_s9tmmtfgjjhpdirahpec_yqkd-qu1va0wro2toea9ydr1w.png)

A table named sales_rollup. Image by Author.  
  

To do so, I use the following formula:

	`SalesWithRollup = 	SUMMARIZE( 	    sales_rollup, 	    ROLLUP(sales_rollup[Region], sales_rollup[Product]), 	    "Total Sales", SUM(sales_rollup[Sales]), 	    "Total Quantity", SUM(sales_rollup[Quantity]) 	)`

[](https://app.datacamp.com/workspace)

![SUMMARIZE() used with ROLLUP() in Power BI using DAX](https://media.datacamp.com/cms/google/ad_4nxcts6znntsyht7nybuxxiet5t9emg_irqd6qqa6aksc60zrtbqqmbnhbsuqo7lzseu84ok_7vktvesmy2g84cnyvpo2a1apypf5gtruyhlsjap0qnicufxlgzamkkwuo02ss8txr2-uwpyhzp6r3rxlxtmx.png)

Using the ROLLUP() function. Image by Author.  
  

You can see — here the `SUMMARIZE()` function groups sales data by Region and Product to calculate Total Sales and Total Quantity. `ROLLUP()` adds subtotal and grand total rows to give a hierarchical summary of sales performance across different levels of detail.

### Combining SUMMARIZE() with ADDCOLUMNS()

You can also extend `SUMMARIZE()` with `ADDCOLUMNS()` to include custom-calculated columns within the grouped data. This can be helpful if you want to add measures or complex calculations to your summary table.

For example, I use the same dataset and apply the following formula to add a new column this time:

	`SalesWithAddColumns = 	ADDCOLUMNS( 	    SUMMARIZE( 	        sales_rollup, 	        sales_rollup[Region], 	        sales_rollup[Product], 	        "Total Sales", SUM(sales_rollup[Sales]), 	        "Total Quantity", SUM(sales_rollup[Quantity]) 	    ), 	    "Average Sales per Unit", 	        DIVIDE(SUM(sales_rollup[Sales]), SUM(sales_rollup[Quantity]), 0) 	)`

[](https://app.datacamp.com/workspace)

![DAX SUMMARIZE() used with ADDCOLUMNS() in Power BI](https://media.datacamp.com/cms/google/ad_4nxfjol2tsoxxn5nudaztjzvaal47mpvuhmotpfrrbo4ucs97dmdlfnkwqwzvpcfg7smaqluvwihyjcynracwhgepmcetbwmpl-on4ygtn6w4jiosua1kdof8pyzqqya-7wjy5jxbbny5dgmyzgqdkh6gr8e.png)

Combining SUMMARIZE() and ADDCOLUMNS(). Image by Author.  
  

Here, the `SUMMARIZE()` function groups sales by Region and Product to calculate Total Sales and Total Quantity. `ADDCOLUMNS()` then calculates the Average Sales per Unit by dividing total sales by the total quantity for each group.

## Common DAX Issues and How to Resolve Them

When using `SUMMARIZE()`, you might encounter a few issues. But don't worry we’ve all been there — I'll walk you through some common challenges and how to tackle them.

### Avoiding ambiguous results

Sometimes, `SUMMARIZE()` may give you results that don't quite make sense. This often happens when your data model or relationships aren't clear. Here's how to avoid this:

1. Double-check your data model: Make sure all your tables are connected correctly.
    
2. Use clear column names: Avoid duplicate names across different tables.
    
3. Specify table names: When referring to columns, include the table name (like `Orders[OrderDate]`) to avoid confusion.
    

### Performance considerations

Although `SUMMARIZE()` is a helpful function, it can be resource-intensive and slow things down when processing large datasets. This means your reports can take a little longer to refresh, especially if you're using the function within complex measures or with lots of grouped columns.

Here are some tips to keep your queries speedy:

- Consider calculated columns: For frequently used summaries, create calculated columns instead of using `SUMMARIZE()` each time.
    
- Remove unnecessary columns: Eliminate columns irrelevant to your analysis, such as primary keys or columns that can be calculated from others.
    
- Use filters: Use DAX `SUMMARIZE()` with `Filter()` before summarizing to reduce the amount of data processed.
    

## DAX Alternatives to SUMMARIZE()

While `SUMMARIZE()` is a useful function, sometimes other tools might do the job better. Let's look at a couple of alternatives and when you might want to use them.

### SUMMARIZECOLUMNS()

`SUMMARIZECOLUMNS()` is another DAX function that makes it easier to create summary tables when working with big data or complicated situations. It's similar to `SUMMARIZE()`, but with some differences.

- You can add filters directly to `SUMMARIZECOLUMNS()`, which makes it faster.
    
- With `SUMMARIZECOLUMNS()`, you can include measures directly in your output. There is no need for extra functions like `ADDCOLUMNS()`.
    
- `SUMMARIZECOLUMNS()` deals with blank rows automatically, so you don't have to worry about them.
    

```none
SUMMARIZECOLUMNS(
    <groupBy_columnName> [, <groubBy_columnName>] …, [<filterTable>] … [, <name>, <expression>] …
)
```

For example, I have a dataset, and I want to summarize employee salaries by Region and Department while filtering for employees with the first name Raven. I will use the `SUMMARIZECOLUMNS()` function to calculate the total salary for Raven across different regions and departments.

![DAX SUMMARIZE() and SUMMARIZECOLUMNS() in Power BI](https://media.datacamp.com/cms/google/ad_4nxf5tfldcl8sz1updfhftebftgmmvddbb8vza1usielrsgka04medopdmirfxm9yzt6jsbptc20xq_vvbix_ok3ufuivrnnwgljfb8gvncp78syqxygtl7e3gxdomnukuj5ynargow_nyf1fefmqjnqkxvby.png)

A table named employee_data. Image by Author.  
  

For this, I use the following formula:  

	`SalarySummary = 	SUMMARIZECOLUMNS( 	    employee_data[Name], 	    employee_data[Region], 	    employee_data[Department], 	    FILTER(employee_data, employee_data[Name] = "Raven"), 	    "Total Salary", SUM(employee_data[Salary]) 	)`

[](https://app.datacamp.com/workspace)

In the above formula: 

- `SalarySummary` is the name given to the calculated table being created.
    
- `SUMMARIZECOLUMNS(...)` creates a summary table based on the specified columns and calculations.
    
- `employee_data[Name], employee_data[Region], employee_data[Department]` are the columns by which the data will be grouped.
    
- `FILTER(employee_data, employee_data[Name] = "Raven")` restricts the results to only include rows where the Name is Raven.
    
- `"Total Salary", SUM(employee_data[Salary])` creates a calculated column in the result.
    
- `SUM(employee_data[Salary])` calculates the sum of all Salary values for each group.
    

![Using SUMMARIZECOLUMNS as an alternative of SUMMARIZE in Power Bi.](https://media.datacamp.com/cms/google/ad_4nxc63viurizqbmmoomtjvjmifuycwnuqvgkc68qe_gegdqiw1shv_tqhrrr6oeftt7wdcljxtbr1odducrlokhpqd5_kowwjcnrbycjrtywlvuolammzq0k0wy3qlc7qwmdx0yeswgiudobcydkrauaidwr8.png)

Use SUMMARIZECOLUMNS to summarize the results. Image by Author.  
  

You can see the results — the `SUMMARIZECOLUMNS()` function filters through the dataset and calculates Raven's salary totals across different locations and departments. 

### GROUPBY()

`GROUPBY()` is another function that can sometimes replace `SUMMARIZE()` when you just need to group data and perform calculations on those groups. It can be more efficient than `SUMMARIZE()` for simple grouping operations.

While `SUMMARIZE()` can work across related tables, `GROUPBY()` focuses on grouping and aggregating within a single table, which improves performance in certain scenarios.

Let's see an example. I’ve to create an inventory dataset to track items, categories, units sold, and unit prices, then group the data by category to calculate the total revenue for each.

![DAX SUMMARIZE() compared to GROUPBY() in Power BI](https://media.datacamp.com/cms/google/ad_4nxf1zoqm5_fss-3demnkk6fr8jmkt0ygreddx1otf9l0zqjg21h20pqmwggewf7er72ny5z4ldq_xsmnnutuypchgndzi8i1sx3beodpmeej4hyimzikfsv9qt91kfhc5zjhukvbkh1srcjh_l_-f2_bltol.png)

Inventory table. Image by Author.  
  

For this, I use the following formula:  

	`SummaryGroupBY = 	GROUPBY( 	    Inventory, 	    Inventory[Category], 	    "Total Revenue", 	    SUMX( 	        CURRENTGROUP(), 	        Inventory[Units Sold] * Inventory[Unit Price] 	    ) 	)`

[](https://app.datacamp.com/workspace)

In the above formula:

- `GROUPBY()` groups the data by Category.
    
- `CURRENTGROUP()` refers to each category group (e.g. electronics, furniture or appliances).
    
- `SUMX()` calculates the total revenue for each group by multiplying Units Sold with Unit Price.
    

![Using GROUPBY() to group the data in Power BI.](https://media.datacamp.com/cms/google/ad_4nxexs-l9i-s1cpvxocnd_lhsotdxha7d_xrhsfh42mdi4qexotmaflcny7zf3kx9a5udbkinopcw6t12pmvkhfinzsczvd2zqytz9dsd8rsifbg62o2idwzmqnxiq6vb1hwr6ykqqohrdzkwq_scg-d5ouqf.png)

Using GROUPBY to group the data. Image by Author. 

You can see — the `GROUPBY()`  function easily calculates the Total Revenue by multiplying Units Sold by Unit Price for each item in the category and summarizing these individual revenues. 

## Final Thoughts on DAX SUMMARIZE()

You now know how the `SUMMARIZE()` function in DAX can help you group and analyze data in Power BI, Excel, and other tools. From basic grouping to advanced techniques like `ROLLUP()` and `ADDCOLUMNS()`, `SUMMARIZE()` helps create insightful summaries.
up:: [[Power BI MOC]]
