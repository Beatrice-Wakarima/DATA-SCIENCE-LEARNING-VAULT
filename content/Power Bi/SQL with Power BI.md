## 1. Power BI

[Power BI](https://powerbi.microsoft.com/en-us) gives the ability to analyze and explore data on-premise as well as in the cloud. Power BI gives the ability to collaborate and share customized dashboards and interactive reports across colleagues and organizations, easily and securely.

![graphic](https://cdn-images-1.medium.com/max/800/1*jWt7QPw7x86-BmiDMm3l_w.png)

[Source](https://docs.microsoft.com/en-us/learn/modules/get-started-with-power-bi/1-introduction)

### Advantages of using Power BI

Power BI provides certain advantages which makes it superior to the existing analytical tools:

- Provides a cloud-based along with a desktop interface.
- Provides capabilities like data warehousing, data discovery and interactive dashboards.
- Ability to load custom visualizations
- Easily scalable across the entire organization.

Due to the immense capabilities of Power BI, Microsoft has been recognized as a **Leader** in the “Analytics and Business Intelligence Platform”, by [Gartner](https://info.microsoft.com/ww-landing-2020-gartner-magic-quadrant-for-analytics-and-business-intelligence.html?LCID=EN-US?LCID=EN-US), for 12 consecutive years.

![Gartner Magic Quadrant for Analytics and Business Intelligence Platform](https://cdn-images-1.medium.com/max/800/1*nH9JitPS1XLb6z90zzrc3Q.jpeg)

2019 Gartner Magic Quadrant for Analytics and Business Intelligence Platform

### Power BI Components

Power BI consists of various components which are available in the market separately and can be used exclusively.

![powerbi components](https://cdn-images-1.medium.com/max/800/1*QZ0k9tHvzI98YSCce8mSHQ.png)

[Content Source](https://en.wikipedia.org/wiki/Power_BI)

Choosing which component to work with depends mainly on the project or a team. We, however, will be working with **Power BI desktop** since this is a component primarily used for Business report generation and desktop creation. Also, the other works usually begin with Power BI desktop, where the report creation takes place.

## 2. Power BI Desktop

Power BI Desktop is a free application that can be downloaded and installed on the system. It can be connected to multiple data sources. Typically, an analysis work begins in **Power BI Desktop** where report creation takes place. The report is then published to **Power BI service** from where it can be shared to the **Power BI Mobile apps** so that people can view the reports even on mobiles.

![Power BI Desktop](https://cdn-images-1.medium.com/max/800/1*SZGJXc9mPw3P_EguKtiJUg.png)

[Source](https://docs.microsoft.com/en-us/learn/modules/get-started-with-power-bi/2-using-power-bi)

### Installation

Power BI only runs on Windows Machines. Mac users could spin up a Windows VM in Azure and load Power BI onto that or use [Turbo.net](https://app.turbo.net/run/powerbi/powerbi), which can stream Power BI to the Mac directly from the cloud.

Power BI can be accessed in two ways:

- We can get it as an app from the Microsoft store and just sign in to get started. This is the online version of the tool.
- Sometimes, we need to work in offline mode with our data. In such situations, [download](https://www.microsoft.com/en-us/download/details.aspx?id=45331) the software locally and then install it. Make sure you read all the installation instructions.

Depending upon the choice of product, download the software on to the computer. After accepting the license agreement, verify the installation by clicking the Power BI Icon/App. If the following screen appears, you are good to go.

![Power BI Desktop](https://cdn-images-1.medium.com/max/800/1*9g4z7xVvx_6s6sMa0mXnEw.png)

## 3. Getting Started

Let us now get an idea about working of Power BI Desktop. In this section, we shall explore it a bit to get accustomed to its interface.

### Workspace

The image below highlights the major components of the workspace of Power BI.

![Workspace](https://cdn-images-1.medium.com/max/800/1*T5vOMi8AaPcJB3spA870IQ.png)

Power BI Desktop workspace

### Data Source

Power BI can be connected to a number of data sources. The `Get Data` icon displays all the possible available options from where data can be imported into Power BI.

![Data Source](https://cdn-images-1.medium.com/max/800/1*-XzTx1lkwdqh9UwEzbjFJg.gif)

## 4. Connecting to SQL Server

Let us walk through an example depicting how to connect SQL server database to Power BI Desktop and then use it to analyze the database.

### Sample Database

For the demonstration purpose, we will be using a publicly accessible SQL Server instance on AWS and a database which has been created based on the **Superstore** dataset.

This dataset contains information about products, sales, profits, etc. and our aim as Data Analysts is to analyze the data and find critical areas of improvement within this fictitious company. This SQL server instance has been hosted by [Ken Flerlage](https://www.blogger.com/profile/03698843288892226027).

### Accessing the sample database

- Install the [SQL Server Management Studio](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-2017)(SSMS). SSMS is a free and integrated environment for managing any SQL infrastructure. With SSMS one can deploy, monitor, and upgrade the data-tier components used by your applications, as well as build queries and scripts.
- Once downloaded and installed on to your system, you will see the following screen asking for specific credentials.

![Accessing the sample database](https://media.datacamp.com/legacy/v1725011943/image_d3f1f7735c.png)

Enter the following credentials:

`Server Name: ec2-52-14-205-70.us-east-2.compute.amazonaws.com Authentication: SQL Server Authentication Login: SQL Password: SQL`

[](https://app.datacamp.com/workspace)

You will now be granted a ‘Read Only’ access to the ‘**SuperStoreUS**’ database.

![Accessing the sample database](https://media.datacamp.com/legacy/v1725011943/image_f3fa8e8a2f.gif)

For our example, **ec2–52–14–205–70.us-east-2.compute.amazonaws.com** is the name of the instance, **SuperstoreUS** and **Test** are the databases, and **Orders**, **Customer**s etc. are the tables within the **SuperstoreUS database**. Thus there can be multiple instances, and each instance can further contain numerous databases which can also have multiple tables.

## 5. Importing SQL data into Power BI

Power BI Desktop organizes the data into queries. This means all the data is laid out into a table like structure.

### Setting up the connection

Open the Power BI Desktop and navigate to the start screen. Here the `Get Data` tab pane offers a lot of choices in terms of the data sources that can be connected to Power BI Desktop. We will connect to the [SQL](https://en.wikipedia.org/wiki/Microsoft_SQL_Server) Server.

![Setting up the connection](https://media.datacamp.com/legacy/v1725011943/image_086ed3c31f.png)

On Clicking the `SQL Server` option, a new screen will open up which will ask for the Server to which we want our Power BI Desktop to be connected. Enter the details and its done.

![Setting up the connection](https://media.datacamp.com/legacy/v1725011944/image_512c1d723c.gif)

We can now click on the desired table and view its contents. To load a particular table, simply tick the checkbox next to it and load it.

![](https://media.datacamp.com/legacy/v1725011942/image_8f1d784e10.png)

### Data Connectivity Modes

SQL database can be connected to Power BI Desktop in two ways, both the options which appear on the main screen.

### Import

As the name suggests, import method ‘imports’ the selected tables into Power BI Desktop. Power BI then uses this imported data for creating a visualization or doing any manipulations. To see any changes in the underlying data, we need to refresh the data which imports the entire data set again.

### DirectQuery

If DirectQuery is used as an option, no data is imported or copied into Power BI Desktop. While we create or interact with data through visualizations, Power BI Desktop queries the underlying data source, which means we are always working with the current data. However, this method provides limited options as to data manipulation, unlike the import method.

![DirectQuery](https://media.datacamp.com/legacy/v1725011943/image_d14430104b.png)

Here is a [link](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-use-directquery) that goes in depth regarding the Direct Query method.

## 6. Query Editor

All the selected tables will be loaded into the Power BI Desktop and will be displayed as individual datasets in the `Data view`.

![Query Editor](https://media.datacamp.com/legacy/v1725011943/image_28b41ddda2.png)

From here, we can modify our datasets. For this, we will take the help of the **Query Editor**. Query editor can be used for modifying datasets irrespective of their data source. We can do manipulations like renaming a dataset, removing a single or multiple columns, etc. in the query editor.

![Query Editor](https://media.datacamp.com/legacy/v1725011944/image_5ef3cbd9a2.gif)

The Left pane displays the number of active queries while the right pane is called the **Query Settings** pane and displays all the steps associated with a query.

### The Advanced Editor

The Advanced Editor displays the code for the query that is being executed against the data source. The syntax corresponds to **M, the Power Query Formula Language**. One can also create their own code.

![The Advanced Editor](https://media.datacamp.com/legacy/v1725011944/image_42e696cfcc.gif)

### Saving your work

After having performed the necessary modifications in data through the query editor, select **Close & Apply** from Query Editor’s File menu. This will apply the changes to the data in the Power BI Desktop.

![Saving your work](https://media.datacamp.com/legacy/v1725011942/image_6f402a5559.png)

## 7. Merging Datasets

Merging datasets comes in handy when we want to combine one or more datasets into one. This merging is also facilitated through the Query Editor. This time we will load in three tables from the SuperstoreUS database. The tables are `Orders`, `Customers`, and `Returns`.

![Merging Datasets](https://media.datacamp.com/legacy/v1725011943/image_a00b08654d.png)

The Fields column is populated with the three selected tables. Now, click on the `Edit Queries` button and navigate to `Combine` option, where the dropdown will expose the `Merge` option. We shall use the create a new query by merging existing queries.

![Merging Datasets](https://media.datacamp.com/legacy/v1725011943/image_58d1865793.png)

The Merge dialog box opens up (as shown in the following figure), and we select the tables to be merged and the type of join we want. We need to select columns which are common to both tables.

Let’s create a new query and name it as `Orders and customers.` We will combine the `Orders` and `Customers` table through this query.

![Merging Datasets](https://media.datacamp.com/legacy/v1725011944/image_94076d9435.gif)

This new query contains all the primary columns from the `orders`’ table and relationship columns from the `customers`’ table. Delete all the relationship columns except the last one, which represents the `Customers` query. Then select columns from `Customers` query to add to the new merged query.

The following demo will make the process more clear.

![Merging Datasets](https://media.datacamp.com/legacy/v1725011944/image_7838c53799.gif)

This merged query consists of a single database with all the desired columns. We can now easily work with this single database instead of working with multiple data sources which can lead to confusions.

## 8. Building & Publishing a Dashboard

Once we have the dataset ready with all the manipulations done, we can proceed for **the Dashboard** creation process. A Power BI dashboard, also known as canvas, consists of many visualizations on a single page which helps to tell a story. These visualizations called **tiles** are pinned to the dashboard from the reports.

Let’s now try to understand what insights we can get using superstore data set (Source: [Power BI Dashboard](https://www.edureka.co/blog/power-bi-dashboard)):

- **Profit by States**

![Profit by States](https://media.datacamp.com/legacy/v1725011944/image_34a82c7b7d.gif)

- **Sales & Profit by segment**

![Sales & Profit by segment](https://media.datacamp.com/legacy/v1725011944/image_817280baad.gif)

- **Sales & Profit by Region**

![Sales & Profit by Region](https://media.datacamp.com/legacy/v1725011944/image_7ad39fc618.gif)

- **Sales by Sub-Category**

![Sales by Sub-Category](https://media.datacamp.com/legacy/v1725011944/image_cb1ef408a9.gif)

- **Profit by region**

![Profit by region](https://media.datacamp.com/legacy/v1725011943/image_c1f5676152.gif)

- **Quantity**

![Quantity](https://media.datacamp.com/legacy/v1725011944/image_272d39c2f5.gif)

After formatting the size, appearance, and color, we will get a dashboard which resembles the one below.

![dashboard](https://media.datacamp.com/legacy/v1725011943/image_05dd7a8e46.png)

Superstore Dashboard

### Publishing

Data is only useful when it can be shared among people or organization. The generated Dashboard or reports can also be shared by publishing it to the Power BI Service. We can then use the Power BI Apps to view or interact with the Dashboards/Reports.

![Publishing](https://media.datacamp.com/legacy/v1725011943/image_54d785525e.png)

## 9. Conclusion

Using SQL and Power BI together takes the data analysis to the next level. We can easily connect the SQL Server to Power BI and extract the data directly into it. Power BI enables the users to toggle connections with a click to apply in-memory queries to a larger dataset. SQL is a pretty useful tool and when leveraged with the expertise of Power BI can help to make the analysis more powerful and insightful.
up:: [[Power BI MOC]]
