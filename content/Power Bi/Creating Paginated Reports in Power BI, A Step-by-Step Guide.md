## What are Paginated Reports?

A paginated report is designed for exporting or printing, unlike the Power BI Desktop report that displays dynamic visuals and charts. You can also export paginated reports in formats like Excel, Word, PowerPoint, PDF, CSV, XML, and others.

You will notice in this article that I also talk about Power BI Report Builder. Power BI Report Builder fits in because it is the tool used to create paginated reports. While Power BI Desktop is used for building interactive reports with dynamic visuals, Report Builder focuses on precise formatting, structured tables, and multi-page layouts. So the job of Report Builder is to ensure the final report appears the same regardless of how it is exported.

### Setting Up Power BI Report Builder

Before proceeding, ensure you install the [Power BI Report Builder](https://www.microsoft.com/en-us/download/details.aspx?id=105942). It is free and doesn’t require a license. Power BI Report Builder works with the Power BI Online service when signed in. 

- Go to the top right-hand corner of the Power BI Report Builder page, then click the **Sign** **in** button.
- When the sign-in window pops up, enter your **email**.
- If you don't have a Power BI account, follow the prompts to sign up for a [free one](https://learn.microsoft.com/en-us/fabric/get-started/fabric-trial).

![Image showing the sign in button at the top right hand corner of Power BI Report Builder](https://media.datacamp.com/cms/ad_4nxcw1ptiwxy1vujfqpeahvegw8vcccukavno7b95bupyeedot6dhzcihxa8kcefhnxevu1x5dww-bpczhpg02jjapasyjmzlurawu1qwvfk8plvnnfegdeo7n2umdkkxr-n4ro329o68xink-pvd-yuxqneb.png)

### Connecting to data sources in Power BI Report Builder

You can connect to any data source your organization uses:

- Go to the **Data** tab, then click **Get Data (Preview)**.
- When the **Get Data** window opens, look for your data source.
- If you don't see the data source, click **View More** to access additional options.

![Image showing the list of popular data sources on the Get data window.](https://media.datacamp.com/cms/ad_4nxdsteibq_swdo0frrj1wp18dy-pnhoyrbf0yefn5_0ab_kneiehgty7rvia96vaewk4pefowuh1oyhrjz5wxon045tkrwllgsyclnmdqkhjflrs13g_v6slzskpb0lqgqxsia0w6jtd_r8yeku0xalck1pm.png)

The [AdventureWorks2022](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver16&tabs=ssms#download-backup-files) sample database and [Microsoft SQL Server](https://app.datacamp.com/learn/tutorials/how-to-install-sql-server) to show you how to build a paginated report with Power BI Report Builder.

- Go to the **Report Data** pane, then right-click on the **Data Sources** folder.
    
- Click **Add Data Sources** to open the **Data Source Properties** window.
    
- In the **Data Source Properties** window, select **"Microsoft SQL Server"** as the connection type.
    
- Rename the data source to `AdventureWorks2022`.
    
- Paste your **Microsoft SQL Server connection credentials** into the **Connection string** field.
    
- Click **OK** to save the data source.
    

![Image showing how to fill the connection string field and connect to the microsoft sql server database.](https://media.datacamp.com/cms/ad_4nxdn_rq1quwkwsxyuqpyxft0jibaeikuwgxovfki6ghxbkbp4qtteurcwp2xidioszwrci9ah4y765iwgibkosszpfkh5tfqg0oak-_l3zhjz4fe6mozlw1pw6k7hvdxqmye8iwlfajr-iw-gvck8ipx_wht.png)

## Creating and Customizing Datasets

Data Sources are where you get your data from, while Datasets are subsets of your Data Sources built by the Report Builder. Let's explore how we can use the **Query** **Designer** to create datasets from our data source.

### Using Query Designer for paginated reports 

The Query Designer extracts a dataset from a data source using the language of the data source. Let’s say your data source is from the Power BI dataset, then the Query Designer will use [DAX](https://app.datacamp.com/learn/tutorials/power-bi-dax-tutorial-for-beginners) to extract the data. Likewise, the Query Designer will use SQL as the query language if it's from Microsoft SQL Server.

Let's practice and create a sales report. This report will contain details about the total sales made for each product, showing the product line, class, and color.

- Go to the **Report Data** pane, then right-click on the **Datasets** folder.
    
- Click **Add Dataset** to open the **Dataset Properties** window.
    
- In the **Name** field, enter `AdventureWorks2022_sales`.
    
- In the **Data source** field, select the **AdventureWorks2022** database.
    

![Image showing the query tab of the dataset properties window of power bi report builder](https://media.datacamp.com/cms/ad_4nxfegy9dzlc1hxxbwnhn8ksex58kpxdox2_xm9tptldgu6ek2qaki-6kqxg7cybselrpxkzfoadpjhryqpejhr66xundldlccpbv3195jyny138dnlyhbsxamscitbihglytdzlvd4esgwnt4t4ku9yt9os.png)

Type the following SQL into the Query field to select the different variables from `AdventureWorks2022_sales`.

`SELECT 	Sales.SalesOrderDetail.ProductID, 	Production.Product.Name, 	Production.Product.ProductLine, 	Production.Product.Class, 	Production.Product.Color, 	SUM(Sales.SalesOrderDetail.OrderQty) AS Quantity, 	SUM(Sales.SalesOrderDetail.UnitPrice) AS UnitPrice, 	SUM(Sales.SalesOrderDetail.UnitPriceDiscount) AS Discount, 	SUM(Production.Product.StandardCost) AS CostPrice, 	SUM(Sales.SalesOrderDetail.LineTotal) AS LineTotal FROM 	Sales.SalesOrderDetail LEFT JOIN 	Production.Product 	ON Sales.SalesOrderDetail.ProductID = Production.Product.ProductID GROUP BY 	Sales.SalesOrderDetail.ProductID, 	Production.Product.Name, 	Production.Product.ProductLine, 	Production.Product.Class, 	Production.Product.Color ORDER BY 	SUM(Sales.SalesOrderDetail.UnitPrice) DESC;`

[](https://app.datacamp.com/workspace)

Typing in your SQL query is a good practice, giving you complete control over your database relationships. To see if your code runs without error, go to the Dataset Properties window and click Validate Query.

![Image showing the query tab of the dataset properties window with the pasted sql query to query the dataset from our data source.](https://media.datacamp.com/cms/ad_4nxfegy9dzlc1hxxbwnhn8ksex58kpxdox2_xm9tptldgu6ek2qaki-6kqxg7cybselrpxkzfoadpjhryqpejhr66xundldlccpbv3195jyny138dnlyhbsxamscitbihglytdzlvd4esgwnt4t4ku9yt9os.png)

**Now, on the Dataset Properties window, click the Query Designer button to open it. If you can’t see the SQL query field, ensure the Edit as Text button is highlighted. Click on the exclamation mark (!) to run and preview the query.**

![](https://media.datacamp.com/cms/ad_4nxeirovsylsn2e5msh-fhdb-uz43vra-_dzzkimkxpknjmpqnspb9cy1kry84jlvsjkgjyvkn32snrlttzrjjq8miv19vkcei3kg9luqouq-nexvehfef4rg9b6qfnr-ctiy592jonxt6tnfhcg98m8o-g92.gif?f=png)

### Inserting a table

Now, it's time to insert a table:

- Go to the **Insert** tab, then click the **Table Wizard** icon.
- When the **Table Wizard** window opens, select the **AdventureWorks2022_sales** dataset.
- Click **Next** to proceed and add the table fields.
- Drag **ProductLine** and **Name** fields into the **Row Groups** pane.
- Drag **LineTotal** into the **Values** pane.
- Click **Next** to continue.

![Image showing how to arrange fields and select row or columns for the new table or matrix.](https://media.datacamp.com/cms/ad_4nxf_qngr4ww531-qjsad4in-wip13dqkwpr2d6ci_1q--xaqiv-r-hc_7aoq8a-0q-1mdboeruhkjojljerk63zb4mpzhm_iqwcxskhzsm_7s_2f4h7hjg0xyy_tfohgbzmqird8mdf4-l44_xawsbijkrs.png)

Choose your preferred layout for the report, then click Next.

![Image displaying options to choose the layout of the table in the report body.](https://media.datacamp.com/cms/ad_4nxfb_o5vai4pgrnnt5usz0ufg7lgyaeiilxbmwo7ixbphoy_cpczunazd2hgjwypiyin7xr6ido3zja8iq2oko2mbnj1nbst7e_tlgi4d76cdj6n5yiww4qomzg4jm0t797aoctdts1tzs6yez5ylimzjuea.png)

The Preview window, which is the last step, gives a blueprint of the report layout. If you are satisfied with the layout, click Finish. If you have more fields to add, you can drag and drop them into the Table layout of the report body.

### Parameters for dynamic paginated reports 

A user viewing a report may want to filter the report by a particular field, such as filtering the sales report based on the color of items. This is where parameters come into play. A report parameter is a list of values your readers can use to control the report. Let’s create a parameter based on a product color. 

- Go to the **Report Data** pane, then right-click on the `AdventureWorks2022_sales` dataset.
    
- Select **Dataset Properties**.
    
- In the **Dataset Properties** window, go to the **Parameters** tab.
    
- Create a **color parameter**:
    
    - Set the **Parameter Name** as the parameter's name.
        
    - Set the **Parameter Value** to link the parameter to the query.
        

![Image showing how to add a query parameter name and value.](https://media.datacamp.com/cms/ad_4nxdlwx88fnfmh7t552pd5stvkguvfzirrgu2rs-el6w_vnvf8mot_ltun_audxgi8-el6-cin2zujvzzcch48lz8psy4ikrz_ivix-btqinf_dwld-cl_ulkolqlnjuwlarpmtigye-wrkobziw_eqjlznor.gif?f=png)

If you want to create a filter, go to the Filter tab. Here, I will create a color filter for all products in the report.

- Type the expression name `[Color]` in the Expression field.
    
- In the Operator field, select the `=`.
    
- In the Value field, type in the name of the parameter `[@ProductColor]`, then click OK to apply the filtering.
    

![Image showing how to set a query parameter to filter for a dataset field.](https://media.datacamp.com/cms/ad_4nxe1iznahkee2n8zqcqupfb_sfbu3ux6ra_aplxe3qg77ualesadf6fd6rxblohrevtc6m3qtd1tfdc7am1sjtwjhruojbsn4oagvvz2ulhusxrcf5ts535r0l34tqbturcyeygpn6r9vt-yy7flngx1cde1.gif?f=png)

If you want to customize the parameter further, like in our case, you could define values to appear like a drop-down instead of inputting a text.

- Go to the **Parameters** folder, then right-click and select **Parameter Properties**.
- In the **Parameter Properties** window, go to the **Available Values** tab.
- Select **Specify Values** to define preset values for the parameter.
- Add the values you want to appear in the drop-down.
- Click **OK** to save the changes.

![Image showing how to specify parameter values](https://media.datacamp.com/cms/ad_4nxc8qjiepjtjxyv5xcunuydnwe8e8w12jnfd30xg4ungry-j5magl8l_qbuw9pmnuvfciomhagjdwxebkm6viblvk73jjm7t_tcsjpopo1mqobeykvl0s-15z2dlcwua2-f-ubakc9tlargdubzynf1hqkc.png)

## Designing the Report Layout

With the Power BI Report Builder design canvas, you can design how to present a report. You can customize the table formatting and make it look clean, add your organizational logo to appear consistently across various report pages, and control the appearance of report pages using page breaks.

### Structuring multi-page reports 

Pagination is the number of pages in a report, which varies from a single-page report to multiple depending on the dataset generated by a query. There are two ways of viewing a report in Power BI Report Builder: the report body and the physical page.

#### Report body

The rectangular container displayed as a white space on the report design is known as the report body. You can grow your table or the report body to accommodate the items in a report. The report body does not determine the page size, as increasing the report body beyond the page size can make the report span multiple pages. 

![Image showing how to resize the table to fit the report body.](https://media.datacamp.com/cms/ad_4nxdl9bg10vfohl2b1xsqwiujzxghpneclgovvudnoza-smttztvacgcm73iz9-7ttjjx-f6ekhy5lmyvgpjpfxxizg7cjvfc9hfnr9cmhfj8zvvkw-uk798mwxwlsehrbrhqgin5b-n3i1bqzjvm-3mmhyrl.gif?f=png)

#### Physical page

This is the paper size that determines how the report is rendered. Here is how you can access and edit a report's page properties:

- Right-click on the **report body**, then select **Report Properties**.
- When the **Report Properties** window opens, customize the **paper size, margins, and units** as needed.

![Image showing how to set the page properties under the reference tab of the report properties window.](https://media.datacamp.com/cms/ad_4nxdskghwc5tzi63idunka4qqkyzitqtf_fcc21iq7dfdgdzsdnxrpdooqi7w8_hi8qqosxrpe9rxebbr80cd5ecwiovptrql9r3vfptgaww6kdfvmkrtgziaaq2yaewhna61iimgm2iga1mzwx-eaptyvj3p.png)

Now, if you want to span row headers and column names across pages:

- Select the **table** on the report page, then right-click and choose **Tablix Properties**.
- In the **Tablix Properties** window, enter "SalesSummary" as the table name.
- Under the **Row Headers** and **Column Headers** sections, check **all options**. Click **OK**.

![Image showing how to set the row and column headers in a power bi report builder paginated report.](https://media.datacamp.com/cms/ad_4nxclwiqmn7sxco0pu8xu59odjvskl67ih5bashn8jf_ese5hhxavrr7ilrx8e3ucavqnh_6e3uoukph--s6zghu47gktkisfeo4vzkazqrdqgthlsrmwv8hq59aujp3fltm9smgvwwepod5sqro8qa2icooy.png)

Next, select the report table, then:

- Go to the **Column Groups** pane, click the **drop-down** and select **Advanced Mode**.
- Go to the **View** tab, then check the **Properties** option to display the properties of each element.

![Image showing the advanced mode button, properties check box and the properties window](https://media.datacamp.com/cms/ad_4nxdqe4uvf9upjw29kiombawflfi2tebedxi39wxkxsptocqfspuk9o50x64n33bocsvkdrojib8njks3vl2r3j9c2xby4o8h-imgfprbsa_mhcjd42bqniov6owf8alv3qw6pqd1ndmpprluk5lcctgsn8zd.png)

**Under the Row Groups pane, select each static member corresponding to the row or column you want visible while navigating between pages:**

- In the **Properties** pane, set **RepeatOnNewPage** to **"True"**.
- Set **KeepWithGroup** to **After**.
- Repeat these steps for the four adjacent members as needed.

![Image showing how to set the values for the repeatonnewpage and keepwithgroup properties field to "true" and "after" respectively.](https://media.datacamp.com/cms/ad_4nxfukatqyyytfidfoqdddrai4rcjwmltjcvvcitq6guz54uw2pxus-hwoumuxh1ikudrsvhfjvjqmc0hctbpdrxy_yyru086yq_sa8ic8g3cfg4ubkwg_tmp7vps6ahqgtqow_ypytioc2sxxmv5g7cf2h4.gif?f=png)

### Adding static and dynamic elements in paginated reports 

Let’s improve the report by adding the report title, logo, and text to display the overall total.

- **Download** the **AdventureWorks** logo.
- Go to the **Insert** tab, then click the **Image** icon to open the **Image Properties** window.
- In the **Name** field, enter "AdventureWorksLogo**".**
- Click the **Import** button and locate the saved **AdventureWorks** logo file.
- Select the file, then click **OK**.

![Image showing how to change the name of an image on the image properties window.](https://media.datacamp.com/cms/ad_4nxfwhiq5h8jb6x0zhgmnyw3cgwdfyieogv0xtifxr4ut7qtfjw0ufyecadaflhrit0-pbyozcbaxy0fxvirfrftbtpvljnif958vqrisogka_kalhi3i0n5t6jopdplvuf9e2xos64n2orfx7q50xemsjmnh.png)

Click the text box at the right-hand side of the logo, and type in “AdventureWorks Sales Summary.” If you don’t have a textbox, insert one from the Insert tab.

![Image showing how to add a heading to the report body.](https://media.datacamp.com/cms/ad_4nxfujov2ht3t2kj4lxtkxft0clnbplgf1dvocgc3a1p7b8b-o73bvqjid6lyf8umqzj9fnnboitipa7yerufbl2n3rcuuslfe26cceld24xqoyruvlkfmnxmuksjnr_xwrpb6gmjpbditgaghvyu2-rsluqs.png)

If you notice, the alignment of column names, row names, and values is not uniform, but we can fix this:

- Select the **table column header**.
- Go to the **Home** tab, then click on the **Fill** icon under the **Border** group.
- Choose **yellow** as the fill color.
- Check the alignment of **column names, row names, and values**.
- Select all **four rows**.
- Go to the **Paragraph** group in the **Home** tab, then click **Left Alignment**.

![Image showing how to center the column headers form the paragraph group of the home tab of the power bi report builder.](https://media.datacamp.com/cms/ad_4nxfggdl6sv5shiw7kxb40muyalcbzwc5ui06kzrsadn0rntfvm0mqaszofjjzcefz6ksyceliuwharjucgmruy_zw8pvz_gwqhcefu21ssqqwxwcp2hvuik1ku78ug4gz4k-tp0gbi2hwocidldqx7upcgwk.png)

The report title and logo are fixed to only one page. To span the logo to cover all pages, you need to add a header to the report body by clicking on the page header icon under the Insert tab.

![Image showing the report title and logo moved to the page header.](https://media.datacamp.com/cms/ad_4nxccegn_ywl00x4n0g0sujc5dgb0s5hksdrszgjyfeprtm78zh2yasg-ndfurxbwmxyogwrctuy2dqzyewvoaqeaa417cib9rjkayuc3hnjbhrayuvexjsgq1d6oc6358khcfoide2hgxhnrbcqt0pqdqpkk.png)

**Select the Line Total column, then go to the Home tab. Under the Number group, select Currency from the dropdown to format it as currency.**

![Image showing the number format group under the home tab of the power bi report builder.](https://media.datacamp.com/cms/ad_4nxd12qwkmvxwoolhoh99_vv9dyikcssfk__jnvgilveut80lddjtdmckbbkpsggmcudwpffvuuxhdumjizovf8r_h-rhrkjwn1gb4a1217upoh1txifvpgtrejizpov2mgxju0gkaec0a3lhqcpop0o5zqqt.png)

Here is how you can add a text box just above the table:

- Go to the **Insert** tab, then click on **Text Box**.
    
- In the **Report Data** pane, expand the **Datasets** folder.
    
- Drag the **LineTotal** field into the text box.
    
- Select the text inside the text box, then right-click and choose **Text Box Properties**.
    
- Under the **Value** field, type `[Sum(LineTotal)]` to display the overall line total, even when filtered.
    

![Image showing the general tab of the text box properties window.](https://media.datacamp.com/cms/ad_4nxcc9n_cyeilbevrxiqoe8laej7a-9opggfpjc4wesh63osex9bfudcqbrxggyuhqezwva0sfftjae4znauqdfspusgko4rdh_nqnwdvhyfc0pt4lgulvghw4hovgz_pvovqlmajhglrhuma-wih81i7nu8.png)

Then, on the **Home** tab:

- Select the **LineTotal** text box.
    
- Under the **Number** group, format it as **Currency**.
    
- Click inside the text box and type `Total Sales` above the`[LineTotal]` value.
    

![Image showing  the line total text box](https://media.datacamp.com/cms/ad_4nxcvwbbaijo7mu4r8szcs_vskkli_ltoklcnvx9xeg0n6doapmxdwrieqkc8kar5xwws6ijdwp-kuntssgeb5oihd3y0wi-4im1bm424gjnzek_kky5kdhnerhqdi2rr_qv-ymgc5-30qjdwe2wfddfwz5e.png)

### Controlling pagination and page breaks

Page breaks determine how content fits into a page, they are applied to divide the report into various pages for viewing and printing purposes. You can use page breaks on various report elements, from table elements to charts, depending on how you want the report presented. 

#### Applying page break to a table and table elements

- Select the **table** in your report, then right-click and choose **Tablix Properties**.
- Under the **Page Break Options** section, check **Add a page break before**.

This ensures the **Total Sales Summary** appears on a single page, while the table starts on the next one.

![Image showing how to add a page break to the table of the paginated report.](https://media.datacamp.com/cms/ad_4nxeafoc5_xfxm0uoj10gbhzrctzt1i3k5dqrzqevbpge-ncpub7lpbjq73gmfmpyhhu8ceoubxkl7n9bp7dyukohps2_s_gfjiwvwne5sn9tvry5dtcmznci76tvxbcvcqjyyxajhu7hfyvxjvzlbu7ucour.png)

When you want a particular group on each page, you can apply a page break such that even if a group member spans into another page, the next group member will start on a new page.

- Go to the **Row Groups** pane, then right-click on **ProductLine**.
- Select **Group Properties**.
- In the **Group Properties** window, go to the **Page Breaks** tab.
- Check **Between each instance of a group** to apply a page break between each group instance in the table.

![Image showing the page breaks tab of the group properties window of power bi report builder.](https://media.datacamp.com/cms/ad_4nxcc74kmystbvx1avor18jnq5puiccehbmpbfsnkbp0iv9tczgu17dbca0efdegxomajego_-38gwif5lknoziwxpn67kkzhzvm85_7wnhfmph33vpwgccvaqo_m8yiolh7oae2victgefkxr0lqc9y6cpyr.png)

### Adding page numbers to the report

Here is how you can add page numbers:

- Go to the **Report Data** pane, then expand **Built-in Fields**.
    
- Drag the **Page Number** field to the **footer** of the report body.
    
- If the report body does not have a footer:
    
    - Go to the **Insert** tab.
        
    - Under the **Header & Footer** group, select **Footer** to add one.
        
- Right-click on the **Page Number** field in the report body.
    
- Select **Expression** to open the **Expression** window.
    

Now, In the **Expression** window,

- Locate the **Set expression for: Value** field.
    
- Modify the expression by adding `"Page " &` between the `**=**` and `Globals!PageNumber`, so it looks like the following:
    

![Image showing the expression window of a page number](https://media.datacamp.com/cms/ad_4nxembjsrkhqh8tz-whff0slzce1yi1ye8tmobrxqdwami3haibe4sjcnltxvlwglqsdpkoya02vyiujb7b24bid9h_j17njy_vayqqdtsxd_mc6dqguudncbnaxdmp0zuymhsfgktntja7rfezz7xe5fyrq.png)

## Adding Visualizations to Your Paginated Report

Before presenting data in a report, you may want to summarize the key insights. For example, we want to insert a chart showing the top five products with the most sales. 

### Adding charts that span multiple pages 

To add a chart showing the product with the highest amount of sales, follow these steps:

- Go to the **Insert** tab, then click on the **Chart** icon.
- In the dropdown, select the **Chart Wizard** to open it.
- In the **Chart Wizard**, select the **dataset** containing sales data.
- In the next window, choose the **bar chart** as the chart type. Click **Next**.

![Image showing option to select a chart type.](https://media.datacamp.com/cms/ad_4nxdwuexrd6zbaqztv-1o2xul5eltjlk-et8yychi3es1z_7iiecqowy86sty9k7yrk6bsemgnkjrp3ccswgcarrgyv4qdcbj4qydzazp-k6dt073xldadwzsjc1qh4ed5udmj-ebv_9qz0yux87fq4d4pahz.png)

- Drag the **Name** field to the **Categories** pane.
- Drag the **LineTotal** field to the **Values** pane.
- Click **Next** to preview the chart.

![Image showing how to arrange the chart fields in power bi report builder.](https://media.datacamp.com/cms/ad_4nxffdadljcczwzndnqd4buvqs0omaeahl6w37b3gyxvyqhvtxe_rbhzs_qxtduzh0fh-_z-yoqdz-lo0_lcntbrxsgonoul1rpzztehcpqvqpaacyf4qbe6mq3ko6opo1ncc1mdd5ecuvuedkmn4gan0tevh.png)

#### Applying sorting to the chart

- Select the **chart**, then right-click on it.
- Go to the **Category Groups** pane.
- Click the **drop-down** on the **Name** group.
- Right-click on the **Name** group, then select **Category Group Properties**.

![Image showing the chart data pane with values, category groups, and series groups fields of the chart.](https://media.datacamp.com/cms/ad_4nxcs-8uhf67z4s9z8-8ekog0fobbrsfxqx3gkcw4wulolwna-fgvrkjuaptlmsdlcolbudcindvn7jbdawc_y9tsvw1zmocllub0vchsnxzdu4nf_dnadqd4ngev49fx5ebny2a9hekodo0tfmezk59tgf28.png)

- In the **Category Group Properties** window, go to the **Sorting** tab.
- In the **Sort by** field, type `[LineTotal]`.
    
- Set the **Order** to **A to Z** to sort in **descending** order.
    

![Image showing how to change the sorting options of the chart on the category group properties window.](https://media.datacamp.com/cms/ad_4nxeijvyurtgn6pn6pth0srsfmjacgiryygjn7q0oy12kvwwjhviyhjft2uujflft72gw9urx7o_o5nqkug_pwpdxk1tzozpbfc7siv7qomgb1nidqwol8lzl037l-rnjdqmtcl0-hs-f2q4mqtbiljtfm3w.png)

#### Applying filtering to the chart

Now, let's apply some filtering:

- In the **Category Group Properties** window, go to the **Filters** tab.
    
- Click **Add** to create a new filter.
    
- In the **Expression** field, type `[Sum(LineTotal)]`.
    
- Under the **Operator** field, select **Top N**.
    
- In the **Value** field, enter `5` to display the top five sales under each product line.
    
- Ensure the **data type** of the expression is set to **Text**.
    

![Image showing how to insert the appropriate values into the filter fields.](https://media.datacamp.com/cms/ad_4nxdjyrstpey9s6h1mvhhbwcno-3bq4uwfwe8n3glrusigqjnju1wkbukbsuxrz2vgacs3y-vf6upzs3zts5arhs-r6ntppnvr-vnb1c_nudm6o-gsjnewi8jvbqmkh8is9zvokhdeyywc7yma8wpytn76oyr.png)

### Formatting visualizations for print-ready reports 

The bar chart is made of various elements such as the chart title, legends, bars, and the chart series, which you can each customize.

- Double-click on the **Chart Title** textbox on the bar chart.
    
- Replace the text with `Top 5 Product Sales`.
    
- Select the text, then click **Bold** to make it bold.
    
- Set the **font size** to **11**.
    

![Image showing the new chart title "Top 5 Product Sales"](https://media.datacamp.com/cms/ad_4nxfeum7bpxl-jzbji4inq41ligaecpccssmybjwq1ogidgc6vetjkxze4pkuaekhf264qhe1ora54rd6dfsw4xicqvui3zwfleneaa-ntpwlhcbgddwz9mpreho-pwf2z6drav1e7ume4js40zokcgwdnacn.png)

Next, Select the X-axis on the chart and apply a currency format.

![Image showing the x-axis formatted into currency format](https://media.datacamp.com/cms/ad_4nxc1j2o4tdhzyfovo7figp8kthaae6rax9rests2_d5qj_fpjedcjzgvhozbjrxm_6wtgul7laduc8efh263pzo2g30uih7_mgjkkm6x7erk77z3qavakbd0beivvtky66syiygquk3bxicr_bntnbbywnrf.png)

To change the color of the chart bars,

- Select the **chart**.
- Go to the **Properties** pane.
- Expand the **Chart** section.
- Locate the **Palette** option and change it from **Pacific** to **Fire**, for example.

![Image showing how to set values for chart palette form the properties pane.](https://media.datacamp.com/cms/ad_4nxcu876arhusykzeuhiykl60mjrrse6cgfnul0x6cfx4h_d0s6lcz7a5pwjkpseel1i5bnrhjhizunbg_bnvvdyap0mgnovgkct74qpkp4rym_mta7k-o9wa47y8hykdrnup1wr-dp3jdtuqd-f354y9fcbt.png)

Note that if you want your table to start on a new page, ensure you have applied a page break either on your chart or the table. We already applied a page break earlier on the table, so using it in the chart is not necessary.. 

However, if you want to apply a page break to a chart, select the chart and go to its properties. The General tab has options for setting the page break.

![Image showing the options to add a page break on the chart, from the general tab of the chart properties window.](https://media.datacamp.com/cms/ad_4nxdmfwxqvjdq3igvwzkauckannfb3uwcqmg3g7zr-gl4szqgdlrk4t6d5r_pojr3y5rv44xgj_bglug0qn9jylvfjsn-g4c4mz7julziqsoodhvf27ohg5avpsuslqtb55cuokfydbm0nipmsig_wuegrbvf.png)

## Previewing and Running the Report

You can run your report to render it, and see that all the parameters and formatting applied appear as it should.

### Previewing page layouts in paginated reports

Click the Run icon on the Home tab for a live preview of your report. If you have applied any parameters to your report, you should see it below the Run tab. 

Earlier on, we only gave two values for the parameter: black and white. Select the Black option under the parameter, and click View Report.

![Image showing the view of the rendered paginated report.](https://media.datacamp.com/cms/ad_4nxfqs5bqn19zxztvnq7gjmvssu2tlp82xtn-bicv-g5ngtddaui8dve9w4kuonv1bqqfalhdplbcd1m0tau5alsiuayhbfhawhxebayrb4qsisyueqh79-fmyiidblhxjqef2fc2ze1lspz7wmavwnimmvna.png)

Here is how you can view the **print preview**.

- Click on the **Print Layout** icon.
- If the graph [doesn't appear as expected,](https://community.fabric.microsoft.com/t5/Desktop/Paginated-Report-Builder-Chart-does-not-fully-generate-within/td-p/1123891) don't worry—your report will still look correct in the export.
- Use the **Navigation** group icons to move through pages.
- To adjust the page setup, go to the **Print** group and click **Page Setup**.

![Image showing the print layout of the paginated report.](https://media.datacamp.com/cms/ad_4nxfbdhsj5qdrzq8rfbyuev-i7a2m4u-ff6wsnvyxlcbgf9pryo--0ofx1m7fxnufh_p5dba8t23gfm7cccuzvsj_6fshqqj4iymzo5i9gxkibuvrjqkdkhoqwltug6dldmjjyqlbfjye3hfx-2brwyxoiwsk.gif?f=png)

### Testing pagination with different parameters

We added only one parameter in the report, which is the Color, if you have added others, you can select a value in each to see how the report appears.

![Image showing the paginated report display when different parameter values are tested](https://media.datacamp.com/cms/ad_4nxf7cqlay9ott4qutp4s2qspkojsypn-uaxp_qafh2dx07thk4ilukxohi6wj-usfr11e1cfkizf6qhk_sclibigxrr47aaccxq70-xo68qxbxjiq3oq_jiu4qeo6ji-3zr73gvoe9ervbr09p0toz0ctihx.gif?f=png)

Note that the report is currently controlled by the parameter settings, all values are filtered by the parameter provided. If you want to view the whole sales report, you would need to disable the parameter 

## Publishing and Sharing Paginated Reports

You can make the paginated report available to users either in print-ready format such as PDF or Excel or publish to the Power BI Service.

### Exporting paginated reports to PDF or print-ready formats 

You can export the report by clicking the Export button on the Run tab and selecting the preferred print-ready format. 

![Image showing options of print-ready formats to export the paginated report.](https://media.datacamp.com/cms/ad_4nxdwgistropyzo88gbdhevngdxxti1igm-jegqih4tfefvin8skogvjdj-4_nh1aamrt3ibv4m5otcyzg5dtddacdpdbqiwfplek3zpalbndj62heymyiabkxolzsmz9smcgca_0ozxodqai3eekmxjc3krh.png)

### Publishing paginated reports to Power BI service 

You can publish your report online by publishing it to Power BI service and making it accessible to users, by going to the File tab and clicking on Publish. 

![Image showing the Publish button under the File tab](https://media.datacamp.com/cms/ad_4nxd2vxntguilxnr0ec4swees_xou0lqbkihp5wj_y26ot5qkzagke0oh41iuyagqnvbmq-ponql5ffmkgtfg21alhn9s_wvcaobuz3xkshbe6r71qkkyzlzhyqblxyl_slzup2x1z89tcsxwzmfwvqhxnw78.png)

On the Power BI Service window, select a workspace to publish to, and give it the name “sales_summary,” then hit **Publish**.

![Image showing the power bi service window](https://media.datacamp.com/cms/ad_4nxcwzb5ee8xqupr8vxq5ircc9xtfi_lfbpaso9s9xee4gjqmrwaibrpr2tmd5l4m_odzqmj3gturmy9aa_jq1shripwm_ddjnxn_uaqyaklbopl1degsigkfmx4hsjvktdwhspk25odd0y7qhqh4qdj9knvr.png)

A window will show you that the publication was successful. Click on the Open ‘My Workspace - sales_summary’ in Power BI to go to the report on Power BI Service.

![Image showing the successful publication of the power bi paginated report from power bi report builder to power bi service.](https://media.datacamp.com/cms/ad_4nxeptt2rwpkvp6zw0d2wydna0au91cphrpajquenuqewsil-cflibie0c_qy6icot-kggyhm8bialshjxa3x9lokdtjxuqgibycbi9lqjcem0nafidnjc6cxy9xct1bjts04vowesogdzqcqqulj-qpe2gmh.png)

If your report uses an on-premises data source, just like in our case. You must install a [Power BI gateway](https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-onprem) to access and share the report on the Power BI service. The Power BI gateway lets you connect to any data source not on the cloud.

## Best Practices for Paginated Reports

Here are some tips from my experience which I think might help.

### Use page breaks to improve readability 

It is a good idea to apply page breaks between the report elements.

For example, you can apply page breaks to data groups, as in the report we built. Each page carries a single combination of product line and class. The page also breaks our table and starts on a new page without overlapping other important info.

### Optimizing large data sets for paginated reports 

Cases where you have to deal with large data sets make your report load slower, leading to timeouts. You might also encounter inconsistent results and poor user experience. Here are some tips to optimize large data sets for paginated reports.

- Use Query Optimization Techniques: Always make sure you write efficient SQL queries. Implement appropriate [indexing](https://app.datacamp.com/learn/tutorials/introduction-indexing-sql) and use [stored procedures](https://app.datacamp.com/learn/tutorials/sql-stored-procedure) where possible. 
- Caching: Ensure you [cache](https://community.fabric.microsoft.com/t5/Service/Caching-in-Power-BI-Embedded-Pagintaed-Reports/m-p/3859402/highlight/true) datasets to reduce the execution time and schedule the cache to refresh during off-peak hours. 
- Implement Data Partitioning: When working with time-series data, use date-based partitioning and try splitting large tables into smaller datasets.

### Design tips

A report is meant to convey information effortlessly for the report users to understand. Always choose the most appropriate chart to display information. Trend graphs are advisable when dealing with time data, and bar or column graphs are preferred when working with groups.

When building the report, avoid cluttering the body and ensure you appropriately align elements using their bounding boxes. When dealing with complex elements, try to expand the body and ensure your paper size accommodates the expansion. 

I recommend taking our [Power BI Fundamentals](https://www.datacamp.com/tracks/power-bi-fundamentals) skill track so that you can practice and make sure these kinds of design ideas become intuitive.