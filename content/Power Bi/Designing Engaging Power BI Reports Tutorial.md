## Why is Report Design Important?

It's now easier than ever to design reports and dashboards thanks to a huge variety of BI platforms. However, many of these fail to live up to their purpose and provide true business value.

Fortunately, there are some good design guidelines that you can follow to ensure that your reports are useful and able to convey key business insights to those who use them. In particular, a well-designed report should be able to:

- Simplify complex information
- Convey insights as concisely as possible
- Elaborate on information only as needed

Note that the terms ‘report’ and ‘dashboard’ are often used interchangeably in the Business Intelligence space. In Power BI, a ‘dashboard’ is specifically built and used from existing reports only in the Power BI service, while a ‘report’ is typically built using Power BI Desktop. The design principles in this article can be applied to both reports and dashboards; however, we will focus on their application in designing reports in Power BI Desktop. If [you are new to Power BI](https://www.datacamp.com/learn/power-bi), you might also want to check out this [introductory tutorial](https://www.datacamp.com/tutorial/tutorial-power-bi-for-beginners).  

![Power BI Report Screenshot](https://images.datacamp.com/image/upload/v1651737310/image3_0832d5b757.png)

## Main Elements of Report Design

There are many aspects to report design which can also vary depending on the capabilities of the platform used to build those reports. 

However, no matter what platform you are using or what industry you are in, there are a few main elements of report design that apply to all:

- Design for the user and the role: Different users and business roles have different requirements and uses for the reports. For example, a CEO will likely need information about many different departments at a glance; whereas a finance manager or sales manager more often needs to be able to dig into the report, identify issues, and discover insights that inform their day-to-day decision making.
- The 5-second rule: This is a general design rule. In this context, we say that a report should be able to convey the most high-value, high-impact information within 5 seconds. This requires regular communication with business users to determine what types of information are most relevant and important to them.
- Keep it simple: Users should not need to put in a lot of effort to figure out what is important or whether they need to take any action based on the information in the report.
- Consistency: This applies to the design aspects within a single report as well as across all reports in the business – the choices of colors, fonts, formatting, layout, etc. should remain consistent. 

## Master Power BI From Scratch

No experience required—learn to work with data via Power BI.

## Guidelines for Designing Engaging Reports

These guidelines will help you to build engaging, useful, and valuable reports. Each guideline below should be implemented while also keeping the aforementioned main elements of report design in mind.

We will discuss the following design guidelines:

- Choosing the right chart
- Placement and spacing
- Context
- Formatting and decoration

### Choosing the Right Chart

Power BI has around 200+ visualization options to choose from, including the custom visuals that are available through AppSource. The number of options available makes it even more challenging to choose the appropriate chart.

Usually, data types will inform the chart selection process and narrow down the best visuals to use for that data type. So, it is useful to consider the purpose of the information you want to include in the report. Ask yourself what action or decision a particular visual should inform. 

There are a handful of visuals that I use most often in my reports. If I ever find myself struggling to choose a particular visual, I usually go back to the basics and start with the simplest chart to convey the information and ignore all other choices for the time being.

These are my most-used visuals:

- Bar charts for comparisons across categories
- Pie or donut charts (only if there are less than 5 categories to compare)
- Line charts for showing trends over time
- Cards and KPI’s for showing single numbers
- Tables and matrices (only if more detail is needed)

See [this reference](https://www.sqlbi.com/ref/power-bi-visuals-reference) for a complete list of all visualizations available in Power BI and the best way they can be used.

### Placement & Spacing

There is a limited amount of space available on the canvas when designing a report in Power BI. For this reason, it is important to ensure you are making the most of the space available without adding unnecessary or useless clutter.

We are trained to read from left to right and top to bottom. Consequently, when someone first opens a report, their eye will naturally start at the top left corner, unless something immediately pulls their attention somewhere else. This natural human tendency informs us where visuals should be placed in a report – starting at the top and continuing in a logical flow with increasing amounts of detail towards the bottom.

According to the 5-second rule, the most high-value, high-impact information should be conveyed within 5 seconds of opening the report. Therefore, this information should be positioned along the top of the report where the user will naturally see it first. Avoid placing images, icons, or text in this area unless they contain information that is relevant to the user and the report.

Design the rest of the report page with a logical flow in mind:

- Group visuals together that have a common goal. Avoid randomly placing visuals wherever they might fit as this could imply a relationship where there is none.
- Allow space between the visuals to improve readability and to create separation between visuals that convey different meanings and are not related.
- Avoid haphazard size and placement of visuals as this makes it difficult to know where to look first or what to focus on.
- Align the visuals in a consistent manner.
- Do not densely pack the report with too many visuals or too much information.

### Context

It is important to give the user some context for the information they are viewing in the report. This context can easily be conveyed by using comparisons across time or categories. 

For example, if a card in the report states that revenue for the year is $1 million, then context can be added to this by comparing it to last year’s revenue or to the budget. A simple way of adding this context is with color indicating if revenue is above or below budget.

Alternatively, a single measure can be used to quickly highlight the comparison between two numbers: for example, using a percentage change in revenue for this year compared to last year. In this way, using a single number can answer at least two questions at once: is revenue higher than last year and if so, then by how much. Imagine the time lost if a user has to manually calculate the difference between these numbers or if the comparison was not given at all.

### Formatting & Decoration

There are many ways to ‘beautify’ a report – from color and pictures to fancy fonts. However, these elements of formatting and decoration should only be used insofar as they are useful or convey some meaning. This also applies to gridlines in a chart or even borders around the chart area.

One of the most powerful formatting options is color. You can make comparisons and use conditional color formatting to make a piece of information stand out. If it is ‘bad’ information, the user will immediately know where potential issues are that could require action.

However, choose colors wisely – keep it simple and be consistent! Follow these rules when it comes to using color in your report:

- Use colorblind-friendly color palettes – red and green are two of the most problematic colors to use (especially when used together). [Choose color combinations](https://davidmathlogic.com/colorblind/#%23D81B60-%231E88E5-%23FFC107-%23004D40) that do not cause unnecessary confusion. 
- Color should be used consistently across fields or categories so that the color itself carries meaning (create a legend that the user can refer to – the information overlay that we will discuss later on in this article is an excellent use for this).
- Avoid overusing color – having too many colors across every aspect of the report can make it confusing and the user will not know where to focus their attention.
- Avoid any bold or bright background colors as this makes the report hard to read and is not practical if the user would like to print a PDF version of the report.

The last element of formatting concerns fonts and number formats:

- Avoid using multiple or exaggerated font styles – stick to one font throughout all reports.
- Avoid unnecessary text formatting (bold, underline, large font sizes, etc.) as this can increase the noise in the report and the time it takes to extract insights.
- For numbers, use thousand separators (such as 10, 000) or use a compact form of the number (such as 1M for 1 million or 100k for 100 thousand) to improve readability.

## Power BI Key Design Features

The flexibility of Power BI means that you can design a beautiful report that is also very valuable. Using a few simple features you can cut out a lot of noise and keep the canvas free to show only the most important visuals.

Many of the below features can be implemented by making use of the bookmarks feature in Power BI. You can do a lot with bookmarks and I highly recommend [learning more about them](https://campus.datacamp.com/courses/reports-in-power-bi/bookmarks-and-buttons?ex=1).

### Custom page navigation

Traditionally, navigation is carried out by selecting the page views along the bottom of the report. However, by designing your own custom page navigator you can build it in a way that matches the theme and branding of your report. There are many different ways to create your own navigation panel, and some people have been truly creative with it.

The easiest way to add a page navigator is to select the ‘Page navigator’ option under the ‘Buttons’ menu option in the ribbon. This feature in Power BI allows the navigation panel to automatically update whenever a new page is added to the report.

![Power BI Page Navigator Screenshot](https://media.datacamp.com/legacy/v1724173244/image_add64844ce.png)

In the screenshot below, you can see a simple navigation panel that expands when you select the menu icon. This report contains only two pages.

![Power BI Navigation Panel Screenshot](https://media.datacamp.com/legacy/v1724173244/image_452c7e9a01.png)

### Contextual navigation using buttons

Another way to navigate your report is to create contextual navigation buttons in specific locations on the page. For example, in the screenshot below we have created a button that takes you to the Segment Analysis page; and this button is located in the top right corner of the Profit Margin by Segment chart. With this option, the user can quickly navigate directly from this chart to a page that elaborates on specific information given in the chart. .

This navigation method is a good way to add additional, detailed pages which might otherwise be overlooked, and  which keep the navigation panel from being over-cluttered by too many pages.

![Contextual Navigation in Power BI Screenshot](https://media.datacamp.com/legacy/v1724173243/image_c4593b5416.png)

### Creating a custom slicer panel

Similar to the navigation panel above, a custom filter panel can be created that pops out when the filter button is clicked. I like this panel in particular as slicers can take up a lot of space on the canvas and do not offer any value on their own.

![Creating a Custom Slicer Panel in Power BI Screenshot](https://media.datacamp.com/legacy/v1724173244/image_06c0388804.png)

### Creating an information overlay

An information overlay is an excellent way of helping a user to understand the elements of your report from right within Power BI. Before learning about this little hack, I would create a PowerPoint presentation with screenshots of the report in much the same way as shown in this overlay. 

With this hack, you can save yourself and your user a lot of time in learning about a new report or refreshing their memory about an old report.

Just like the other two panels discussed above, this information overlay appears when the user clicks the small info button at the bottom left of the report.

![Creating an Information Overlay](https://media.datacamp.com/legacy/v1724173244/image_3b152b7944.png)

### Creating dynamic titles based on filters

Dynamic titles allow you to show information about the current filter in the title of a chart. 

A dynamic title is obtained by using a measure. The measure for the title in the following image looks like this:

Segment Title = “Sales and Profit Margin for: “ & SELECTEDVALUE(‘Segments’[Segment], “All Segments”)

The key function in this formula is SELECTEDVALUE and its purpose is to return either the value that is selected (in a slicer or filter) or “All Segments” when no selection is made.

In the image below, we have filtered the report to show only the Channel Partners segment; and this filter has dynamically changed the title for the line chart to reflect the selection.

![Creating Filters in Power BI Screenshot](https://media.datacamp.com/legacy/v1724173244/image_e62066a904.png)

### Using tooltips to add contextual detail

Every chart has tooltips that display the exact value when you hover over an element in the chart. However, you can actually use a report page as a tooltip! In the image below, you can see that while hovering over the VTT product, a tooltip appears that is in fact a page from the report with some visuals relating to this product.

![Using Tooltips in Power BI Screenshot](https://media.datacamp.com/legacy/v1724173243/image_bdcff60b5c.png)