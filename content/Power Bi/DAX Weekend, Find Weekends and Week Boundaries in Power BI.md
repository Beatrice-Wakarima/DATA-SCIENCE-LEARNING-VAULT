## Understanding Weekends in DAX

Let’s start with the basics, figuring out which days are weekends in your dataset. DAX gives you the `WEEKDAY()` function for this, and it’s surprisingly flexible once you know how the numbering system works. By default, `WEEKDAY()` returns a number from 1 to 7 that represents the day of the week for a given date. The second argument controls how those numbers are mapped. The version most developers use is `WEEKDAY(date, 2)`, which returns `1` for Monday through `7` for Sunday, matching the ISO standard that most business calendars use.

Here’s a quick example:

|   |   |   |
|---|---|---|
|**Date**|**WEEKDAY(Date, 2)**|**Day**|
|2025-10-13|1|Monday|
|2025-10-14|2|Tuesday|
|2025-10-18|6|Saturday|
|2025-10-19|7|Sunday|

Now let’s make this useful. You can add a calculated column in your `Date` table to flag weekends:

`IsWeekend = VAR DayNum = WEEKDAY('Date'[Date], 2) RETURN IF(DayNum > 5, TRUE(), FALSE())`

[](https://app.datacamp.com/workspace)

Here’s what’s happening:

- `WEEKDAY('Date'[Date], 2)` gives you the day number (`1` = Monday, …, `7` = Sunday).
    
- `DayNum > 5` identifies Saturday (`6`) and Sunday (`7`).
    
- The column returns `TRUE` for weekends, `FALSE` for weekdays.
    

If your week doesn’t follow the standard Monday–Friday pattern, for example, your business treats Friday and Saturday as weekends, you can adjust the logic easily:

`IsWeekend_Custom = VAR DayNum = WEEKDAY('Date'[Date], 2) RETURN IF(DayNum IN {5, 6}, TRUE(), FALSE())`

[](https://app.datacamp.com/workspace)

That one-line change makes your model work for custom operating calendars. After creating this column, drop it into a simple table visual in Power BI with the `Date` field and check whether your weekend days line up correctly.

## How to Create Custom Week Boundaries

Most Power BI models assume a Monday–Sunday calendar, but real-world reporting rarely follows that neatly. Retail dashboards, for instance, often close on Fridays; some organizations instead track Saturday–Friday cycles. In DAX, you can create custom week boundaries that match your business calendar. Let’s walk through how to do that cleanly, step by step.

### Setting a week ending on Friday

If your business week ends on Friday, you can assign each date a corresponding weekend date. The logic is simple: take each date, find its weekday number, and offset it forward until it hits Friday.

Here’s the calculated column formula:

`WeekEnd_Friday = VAR WeekdayIndex = WEEKDAY('Date'[Date], 2)        // Monday = 1, Sunday = 7 VAR DaysToFriday = 5 - WeekdayIndex                // 5 represents Friday RETURN 'Date'[Date] + IF(DaysToFriday < 0, DaysToFriday + 7, DaysToFriday)`

[](https://app.datacamp.com/workspace)

Here’s what it does:

- `WEEKDAY('Date'[Date], 2)` gives you the weekday index (`Monday = 1`).
    
- You calculate how far that date is from Friday.
    
- If the day has already passed Friday (e.g., Saturday or Sunday), it rolls over to the following Friday by adding 7 days.
    

This approach groups all dates between Saturday and Friday under the same week, ending on Friday.

To check it:

- Add this column to your Date table.
    
- Create a table visual in Power BI with `Date` and `WeekEnd_Friday`.
    
- You’ll see that every Saturday–Friday sequence maps to the same weekend date.
    

### Setting a Week Starting on Saturday

If your reporting week starts on Saturday, you can pair the previous formula with a week start column. You can do this using the same logic, but in reverse, find the most recent Saturday relative to each date.

Here’s the companion DAX column:

`WeekStart_Saturday = VAR WeekdayIndex = WEEKDAY('Date'[Date], 2)       // Monday = 1, Sunday = 7 VAR DaysSinceSaturday = WeekdayIndex - 6          // 6 represents Saturday RETURN 'Date'[Date] - IF(DaysSinceSaturday < 0, DaysSinceSaturday + 7, DaysSinceSaturday)`

[](https://app.datacamp.com/workspace)

This works almost identically to the previous expression, but shifts backward to the previous Saturday.

You might also see older code samples using the `EARLIER()` function to capture the current row context inside a calculated column. For example:

`WeekStart_Saturday = VAR CurrentDate = EARLIER('Date'[Date]) VAR WeekdayIndex = WEEKDAY(CurrentDate, 2) VAR DaysSinceSaturday = WeekdayIndex - 6 RETURN CurrentDate - IF(DaysSinceSaturday < 0, DaysSinceSaturday + 7, DaysSinceSaturday)`

[](https://app.datacamp.com/workspace)

Modern DAX doesn’t require `EARLIER()` in this scenario, since calculated columns already evaluate row by row, but it’s still helpful to understand for legacy models or when nesting row contexts in iterators.

Once you’ve added both columns, try plotting `WeekStart_Saturday` and `WeekEnd_Friday` in a table visual with your `Date` column. You’ll see clear week boundaries that follow your business rhythm, not the default calendar.

Next, you can use these week start and end dates as grouping keys in visuals or as anchors in measures, perfect for calculating totals per business week, comparing week-over-week performance, or aligning with non-standard fiscal calendars.

## Choosing Between Columns and Measures

Now that you’ve set up your custom week boundaries, it’s worth deciding how to use them in your model, as calculated columns or as measures. Both have their place, and knowing when to use each keeps your Power BI model efficient and predictable.

Think of calculated columns as static attributes you want to slice or filter by. For example, your `IsWeekend`, `WeekStart_Saturday`, or `WeekEnd_Friday` columns describe each date. They don’t depend on user interactions or filters; they just define what each day is. That makes them perfect for grouping visuals, setting relationships, or building hierarchies.

In contrast, measures are dynamic calculations that respond to filters, slicers, and context. If you’re summarizing or comparing metrics, say, counting working days in a selected range or calculating average sales per week, you’ll want a measure.

Here’s a quick comparison to keep in mind:

|   |   |   |
|---|---|---|
|**Use Case**|**Type**|**Example**|
|Identify weekends or week boundaries|Calculated column|`IsWeekend = IF(WEEKDAY('Date'[Date],2)>5,TRUE(),FALSE())`|
|Slice visuals by custom week ranges|Calculated column|`WeekStart_Saturday`, `WeekEnd_Friday`|
|Count working days in current filter|Measure|`WorkingDays = COUNTROWS(FILTER('Date', 'Date'[IsWeekend] = FALSE()))`|
|Compare total sales between custom weeks|Measure|`TotalSalesByWeek = SUM(Sales[Amount])` grouped by `WeekStart_Saturday`|

In short:

- If you need the result stored with each row (and usable in slicers or filters), go with a column.
- If you need a calculation that updates with user interaction, go with a measure.

## Calculating Working Days with NETWORKDAYS()

Once your weekends and week boundaries are defined, the next logical step is to calculate working days—the number of weekdays between two dates, optionally excluding holidays. Power BI and DAX make this straightforward with the `NETWORKDAYS()` function, introduced in recent versions of DAX.

At its simplest, the syntax looks like this:

`NETWORKDAYS(<start_date>, <end_date>[, <weekend>[, <holidays>]])`

[](https://app.datacamp.com/workspace)

Here’s how each parameter works:

- `<start_date>` and `<end_date>` define your range.
    
- `<weekend>` is optional and lets you specify which days count as weekends.
    
- `<holidays>` is also optional — you can pass in a column or table of holiday dates to exclude them from the count.
    

### Understanding Weekend Codes

The `<weekend>` argument uses numeric codes to define which days are considered weekends. Here are some standard options you’ll likely use:

|   |   |   |
|---|---|---|
|**Code**|**Weekend Days**|**Description**|
|1|Saturday, Sunday|Default (Western workweek)|
|7|Friday, Saturday|Common in Middle Eastern calendars|
|11|Sunday only|For Sunday-only closures|
|12|Monday only|For Monday-only non-working days|

For example, if your workweek runs from Sunday to Thursday, you’d use code `7` for Friday–Saturday weekends.

Here’s how to calculate working days between two columns in your model:

`WorkingDays_Default = NETWORKDAYS('Sales'[StartDate], 'Sales'[EndDate])`

[](https://app.datacamp.com/workspace)

That formula assumes Saturday and Sunday are weekends. If your business follows a Friday–Saturday weekend, you can adjust it like this:

`WorkingDays_FriSat = NETWORKDAYS('Sales'[StartDate], 'Sales'[EndDate], 7)`

[](https://app.datacamp.com/workspace)

### Excluding holidays

You can go a step further by excluding official holidays stored in a dedicated `Holiday` table. Let’s say you’ve got a table with a `Holiday[Date]` column. Here’s how to include it:

`WorkingDays_WithHolidays = NETWORKDAYS(     'Sales'[StartDate],     'Sales'[EndDate],     1,     'Holiday'[Date] )`

[](https://app.datacamp.com/workspace)

This setup ensures that weekends and your organization’s defined holidays are skipped from the count. It’s a small addition that makes your reports much more accurate, especially for workforce planning, SLA monitoring, or operational dashboards.

### Example Use Case

Imagine your company tracks project timelines in Power BI. Each record has a `StartDate` and `EndDate`. By adding the `WorkingDays_WithHolidays` measure, you can quickly visualize:

- How many working days did each project take?
- Which projects ran across weekends or public holidays?
- Average working duration per department or project type.

To see it in action, drop this measure into a table visual along with `Project Name`, `StartDate`, and `EndDate`. You’ll instantly get a more meaningful picture of timelines based on actual working days, not just raw date differences.

## Practical Applications in Business Dashboards

Now that you’ve got working days, weekend flags, and custom week boundaries in place, let’s look at how these fit into real-world Power BI dashboards. The ability to redefine weekends or fiscal weeks isn’t just a neat technical trick; it directly impacts how metrics are calculated, visualized, and understood across departments.

### Payroll and timesheet cutoffs

Many organizations process payroll on a fixed Saturday–Friday or Sunday–Saturday cycle. By defining week boundaries in DAX, you can align salary periods, overtime calculations, and timesheet entries with the exact working week your HR system uses. For instance, you could calculate the total hours worked or shifts completed per custom week, ensuring payroll reports align perfectly with internal schedules rather than the default Monday–Sunday calendar.

### Operational KPIs and service monitoring

Operations and logistics teams often measure KPIs like delivery turnaround time or incident resolution using working days only. Using `NETWORKDAYS()` ensures those metrics reflect real-world business capacity, not weekends when nothing moves.

Pairing your working day calculations with your `WeekStart_Saturday` or `WeekEnd_Friday` columns lets you group data by the exact operational week that management tracks in meetings and reports.

### Retail and sales performance

Retailers rarely follow calendar weeks. Many prefer Saturday to Friday to capture the full weekend sales period in one consistent reporting block. By modeling your date table around that schedule, weekend sales trends stay intact within the same week, making comparisons between weekends meaningful. This small adjustment can prevent distorted “week-over-week” visuals and give more accurate rolling averages.

### Custom fiscal weeks and forecasting

Some finance teams work with fiscal weeks that start midweek or follow a 4-4-5 accounting pattern. Your custom week boundaries can be easily plugged into that.Once your date table includes `WeekStart` and `WeekEnd` columns, measures such as revenue recognition, expense tracking, or forecasting can be aggregated consistently, regardless of how unconventional your fiscal calendar may be.

### Rolling averages based on working days

When calculating moving averages, especially for KPIs such as daily sales or production rates, it’s better to base the calculation on working days rather than calendar days.

For example, if weekends are excluded using your `IsWeekend` flag, a 7-day rolling average would truly reflect one business week of activity, no inflated or misleading dips on non-working days.

In short, custom week definitions and working-day logic bring your Power BI dashboards closer to how your business actually operates. Whether you’re tracking payroll cutoffs, shipping lead times, or weekend sales peaks, these DAX patterns make your insights cleaner, fairer, and far more actionable.

## Key Points to Remember

Before wrapping up, let’s summarize the main takeaways so you can apply these DAX techniques effectively in your Power BI projects.

- Use calculated columns for row-wise classification: When you need to label each date, such as marking weekends, assigning week boundaries, or categorizing business days, calculated columns are your best bet. They provide static attributes that work seamlessly in slicers, filters, and relationships throughout your model.
    
- Use `WEEKDAY()` carefully with the right return type: Remember that `WEEKDAY(date, 2)` starts the count on Monday (`1`) and ends on Sunday (`7`). Adjusting this parameter helps you align your calculations with regional or organizational workweek standards. Always double-check your return type. It’s one of the most common sources of off-by-one errors in DAX time logic.
    
- **`NETWORKDAYS()` is your go-to for excluding weekends and holidays**: This function simplifies working-day calculations, saving you from complex date filters or manual loops. Combine it with your company’s weekend code and a holiday table to get accurate counts that reflect real business days, not just calendar gaps.
    

By mastering these fundamentals, custom week structures, careful weekday logic, and precise working-day counts, you’ll bring more accuracy and flexibility to every Power BI dashboard you build. Next time you’re setting up a date model or aligning reports with business calendars, these DAX patterns should be at the top of your toolkit 

## Common Mistakes to Avoid

Even experienced Power BI developers can run into subtle pitfalls when working with date and week logic in DAX. Here are a few issues worth watching out for:

### Mixing up quotes in text comparisons

DAX distinguishes between single (') and double (") quotes, and using the wrong one can break your logic, especially when comparing text values like day names or flags. For example:

`IsWeekend = IF(WEEKDAY('Date'[Date], 2) > 5, "Weekend", "Weekday")`

[](https://app.datacamp.com/workspace)

### Always use double quotes for text strings inside functions 

Single quotes are reserved for table and column references, like `'Date'[Date]`.

### Forgetting about row context 

This is one of the most common conceptual mistakes. Calculated columns evaluate each row independently, while measures depend on filter and evaluation context. If you’re referencing a column without aggregation in a measure, it won’t behave as expected because there’s no row context. For example, `IF(WEEKDAY('Date'[Date], 2) > 5, TRUE(), FALSE())` works as a calculated column ,but if you need it to respond to filters dynamically, you’ll need to wrap it in an iterator like SUMX() or use it within a measure that counts or filters rows.

### Ignoring time zones or calendar alignment 

When using imported data with time stamps, DAX date functions operate on the date portion of your column. If your data crosses time zones or uses UTC adjustments, those weekend flags might shift unexpectedly. Always clean and normalize your datetime fields in Power Query before applying DAX logic.

### Hardcoding weekend logic 

Avoid embedding fixed logic like “Saturday and Sunday” directly in multiple formulas. Instead, define a reusable variable or disconnected table that lists your organization’s weekend days. This makes maintenance easier when business calendars change.

Catching these small issues early can save hours of debugging later. When in doubt, use the Data View in Power BI to inspect calculated column results row by row , it’s one of the fastest ways to verify that your DAX logic behaves as intended before rolling it into visuals or measures.

## Conclusion

Working with weekends and custom week boundaries in DAX isn’t just about date math, it’s about making your Power BI models reflect how your business actually runs. Whether you’re marking Saturdays and Sundays as non-working days, aligning your fiscal week from Saturday to Friday, or calculating working days that exclude holidays, the goal is the same: accuracy and context in every calculation.

You’ve seen how functions like `WEEKDAY()` and `NETWORKDAYS()` help define flexible date logic and how calculated columns and measures each play their part: one for structure and the other for dynamic analysis. Along the way, we’ve examined real-world use cases, from payroll cutoffs to retail calendars, and learned how to avoid common DAX pitfalls, such as misused quotes or lost row context.

The next time you’re building a Power BI dashboard that deals with dates, think beyond the default calendar. Customize your week, make weekends explicit, and treat working days as the first-class metrics they deserve to be. With these DAX patterns in your toolkit, your reports won’t just show time, they’ll show time as your organization experiences it.
up:: [[Power BI MOC]]
