## What is a Waterfall Chart in Power BI?

Let's take a moment for a closer look at waterfall charts.

### Understanding waterfall charts

A waterfall chart, also known as a bridge chart, visually represents how a factor is affected by a series of increases and decreases over a specific factor. It shows the changes in a variable from the initial starting point to the final stage. The waterfall chart also shows the cumulative effect of positive and negative values on a starting point.

The name, as you might have guessed, comes from the way the chart visually resembles a cascading waterfall. As you will see in the examples below, instead of having all the bars start from the x-axis, they appear to float and build upon one another, creating the effect.

### Critical components of a waterfall chart

The following are the various components of the waterfall chart:

- Starting Point: This is the waterfall chart's initial value and first column.
- Upward Columns: These columns represent factors that contribute to the increase of the initial value.
- Downward Columns: The downward columns represent factors that contribute to decreasing the initial value. 
- Endpoint: This is the final result of a waterfall chart, which has the accumulated effects of the upward and downward columns. It is also the last bar on the chart.
- Intermediate Steps: They are additional bars that show the breakdown of the upward and downward columns influencing the final value. 
- Color Coding: This helps to differentiate between the upward and downward columns in a waterfall chart. Upward columns are represented mainly by green, while red represents the downward columns.

Imagine a company’s CFO needs to explain to the board of directors why the company’s net income decreased from the previous year. A waterfall chart would illustrate the following:

|Component|Factor|Value|
|---|---|---|
|Starting Point|Last year’s net income|$10 million|
|Upward Column|Increase in revenue|+$5 million|
|Downward Column|Increase in cost of goods sold|-$3 million|
|Downward Column|Increase in operating expenses|-$2 million|
|Downward Column|One-time legal settlement|-$4 million|
|Downward Column|Increase in tax expenses|-$1 million|
|Endpoint|This year’s net income|$5 million|

![Waterfall chart image illustrating the above example](https://media.datacamp.com/cms/ad_4nxfc81258avpc9vgquqblr5mdai-avd5xk0gbsbcyrsrf31gfcsr1huzfy5zqsh8ri6if-fwm-nfnmnf0e7rldlkkr_y3ccg3-5yym0h_zopkmrkj5uglpevjqtqq2ch-mjwmpyq7-irqexvj-uezfxwabhd.png)

Waterfall chart explaining a company’s revenue decrease in millions. Image by Author  
  

## Creating a Waterfall Chart in Power BI

In this section, you will create a waterfall chart using the [supermarket sales](https://www.kaggle.com/datasets/akashbommidi/super-market-sales) dataset to investigate products driving the most profit. Before you continue, ensure you have [Power BI Desktop](https://app.datacamp.com/learn/tutorials/tutorial-power-bi-installation) installed on your PC.

### Step 1: Importing and preparing your data

- Import the `supermarket_sales.csv` file into Power BI.
    
    - Go to the File tab on the main menu.
        
    - Click on Get Data.
        
    - Select Text/CSV as your data source. 
        

![GIF showing how to import a CSV into Power BI](https://media.datacamp.com/cms/ad_4nxeyyhsjcfhg1w-5qmnziclfxj6zbhugc0x8hv-xjljwgm_sfan3_0r5uxlzgffswqjnqk3xybfoqy8pzxoemve61cy6nw05ckfocccvvplqk4fgrwuhogx_0gwstzxzgunq78nnj_mesz5q8gfdq7zzphv1.gif)

Import data into Power BI. Image by Author  
  

A window will pop up, showing a preview of the variables in the data and providing options to Load or Transform the data.

- Click Transform Data on the window to open [Power Query](https://www.datacamp.com/cheat-sheet/data-transformation-with-power-query-m-in-power-bi).

![GIF showing how to load the supermarket sales data into Power Query window](https://media.datacamp.com/cms/ad_4nxfgs2nq6cvipykiou2fp81ijvrd6ryrb2xog8as3elkbshxjd8znbey2gc53bxcay7dgnswg3ljmoghldwzwbe5db8duj2be1clflzriho15ih58mgsla6rpeg8jpf4wk_ajv53s9y3ovzdb_69yws0uxdt.gif)

Open the Power Query window. Image by Author  
  

From the Power Query window, you can see that the data has  17 columns and 1,000 rows. Power Query cleans and transforms data before loading it into Power BI. Since the data we are to work with is already clean, there is no need for cleaning or transformation. Check out [Data Transformation with Power Query M in Power BI](https://www.datacamp.com/cheat-sheet/data-transformation-with-power-query-m-in-power-bi)  to learn how to clean data in Power Query, in case you need to go through that step.

- Click on Close & Apply on the Home tab to apply any changes to the data and close the Power Query window. 

![Image showing how to close the Power Query window](https://media.datacamp.com/cms/ad_4nxdwutqxozrs6fmyjxvhyddyi9a982cz9xuo6t3ekvpa5pdvn4pybcpehgipynapyxad55kzcxrh63kyrmyky45lzlo5qkocsegnueqylvof0khygdnfzfr5acasapbynsgnijdqbq1irco7kfbf4eoikji.png)

Closing the Power Query window. Image by Author  
  

### Step 2: Creating a basic waterfall chart

To create a waterfall chart, you first need to create a [Measure](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-measures) that you can apply to any visual. Measures in Power BI are calculations created using DAX Query. In this context, we will calculate a measure of Total Profit and use it to create the waterfall chart through the following steps.

- On the Data pane, right-click and click on New Measure. Create the **Total** **Profit** measure by pasting the following DAX syntax on the editor provided to you. The **Total** **Profit** is the sum of the gross income from all products, which is the total profit made from each sale.

`Total Profit = sum(supermarket_sales[gross income])`

[](https://app.datacamp.com/workspace)

![Image showing how to create the Total Profit measure](https://media.datacamp.com/cms/ad_4nxccdturetopx8wvwuzcnxeotqgh5ez1qqpq37wrtgxagds_n_dry385huqqqpd2vcxt55ygmmkxhnlloguhpzqi2h-wt9wjxotbunbymbjgmtvcndkdbmnb4beuomkw5gkri9bglb3vefl65ay6ltxaonqn.gif?f=png)

_Create the Total Profit measure. Image by Author_

- On the Visualizations pane, click on the waterfall chat icon. An empty chart will appear on your canvas.

![Image showing the waterfall chart icon on the visualizations pane](https://media.datacamp.com/cms/ad_4nxeyo00mj0vqm730kqsfv6d2ah2vphd2ow9t7jqylmer00j75cjmxtbhr00jag04spdtlmhs25ku0etyzd19t4ps14n2t0x8wf6yxhh76i3ycgwcribaayb3u73mobtecbqu82ftmlh5qroacqfqag-1d7g.png)

_Waterfall chart icon on the visualization pane. Image by Author  
  
_

- Select the empty chart and drag the **Total** **Profit** measure to the Y-axis field of the waterfall chart.

![Image showing how to add the Total Profit to the Y-axis of the waterfall chart](https://media.datacamp.com/cms/ad_4nxdc0juczpiwcqjfnpfi5pn-w2u0p14etbghvgdx1138jn5klpvgytd1jh1s8ggszvpfweydv89nluks0zzfe-nf3ij3svhstyrdcycyyj9b7ohuxpadwbbbcekzo4onoexkbfwzukz7m-wigrsdc1lff26w.png)

_Add the Total Profit measure to the Y-axis. Image by Author_

- Drag the Month variable into the Category field of the waterfall chart.

![Image showing how to add the month category into the waterfall chart](https://media.datacamp.com/cms/ad_4nxcofo0uoulso9l0i5atr7jd4-5-jdbuqnj9ov20sn5korsows4dsx1diianram9nmg-kun--jigekv69woqhoron3zwjtt6l8djylksqwseujisqpseerug01hkl29zzf6t-vxstp7edrmeruj6h7tchcde.png)

_Add the Month_ _category to the waterfall chart. Image by Author_

The waterfall chart shows each month's contribution to the overall profit gained from January to March. You can follow the same procedures and visualize for other categories, such as **Gender**, **Product line**, and so on.

### Step 3: Exploring and customizing the waterfall chart

To explain the variances in each month, you can add breakdowns based on another category. Let’s use the **Product line** category to see the profit difference between two consecutive months. To add a breakdown, drag the **Product line** variable to the Breakdown field of the waterfall chart. 

![Image showing how to add the Product Line as breakdown into the waterfall chart](https://media.datacamp.com/cms/ad_4nxdrfmwaypuk_ayin52n3nncmmauuib189nmhfnhoupsaa0pkvmljesbbnke-nmf07t9y7vkfx3uqk-b9m4xo5ahojnxtckdaaxlvnxtlqlsmmx94khigfbrwgaymgz8sqlgkr0fetz8hs1vd4vv6bt4rqud.png)

Add breakdown to the waterfall chart. Image by Author  
  

By adding **Product line** as a breakdown to the waterfall chart, the columns now represent the difference in profit between the current month and the next month. If the profit in the next month is higher than the current month, it shows an increase signified by green, and it's red if it moves in other direction. The waterfall chart groups other categories in the **Product line** as **Other**.

One cool feature about Power BI: If you hover over each chart column, you will get information about the percentage increase or decrease between profits for two consecutive months. You will notice, for example, that the highest profit increase was in food and beverage products between January and February, with a change of 2.2%, while the lowest was in home and lifestyle products, with a decrease of 39.33%.

![Image showing how to get numerical information from a waterfall chart by hovering over the columns](https://media.datacamp.com/cms/ad_4nxeywdtpbv1awxlwxrv8uaghazrx9xrkuzc-f6sqfn-h1v7kvpjh2ja5s1vdnoys1n0rmb6e1xlcsf4mdqehs_h1jdt7bgvdek2c_ky_samwmvxof2mnkezemrmjqp039gdgx_t4qq1jq3bbs6ke27a_rlq7.png)

Hover the waterfall chart to get numerical information. Image by Author  
  

You can customize the waterfall chart by setting the number of breakdowns in each column. 

1. Click on your visual.
2. On the visualization pane, go to Format your visual.
3. Click on Breakdowns and set the preferred number of breakdowns. The maximum number of breakdowns you can set is the number of categories in the breakdown variable.

![Image showing how to customize the breakdowns in a waterfall chat](https://media.datacamp.com/cms/ad_4nxcnnrn0gt9zix7ucniwb7lfqpcrl3xjxnux8-uykr-73wz2a4k1qxf6coyo0ntrwwu1iowyuvgdds4slfh0_zsgrym3o3sla6e2sdz76g5nw35v52py3wjampefq9kt1kbd2ggafzt6xl1aw25nrrwxzp_w.gif?f=png)

Customize the breakdown numbers. Image by Author  
  

### Step 4: Sorting the waterfall chart

You will notice that the waterfall chart is sorted chronologically by month. You can change the sorting to get different perspectives of the data.

On the waterfall chart, click on More options, then Sort Descending. This will change the sorting of the **Month** category to reverse chronological order. 

![Image showing how to apply sort descending to a waterfall chart](https://media.datacamp.com/cms/ad_4nxcp1zuvs_k7df5tzqohb1vm-i9ef0c1prxcfmtwxoks5o4ajol3zk2mppwfje95fxe6cpnnbn1ttgvbcdo9z9cngxb1vfd5ckj3pbte-t6rkjpi6dtrfd8gw7_dze6evslfuo0nipmf-9ntj5yq_tw699ax.gif)

Apply sort descending. Image by Author  
  

You can change the axis used in sorting from Month to **Total** **Profit** by clicking on More options on the visual, then Sort, and selecting the variable or measure to sort by.

![Image showing how to change the sorting variable](https://media.datacamp.com/cms/ad_4nxddywllssckmhdhxiryjq3fiahppukvufyukpeppkxz51ze1dhuu1p9vv-wj7ea-kmxa-xmry-ctdad2g-f67gs19uz6ju3grej3j8gcitzpp7fljnct-bt4qrkggj0uh3esqiksafcg7ldrnfzeyv9flc.gif)

_Change the sort variable. Image by Author  
  
_

When you apply sort ascending by Total Profit, the chart will display the columns of each month starting from the lowest to the highest and from the highest to the lowest when sort descending is applied.

### Step 5: Adding advanced customizations

Power BI offers many options to customize the waterfall chart to better suit your narrative—these range from changing the chart colors to adding labels and filters. 

#### Change column colors.

Colors make it easy to distinguish between increases and decreases in the waterfall chart and also make your visual more aesthetic. Change the colors of the column:

1. Click on your visual.
2. Go to Format your visual on the Visualizations pane.
3. Click on the Columns dropdown to display various options to customize the columns in the waterfall chart.
4. Select the Colors dropdown to customize the columns in the waterfall chart.

![Image showing how to add colors to a waterfall chart](https://media.datacamp.com/cms/ad_4nxedso9o_gtw0xerwboy7gxvdjltz-4mcyyzxhuk_gsa0swbzomfgttr6be5sjhjok4kzjvu-zs9g5krucwpolesfzaq_icwpdbaeyom721viqunncathmpeoasvampqxzabrt3zdg7gxt6gfvcnivcy53c-.gif?f=png)

Add colors to the waterfall chart. Image by Author  
  

#### Add labels

Data labels allow anyone viewing the visual to know the actual value of each column, which is essential if you have columns of similar heights in your chart.

1. Select your visual, and go to the Visualizations pane.
2. Click on the Format your visual tab.
3. Turn on the Data labels toggle.

The waterfall chart will display the value of the profit difference between two consecutive months for each product. 

![Image showing how to add data labels in a waterfall chart](https://media.datacamp.com/cms/ad_4nxemyjqn2lppom4jlwtkwmjucu03bwbwtiiycrtcfxbtsc0ed5z1prtckb1rkrgnmwcwlw3bze0sk9wdo1zqfbfs80l7uqgnlbysvz_ivclr9h4v26nfzkimfalhctiipqd5ox6hko68hoke1dswocwvpfz3.png)

Add data labels to the waterfall chart. Image by Author  
  

#### Adding filters

What if you want to know what the whole waterfall looks like for a particular category? This is where filtering comes into play. You can filter your visual to show information about a single category. For example, you could filter the waterfall chart by applying the **Customer** type variable.

1. Select your visual and go to the Filters pane.
2. Drag the **Customer** type variable into the Add data fields here field on the Filters pane.
3. Under the **Customer** type column in the Filters pane, you will see a list of all the categories. Select any category to see a waterfall chart for that specific category.

![Image showing how to apply filtering to a waterfall chart](https://media.datacamp.com/cms/ad_4nxciug2igpd8prmrythav0kc8-gw7jyiblzusqfr762zg1flh5mthy9ng6i5n7mvqb2mbi2yso0q8quxjifuxy_lg6ucghs75yxaljyffn_ozfeccsdxxyn3hqfzmz6waigrme-ipek7nnolml8dmevqxrgs.gif?f=png)

Apply filtering to a waterfall chart. Image by Author  
  
  

## Best Practices for Power BI Waterfall Charts

Consider these subtle enhancements that can transform a straightforward waterfall chart into a more refined, insightful visual:

### Tips for clarity and readability

- **Dynamic, Contextual Tooltips**: Go beyond the default data labels. Create custom tooltips that not only show raw numbers but also provide context—like historical trends, relevant benchmarks, or even brief annotations. This layered information can reveal insights without crowding the main visual.
- **Precision in Cumulative Calculations**: Waterfall charts build on successive values, so rounding can introduce visual artifacts that mislead. Fine-tune your precision settings and be mindful of how small rounding differences might impact the overall narrative.
- **Refined Color Saturation**: Rather than simply assigning a distinct color to each category, play with saturation and brightness. Use a more saturated color to draw attention to key contributors, while subtler tones can indicate minor changes. This layered approach can make your chart more intuitive and reduce reliance on labels alone.
- **Integrating Reference Lines or Benchmarks**: Embedding a faint reference line for industry averages, targets, or historical medians can add a layer of context. This gives your audience a baseline for comparison, turning raw cumulative values into actionable insights.
- **Adaptive Layout for Varied Displays:**Consider how your waterfall chart will look across different devices and screen sizes. Subtle adjustments to bar width, font size, and spacing can make a difference.

### Common mistakes to avoid

Also, try to avoid some common mistakes.

- Using Waterfall Charts for Unmeaningful Categories: Imagine using a waterfall chart to show different characteristics of cars, such as speed, weight, price, and fuel efficiency. Adding or subtracting these unrelated metrics wouldn’t produce a meaningful result, and the cumulative total would not make sense.
- Overcrowding: When using breakdowns to explain variances between columns in your waterfall chart, make sure you don’t overcrowd the chart with too much info. Let’s say you have a variable with ten categories. You can add a breakdown of five, where the fifth category would encompass other categories not visible in the waterfall chart to prevent you from overcrowding your chart, making it a bit more simple.
- Not Sorting the Data Properly: By sorting your waterfall chart, you make it easy for your audience. Let’s say you are working with a month category. For this category, sort it in chronological order, not by value. But in cases where you are not working with a category with a defined chronological order, you can instead sort by the value in ascending or descending order.

## Conclusion

The waterfall chart is famous because it can show the pattern of a variable from baseline to a final value while showing the contribution of other factors over time. Maybe, no other chart does this quite as well, which is why is has gained wide acceptance and use in finance and project management.

In this article, you have learned how to use Power BI to build and customize your very own waterfall chart. You have also learned the best practices to follow and pitfalls to avoid. Browse through [DataLab datasets](https://www.datacamp.com/datalab/datasets) to keep practicing the steps covered in this article.

You can also check the following courses to learn more on Power BI.
up:: [[Power BI MOC]]
