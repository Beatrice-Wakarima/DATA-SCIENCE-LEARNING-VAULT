## What Does it Mean to Merge Tables in Power BI?

Merging tables in Power BI means combining two or more tables into a single table.

One of Power BI's unique selling points is its ability to combine data from multiple sources into one unifying platform. Whether your data comes from a warehouse, Excel files, third-party applications, or even a webpage, Power BI can access it and merge it.

The beauty of Power BI is the simplicity of this process. You don't need to learn any complex syntax or take a course in programming just to merge your data. The experience on Power BI is very intuitive and easy to follow.

For example, you might have one table with customer details and another table with their purchase history. By merging these tables, you can create a unified view that shows both customer information and their purchases in one place.

In Power BI, you do this by using the "Merge Queries" feature. It allows you to join tables based on common columns, like customer ID or product ID, so you can see all the related data together.

Keep our [Power BI cheat sheet](https://www.datacamp.com/cheat-sheet/power-bi-cheat-sheet) on hand as you go through this tutorial and others for quick reference on some essential Power BI concepts.

[![Power BI Cheat Sheet](https://media.datacamp.com/cms/google/ad_4nxdeai6twx9xdgpebdqqtxekdszsl7mgwog8mwqhzg1lf6vsbejohyo5vbjnk9p3jek3nojjniqq2qwc7inimrmakmdwh9xdz1gpasyqz95lzwqtlcq8kxjr-k96vhrnjiipscws1shhuvflaqnkvc49max_.png)](https://www.datacamp.com/cheat-sheet/power-bi-cheat-sheet)

DataCamp Power BI Cheat Sheet

## Why Merge Tables?

Before we go into the details, let's clarify why you would need to merge tables in the first place.

Merging tables is not strictly necessary. After all, we can create relationships between our tables to form a comprehensive data model. Through this data model, we can easily reference the columns in connected tables and add them to our visuals.

However, let’s suppose your data model has an extensive network of connected tables, forming a snowflake schema. This reduces the speed and refresh time of your reports to a crawl. So, what’s the solution in this example?

By merging the far-out tables, you can convert your data model to a star schema, boosting performance and improving the user experience (not to mention reducing your own headaches).

Chapter 4 of our [data modeling in Power BI](https://www.datacamp.com/courses/data-modeling-in-power-bi) course explores the concepts of star and snowflake schemas in detail. Alternatively, you can get a quick introduction by reading our [data modeling in Power BI tutorial](https://app.datacamp.com/learn/tutorials/data-modeling-in-power-bi-tutorial).

## Merging Tables vs Creating Relationships: When to Use Which

Creating relationships between tables and merging tables are both valid approaches in Power BI, but they serve different purposes and have different benefits.

Use relationships when you have a well-structured data model with clearly defined relationships between tables, especially with larger datasets. This approach is great for maintaining a clean and organized data model.

Merge tables when you need a simplified dataset for a specific analysis or when dealing with smaller datasets where performance impact is minimal. Merging can also be a good choice when you need to perform extensive data cleaning and transformation.

In practice, you might use both techniques depending on your needs. For example, you might create relationships for your overall data model and merge specific tables for particular analyses or reports.

## Getting Started with Merge Tables in Power BI: A Simple Example

To kick things off, let's start with a simple example.

Suppose you have a daily Sales table showing the number of sales per product per day. However, instead of full names, all you have is the Product IDs. This will not look very nice when visualized, and your stakeholders may not know which Product ID corresponds to which product.

To build a more intuitive, effective report, we need to merge the Products table into the Sales table so that we have access to the product names.

This is our current data model containing two tables (we are ignoring relationships for the purposes of this example):

![Power BI example of merge tables: sales table](https://media.datacamp.com/cms/google/ad_4nxfu827zhqngigesbjqkhidqjkg_lldhbkza362-s7vuqxv7dfuzkse-wf57kj0dinawpewrr1wxbtn1k4kvkdqlgr_6vqstgj2hi577i0xr38wprvyu2zrn7xw1vysfl4og0oauqamencttmmcbkerbkqvz.png)

Sales table

![Power BI example of merge tables: products table](https://media.datacamp.com/cms/google/ad_4nxd4q6und5pbfh9rmveiyp6rgmfyxt61yincuhjrt5jhmgv4wmaqvexxn9hfwqaic85p6yq1txv3tdeld4blavmurtptaltkdggqcxc3w6u224ttvnofhl6bejldrttxdlc7zjrt3v1v2eqaxteodmmf2vss.png)

Products table

To perform the merge, select "Edit Queries" in the Home tab of the ribbon to open up the Power Query editor. From the Sales table, select "Merge queries" from the Transform section of the ribbon.

![Power BI merge queries location in the ribbon](https://media.datacamp.com/cms/google/ad_4nxcn-qgsihsvhbjsi0ma89e7_puq-tyyswcxj1wjgofv7vs4af9vtcgt1vbmykyih_7tnt8-iwilta-um3ixu6nojg0qvrnzm9mhiotdzp604ecfeprtseobqbz1youn-mjzmgjeqdcrsqobslkz95p_-4m.png)

Power BI merge queries location in the ribbon

In the first table, select the Product ID column. Add the Products table from the dropdown to include it as the second table in the merge, and select the Product ID column again.

Power BI will confirm the number of matching rows so that we can quickly identify possible issues with our data. Here, we see that all five rows of our data are matched. Click OK to perform the merge.

![Power BI merge tables dialog](https://media.datacamp.com/cms/google/ad_4nxf7i0bvuqu67quagyhkwljddtlryl8gq0lamxnlg_yw2_lvutb7-xbo1al642khccwpfnmxdf4hybtqd_caazl8jg2xu1zfnh-6g2qlqwo4lodkz0iilo3imal_fgkfqntxihdlloybdyn1e69bwd3cqtjo.png)

Power BI merge tables dialog

We now need to choose which columns of the Products table we would like to add to the Sales table. In this example, we only want to keep the Product column.

![Select columns to expand after merging tables](https://media.datacamp.com/cms/google/ad_4nxfbyzl6_vx-jsuqr6yxajyris27e1rnfcrl88rfpt6zmqjanmgdfrq_kikpydjlfbty22_nesupuh_cwvqcytsvpn37_fgpjqbj07oxkx-xd3msmb8fnnt9suf5fefmskgy2dh6yzukg4ayobcjz82vvgxj.png)

Select columns to expand after merging tables

Below is the result of the merge. The Product column is now included in the Sales table.

![After merge: Product column is added to the Sales table](https://media.datacamp.com/cms/google/ad_4nxfc6tyzuhookmtxnqw9igrnuhhyxgife1wystwn76kwzcli8vpae11bydgxylefz210ye5hdvnzjeuxgfvkaccmdaazbabqepxuyl5jetjak8-tcbu_z8q2nofhema21o46pbwfa_swuyn-tiramgv8w-zn.png)

After merge: Product column is added to the Sales table

## Types of Joins in Power BI

When merging tables in Power BI, you can use several types of joins. Each type determines how the rows from the tables are combined based on the matching columns.

The good news is that you don't need a deep understanding of database design or SQL to perform these joins in Power BI. The interface makes it quite intuitive.

Here are the different types of joins you can use:

![Microsoft: Types of joins](https://media.datacamp.com/cms/google/ad_4nxcdtui580qm16dzuqm1ffivjrpndomvzisllwktl7et0sceocx5hayi6v-9tnkvy4p418issydx544bynk74kqwap53btxzytlvbcy4asxkldfdaaz0lpxf7gudd4mrswnsygkeaendons0dgvlsu0mzhqx.png)

Microsoft: [Types of joins](https://learn.microsoft.com/en-us/power-query/merge-queries-overview#join-kinds:~:text=later%20this%20year.-,Join%20kinds,-A%20join%20kind)

We refer to the following two tables to illustrate each join below.

![Power BI joins example: Sales table](https://media.datacamp.com/cms/google/ad_4nxfyvpx4dl8waoswudjfmhrsoq7pgsqs7o5zxnq84rjvuyylgxquzv7daebpsewslnl-lpcxkuodhgaxttgnc4fhuq8lf1fsvjnim71au61wzcscsi9dy91fakhjaegijxfkwr2tl4hmcahojnpztnxgz0ri.png)

Sales table

![Power BI joins example: Products table](https://media.datacamp.com/cms/google/ad_4nxeqeuy7tple1iomebqp_ct5qlkuweulkmzx5psc5hfxdgxver-yfppmnpadfnrwl-23e_ozf_nwwsaaz88cdlbkji_yryoyb7gqxhw2mrnkcgnt3q__ln7rqjxxoyttukms7wuc7mu-ftykp7u0n2_3teqw.png)

Products table

### Inner join

This join returns only the rows where there is a match in both tables. If a row in one table doesn’t have a corresponding row in the other table, it won’t be included in the result.

In our example, the Sales table is reduced to 5 rows since Product ID ‘P020’ is not found in the Products table. Additionally, two rows from the Products table are not even included in the Sales table since no sales are recorded for them (that is, Product ID ‘P010’ and ‘P001’).

![Inner join example](https://media.datacamp.com/cms/google/ad_4nxe6-z_xx8diktv4yoixoqzattp-qlvsv6aewytmddyxk2bxaqr4tff9j5gly9ysq5jhra4bmjim4ogy8hcgoqpmztkb2uqicupexhlrvoozyb4txxrdnfxulvjy305q0fm-ib5dp7ho8quzj3xaesnenwha.png)

Inner join example

### Outer join

When merging tables in Power BI, you will likely encounter and use outer joins the most (particularly the left outer join).

Let's explore the three types of outer joins:

Left outer join: This join returns all the rows from the first (left) table and the matched rows from the second (right) table. If there is no match, the result will still include all rows from the left table with null values for columns from the right table.

In our example, Product ID ‘P020’ has no associated product name because this product is not found in the Products table, so we just get a null value in the Product column.

![Left outer join example](https://media.datacamp.com/cms/google/ad_4nxeioc3c7girb3nnyuopmvt15bxbbdnyvmld6ovrzeq3cj_jcl1_cdy-etvrtzztrldc-eb8n0fc_wj0i2tey2chxxayi74hrwsxjc4tcrtevhkpjebsq6f-wu4s0unz4j605egogzw2o4mgu2z63rqbeks7.png)

Left outer join example

Right outer join: This is the opposite of the left outer join. It returns all the rows from the second (right) table, and the matched rows from the first (left) table. If there is no match, the result will include all rows from the right table with null values for columns from the left table.

In our example, two products (Binder and Paper) can be found in the Products table but do not have any associated sales in the Sales table. Therefore, we have two extra rows in our Sales table that are completely blank for all columns except the Product column.

![Right outer join example](https://media.datacamp.com/cms/google/ad_4nxeqyrqurocu7pukiazer4c0sbstqc4tfni0sz3ixgdw1stg60ynqt8qonqdcmdboql4i0-u38tfdnn1rdfggf7lwakkbvmrijycv_txyxdvjhc_w7isxvptrpohrlio6xvgs9d17cq54acnujucymgelfgd.png)

Right outer join example

Full outer join: This join returns all rows when there is a match in either the left or right table. If there is no match, the result will include rows with null values for the non-matching side.

In our example, we see all rows from both the Sales and Products tables, with matches where they are found and null values everywhere else. 

![Full outer join example](https://media.datacamp.com/cms/google/ad_4nxeujckcsnyydka1-lkvnyqgd62hrm-h2lbbgv7foesthgrbuwl9s4q1bi2iehy6dk5wv1cjjmmkuurwmnkojiywhzf45lno-j6kjyvoczxllyh7ugmjl9dqtmashu9jddwuul7ol97qxup467xzy9c7_htd.png)

Full outer join example

### Anti join

The anti join is useful for cleaning or investigating any suspected issues. For example, if a left outer join returns a lot of blanks in the joined columns this could indicate that there are data quality issues preventing Power BI from identifying unique matches.

There are two types of anti joins:

Left anti join: Returns only the rows from the left table that do not have a match in the right table.

In our example, only the row for Product ID ‘P020’ is shown because this is the only product in the Products table without an associated product name. This immediately tells us that our Products table needs attention: it’s missing a product!

![Left anti join example](https://media.datacamp.com/cms/google/ad_4nxdkm1ootoxsf0hmqobcenttm_nbdpvhrb_ax05ckxske9neyi3pffvrw9yzd6mxqlbnw_oacbxvi_ik4nlh-cuqn1dznd3ylb5nbhfxrvegt3p4ckrpctamt-unqgydtk9q9vek9u4edu6lds0-qbu9fd4h.png)

Left anti join example

Right anti join: Returns only the rows from the right table that do not have a match in the left table.

In our example, only two rows are returned because these are the products for which we have no associated sales. 

![Right anti join example](https://media.datacamp.com/cms/google/ad_4nxdaxgdyapcr2bg0de5fe9yp_zcjx7lxzzix3zcdoq1eun12zqxehcg0wjkvqvbg56p3in-zzrb_hwfr8319eftnw3ahd-4jdr181wozy3w8xzdtiokyluisj1is0wt0hco9srutebvcvyam0gqjbxggbos.png)

Right anti join example

While this may not be an urgent issue to address, it is useful to know which products are getting imported into our data model but serve no purpose. 

If you have large amounts of data and are looking for a way to speed up the performance and refresh times of your reports, the first thing to look into is whether your tables are bloated with useless data that is not used in your report.

## Merging on Multiple Columns in Power BI

Merging on multiple columns is necessary when you cannot identify unique matches to join on when specifying just a single column.

For example, let's suppose you've been asked to create a Power BI report showing the sales per salesperson for the month against their targets. The tricky bit is that each salesperson is responsible for multiple stores and has different targets for each store.

Here are the tables we will be using for this example:

![Merging on multiple columns example: sales table](https://media.datacamp.com/cms/google/ad_4nxfstjptico183qb-he_ziempxh2ma3djlmejf6emmrrv3nan8txlfdmzce-bs6qqilewylac2yax1go-tntxdsue154oujxw4-00m3tivso6xjablwk3w8oxcrrv6pyvbjrnvzqfqm4r6ubacjymngotqed.png)

Sales table

![Merging on multiple columns example: targets table](https://media.datacamp.com/cms/google/ad_4nxde9kess03vqlpu5lql7qerrfq79bnf-ziwlbdudu5joj-dpy968ypfeki5zvorqppkyrhbovetpva0fetgjk3sp8tekj7syekiyrrtnw0tq9sv1biwapzoio4sfuokantjtmzm0jlfjzlqdnlnwzptb2xn.png)

Targets table

The Sales table contains data for each Salesperson and their assigned Stores. The Targets table contains the sales Target for each Salesperson and Store.

It is not possible to join these two tables using only the Salesperson because Power BI would not be able to find unique matches (effectively creating a many-to-many join).

Thus, we will need to join these two tables using two columns in each table: Salesperson and Store. 

To do this, we must select the Salesperson column and then, while holding the ctrl button, select the Store column for both tables. You must select the columns in each table in the same order. Power BI adds a little 1 and 2 annotation next to each column name so you can confirm the order.

![Power BI merge on multiple columns: merge dialog](https://media.datacamp.com/cms/google/ad_4nxftj4sxougca65k6dsr2kuiklpjdb5yozzbwnvo9r_evx_fxjzu6l_ekwkkmzxniotyrb_jk0u7mnjcji_sytofpmlab9mx_ggoxxtioctlezzcbnf8xcypwpvbkriz0vj_jq3bir_fp3aj_1ix28ydnohe.png)

Merge on multiple columns dialog example

Now, the Sales table contains an accurate and comprehensive view of each salesperson's Sales and Targets.

![Merged Sales table: merging on multiple columns](https://media.datacamp.com/cms/google/ad_4nxe4egabw5bod4xvkp3o323neecfz3_je_koh7lreifo6__gcb3qqwglmc0lhzdgsidtkenlpntmczscor02grp1rtxhoyplqkf1o4ukprgfwu8jukmtqmjyvjthb5p6p14autkabsv45kdu-zxyoyue-7rk.png)

Merged Sales table: merging on multiple columns

## Merging Tables with Fuzzy Matching

Fuzzy matching only works on text-based columns and is incredibly useful for cleaning data.

What does "fuzzy matching" mean? It's a feature of merge tables that finds and merges rows that are similar but not exactly the same. For example, when there are typos or minor variations in customer names. Regular joins only merge on exact matches, but fuzzy matching allows us to merge on similar matches based on the sensitivity level we set.

Remember to always review the fuzzy match results to ensure they’re accurate. Sometimes, you'll need to make a few manual changes for edge cases where fuzzy matching doesn't work perfectly.

Let's try this with a simple example.

Suppose you have a Sales table containing customer transactions where the customer names are inconsistently recorded. You want to clean up these names to ensure each customer is represented consistently across all records.

![Sales table: messy customer names example](https://media.datacamp.com/cms/google/ad_4nxd3tbmbwdkr63zvti0fx5pbpkz47snzpxfckt_rkpiw4uazfpokyypdtrosyagbplk3qjvymu63fr8xwzcj0irns9-9938shwmrn8pwmonrb2xt7nmdrg8u1kxmb1abflar_6qhjdd4nd2djhhmkqqnoqgy.png)

Sales table: messy customer names

We'll be able to clean up these customer names by merging the Customers table (with the correct customer names) onto the Sales table and dropping the original messy customer name column.

In the Query Editor, select the Sales table and choose the Customer column for the join. Check the “Use fuzzy matching to perform the merge” option and configure the fuzzy matching options if necessary (e.g., similarity threshold).

![Merge tables: Fuzzy matching](https://media.datacamp.com/cms/google/ad_4nxdxaaphh3hj_tt6tjmrbqualzukkw0boqw6drwutfy17edswbaek_tro_cgo4vskmqf6_wgfr74auwf6ugucogtpits3y8fuaqu8lnosz_yvskf9toi-docqwoyugdd7vtmzuhglhcylmd4f7nh5ldvxbmh.png)

Merge tables: Fuzzy matching

Comparing with and without fuzzy matching for this join, we can see that the two customers with typos in their names are included.

![Without fuzzy matching](https://media.datacamp.com/cms/google/ad_4nxenmn3rgawkajyfm_ptyr7phyibhox-rbljus6skps2lmsuau3telbicxiu69asvwuvyrvydfpvacumdw4v7yp9tw3j_ptxftjx53t2nqdcldo3qd5umnn51zurxfho8wc8s7ddvqsylg7ori59xwabut3w.png)

Without fuzzy matching

![With fuzzy matching](https://media.datacamp.com/cms/google/ad_4nxeyr_rwv0yh_gvn-myprcoengm6djxfj3orgssltcsgvvabvdgyqtwwawj9nfkl4o0n5aqgcce30kbvcvw9pripxpcj-p5aqqrh7rlpfqimvp9mn7tywurntu38_8nfllcakr3_p8wl6rlmppwjayqhbjcl.png)

With fuzzy matching

Expand the column from the Customers table to include the clean Customer column in the Sales table. We can now safely remove the original Customer column and continue building our report using the cleaned Customer column.

![Using fuzzy matching to clean text data](https://media.datacamp.com/cms/google/ad_4nxfbyva7uvip4szi3phvic_0my1jf_ungsjtykrsyzyxpvnpxpicthbcn5yxipkucnkgzvjg_m816-r6hmkghxai65m9zkvprf1qec5mq44sjrspqarccnblosqmsldzy3qdpa9vfy9xod75i-drizz-qeyu.png)

Using fuzzy matching to clean text data

## Transformations After Merging Tables

Using our first simple example above, let's explore what data transformations are possible after merging the two tables.

If you transform the Products table after merging, those transformations will update the merged results. For example, if you clean up data or add new columns in the Customers table, these changes will be visible in the merged table when the data is refreshed. 

For this reason, be careful not to make any changes that could cause errors or inaccurate results for any tables that use the Products table in a merge (such as the Sales table in our example).

On the other hand, you are free to apply transformations to the Sales table in the steps following the merge, as these do not directly affect the merge itself. However, be careful not to add additional transformation steps before the merge, as this could cause an error in the merge and prevent the entire table from loading.

Check out our course on data [transformations in Power BI](https://datacamp.com/courses/data-transformation-in-power-bi) to learn your way around the Power Query editor and everything you can do to prepare your data for reporting.

## Conclusion

Managing and merging tables in Power BI can be challenging, especially since there are so many types of joins to choose from. 

However, merging tables is too useful a feature for it to be overlooked. 

With this tutorial, you can now confidently use Power BI’s merge tables to clean your data and build reports that can incorporate data from various sources.
up:: [[Power BI MOC]]
