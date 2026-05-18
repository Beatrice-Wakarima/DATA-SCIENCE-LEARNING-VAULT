## Understanding Conditional Formatting in Power BI

In Power BI, you can apply conditional formatting in many different ways, such as dynamically formatting individual elements in your visuals or changing the font color of data labels and chart titles.

Power BI offers an easy way of applying basic conditional formatting to change the background and font color of cells in a table or matrix. You can also add data bars (which fill the cell with a bar proportional to the value it represents) and icons (such as arrows or shapes) based on the values in the cells of a table or matrix.

The conditions for formatting can be simple (e.g., values above or below a certain threshold) or complex, involving DAX expressions with highly specific formatting rules.

Power BI evaluates each data point against the specified conditions and applies the formatting styles automatically whenever the underlying data changes.

## Basic Conditional Formatting in Power BI

These are the main types of conditional formatting you can apply to the table or matrix visuals in Power BI:

- Background color and font color
- Data bars
- Icons
- Web URLs

![Basic Conditional Formatting in Power BI](https://media.datacamp.com/legacy/v1711536173/image_142c736bed.png)

_Image by author_

### Background color and font color

These options allow you to change the background color or font color of cells or text based on their values. Background color formatting is commonly used to create heat maps within tables or matrices, making it easier to spot high and low values through color gradients.

There are three format style options here. You can apply conditional formatting based on a field value, a gradient, or rules.

![Format style options](https://media.datacamp.com/legacy/v1711536173/image_369361e7df.png)

_Image by author_

#### Field value

Using this format style, you can apply colors based on the cell values or other fields in your data model. This option is more complex since it requires colors to be specified in a column or a DAX measure to work correctly.

We provide an example of how to do this in the next section.

#### Gradient

The gradient format style applies a color scale across the range of values, often from a low-value color through a midpoint (optionally) to a high-value color.

![Power BI gradient format style](https://media.datacamp.com/legacy/v1711536173/image_e2581bcea3.png)

_Image by author_

#### Rules

Rules-based formatting lets you set specific conditions (e.g., greater than, less than, or equal to a specific value) for when to apply certain background colors or font colors. This method offers more control than the gradient and is good for comparing values against a target or predefined threshold.

You need to specify each rule individually with a color that should be applied when those rules are met. Remember to apply each rule in the correct order, especially if your rules overlap.

#### ![Power BI Rules formatting](https://media.datacamp.com/legacy/v1711536173/image_cfddda92de.png)

_Image by author_

Here is an example of how the above rule would look in a table:

![Power BI Rule example](https://media.datacamp.com/legacy/v1711536173/image_1ac0ac2eb5.png)

_Image by author_

### Data bars

Data bars add a horizontal bar within the cell. The length of the bar represents the cell's value compared to other values in the column. This is a useful way of visually gauging and comparing data points directly within the cell.

![Power BI data bars formatting](https://media.datacamp.com/legacy/v1711536173/image_a99e352511.png)

_Image by author_

Here is an example of how the bars look in a table:

![Power BI data bars formatting example](https://media.datacamp.com/legacy/v1711536173/image_52523a4b32.png)

_Image by author_

### Icons

Icon sets are applied the same way we did using the rules format style above, except you can add symbols or icons next to your data points based on the defined rules.

For example, you could use upward or downward arrows to indicate performance trends or, as in our example below, shapes to indicate whether certain targets have been met.

![Power BI icons formatting](https://media.datacamp.com/legacy/v1711536173/image_e1116eaed7.png)

_Image by author_

Here is an example of how the above icon rules look in our table:

![Power BI data icons formatting example](https://media.datacamp.com/legacy/v1711536173/image_ca0a6a575e.png)

_Image by author_

### Web URLs

Although not a visual style per se, this type of conditional formatting allows you to add hyperlinks to your tables based on the URL data in another field. This can be useful for creating drill-through experiences or linking to external resources for additional context.

## Power BI Conditional Formatting Based on DAX Measures

As we saw in the previous section, applying rule-based conditional formatting to your charts is quick and easy with the built-in Power BI formatting menu.

However, what if you have several similar visuals, like cards, for displaying different metrics?

You would have to go through the same process for applying red-yellow-green rules to each card in your report. This is a tedious and highly manual process. Even worse, what if you just need to change the value for when the font color of each card turns yellow?

Instead, you can create DAX measures to define the conditions for when the colors should be applied. Not only that, but you can easily change a single DAX measure, and every visual that uses it for conditional formatting will be updated automatically.

Let's review a simple example using the SWITCH function. If you're unfamiliar with the function or how it works, check out our comprehensive [SWITCH tutorial](https://app.datacamp.com/learn/tutorials/switch-in-dax-for-power-bi).

First, we create our measure, which assigns colors based on the difference between our profit margin and the target.

`Profit Margin vs Target Color =  VAR Diff = [Profit Margin] - [Profit Margin Target] RETURN SWITCH (     TRUE(),     Diff > 0, "Green",     Diff < 0, "Red",     "Black" )`

[](https://app.datacamp.com/workspace)

After creating a bar chart showing profit margin by product, we can go to the formatting pane for our visual. Under the “Columns” dropdown, we can select the “fx” icon to add conditional formatting to the colors of the bars.

![Power BI conditional formatting](https://media.datacamp.com/legacy/v1711536632/image_e79aa2f738.png)

_Image by author_

Like with the background color and font color conditional formatting options, we can choose between gradient, rules, or field value. For this example, we chose field value and added our new measure.

![field value](https://media.datacamp.com/legacy/v1711536632/image_607ecec0ba.png)

_Image by author_

Now, the colors of the columns in our bar chart will change depending on whether the profit margin target was reached.

![Columns in the bar chart with different colors](https://media.datacamp.com/legacy/v1711536633/image_336942b756.png)

_Image by author_

## Advanced Conditional Formatting Based On User Selection

Starting with a bar chart showing the total sales by month, we want to highlight the top-performing months so that they stand out to our users. First, we’ll apply basic conditional formatting based on the top three sales months. Then, we use an advanced technique to make the conditional formatting more dynamic.

![Total sales by month chart](https://media.datacamp.com/legacy/v1711536632/image_ddd09682b0.png)

_Image by author_

### Top 3 sales months

For the first example, we create a measure that ranks the total monthly sales and highlights the top 3 in green while the other bars are gray.

`Top 3 Monthly Sales =  VAR Ranking = RANKX ( ALL(Financials[Date]), [Total Sales], [Total Sales], DESC ) VAR Top3 = IF ( Ranking <= 3, "Green", "Gray" ) RETURN Top3`

[](https://app.datacamp.com/workspace)

To improve the readability of our highlighted bars, we also create a measure for the font color of the data labels. In this case, the top three green highlighted bars will have a black font color while the other bars will have a white font color, essentially hiding those data labels from the bar chart.

`Top 3 Monthly Sales Data Label =  IF ( [Top 3 Monthly Sales] = "Green", "Black", "White" )`

[](https://app.datacamp.com/workspace)

Below is the result of applying this formatting, which is already looking much more striking:

![Total sales by month chart highlight](https://media.datacamp.com/legacy/v1711536744/image_a74556f395.png)

_Image by author_

### Top N sales months based on user selection

In this second example, we take our conditional formatting a step further by allowing the user to select the number of months they would like to highlight in the bar chart.

We can achieve this by using parameters based on a numeric range. Go to the “Modeling” tab in the Ribbon, select “New parameter,” and then “Numeric range” from the drop-down menu.

![Top N sales](https://media.datacamp.com/legacy/v1711536744/image_a6c6195770.png)

_Image by author_

The parameters dialog box asks us to enter a name for our parameter and the minimum, maximum, and desired increment. For this example, we set 5 as the maximum.

![Top N sales parameters](https://media.datacamp.com/legacy/v1711536744/image_37256e1b80.png)

_Image by author_

Once we create the parameter, a new table gets added to our data model.

![Top N sales data model](https://media.datacamp.com/legacy/v1711536744/image_3f75ef0fbe.png)

_Image by author_

Now, we can adjust our measure to use the “Top N Value” measure from this new “Top N” table.

`Top N Monthly Sales =  VAR Ranking = RANKX ( ALL(Financials[Date]), [Total Sales], [Total Sales], DESC ) VAR _TopN = IF ( Ranking <= 'Top N'[Top N Value], "Green", "Grey" ) RETURN _TopN`

[](https://app.datacamp.com/workspace)

We also adjust the measure for the font color of the data label so that it dynamically changes based on the number of highlighted columns.

`Top N Monthly Sales Data Label =  IF ( [Top N Monthly Sales] = "Green", "Black", "White" )`

[](https://app.datacamp.com/workspace)

The result is a dynamically formatted bar chart that the user can adjust as needed:

_![dynamically formatted bar chart that the user can adjust as needed](https://media.datacamp.com/legacy/v1711536819/image_fece8f0901.png)_

_Image by author_

## Tips for Applying Conditional Formatting in Power BI

### 1. Start with a clear objective

Understand what you want to achieve with conditional formatting. For example, if you want to highlight specific outliers in your data, there might be better choices than icon sets. Having a clear objective with your report will guide your formatting choices.

### 2. Use color with purpose

Choose intuitive or meaningful colors for your users (e.g., red for decrease, green for increase) to make your visuals instantly understandable.

Also, consider whether your users may be color blind and improve accessibility in your reports by using color schemes that are distinguishable to all users.

### 3. Simplify your color palette

Use a simple and consistent color palette to avoid overwhelming your audience. Too many colors can be distracting and may reduce the impact of your dashboard.

Reserve strong or contrasting colors for the most important data points you want to highlight.

### 4. Test regularly

Review and test your report regularly with end-users to ensure the conditional formatting is clear, intuitive, and adds value. Getting feedback from your users can go a long way toward ensuring your formatting is clear and easy to understand.

Also, be sure to keep an eye on the performance of your Power BI reports, especially if you use complex DAX expressions for conditional formatting, as they can impact report loading times.

### 5. Iterate and improve

Conditional formatting in Power BI is not a "set it and forget it" task. As your data changes or as you receive feedback from your users, be prepared to iterate and improve your formatting choices to keep your reports valuable and aligned with the original objectives of the report.

## Avoid the Biggest Pitfall of Conditional Formatting in Power BI

Conditional formatting overload.

Find a balance between highlighting key points and overloading your report with so many colors that they lose all their meaning.

Be selective with what you choose to highlight. Too much conditional formatting can make a report busy and hard to read. Focus on key metrics and insights that drive decision-making and tie in with the objective of the report or dashboard.

Use icons and data bars to add context or to simplify the understanding of the data without adding additional columns, charts, or other text. Arrows can indicate trends, while data bars can give a quick comparative view of a column in a table.