## Getting Started with Power BI Pivot Tables

To get started with pivot tables, we first need to import our data, and then we can start creating a pivot table using the matrix visual.

For a step-by-step guide to importing data, check out our [Power BI tutorial for beginners](https://app.datacamp.com/learn/tutorials/tutorial-power-bi-for-beginners).

### Setting up your data

We use a mock dataset for this section to keep things simple. 

To import this data into our data model, we combine manual data entry with importing an Excel file containing sales data. We can do this by clicking "Transform data" to open the Power Query editor, and then we can select "Enter data" for manual data entry.

![Power BI - enter data manually](https://media.datacamp.com/cms/google/ad_4nxdczdm1dpfosutsixh9b_rwnggcjphlmdcw06suyzpu5o57pwc3hhe46yc1amua57bz86u1jrhnatqv7k0qgelmgc2k8ngm0sy9fps3ey8w0hw9esuqsp8kdx3rlxzorroqs5rp7rbsmbrqbedo0zhrboza.png)

Power BI - enter data manually

Once we've entered our data, we can select "OK."

For the Sales data, Power BI allows us to easily import data from many different data sources by clicking "New Source," and then we can choose Excel as our data source.

![Power BI - list of data sources](https://media.datacamp.com/cms/google/ad_4nxf6k9bstw6znnbngxz0j8e65su2lsibh1nnqrcavo5vcke5dl0ynvcmydo6mg93hpvkyfmk8t7mtvagkzznu-oznns3j6-kow19sjvr108bkkptdzi1tau9hdcphmo_gpc7gqxzwnznxa8zf3oh3bnw1rye.png)

Power BI - list of data sources

### Creating your first pivot table

Now that we have imported the data into our data model, we can go to the Report view and click on the Matrix visual from the Visualizations pane on the right-hand side.

![Power BI - matrix visual selection](https://media.datacamp.com/cms/google/ad_4nxcyy_gfmhdfmim16ncgjjn0_x42gihxzekp1s7qexqcjyw2fkcj_uwrdle8tczi7qrufhhcto93455ebp4mhxighi_fw236kceamjpw9-nj0k7pjcxcz-mjacupm6vc0ik2u0vebgiep0oo7574lbvq9xgq.png)

Power BI - matrix visual selection

This will insert a blank matrix on the canvas.

![Power BI - blank matrix visual](https://media.datacamp.com/cms/google/ad_4nxdeskrhdd-ujfcfb6y_zmcmoscsjivqx11ic0dbixnshwyvtbrxxqjcunjdhrvjtxacda4vlr8rdacmvvebp1opalk0xeai_g4tywcl_wgh28pxgekyw7rflxenwopybiuf16z0v7xzttwd5dccayoypa0n.png)

Power BI - blank matrix visual

We can now start dragging fields from our data model into the matrix. You'll see options for Rows, Columns, and Values.

Drag in the fields you want to use as categories for rows and columns. For our example, we add Product category, sub-category, and Product under Rows, and Month under Columns.

In the values section, we must add the measures we want to analyze. For this example, we want to analyze Sales, which contains the total sales value for each product by month.

![Power BI - product by month pivot table](https://media.datacamp.com/cms/google/ad_4nxc00pgycuhtbdhnzdnuolrwgzx3uwycqlefjurhrdzyldyz_owih9jzowhuw3nvra2_nukys2cxgml1dzrcf-xdyr5dgf7pwfaf3oftwyxrinlx9puiikmape-keax3ubsphjfjsowsqhxzugsypnbue3a7.png)

Power BI - product by month pivot table

Great! We just created our first pivot table in Power BI, showing sales by products grouped into categories and sub-categories in rows, with months across the columns.

## Customizing Your Pivot Table

The matrix visual in Power BI offers a wide range of customization options as well as the ability to sort and filter your pivot tables based on your requirements.

Basic customization options include colors, fonts, alignment, borders, and cell sizes. However, some pre-built style presets also give you a faster way of formatting your pivot tables.

### Formatting your table

The “Layout and style presets” formatting options contain a few pre-built styles and are the quickest and easiest way to format your pivot tables. After you apply them, you can easily customize these presets further.

Here’s a quick preview of the “Minimal” style preset with the “Compact” layout.

![Power BI - minimal style preset](https://media.datacamp.com/cms/google/ad_4nxfsz58ydvt_6cr4czr-6esoblk0stx3dm_z8dbifcofqbjqknhb9del6jhu7sc1nht9cxzrkp3toywe_dkj-qlorgkr9gvl23jhf00z1mie922cqwcfcry3t7w4i_zfpkd9am84bsyhl84zwamzxqr1lqjc.png)

Power BI - minimal style preset

Here’s a preview of the “Bold header” style preset to compare.

![Power BI - bold header style preset](https://media.datacamp.com/cms/google/ad_4nxcjvxt3imdhoibcpuqmxydemn6bzrgmxqghfinwoxdy0spuubnniap11mmqbvocspc5upvhtexi0po2fszhmesvz0jbfopbedcz-xkztsnzebhqlmnur9zk8hzfdrtxgyp3fxtgow_1hdwqsp0kmvdv6fre.png)

Power BI - bold header style preset

### Sorting

Sorting on matrix tables only applies to rows. However, it’s important to remember that your sort is restricted to the drill-down level that the matrix is set to.

For example, if we drill our table down to the Product level, we get the option to sort based on Category, Sub-Category, and Product.

![Power BI - matrix table sorting](https://media.datacamp.com/cms/google/ad_4nxftwatehihkxlpbaiet574aorxcw9og61_a9qvsuu5hesxesi0jjjb-3kcrk2-gq5b4akt4g6zquf7blegoynadjfb7ajjlv9rzovxlnylnilgzzxmmupggcynfkqbybapsdnjde71c58lv-rebr4ug8qdg.png)

Power BI - matrix table sorting (expanded row levels)

However, if we collapse all levels of the matrix table and drill up to the highest level, we would only have that top-most level available for sorting.

![Power BI - matrix table sorting (collapsed row levels)](https://media.datacamp.com/cms/google/ad_4nxfi9_22vhnvmnpqwgeatv64q1prtl4zn6gsqvruutn_riae_ngqluew4kct4lsuktz8pyp-1a85oa9isnom9o1obxwhuu-dflsnvx9wori1kp6ndgqwyb44ak_5fwzew2mm6wz4zb87dh5orvkwmloe72m.png)

Power BI - matrix table sorting (collapsed row levels)

### Filtering

You can easily filter your pivot table by adding a slicer to your report canvas and filtering the matrix visual one field at a time. 

![Power BI - filtering a matrix with slicers](https://media.datacamp.com/cms/google/ad_4nxcmx3wvo4hierb_ivba-dq5intycy6qkkojpcaqoje3jrtnhbuwcimifvmejibxfszewdqijkdkudgiucw7efeapveki5kcki83y9lu0xhqp-xa17_cmsfqneuo5uuwqedgjnyzznntjhprf7hj3s3ozgga.png)

Power BI - filtering a matrix with slicers

Alternatively, by selecting a field, bar, or line from another visual, you can easily cross-filter the matrix visual. These are called interactions, and you can control how visuals interact with each other from the Format tab of the ribbon when a visual is selected.

For example, we can replicate the above filter for the Sub-Category “Stationery” by cross-filtering from a bar chart.

![Power BI - matrix visual cross-filtering](https://media.datacamp.com/cms/google/ad_4nxdshaiaymmah0dfvujw4h4xvdplc7lu_-a1vs_ygurfbyy3fwsnnijvvif8jp1x-mje0ortshtaxoc_fmm_usft34t4rrmm1efqusw0610n950d7nihm-myhb75afbgdw9cuecckqr2sbzvogyxbxphoz5b.png)

Power BI - matrix visual cross-filtering

## Advanced Customization with Conditional Formatting

Conditional formatting is a powerful tool for making only the most important information stand out in your reports. For pivot tables, in particular, conditional formatting can make it significantly easier to glance at a large matrix and quickly pull out insights or identify possible problems.

We have an [in-depth guide on conditional formatting](https://app.datacamp.com/learn/tutorials/guide-to-power-bi-conditional-formatting), so check it out if you want to learn more about using this powerful tool in your Power BI reports.

The easiest way to add conditional formatting to a matrix visual is to click on it and then navigate to the “Cell elements” formatting option. Here, you will see all available conditional formatting options, and it’s easy to toggle them on and off and apply advanced rules using DAX formulas.

You can learn more about DAX through our [Introduction to DAX](https://www.datacamp.com/courses/introduction-to-dax-in-power-bi) course.

![Power BI - matrix conditional formatting options](https://media.datacamp.com/cms/google/ad_4nxdqaibao91agcu9saq34ikvpoqp5q3hwhfxv0dvj4mso_lqttbt8vnzf-oaxs4qmjk9novjjueigxh71pt0idper797aytmhb6zd515dgvogkt2icwfv7ky95xmus6t2j1urvq4o9zug6w0s8rfjzjsblpx.png)

Power BI - matrix conditional formatting options

By adding background color conditional formatting to our fully expanded pivot table, we can immediately pull out the top-performing product and month (highlighters in May) and the lowest-performing (photo paper in February).

![Power BI - matrix visual conditional formatting](https://media.datacamp.com/cms/google/ad_4nxf2rzgaqj5qdxk4bf3vkg2rpaw6d_-uwxowzfa7q7qco5vl0lrsj_s8jutel8babtpxn_9kbw6fh3luvzmskvj2_alpjdto10rarejaeequlu791gxkqtjwcxqsqokkjlndo77x7cngahmypdps_lk693fg.png)

Power BI - matrix visual conditional formatting

## How to Optimize Your Pivot Tables

As data volumes increase, the matrix visual can become a huge bottleneck in your report performance. However, there are a few things you can do to minimize the impact.

First and foremost, optimize your data model. 

Remove unnecessary columns and filter your data using the Power Query editor so that you only import the data that you actually need.

Also, build your data model around the star schema framework rather than the snowflake schema. This will ensure that there aren’t too many additional relationships between tables causing bottlenecks.

Check out our [Data Modeling in Power BI](https://app.datacamp.com/learn/tutorials/data-modeling-in-power-bi-tutorial) tutorial for best practices when designing your data model.

Next, avoid adding too many row and column fields to your pivot tables since this can cause the matrix visual to take extremely long to load, especially for end users who are accessing your report from the Power BI Service.