## What are Power BI KPIs?

Before we begin, let's define what KPIs are and how we can visualize them in Power BI.

KPIs ([Key Performance Indicator](https://en.wikipedia.org/wiki/Performance_indicator)) help you measure how effectively your company achieves key business objectives.

In Power BI, you can visualize KPIs using a specific KPI visual, which shows the KPI, the target, and its trend over time.

Alternatively, you can present your KPIs using the card or gauge visuals. You can also get creative with measures and formatting to incorporate KPIs into your Power BI reports. Here, we'll review both the traditional KPI visual and some alternative methods.

You can learn more about customizing and optimizing your KPIs with our webinar on [calculating KPIs with DAX](https://www.datacamp.com/resources/webinars/calculating-kpis-with-dax-in-power-bi).

KPIs in Power BI are not just about visual appeal. They enable businesses to:

- Monitor their most important metrics at a glance.
- Track these business metrics against a pre-defined target.
- Identify trends and patterns that could indicate business opportunities or risks.

If you are a beginner in learning Power BI and want to pick up the basics quickly, then our [Power BI for Beginners](https://www.datacamp.com/tutorial/tutorial-power-bi-for-beginners) tutorial is an ideal choice for you.

However, if you are ready to take on some in-depth Power BI courses, our [Introduction to Power BI](https://www.datacamp.com/courses/introduction-to-power-bi) course is the best place to begin.

## Master Power BI From Scratch

No experience required—learn to work with data via Power BI.

## Choosing Your KPIs

Always ensure you have clear, measurable goals before you add KPI visuals to your dashboards. Your KPIs should closely align with the company's business objectives.

Less is more when it comes to KPIs. Avoid adding too many KPI visuals to your dashboards.

We'll consider a common KPI for many businesses: profit margin. We also set an arbitrary target of 15% for our profit margin.

## Step-by-Step Guide to Creating KPI Visuals in Power BI

We'll visualize our profit margin KPI in three ways:

- Using the KPI visual
- Using the gauge visual
- Using the card visual with a few creative adjustments

### Step 1: Get your data ready

The first step is to ensure that your data is clean, reliable, and structured so that Power BI can digest it.

Getting your data ready often involves some data prep work, such as:

- Importing data into Power BI Desktop. This could be from Excel, a database, or any other data source.
- Performing data transformation as needed to clean up duplicates, missing values, data types, extra columns, and so on.
- Setting up the data model, with relationships defined if you're using multiple tables.

Luckily, this sample data is cleaned and ready to use, so we'll import it into Power BI and start visualizing our KPI.

### Step 2: Create your measures

We need to create measures for the base and target values of the KPI and gauge visuals (and two other measures for our card visual). Measures are formulas that you define using DAX ([Data Analysis Expressions](https://learn.microsoft.com/en-us/dax/)).

To get started with DAX, check out our [Introduction to DAX](https://www.datacamp.com/courses/introduction-to-dax-in-power-bi) course and keep our [DAX cheat sheet](https://www.datacamp.com/cheat-sheet/dax-cheat-sheet) on hand for a quick reference on many of the most useful DAX functions you will encounter (including the ones we’ll use in this tutorial).

_[![Power BI DAX Cheat Sheet](https://media.datacamp.com/legacy/v1711033567/image_f98a2ec4de.png)](https://www.datacamp.com/cheat-sheet/dax-cheat-sheet)_

_The DataCamp DAX Cheat Sheet_

Profit margin is calculated as profit divided by total sales. Here is the formula we use:

`Profit Margin = SUM ( Profit ) / SUM ( Sales )`

Our target measure is a simple scalar:

`Profit Margin Target = 0.15`

For the card visual, we must create two additional measures.

The first measure calculates the difference between the actual profit margin and the target. Then, it uses the FORMAT function to effectively convert the numbers to text so that we can concatenate a few other strings to make our “Goal” line, as seen in the KPI visual.

`KPI Profit Margin vs Target =   VAR Diff = [Profit Margin] - [Profit Margin Target]   VAR Sign = IF(Diff > 0, “+”, “”)   RETURN   “Goal: “ & FORMAT([Profit Margin Target], “#0%”) & “ (“ & Sign &  FORMAT(Diff, “#0.0%) & “)”`

[Powered By](https://www.datacamp.com/datalab) 

The second measure controls the color of our card. You’ll see that we use the SWITCH function in this expression. If you’re new to SWITCH and want to learn more about how it works and how you can use it, check out our [guide to the Power BI SWITCH function](https://www.datacamp.com/tutorial/switch-in-dax-for-power-bi).

`KPI Color =   VAR Diff = [Profit Margin] - [Profit Margin Target]   RETURN   SWITCH (     TRUE(),     Diff > 0, “Green”,     Diff < 0, “Red”,     “Black” )`

[Powered By](https://www.datacamp.com/datalab) 

### Step 3: Add the KPIs to the report

#### KPI visual

In Power BI Desktop, go to the "Report" view. From the "Visualizations" pane, select the KPI visual.

The Power BI KPI visual contains these three fields:

- **A base value**: This is your actual data point, like current sales figures.
- **A target value**: The goal or benchmark you're aiming for, such as sales targets.
- **A trend field**: Most effective KPIs are tracked over time, so having date data is crucial.

_![Power BI KPI visual](https://media.datacamp.com/legacy/v1711033565/image_594cf0d91b.png)_

_Image by author_

#### Gauge visual

From the "Visualizations" pane, select the gauge visual.

The gauge visual is much more flexible than the KPI simply because it offers more fields for adding measures that control the minimum and maximum values on the gauge. You are also not obligated to add a date column for showing a trend, which makes the gauge visual more suited to KPIs that may not need to be tracked over time.

_![Power BI Gauge Visual](https://media.datacamp.com/legacy/v1711033565/image_a4efc18f9e.png)Image by author_

#### Card visual

Back in the "Visualizations" pane, we are now going to select the card visual.

Typically, this visual shows a single summarized metric. However, with the formatting and customization options, you can get creative with the type of information you can show with a card visual.

We will recreate the KPI visual using a few measures (that we already created in step 2 above) and some customization options in a card visual.

Here is the final product:

_![Power BI Card Visual for KPIs](https://media.datacamp.com/legacy/v1711033565/image_d8a8bda76c.png)_

_Image by author_

The card visual is my first choice when visualizing KPIs in scenarios where I need more flexibility. What if I don’t need to track my KPI over time and don’t have a date column in my data? What if I want to add a custom calculation showing the difference between the actual value and the target?

One key difference between our card here and the KPI visual that we created earlier is that the KPI visual always calculates the percentage change between the actual value and its target. This is unintuitive for percentage-based KPIs since it makes more sense to calculate a simple difference between the actual value and the target.

With the card visual, we can choose how we want the KPI to be calculated, displayed, and compared against our target.

If you're interested in exploring [advanced analytical features in Power BI](https://www.datacamp.com/tutorial/advanced-analytical-features-in-power-bi-tutorial), we have a tutorial to guide you through the process.

## Best Practices for KPI Reporting

Keep it simple: Don't overload your KPI with too much information. Focus on a few key KPIs that reflect your current business objectives. Explore other visualization options or use drill-down features to allow users to explore more detailed data without overwhelming the main dashboard view.

Check out our course on [data visualization in Power BI](https://www.datacamp.com/courses/data-visualization-in-power-bi) to learn more about how to visualize and present your insights to your users effectively.

Use color wisely: Colors can draw attention to key information or trends. For example, red could indicate performance below targets, while green shows areas of success. If your users are color-blind, you can also select from color palettes that are color-blind-friendly. Just be sure to communicate the meaning of the colors to your users.

Use your KPIs to tell a story: Arrange your KPIs logically, guiding the viewer through a narrative. Highlight insights and takeaways to draw attention to the most important aspects of the data.

Check out these [9 dashboard examples](https://www.datacamp.com/blog/9-power-bi-dashboard-examples) to get inspiration on the different ways you can tell a compelling story with your data in Power BI.

For a quick tutorial on [designing engaging Power BI reports](https://www.datacamp.com/tutorial/power-bi-reports-tutorial), we’ve got you covered on that too.

Align KPIs with business objectives: Ensure each KPI is directly linked to a strategic business objective. This alignment guarantees that the insights gained from the KPIs are relevant and actionable.

Balance leading and lagging indicators: Include both leading indicators (which predict future performance) and lagging indicators (which reflect past performance) to get a comprehensive view of your business.

Regularly review and update KPIs: It's important to review KPIs regularly to ensure they remain relevant. Update your KPIs to reflect changes in strategy, market conditions, or operational focus.
up:: [[Power BI MOC]]
