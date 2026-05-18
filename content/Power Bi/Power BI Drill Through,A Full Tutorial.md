## What Is Drill Through in Power BI?

Drill Through in Power BI lets users investigate deeper into a data point of interest on one report page. It enables data consumers to go from a high-level summary to detailed insights tailored to a selected category, item, or dimension.

Drill Through functionality is useful when [reports in Power BI](https://www.datacamp.com/courses/reports-in-power-bi) involve many different levels of detail. Rather than crowding a single page with all available visuals, Drill Through lets you guide the user through layers of insight progressively.

## Why Use Drill Through for Deeper Insights?

Drill Through provides a more interactive, [self-service analytics](https://www.datacamp.com/podcast/self-service-business-intelligence) experience. It enables report users to take control of their own explorations and answer their unique questions without modifying the core report structure.

### Key benefits

There are several key benefits of using Power BI Drill Through: 

- Granular exploration: Enables users to deep dive into entity-specific data (e.g., a single customer, store, or transaction).
- Improved UX: Reduces clutter by separating summary and detail views, improving navigation and comprehension.
- Contextual storytelling: Drill Through pages can be tailored to specific business questions or KPIs.
- Cross-report functionality: Supports modular report development across multiple files in Power BI Service.
- Actionable analysis: Facilitates data-driven decisions by putting relevant data in the spotlight for individual data points.
- Scalability: Makes it easy to reuse report templates and drive consistency across departments or teams.

By empowering end-users to drill into their specific area of interest, Drill Through bridges the gap between static dashboards and dynamic analysis.

## How to Set Up Drill Through in Power BI: Step-by-Step

Creating a Drill Through experience in Power BI involves setting up both source and target pages, configuring the necessary fields, and integrating navigation tools like back buttons and tooltips.

### Step 1: Create a mock finance dataset

For this tutorial, we'll use a mock finance dataset throughout to demonstrate Drill Through concepts.

![dataset](https://media.datacamp.com/cms/ad_4nxesirvqwumob3csfaitepnm6ipa3h1dc6p7vidaqrcmbls24m28o6yxy_wb2gmqqmq0_8yblumqv_ncw3yqlpiik_h9bkbdeq-zu1goffhgjmfdwnfnhvuxeatgvsr3qp13rx8jvw.png)

Here’s a Python script using `pandas` to generate a sample dataset you can export to CSV or load into Power BI:

```python
import pandas as pd
from datetime import datetime

# Sample data
data = [
    ['TXN001', 'Asia Pacific', 'Singapore', 'Finance', 'Travel', 'Airfare', 1200.00, '2024-05-12', 'Alice Tan'],
    ['TXN002', 'Asia Pacific', 'Singapore', 'Marketing', 'Events', 'Venue Rental', 3500.00, '2024-05-14', 'Ben Lee'],
    ['TXN003', 'Europe', 'Germany', 'Operations', 'Logistics', 'Freight', 2600.00, '2024-06-01', 'Clara Müller'],
    ['TXN004', 'North America', 'USA', 'Finance', 'Training', 'Workshops', 800.00, '2024-05-18', 'Daniel Smith'],
    ['TXN005', 'Europe', 'France', 'IT', 'Software', 'Licensing', 4500.00, '2024-06-04', 'Emma Dubois']
]

# Define column names
columns = [
    'TransactionID', 'Region', 'Country', 'Department', 'ExpenseCategory',
    'SubCategory', 'Amount', 'TransactionDate', 'ManagerName'
]

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Convert date column to datetime
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])

# Save to CSV (optional)
df.to_csv('FinanceTransactions.csv', index=False)

# Display the DataFrame
print(df)
```

You can run this script in a [Python environment](https://www.datacamp.com/resources/webinars/setting-up-your-python-environment) (e.g., Jupyter Notebook or VS Code) and import the resulting CSV into Power BI for use in your reports.

You can expand this dataset using tools like Python, or generate it in Power BI directly using Power Query with `Enter Data`. Once created, this dataset will form the foundation for the visuals and drill-through examples throughout the tutorial.

We’ll use a fictional dataset named `FinanceTransactions` to walk through each drill-through concept. This dataset simulates financial transaction records for a multinational company.

Sample Fields in `FinanceTransactions`:

- `TransactionID` (Text)
- `Region` (Text)
- `Country` (Text)
- `Department` (Text)
- `ExpenseCategory` (Text)
- `SubCategory` (Text)
- `Amount` (Decimal)
- `TransactionDate` (Date)
- `ManagerName` (Text)

We'll create:

- A summary page showing total expenses by `Region` and `Department`.
- A drill-through target page showing detailed line-item transactions by `ManagerName` or `SubCategory`.

### Step 2: Create a source page and a target destination

Next, to ensure our Drill Through works properly, we’ll need to set up a source page and a target page.

- Source page: This is the primary report page where Drill Through is initiated, typically containing summary-level visuals like bar charts or matrices.
- Target page: A dedicated report page designed to display filtered details based on the user’s selection.

To create the source page, rename the current page as “Overview” and press Enter.

To create the target page, have a look at the bottom of the screen,  and click on the green “+” button to add a new page. Double click on the new page and rename it as “Manager Info”

This target page will be used to show more information about which managers are in charge of the transactions.

Here’s what your pages will look like:

![source and target pages](https://media.datacamp.com/cms/ad_4nxfaqbzwlwyzf2efvsiph9mzxvpv5qdzkzfmg554da91sovi1jd-nucqmjk6filjcruhg8hmzuqrzcg7gyvo8tjyzke-p_mkdjswszweo28qbxjozogcmmkf-rtfwblk318mudc8jg.png)

### Step 3: Add relevant charts

Next, we’ll add some relevant charts to our source and target pages.

For our example, using the `FinanceTransactions` dataset:

In the source page, we’ll create a simple stacked bar chart that we will be using to drill through the data. For this chart, use the following fields: `Amount` and `ManagerName`.

Your chart should look something like this:

![source page chart](https://media.datacamp.com/cms/ad_4nxfliwfoujubtjqyrcwy8ztbwf8xuz3j8su8s7kwzerpzcstampw88m6gz451ytwmpw-wn81pstzpibor1vovgdje0d0o6zeqhqmgjcbmwfa7ocuivu4qcvhza1x7llmbmvw4fmwpa.png)

As you can see, the source page displays a stacked bar chart of total expenses by `Department`.

In the target page, create a matrix with the following fields: `Amount`, `ManagerName`, and `TransactionDate`.

Here’s how it should look:

![target page example](https://media.datacamp.com/cms/ad_4nxfz2qrb4vqlmsgcc7qxzsbsuhq0sg9uk-xxlwn6ldekcoxuvvy05nemk_vfx6jrxuswr5bf_04hheyng9jcivwnkzrg8ihorqvrlrm_sxjuzdda1vj9py0ghhrm91bym-p98op_3g.png)

Now, our target page displays a matrix of detailed rows of expenses and dates.

### Step 3: Add Drill Through fields

1. Go to the target page in Power BI Desktop.
2. Open the Visualizations pane and drag your desired column (e.g., `ManagerName`) into the Drill Through section.

![adding drillthrough](https://media.datacamp.com/cms/ad_4nxf3aritzw3z8hyl8l75g7urziccev7mrupqf0rpuee6gwpbgpt5bqo0cxtgfnw4iamrt-bqtln-cfztliqrqgjd6eoyzwjwstiql74knbpligbw_p6xzpyhs9z0bqdmuegkoaos_a.png)

As you can see in the screenshot above, the `ManagerName` field should be dragged into the Drill through section.

3. You’ll now see a special filter field appear, allowing only Drill Through interactions to this page.

Here’s what you should see:

![drill through filters](https://media.datacamp.com/cms/ad_4nxeefaamu2a_bbvz3-azfn6izd_ykbygb5ehnibfchwdbaw2zfhdmtco3nxr5j7lkpr9wdwqqz5k8mpcolgdtpjgwyxoe9jgfd6-mmght1gpfyfaqagrkngnyjbundeomim4bwr3.png)

4. Enable Keep all filters if you want to retain slicers or filters from the source page (like `Region` or `ExpenseCategory`).

Be aware that Drill Through only works when the selected data point matches the field placed in the Drill Through well. It’s also case-sensitive for text-based columns.

In this case, it’s the `ManagerName` field that is consistent in both charts in the source and target pages.

### Step 4: Configure visuals and performance

Choose visuals for the target page that are:

- Context-rich: Use cards for KPIs like total expenses, tables for line items, and bar charts for category-wise breakdown.
- Purpose-built: Show only visuals relevant to the filtered dimension.
- Performance-optimized: Avoid overly complex visuals or excessive DAX calculations.

For example, you can use KPI charts like this:

### ![KPI card example](https://media.datacamp.com/cms/ad_4nxdeer82abootbys7i8w5yfns8olx8slpumqpx-px6agvqmhh3z1zknshbximg3rrtpwbwunarbfjyyflvxeo3j7yxiau0flpm4eriffgdfl1ksn3dawdhovdkz-curwjifldga3yw.png)

You can improve responsiveness by:

- Using summary tables instead of raw data.
- Reducing the number of slicers and bookmarks on the page.
- Leveraging Power BI’s Performance Analyzer tool to test visual load times.

### Step 5: Set up navigation with back buttons and tooltips

Drill Through pages should always include a way to return to the main report.

By default, Power BI will create a back arrow button to return to the source page upon creation of a Drill Through. This button will only appear once you’ve drilled through, and it looks like this:

![](https://media.datacamp.com/cms/ad_4nxfodiwilh75kacalxnskhb06abrd7yyp4_mjyolu6dqnrlyjc7qe7inokbgc3zhz3xhq24jb7if4n0kkdbhltfxkwr_foos3gwh9ylxakpmgwblyrh64846e_g8pswj_vukjbekhg.png)

1. Click Insert > Buttons > Back.
2. Enable Action on the back button and set it to type Back.
3. Customize the icon, color, and placement.

Additionally, tooltips can be set by:

- Adding tooltip text to the page or visual.
- Using a tooltip page with its own visuals.

This ensures that users understand the purpose of the Drill Through and can navigate intuitively.

### Step 6: Test Drill Through

Lastly, before we’re done, we need to test out our Drill Through function to see if it works.

Before we start, I would like to recommend using Modern Tool Tips in Power BI. To turn on modern tooltips in Power BI, you need to navigate to File > Options and settings > Options > Preview features and select the Modern visual tooltips checkbox. After that, restart Power BI Desktop for the changes to take effect.

To begin testing: 

1. Go over to the source page and hover over any bar in the bar chart. In this case, we can look at the largest bar. Upon hovering, a Drill Through button will appear below your tooltip.

![drill through test tool tip](https://media.datacamp.com/cms/ad_4nxeun9vgvreaf-pq0pzuo4jlrucfmn0dpdzsku0ivv-lr4dvflmikvxxn17au4pgaomiydx-xmp81y0uyojnyty93hf7ubtjcxvpo38_ru9ousrygnikexmkbqoj2htz8mjmfyg3.png)

2. Hover over the “Drill through” button, and an option for our target page `Manager Info` will appear.

![drill through test tool tip target page](https://media.datacamp.com/cms/ad_4nxe4deepropbmxbv-qxlk7yoqtklvpeggziuvffe_qbnkwg-eo2itrndyokbfegtxzwvt6hzlhgaqi5fiporook0qqt-nvpj9-b_faaid4et-kebgogmmiorjgo701p-wzsgzu9q.png)

3. Click on the `Manager Info` option and this will take you to the target page will filters applied.

You should see the following result:

![drill through testing target page](https://media.datacamp.com/cms/ad_4nxfzl1fa2fz7nbzoocqvkeiqoasskxivvxa1kuwcdrmmstzznhkvshsizno5ieivmhjg4s8xj-3r9z6yxmpe4v7f3xkaxnqz4y8sxfc4tzoydh5hanqxpebqspymooibhipkp-aezw.png)

This means that the Drill Through has successfully been created.

## How to Enable Cross-Report Drill Through

Cross-report Drill Through allows users to navigate between separate Power BI reports while preserving filter context. This is useful when breaking down [Power BI dashboards](https://www.datacamp.com/blog/9-power-bi-dashboard-examples) into modular parts by function or department.

### In Power BI Desktop

1. Ensure both the source and target reports are built using fields with matching names and data types. For reliable cross-report Drill Through, it's best if both reports use a shared or certified dataset to ensure metadata consistency
2. Open the target report, then go to File > Options and Settings > Options > Report Settings.
3. Under Current File > Report Settings, enable "Allow visuals in this report to use drillthrough targets from other reports".

![cross-report drill through](https://media.datacamp.com/cms/ad_4nxfxxugxd4xf-jhq-krjs6che-kzesfhwbm0lsaxyxxpgoi04yswabqn_92ks_sagpqwpprdvcsj3fs0iourbbddaxjtcqp1s5rm59yweoz6tzvchq-dan_qtj98iq0dotgmoxkz4a.png)

4. Publish both reports to the same workspace in the Power BI Service.

### In the Power BI Service

1. Open the published source report in the Power BI Service.
2. Right-click on a visual using the shared field (e.g., `ManagerName`).
3. Choose Drill Through > [Target Report Name].
4. Power BI opens the target report, applying the filter automatically.

## Advanced Techniques for Drill Through

Drill Through becomes even more powerful with [DAX](https://app.datacamp.com/learn/tutorials/power-bi-dax-tutorial-for-beginners), conditional logic, and custom behavior.

### Dynamic Drill Through with DAX parameters

You can create a DAX measure to pass dynamic filters based on user selection. Example:

`SelectedManager = SELECTEDVALUE(FinanceTransactions[ManagerName])`

[](https://app.datacamp.com/workspace)

This can be used to:

- Display custom messages on the target page.
- Control visual behavior with conditional formatting.
- Create bookmarks that respond to slicer values.

For more information on DAX measures, here’s a cheat sheet you can follow:

![DAX cheat sheet](https://media.datacamp.com/cms/ad_4nxci05raoscrjv-y0vdepnd4u-dkniqwhximyeyhvl70ooi6ofvg1vmmrig0nfogtw3q0cxgi72oivqdju6vvx5ciybphv9swf3o2rldmssce-gykacrxqyk3cpg8we6birhoeheda.png)

Source: [DAX Cheat Sheet](https://www.datacamp.com/cheat-sheet/dax-cheat-sheet)

### Handling multiple selections and data points

Power BI Drill Through does not support multiple selections by default. If a user selects more than one data point, the Drill Through option will only show the result of one selection.

Workarounds:

- Use a slicer or filter panel on the target page.
- Add a summary table to show high-level values for multiple items.

### Optimizing Drill Through performance

Performance issues can arise if target pages are overloaded. 

Here are some tips to optimize performance:

- Use Import mode instead of DirectQuery when possible. This will lighten the data model.
- Minimize the number of visuals. Instead, create buttons to navigate to other charts when needed.
- Pre-calculate metrics in Power Query. This allows them to be stored in the model instead of being calculated as a measure.
- Avoid complex DAX expressions in visuals.

## Tips and Best Practices for Power BI Drill Through

Drill through is a simple technique that works well most of the time. However, there are some tips to make things faster and more understandable.

Let’s look at them below:

### Design recommendations

Since Drill Through requires action from your users, some design aspects need to be considered.

Some tips for design are:

- Use consistent page names (e.g., "Manager Detail", "Transaction Details").
- Label visuals clearly to reflect applied filters.
- Add help tooltips or a legend to guide users.

### Common issues and troubleshooting

Here’s a summary of how to troubleshoot problems for Drill Through.

|   |   |
|---|---|
|Problem|Solution|
|Drill Through is not available|Ensure only one data point is selected and a valid field is in the Drill Through well.|
|Filters not applied|Check data type compatibility and relationships between tables.|
|Slow performance|Reduce visual complexity; aggregate or pre-filter data.|

## Real-World Applications and Case Studies

Drill Through is powerful in driving deeper business insight since it lets you dive deeper into the actual numbers to take action based on the data.

This applies to several sectors:

### 1. Retail

- Scenario: A retail company uses a sales summary page by region. Managers can drill through into detailed sales by product and employee.
- Benefit: Quick insights into top-performing products and team members.

### 2. Healthcare analytics

![healthcare dashboard example](https://media.datacamp.com/cms/ad_4nxdzrx4sqndxt1kbxteqhxlpkxyytdu5utq2yifo5q6echhsbvqsj6r8o7hdrjin8x2tvvga_stmbz99elby_zcog4mh-bfwbco-wpzneyl7ejkpazilcbf9zjwfl2xmedfv-zdbma.png)

Hospital emergency room decision dashboard. Source: [Microsoft Fabric](https://appsource.microsoft.com/en-US/product/power-bi/powerapps_cxo.powerbi_healthcare?tab=overview)

- Scenario: A hospital dashboard shows admission counts. Users drill into patient-level views by treatment category.
- Benefit: Enables physicians and administrators to monitor effectiveness by procedure or specialist.

### 3. Financial services

- Scenario: A finance team dashboard summarizes spend by department. Executives drill into detailed expense lines by subcategory and project.
- Benefit: Better cost control, improved transparency, and targeted budgeting.