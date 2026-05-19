## What are Power BI Date Tables?

Date tables in [Power BI](http://www.datacamp.com/learn/power-bi) only contain date-related data. They are a standard dimension table that can be used to reference dates in your model and analyze data based on these dates. They are also useful for time intelligence calculations and when creating reports that require precise date information.

_**[Practice creating date tables in Power BI](https://campus.datacamp.com/courses/dax-functions-in-power-bi/setting-up-data-models-with-dax-1?ex=4) with this hands-on exercise.**_

### Why are date tables useful in data analysis?

Date and time-based analyses are usually required in [Power BI reports](https://app.datacamp.com/learn/tutorials/power-bi-reports-tutorial). This is where making a date table comes in handy. Date tables allow you to slice and dice your data by date attributes such as weekday, month, quarter, and year. They also allow you to use DAX time intelligence functions that would not normally work without a date table. For proper analysis, it is necessary to have all of the columns formatted correctly when utilizing date tables.

![Power BI Calendar Screenshot](https://images.datacamp.com/image/upload/v1654682703/image18_11dc302584.png)

### Requirements for creating a date table in Power BI

Some of the requirements for a date table are as follows:

|Requirement|Reasoning|
|---|---|
|Date column with date/time datatype|Ensures that the column is recognized as containing date information, which is essential for time intelligence operations.|
|No blanks in the date column|Guarantees that every date is accounted for, preventing errors in analysis.|
|Unique values in the date column|Prevents duplicates for the integrity of date-based calculations.|
|No missing dates|Ensures continuity in the timeline, which is crucial for accurate time series analysis.|
|Spans whole years|It comprehensively covers all date values, whether by calendar year or fiscal year, for complete temporal coverage in reports.|
|Marked as a Date Table|Validates the table for use in time intelligence functions, marking it as the model’s official date table.|

### Names for power BI date tables

Date tables are also known by various other names, such as calendar tables, date dimension tables, and calendar dimension tables. All these names refer to the same thing: a table with one record per day and a column displaying the date's attribute.

## Generating Power BI Date Tables 

There are four major ways in which date tables can be generated in Power BI:

- Source Data
- Auto Date/Time
- DAX
- Power Query

Let's review each one of these methods.

### Source data

When you import your data, it may already have a date table that was created in the data source. In this case, there is no need to create another date table. This date table is ready to use, so you can simply bring it into the data model, and a relationship with other tables in your data model will be created.

If the date table does not come with the source data, there are several methods for creating it.

### Auto date/time

When filtering data over date periods, the _auto date/time_ approach uses simple time intelligence based on date columns already loaded into your model. It does not, however, provide a date table that may be used to slice and dice other tables. To use this method, you must first enable _Auto date/time in_ Power BI. Navigate to the _File_ ribbon _> Options and Settings > Options > Data Load > Current File > Time Intelligence > Enable Auto date/time._ 

![Power BI Options Screenshot](https://images.datacamp.com/image/upload/v1654682700/image7_9be16d4133.png)

After the option is enabled, Power BI Desktop will create a hidden auto date/time table based on the dates in the date column. It then creates a relationship between the hidden auto date/time date column and the date column in the model. 

When there is an auto date/time table, it will not appear as a field in the _Fields_ pane. Instead,  it can be found as an extendable drop-down with the name of the date column, as shown below. When you expand the date column, you will see a hierarchy called the _Date Hierarchy_, which includes `Year`, `Quarter`, `Month`, and `Day`.

![Power BI Customer ID](https://images.datacamp.com/image/upload/v1654682700/image1_5fd185c726.png)

This can then be used to create a visualizations:

![Power BI Line Chart](https://images.datacamp.com/image/upload/v1654682703/image5_d026af50c3.png)

### DAX

Another method for creating a date dimension table in Power BI is to use [Data Analysis Expression (DAX) methods](https://app.datacamp.com/learn/tutorials/power-bi-dax-tutorial-for-beginners). `CalendarAuto` and `Calendar` are frequently used to create these tables. The difference between these two functions is that the Calendar function returns a range of dates based on the start and end dates specified as parameters within the function. In contrast, the `CalendarAuto` function returns a range of dates that are automatically detected from the dataset. The start date is the earliest date in your dataset, and the end date is the most recent date in your dataset.

To use the `Calendar` function, navigate to the _Table_ tab on the ribbon in Power BI Desktop. Select _New Table_, then input the DAX formula as shown below:

![Power BI DAX Formula](https://images.datacamp.com/image/upload/v1654682702/image22_e3fa1ca9d2.png)

![Power BI DAX Formula 2](https://images.datacamp.com/image/upload/v1654682700/image6_2888dafba4.png)

The above DAX function creates a date table with a date column. Other columns, such as `Year`, `Month`, `Weekday`, and `Week of the Year`, can be added to the table. To do so, select the _New Column_ button on the ribbon and input the DAX equation for each column you want to add. In the following examples, we will write the DAX equation to get the year, month, and month numbers from the date table:

![Power BI Select New Column](https://images.datacamp.com/image/upload/v1654682699/image8_4f91b60915.png)

![Power BI DAX Date Formula](https://images.datacamp.com/image/upload/v1654682701/image23_74968b2803.png)

![Power BI DAX Date Formula 2](https://images.datacamp.com/image/upload/v1654682700/image14_0e46c9c511.png)

![Power BI DAX Date Formula  3](https://images.datacamp.com/image/upload/v1654682702/image20_e6c0d3b8fb.png)

The results of the DAX equations written for all of these new columns are shown below:

![Power BI DAX Date Equations Results](https://images.datacamp.com/image/upload/v1654682701/image16_ac7e1ded73.png)

Other expressions can be used to get as many additional date-related columns as you want.

We have just used DAX to create a date table. However, this method only adds your new table to the data model; you must still create relationships between your date tables and then mark your table as the data model's official date table.

### Power Query

To create a date table in Power BI, use the mash-up language, often known as M-Query.

To do so, click the _Transform Data_ button on the ribbon and then navigate to _Power Query_.

![Power BI Transform Data](https://images.datacamp.com/image/upload/v1654682700/image9_5be4561d8f.png)

Right-click in the empty space of the left _Queries_ pane to access the following drop-down menu, where you will select _New Query_ and _Blank Query_.

![Power BI Select Blank Query](https://images.datacamp.com/image/upload/v1654682700/image19_b30e85a0cc.png)

In the blank query tab, enter the M-query to create the date table as seen below:

![Power BI M-query](https://images.datacamp.com/image/upload/v1654682700/image15_198826329a.png)

The `#date` argument indicates the earliest day in your data's start year, month, and day, and `365*7` represents the date for the next 7 years. The days, hours, minutes, and seconds are represented by `#duration`, and `#duration(1,0,0,0)` indicates 1 day, 0 hours, 0 minutes, and 0 seconds in the query above. The advantage of this approach for creating date tables over others is that it will automatically update when new data comes in, omitting the need to recreate the table.

![Power BI M-equation Results](https://images.datacamp.com/image/upload/v1654682700/image11_4be33857c5.png)

To change the result of the M-equation from a list of dates to a table of dates, navigate to the _Transform_ tab on the ribbon, select _Convert,_ and then _To Table_.

![Power BI Creating a Date Table](https://images.datacamp.com/image/upload/v1654682701/image4_821b73f4e0.png)

After this has been done, you can include other date-related columns, just as we did with the DAX equation approach for creating date tables. To do this, you must first change the date column's data type to _Date_ by selecting the icon on the left side of the column name.

![Creating Date Column in Power BI](https://images.datacamp.com/image/upload/v1654682700/image17_a4cae00035.png)

After changing the data type, you may add new columns to the table by navigating to the _Add Column_ ribbon, selecting the dropdown beneath _Date_, and then selecting _Year_ or any other column you want to add.

![Creating Date Tables in Power BI 3](https://images.datacamp.com/image/upload/v1654682702/image21_e7bfc2c663.png)

As seen above, the date drop-down allows you to enter the Year, Month, Quarter, Week, Day, and Age.

We have now successfully used Power Query to create a date table. You may now mark your newly created date table as such after pulling it into the data model.

## Methods of Generating Power BI Date Tables: A Summary

The following table summarizes the methods described before, providing use cases for each:

|Method|Description|Use cases|
|---|---|---|
|Source Data|Uses an existing date table from the data source.|When the source data already includes a fully-formed date table.|
|Auto Date/Time|Automatically creates a hidden date/time table based on date columns in the model.|Quick time intelligence without the need for a visible date table.|
|DAX|Utilizes Data Analysis Expressions to create custom date tables.|When you need customizable date attributes and precise control over the date range.|
|Power Query|Employs M-query to create date tables that automatically update with new data.|Ideal for creating reusable date tables that automatically update with new data.|

## Marking a Table as a Date Table

After creating the date table using one of the approaches described above, the next step is to mark it as a "date table." To do so, right-click the table's name in the _Fields_ pane and select _Mark as date table_.

![Power BI Mark as Date Table Function](https://images.datacamp.com/image/upload/v1654682701/image13_d7f7afe0b2.png)

Power BI verifies the data in the table by marking it as a date table, ensuring that the date column is of data type `Date` and contains unique values.

![Mark as Date Table in Power BI](https://images.datacamp.com/image/upload/v1654682699/image2_1eda148fdd.png)

When a table is marked as a date table, the autogenerated hierarchies for the date field in the date table are deleted, but the hierarchies for other date fields in other tables remain until a relationship is established between that field and the generated date table.

## Pros and cons of DAX vs Power Query

A few differences exist between the DAX and Power Query approaches to creating a date table in Power BI. The following points are the main distinctions that can be made:

|Aspect|DAX approach|Power Query approach|
|---|---|---|
|Simplicity|Easier to use as it doesn't require opening the Power Query Editor.|Requires navigating to Power Query Editor, which might be less straightforward for beginners.|
|Reusability|Limited to the current Power BI file unless exported or copied.|Allows for reusability through Power BI dataflows, making it accessible for multiple reports or projects.|
|Customization|Offers precise control and customization of date attributes through DAX functions.|Provides dynamic updating capabilities with M-query, which is beneficial for handling data that changes over time.|

## Creating Relationships between Date Tables and Other Tables

Power BI relationships provide a clear understanding of how tables are linked. They demonstrate how a column typically links two or more tables and then joins the columns from the separate tables. These relationships are formed either automatically by Power BI when the data is loaded or manually. When you enter your data into Power BI, the _Autodetect_ feature will help you establish relationships between columns with similar names.

To manually create relationships between the date table and other tables, navigate to the model tab, where the data model is placed, and then drag the relevant column from one table and drop it into the corresponding column from the other table. In the following example, the date field from the `Accidents` table was dragged and dropped onto the `Date` field from the date table.

![Power BI Creating Relationships with Date Tables](https://media.datacamp.com/legacy/v1722015126/image_745440501d.png)

Another option for creating the relationship is to go to the _Manage Relationship_ ribbon in the model tab's relationships view. In this view, you can create, update, and delete relationships between tables and autodetect existing relationships.

![Power BI Manage Relationships](https://media.datacamp.com/legacy/v1722015126/image_ee9bf175ef.png)

![Power BI Manage Relationships](https://media.datacamp.com/legacy/v1722015127/image_051584db47.png)

Creating relationships with the date table propagates filters to several tables, allowing you to display accurate information in your report between the tables connected.

Below are a few illustrations of how filters are propagated from date tables to other tables. Each of these instances can be drilled down to the next level in the hierarchy (i.e., you can drill down from year to month to quarter to day, etc):

![Different Date Tables in Power BI](https://media.datacamp.com/legacy/v1722015127/image_7146228cf4.png)

## Conclusion

You have more than one option when creating a data table with Power BI, as demonstrated in this article. However, considerations such as usability, simplicity, reusability, and your requirements may influence your choice.
up:: [[Power BI MOC]]
