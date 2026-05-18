## What is Power BI Report Builder?

Power BI Report Builder is a stand-alone tool provided by Microsoft that allows users to create paginated reports. These reports are formatted to fit well on a printed page and are ideal for operational or printable documents. 

Unlike interactive dashboards in [Power BI Desktop](https://www.datacamp.com/blog/all-about-power-bi), paginated reports are highly structured and are best for invoices, statements, or tabular-style data that spans multiple pages.

These reports can be created using data from a variety of sources and published to the Power BI Service for secure sharing and scheduled delivery.

![Power BI Report Builder Sample](https://media.datacamp.com/cms/ad_4nxet-byhs-lb9tryeygr_dijs1x82dn0fidiegefkmibpdpouladsbwpveakmu5wsy0dw2msag3is_ndbwh2nqyrafxdbq8pg6gwpzkbv8lbiylapkf5bonufap0maltfkye0r57tw-eaac08.png)

## 1. Installing Power BI Report Builder

To create reports, you must first obtain a copy of the latest version of Power BI Report Builder. Let’s run through the steps below.

### Downloading and installing

1. Visit the official Microsoft [download page for Power BI Report Builder](https://www.microsoft.com/en-us/download/details.aspx?id=105942).

![Power BI Report Builder screen](https://media.datacamp.com/cms/ad_4nxevwf9d5dyfxs9iwj-rs_kju5xj56szommtftm9-mduvqgccv17ax_tbfdgryk4t9n7atftu0h4yfltppmtp5b8khj7d0xxhadvcb6xq4eowuhjuszplkyv9nr01rbc3vi3clhvag.png)

2. Click Download, select the installer file, and run the installation wizard.
3. Follow the on-screen prompts to complete the installation.

Once installed, launch Power BI Report Builder from your start menu. You should be greeted with this welcome screen, as shown below.

## ![launch screen](https://media.datacamp.com/cms/ad_4nxdoyqupeuc15_uoag84a6kskegivody8ht1d09utwiqh9wlm7xqtfnwee67mz7sx6nv5h1p_y0stpv4a_pqjkfr9txpary9lob5qa7zapu8x4xvbuipqfs9dzd_nrg-lhhhmkrw5q.png)

Next, sign up for a free Power BI account and sign in to your account in the software.

## 2. Connecting to Data Sources

### Creating a data source

A data source is your connection to a database or service, such as SQL Server, Azure SQL, or Power BI datasets.

1. Go to the Report Data pane (on the left) and right-click Data Sources > Get data….

![getting data](https://media.datacamp.com/cms/ad_4nxdqqwkmvx-c-cgz9-f63agn5levcb93h4fp2nhwcno-kaq33t9pwcl28vt5fcah0_pygzngv9thvo8kd-082ikeocosg1oebnujchsapmft0_tptp0f05cntuqzb7j9xktyjsiooq.png)

2. Select Blank Table on the left pane.

![creating data source](https://media.datacamp.com/cms/ad_4nxecikeaxvigln-c0o5wct2exnmj9b215zgohijide-pdeq6dakinaahcyairntxcpyvhhp9wzpvuc9toilux8e0__o6vfp-08syqojdrxbe4drwl0qea9jt9pzoqgguzkatzaju.png)

3. Copy and paste the following sample data into the table.

`Region,Product,SalesAmount East,Widget A,3200 East,Widget B,2700 West,Widget A,1800 West,Widget C,3900 South,Widget B,2100 North,Widget A,2400 North,Widget C,3100`

[](https://app.datacamp.com/workspace)

4. Click on Use first row as headers.
5. Enter a table name (e.g., SalesData) and click Next, then Create.
6. In the left-side panel, right-click on the new data source named PowerQuery and rename it as “SalesData”.

![data source created](https://media.datacamp.com/cms/ad_4nxd51efsaizf1ythkhrhe4nv-mrxeb2al9blsiez7ofu4fdsov3o0lanmmff-bjfkmaaifd5pk7buavvgik-higgtdqp53jkalufigjqppod2umglc5qwlflnivxkgtztx_7xplk_g.png)

### Defining a dataset

A dataset is a specific query or table that defines what data will be used in your report.

1. Right-click Datasets > Add Dataset.
2. Name your dataset as Sales Dataset.
3. Select SalesData for your Data source to reference the Data Source that you created previously and click OK.

![creating dataset](https://media.datacamp.com/cms/ad_4nxewzilupnpqmyoyyjitcjs3nqzkai-iulx11cajgtz3apzxfsfxadczrxghlau_j0zpxkolczifhweywm4g4ezsotvexhyn7hbgpdbkwbptircqwkl0nb1mmvldgf4jagvbdopgnw.png)

## 3. Creating Your First Paginated Power BI Report

### Using the table wizard

1. Go to Insert > Table > Table Wizard.

![creating table](https://media.datacamp.com/cms/ad_4nxdym4dwnsylg_oncevpz1ttvboxecljrwulvx6xjghupzqvj92gw3ujxwio7zpkndlaomzedmwn915wjklixs3fekekfl31bgqmxkyjgv472gfzsp1zalesfqentpbmrfh9wberna.png)

2. Select your dataset “Sales Dataset” and click Next.
3. Drag Region to Row Groups.
4. Drag SalesAmount into Values and select the Sum aggregate.

![arranging table fields](https://media.datacamp.com/cms/ad_4nxc_dzgdzzjg7yko5anspt_mdcdxnstz0mk_1izg2pnz-5azaswx2jf6w-wwzlciqpfna1ljs2zmljgrvy5okucd-jjskux024glr_qaz3ok3gjmre4t1hynsmvxivxpg5adlptq.png)

5. Click Next, Next, and then Finish.

You now have a basic table displaying data from your dataset.

![created table template](https://media.datacamp.com/cms/ad_4nxcf9nbkcyjn5vpzco9gokpkvqw-55cjn7mu5sto2sfi1aocoonbbro5bxtlx0j_kjg3e7vmeuqbehsv55w4l_psw4rq56ghwashdyi3ua0ezaokd-5j5hc30a8ogimsjmmzcpkv.png)

You can also resize the table by dragging the corners with your mouse, as shown below.

![resizing table](https://media.datacamp.com/cms/ad_4nxekaik3cr7y5zls6iftdhjoscpak5r6pg4cpkqhcoddyivxch7t_egel3sleent5btaaiomxbf8uxaxotl-k5qtulcsyitvuqbawrloexciz1nweqlr5tkyfigise2qecnvkbefgg.png)

You can preview the data in the table by clicking Run.

You should be able to achieve a printed data table like this:

![printed table after running](https://media.datacamp.com/cms/ad_4nxehhwq02c_p14cpwvyeywgbm2vszvaiedx-hwrpcybwidepjpcvhi99eych8nam-37mdfrtbdpuikcznguwffs8xfie0mh_l2wi1h6vzcbgr-blbymvzx5bv2zkjceslqka0b_j.png)

### Adding charts and visuals

Next, we can beautify the report with some visuals to better present the data.

1. Go to Insert > Chart > Chart Wizard.
2. Choose the “SalesDataset” option and click on Next.
3. Choose a chart type (e.g., bar, line, pie). In this case, we’ll go with Pie.
4. Drag the fields into the following arrangements.

![arranging chart fields](https://media.datacamp.com/cms/ad_4nxeiestv917bwarunl8vg0gqsn-zdo6u7_o_auoiluxvhwiycq7vrgimpno02ngp7zl4stkdd-4b7i0yqlr-vz1z9o0vsjzik2ocwvxwpdge3atri8fsxe4pvhv_wyas-e9fyqblew.png)

5. Click Next and Finish.
6. Resize the chart you’ve created to fit the report using the corners.

Once you’re done, hit Run, and you should see a printout of the chart in your report.

![chart printout](https://media.datacamp.com/cms/ad_4nxfborwefarjq5bn8yewl8-oc6qtfeb3npuwstqytogdvytlwfbxnnp2scyry5im4vmysyntrtperwaqhnodpnu3ogx3z3molid_w3rx7hhyodsj2tjkleuze5jw_zy-zu8ilxkv2q.png)

Charts like these can help visualize trends and are useful for summary sections. If you’re building reports, having a mixture of some charts and graphs like bar charts, line graphs, and pie charts can help your readers understand the data better.

## 4. Formatting and Designing Reports

Before you can start sending these reports out, you’ll need to see how you can make things easier for your readers to view the data. This will involve some basic formatting and designing. If you’re looking for some hands-on practice, be sure to check out our [Data Visualization in Power BI Course](https://www.datacamp.com/courses/data-visualization-in-power-bi). 

Here are some areas to modify.

### Applying styles and themes

You can modify the font size, color, borders, and background color using the Properties pane. This pane is especially useful for the detailed designing of reports that can be used to clean up and enhance the appearance of your report.

To enable the Properties pane, go to View on the top ribbon and check to enable Properties. A Properties pane should appear on the right side of your screen.

1. Select the pie chart you created previously.
2. Go to Properties > Chart > Palette. Select on Seagreen in the dropdown to modify the chart colors.

![chart formatting](https://media.datacamp.com/cms/ad_4nxehriorlgrvucy7fpjbvzflymnhpgv14fj2adfmftej1c5sxvaq7i1lwgvqi1uwsj6-cwiiscklingqj73tzd7br_pp0yh3f9xrh7gdevnoycgc61de1jhtsclqi7gfbdrnudq6.png)

3. Click on the Chart Title box in your chart and rename it to Sales by Region.
4. Click on the title box and change the FillColor to LightGreen.

![title formatting](https://media.datacamp.com/cms/ad_4nxeozxenar6bixuf-s2ky1zokd0jzeuonabqfx_eazs6fawaydrw_vw-t7rj19aemnqeseq71ihedy47zisq4xqbbojseqfqwpbj1_rzqbkqjsmuml4mstdkabfbthhtcllz0imxsg.png)

5. Right-click on the Sales Amount fields of your table and click on Placeholder Properties.
6. Click on Number > Currency > OK.
7. Right-click on the values in the Totals row of your table and click on Text Box Properties.

![number formatting for currency](https://media.datacamp.com/cms/ad_4nxf7mxfnlcmz-jx8ry5ecm_rs7pg9cqmpldcezon-xf9gmrafvqpuyqkzaeb_lmm6shl5wg-kj3bcwl7wa09teosd56ln5cplkl1-jrzeealkz2iu4-qq_vpph0xyljmifosdtkm.png)

8. Click on Number > Currency > OK.

After all that editing, hit Run again to preview your report. It should look something like this:

![color and number formatting](https://media.datacamp.com/cms/ad_4nxcduohwhtfo7yqndhvarmtqhczskg9icw4rvgeyo-itt3zvkhsjrjvj48zjy2ftt9rij5ejw8vlun_hg8pdbd0reflmttk2pfgswa_d3vhrqi1lgxglbgngcn4obn9gucoupqrx.png)

### Setting Up page layout

You can make your report look more professional with a proper header title so your readers can quickly grasp what they’re looking at.

To add a title, click on the “Click to add title” box and fill in “Sales Summary Report”

![final report preview](https://media.datacamp.com/cms/ad_4nxet-byhs-lb9tryeygr_dijs1x82dn0fidiegefkmibpdpouladsbwpveakmu5wsy0dw2msag3is_ndbwh2nqyrafxdbq8pg6gwpzkbv8lbiylapkf5bonufap0maltfkye0r57tw.png)

You may also choose to modify the sizing of your report and set a page size to make it easily printable.

Here is how you can do it:

1. In the run screen, go to Page Setup.
2. Set Page Size (A4, Letter, etc.) and Margins.

![page formatting options](https://media.datacamp.com/cms/ad_4nxcq-at62uq0d22rlbit8ec06eezwipmmlvoxtgsqyysty9yenmmhjn49mg0mddbcnlcmxyt2uzpvu3bn7mcy1loc_ch4jpiuxzmauwztfkdhrt-uu_3bkd_mtfqerxe1ivn9rdvtw.png)

These steps ensure the report prints neatly and is optimized for paginated formats like PDFs. To double-check your sizing, you can use the Print Layout button to preview how your report will look when printed.

## 5. Publishing Reports to Power BI Service

### Saving and exporting reports

You can save your report as an .rdl file for reuse or editing.

1. Go to File > Save As.
2. Choose a local folder or OneDrive location.

![saving as rdl file](https://media.datacamp.com/cms/ad_4nxe1weyz_uhxrlxciac97hz0e8jywdmkivbzs4zbf8da7f5ufpw2rakustyqus8wxknowv0ec-ad5mngrfe-0sptnwrlm35ahcr64-vffpsazmuy2gg73azkinyawhuidixfgsid7a.png)

To export as PDF, Word, or Excel:

1. Go to Home > Run > Export and select your desired format.

![export options](https://media.datacamp.com/cms/ad_4nxfwly8earg4fzlehi9z9rq9wx_oneku7yynthyjcr6b7fqo51nyaiwmrw_iqle148u1rt-qlzhe-x4rzugwh9vejdi93i0-p_s4qbv9gm6zfkul5ql00ullr3ng6kzicz6ds3_81q.png)

### Publishing to Power BI

To publish your report to the Power BI Service:

1. Go to File > Publish > Power BI Service.
2. Sign in to your Power BI account.
3. Select the workspace where you want to publish.

![publishing to Power BI service](https://media.datacamp.com/cms/ad_4nxfo5i2cnbqlg_niplopiy088pufsil2xjxp8r3_nyubb8nnwncyqafce1z6cwy-zrpaewanw1cr-qnq64q9zyvxwfhmlcv36peulatxl3k32sr8ezji1vpx_jly42vheeyra8tehg.png)

4. Name your project and click Publish.

![report publish success message](https://media.datacamp.com/cms/ad_4nxdixir1rwem0pr2lqcrmdopgu_pqyhkrencj-ylcfkbjhgx6q1p2doyuuryajknbwy3fhsmmvagajlklczlv4wmpf5t1entmx0pb1x8b-scqerxjqs-aft_dbvtm6k8cymwyjizhg.png)

Once uploaded, the report is available in the Power BI Service and can be scheduled, shared, or embedded in dashboards.

## Power BI Report Builder vs. Power BI Desktop

Power BI Report Builder is often mixed up with Power BI Desktop, especially for beginners who aren’t familiar with both of them.

To help you make things clearer, here’s a table of some differences between the two standalone software:

|   |   |   |
|---|---|---|
|**Feature**|**Power BI Report Builder**|**Power BI Desktop**|
|Report Type|Paginated|Interactive, dynamic reports|
|Best For|Printable reports, invoices|Dashboards, visual analytics|
|Export Options|PDF, Word, Excel, etc.|PDF, PowerPoint, Excel|
|Data Interactivity|Limited|Highly interactive|
|Charting and Visuals|Basic|Advanced|
|Publishing Destination|Power BI Service (Paginated)|Power BI Workspaces|

In short, you should use Report Builder for structured, print-ready reports and Power BI Desktop for exploration and storytelling with data.

Learn more about Power BI Desktop in this [Power BI tutorial for beginners](https://app.datacamp.com/learn/tutorials/tutorial-power-bi-for-beginners). You can also get some visual inspiration with our guide to the [Top 9 Power BI Dashboard Examples](https://www.datacamp.com/blog/9-power-bi-dashboard-examples). 

## Conclusion

Power BI Report Builder is a powerful tool for creating professional, paginated reports. It also offers tight integration with SQL-based data sources and Power BI Service, making it ideal for generating printable documents and regulatory reports.