## 1. Overview of Power BI

### Overview

[Power BI](https://www.datacamp.com/tutorial/tutorial-power-bi-for-beginners) gives the ability to analyze and explore data on-premise as well as in the cloud. Power BI provides the ability to collaborate and share customized dashboards and interactive reports across colleagues and organizations, easily and securely.

![Overview of Power BI](https://cdn-images-1.medium.com/max/800/1*jWt7QPw7x86-BmiDMm3l_w.png)

_Power BI Overview. Source: [Microsoft](https://docs.microsoft.com/en-us/learn/modules/get-started-with-power-bi/1-introduction)  
  
_

### Power BI’s components

Power BI consists of various components which are available in the market separately and can be used exclusively.

![Overview of Power BI](https://cdn-images-1.medium.com/max/800/1*QZ0k9tHvzI98YSCce8mSHQ.png)

_Power BI Components. Source: [Wikipedia](https://en.wikipedia.org/wiki/Power_BI)_  
  

Choosing which component to work with depends mainly on the project or a team. We, however, will be working with **Power BI desktop** since this is a component primarily used for Business reports generation and desktop creation. Also, all the other works typically begin with Power BI desktop, where the report creation takes place.

### Introduction to Power BI

For a great hands-on introduction on how to navigate the Power BI platform, take DataCamp's course, [Introduction to Power BI](https://www.datacamp.com/users/sign_in?redirect=http%3A%2F%2Fapp.datacamp.com%2Flearn%2Fcourses%2Fintroduction-to-power-bi).

[![Introduction to Power BI](https://images.datacamp.com/image/upload/f_auto,q_auto:best/v1590077786/Introduction_to_Power_BI_interactive_mzw1an.png)](https://www.datacamp.com/users/sign_in?redirect=http%3A%2F%2Fapp.datacamp.com%2Flearn%2Fcourses%2Fintroduction-to-power-bi)

## 2. Advantages of using Power BI

Power BI provides certain benefits which make it superior to the existing analytical tools:

- Provides a cloud-based as well as a desktop interface.
- Provides capabilities like data warehousing, data discovery and interactive dashboards.
- Ability to load custom visualizations, and
- Easily scalable across the entire organization.

## 3. Power BI Desktop

Power BI is a free application that can be downloaded and installed on the system. It can be connected to multiple data sources. Usually, an analysis work begins in [Power BI Desktop](https://docs.microsoft.com/en-us/power-bi/fundamentals/desktop-what-is-desktop) where report creation takes place. The report is then published to **Power BI service** from where it can be shared to the **Power BI Mobile apps** so that people can view the reports even on mobiles.

![Power BI Desktop](https://cdn-images-1.medium.com/max/800/1*SZGJXc9mPw3P_EguKtiJUg.png)

_Power BI Desktop. Source: [Microsoft](https://docs.microsoft.com/en-us/learn/modules/get-started-with-power-bi/2-using-power-bi)  
  
_

### Installation

Power BI only runs on Windows Machines. Mac users could spin up a Windows VM in Azure and load Power BI onto that or use [Turbo.net](https://app.turbo.net/run/powerbi/powerbi), which can stream Power BI to the Mac directly from the cloud.

Power BI can be used in two ways:

- As an app from the Microsoft store and just sign in to get started. This is the online version of the tool.
- [Download](https://www.microsoft.com/en-us/download/details.aspx?id=45331) the software locally and then install it. Make sure you read all the installation instructions.

Depending upon the choice of product, download the software on to the computer. After accepting the license agreement, verify the installation by clicking the Power BI Icon/App. If the following screen appears, you are good to go.

![Power BI Desktop](https://cdn-images-1.medium.com/max/800/1*9g4z7xVvx_6s6sMa0mXnEw.png)

## 4. Getting Started

Let us now get an idea about working with Power BI Desktop. In this section, we shall explore it a bit to get accustomed to its interface.

### Power BI Workspace

The image below highlights the major components of the workspace of Power BI.

![Getting Started with Power BI](https://cdn-images-1.medium.com/max/800/1*T5vOMi8AaPcJB3spA870IQ.png)

### Basic views

- **Report View**: This is the main view where the Dashboard is created.
    
- **Data View**: The data view gives a preview of the entire data.
    

![Getting Started with Power BI](https://cdn-images-1.medium.com/max/800/1*Oy9ySQTRw7325v05Iu6HvQ.png)

- **Relationship View**: The relationship view displays the relationship between various objects.

![Getting Started with Power BI](https://cdn-images-1.medium.com/max/800/1*aKOGIbOkrTWRnmrX0K3A0A.png)

### Connecting to a data source

Power BI can be connected to several data sources. The **Get Data** icon displays all the possible available options from where data can be imported into Power BI.

![Getting Started with Power BI](https://cdn-images-1.medium.com/max/800/1*-XzTx1lkwdqh9UwEzbjFJg.gif)

Let’s look at a few of the most commonly used data sources:

**Excel data**

Let’s connect to an Excel data source. The workbooks consist of some fake financial data. Download the file from [here](https://github.com/parulnith/Data-Visualisation-libraries/blob/master/Data%20Visualisation%20with%20Power%20BI/Financial%20Sample.xlsx). Power BI Desktop loads the workbook and reads its contents, and shows you the data in the file using the Navigator window.

![Getting Started with Power BI](https://cdn-images-1.medium.com/max/800/0*pCdHL-766l6dYsz4.png)

Once loaded, the data can be viewed in the **Fields** pane.

![Getting Started with Power BI](https://cdn-images-1.medium.com/max/800/0*MtIGb0UBc-XPMHxc.png)

#### **Web**

You can also use the data from the web. Here is a dataset which presents the best and the worst states for retirement in the U.S.

link: [_https://www.bankrate.com/retirement/best-and-worst-states-for-retirement/_](https://www.bankrate.com/retirement/best-and-worst-states-for-retirement)

Simply select `Web` as an option in `Get Data` and enter the name of the url.

![Getting Started  with Power BI](https://cdn-images-1.medium.com/max/800/1*8Qgwm-9BJmohX36KIlqTYA.png)

Try experimenting with other data sources too.

## 5. Transforming Data

After the data has been loaded, it becomes visible under the `Fields` Tab. From here, we can modify our datasets with the help of **Query Editor**. Query editor can be used for modifying datasets irrespective of their data source. We can do manipulations like renaming a dataset, removing a single or multiple columns, etc. in the query editor. The Query Editor can be accessed by clicking the `Edit Queries` button on the Home Ribbon.

### Creating a custom column

Using the same [Financial data](https://github.com/parulnith/Data-Visualisation-libraries/blob/master/Data%20Visualisation%20with%20Power%20BI/Financial%20Sample.xlsx), that we used above, let’s shape data to meet our needs. Let’s create a custom column called `New Manufacturing Price`, which is equal to:

`([manufacturing Price])*3`

[Powered By](https://www.datacamp.com/datalab) 

![Transforming Data with Power BI](https://cdn-images-1.medium.com/max/800/1*OPnVtNo5H5iIDZrPcd_4Ew.gif)

### Changing column data types

The data types of the columns can also be changed easily. The `Units Sold` column has a floating point data type which can be adjusted to a whole number.

![Transforming Data with Power BI](https://cdn-images-1.medium.com/max/800/1*bKNOebMFGn6tmRnJolwb5A.gif)

### Removing columns

Removing columns is also easy. Simply select the column to be selected and choose the `Remove Columns` option, as shown in the following figure. Let’s get rid of the `Discount` column as it is adding no value to our dataset.

![Transforming Data with Power BI](https://cdn-images-1.medium.com/max/800/1*5y8cAwK_bVVwSMEfkZUWXw.png)

Similarly, there are other multitudes of functions that can be carried out like removing and adding rows, transpose, pivot and split which can be easily achieved through the query editor. Note that all the steps that you undertake to transform your data also appears in the `Query Settings` panel.

![Transforming Data with Power BI](https://cdn-images-1.medium.com/max/800/1*-FKh_xAQ2Zu2GxoQxn6Thg.png)

## 6. Reports

Reports are a collection of visualizations that can be created on one or more pages. These visualizations are usually related to one another.

![Power BI Reports](https://cdn-images-1.medium.com/max/800/1*VzL1fKbFFsL8_NAJ5jRNYw.png)

## 7. Dashboard

A dashboard is a collection of several views, enabling one to compare a variety of data simultaneously. Whereas the report can encompass various pages, a Dashboard is a single page interface.

### Creating a dashboard

Once we have the dataset ready with all the manipulations done, we can proceed for **the Dashboard** creation process. A Power BI dashboard, also known as canvas, consists of many visualizations on a single page which helps to tell a story. These visualizations called **tiles** are pinned to the dashboard from the reports.

Let’s now try to understand what insights we can get using superstore data set:-

- **Sales by Country**

![Power BI Dashboard](https://cdn-images-1.medium.com/max/800/1*Scx2P5OqhhMjwip1R4eC3w.gif)

- **Sales and Profit by Segment**

![Power BI Dashboard](https://cdn-images-1.medium.com/max/800/1*jMkOIlsKFrkqDh9g9sBw8A.gif)

- **Sales & Profit by Month**

![Power BI Dashboard](https://cdn-images-1.medium.com/max/800/1*G_47evCEtV1C8Tw7OaRQxg.gif)

- **Sales by Product**

![Power BI Dashboard](https://cdn-images-1.medium.com/max/800/1*HQLNRH37AG8sso8ULFMxBg.gif)

- **Profit by Discount Band**

![Power BI Dashboard](https://cdn-images-1.medium.com/max/800/1*dLGe5YP-3prFe5GnZTwlmw.gif)

The Dashboard created is interactive which means a change in one tile affects the other.

![Power BI Dashboard](https://cdn-images-1.medium.com/max/800/1*NbiVk0mtt2_5aWXvZUnfYQ.gif)

## 8. Power BI’s integration with R & Python

Apart from the various visualization advantages that Power BI offers, it also has an amazing out of the box connection capabilities. Power BI can easily integrate with languages like Python, R, and even with DBMS like SQL. This offers increased advantages in terms of functionalities and comes in handy for Data Scientists who are used to working in Python or R. They can directly import the R and Python scripts in the workspace and take advantage of its visualizations which are far more superior than that of these languages.

In this section we shall learn how to work with Python and R scripts in R. For learning about **SQL’s integration with Power BI**, check out our [SQL with Power BI](https://www.datacamp.com/tutorial/sql-with-powerbi) tutorial.

### Power BI & R

R is a popular statistical language used to perform sophisticated analysis and predictive analytics, such as linear and nonlinear modeling, statistical tests, time-series analysis, classification, clustering, etc. Using Power BI in conjunction with R gives the users access to a rich, ever-expanding collection of statistical analysis and data mining libraries to help them gain deeper insights from their data.

#### Pre-requisites

Make sure you have the following installed and running on your local systems:

- R
- A separate R integrated development environment (IDE) like R Studio.

It is also important to note that:

- Only data frames are imported
- Any R script that runs for more than 30 min gets automatically timed out.

Verify that R and R studio are installed on your system. Launch the Power BI and go to `Options and Settings -> Options`

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/800/0*4AIcsRgH4TrdNKxE.png)

Under **Options**, go to the **R Scripting** tab and make sure you can see the correct R version.

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/800/1*xvfLQZMf9IdVhh2qkB9ehQ.png)

#### Using R Scripts within Power BI

[Working with R Scripts in Power BI](https://www.red-gate.com/simple-talk/databases/sql-server/bi-sql-server/power-bi-introduction-working-with-r-scripts-in-power-bi-desktop-part-3) is an excellent resource on this topic. Below is an overview from the same source.

#### **1. R scripts for importing data**

There may be times when you don’t want to import an entire dataset but a portion of it. You can write an R script to only select specific columns or rows from the entire dataset to be loaded into Power BI.

> For this demonstration, we will be working with the well known Iris dataset that is included with the CRAN distribution.

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/800/1*EFCmy418PKuuOLzvu_ay_A.gif)

Datasets can also be imported from files. Here is an example which shows how to **load a CSV file** into the workspace with the following script. Download the file from [here.](https://github.com/parulnith/Data-Visualisation-libraries/blob/master/Data%20Visualisation%20with%20Power%20BI/Iris.csv)

`iris_csv <- read.csv(file="C:/Users/Parul/Desktop/Iris", header=TRUE, sep=",")`

[Powered By](https://www.datacamp.com/datalab) 

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/800/1*l9qWxeRivDmyrsJIk_pJfQ.gif)

Merely importing data with an R script doesn’t serve much of a purpose. The actual use is when we can manipulate data while importing. The following script uses the **summarize** and **group_by** functions available in the **dplyr** R package to group and aggregate the data before importing it:

Launch R Studio and install the following packages:

`install.packages("dplyr")   install.packages("data.table")   install.packages("ggplot2")`

[Powered By](https://www.datacamp.com/datalab) 

Now, use the following R script to import the Iris data. We will get a new dataset called iris_mean which contains the mean for each of the four measures, grouped according to the values in the _Species_ column ([Source: Power BI Introduction](https://www.red-gate.com/simple-talk/databases/sql-server/bi-sql-server/power-bi-introduction-working-with-r-scripts-in-power-bi-desktop-part-3)).

`library(dplyr)  iris_mean <- summarize(group_by(iris, Species),   slength = mean(Sepal.Length), swidth = mean(Sepal.Width),   plength = mean(Petal.Length), pwidth = mean(Petal.Width))`

[Powered By](https://www.datacamp.com/datalab) 

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/800/1*fUSI2aKossJiQm5e5aU9XA.gif)

#### **2. R scripts for transforming data**

R scripts come in handy when we want to manipulate data that is already imported into the workspace. Let’s say we want to apply the `summarize` and `groupby` functions after the entire data has been imported. This can be achieved by running R Script in the Query Editor as follows:

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/800/1*Q4uZg6drV4RPgbkQ_u7w0g.gif)

#### **3. R scripts for creating visualizations**

With the help of R scripts, you can create visualizations in Power BI. Simply type in the script and load in the necessary libraries, and you get visualizations similar to the ones in any R IDE. Let’s go through the steps:

- Import the Iris dataset into the workspace.
- Click on the ‘`R script Visual`’ in the visualization Tab, and a placeholder R visual image appears on the canvas and a script editor at the bottom.
- Select the fields that you want to include in the script. Let’s select `PetalLengthCm ,PetalWidthCm` and `Species`. The selected fields appear under the `Values` Tab, and pre-populated R script appears in the R editor.
- The script creates a dataframe named `dataset` with the selected columns. You can now write your script here or make changes in the existing one. Let’s paste the following code which imports the **ggplot** library and creates a scatter plot.

      `library(ggplot2)         ggplot(data=dataset, aes(x=PetalWidthCm, y=PetalLengthCm)) +           geom_point(aes(color=Species), size=2) +           ggtitle("Petal Widths and Lengths") +           labs(x="Petal Width", y="Petal Length") +           theme_bw() +           theme(title=element_text(size=15, color="blue3"))`

[Powered By](https://www.datacamp.com/datalab) 

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/800/1*w-uiGNNOgfJpH_KqXiLCTA.gif)

### Power BI & Python

Python is a widely used general-purpose programming language, and a large number of Python libraries are available to perform statistical analysis, predictive modeling using [machine learning algorithms](https://www.datacamp.com/blog/top-machine-learning-use-cases-and-algorithms).

Microsoft recently made it possible to integrate Python scripts within Power BI which enables running Python scripts and obtaining Python visuals within Power BI. Let’s look at the steps needed to do the same. But before that there are few pre-requisites:

- Make sure that Python is up and running on your local systems.
- All required packages and libraries should also be loaded such as pandas, matplotlib, etc.
- Currently, only pandas dataframe are supported.
- Any Python script that runs for more than 30 min gets automatically timed out.
- Python needs to be enabled before we can use it. Launch the Power BI and go to `Options and Settings -> Options`

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/800/0*4AIcsRgH4TrdNKxE.png)

Under `Options`, go to the `Preview Features` Tab and enable ‘Python Support’.

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/800/0*cvouQbY2CwXPP7Ts.png)

Restart Power BI and you get the Python icon both in visualization as well as in the `Transform` tab.

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/400/0*2-EIn5l2gUirvUaq.png)

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/800/1*Ah6pI70DtlpzmtAJbGdFww.png)

There are multiple ways of running Python Scripts in Power BI.

#### **1. Running Python scripts exclusively**

Steps:

- To run your Python Script, select `Get Data > More>Other > Python script` as shown below.

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/800/0*qR1OympDDUw9EUGh.png)

Now, simply paste your Python script here in the window that opens. Select `OK` to run the script which and then imports the resulting datasets into the Power BI Desktop workspace.

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/800/1*LiltJl-Ki-QmSV-KhobDNg.png)

#### **2. Creating visualizations using Python**

- Import the dataset into the workspace. Going with the same [Financial dataset](https://github.com/parulnith/Data-Visualisation-libraries/blob/master/Data%20Visualisation%20with%20Power%20BI/Financial%20Sample.xlsx), which pertains to Financials of a hypothetical company.
- Click on the ‘`Python Visuals`’ in the visualization Tab and a placeholder Python visual image appears on the canvas and a Python script editor at the bottom.
- Select the fields that you want to include in the script. Let’s select `Sales` and `Profit`. The selected fields appear under the `Values` Tab, and the scripts also appears in the Python script editor.
- The script creates a pandas dataframe named `dataset` with the selected columns. You can now write your script here or make changes in the existing one. Let’s paste the following code which imports matplotlib and creates a plot.
    
    `import matplotlib.pyplot as plt   dataset.plot()   plt.title("Sales Vs Profit")   plt.show()`
    
    [Powered By](https://www.datacamp.com/datalab) 
    
- Run the script and the visualization appears on the canvas. The visualization appears as it would in any Python IDLE.

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/800/1*7q0CusYGb-IK3c0uezOjGA.gif)

- Next, let’s create a correlation plot. Select `Discounts, gross Sales,` and `Units sold` in addition to the previous fields and replace the script with this new script:
    
    `import matplotlib.pyplot as plt   plt.matshow(dataset.corr('pearson'))   plt.show()`
    
    [Powered By](https://www.datacamp.com/datalab) 
    

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/800/1*N0PFYSXq3eIzAL3Cr9fH4w.gif)

- We can also import other libraries. Let’s import Seaborn library but make sure it is installed on your system. The dataset is called the ‘Tips’ dataset which usually comes pre-loaded with seaborn. Download the dataset from [here](https://github.com/parulnith/Data-Visualisation-libraries/blob/master/Data%20Visualisation%20with%20Power%20BI/tips.csv) and load it into the workspace. Then paste the following code into the script editor, and you will get the seaborn plots.
    
    `import matplotlib.pyplot as plt   import seaborn as sns   sns.set(style="darkgrid")  sns.relplot(x="total_bill", y="tip", data=dataset)   sns.relplot(x="total_bill", y="tip", hue="smoker", data=dataset);   sns.relplot(x="total_bill", y="tip", hue="smoker",col="time", data=dataset);  plt.show()`
    
    [Powered By](https://www.datacamp.com/datalab) 
    

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/800/1*qi9rZFAKGsw3ZZANzzWDlQ.gif)

The Dashboard with all the Python visualizations will finally appear like this.

![Power BI’s integration with R & Python](https://cdn-images-1.medium.com/max/800/1*ueQfl1qsBJRBXgnqlKK-Jg.png)

Python Dashboard

## 9. Saving and Publishing

### Saving and exporting files

You can save your files as Power BI templates. The visualizations can also be exported as PDF files.

### Publishing

Data is only useful when it can be shared among people or organization. The generated dashboard or reports can also be shared by publishing it to the Power BI Service. We can then use the Power BI Apps to view or interact with the Dashboards/Reports.

![Saving and Publishing](https://cdn-images-1.medium.com/max/800/1*VySwsMlEjueEPXXHV_0fqw.png)

## 10. Conclusion

That’s all we need to know to create a good visualization in Power BI although, one might find doing a lot more revising in each stage than we did here. So with experimentation and practice, Power BI becomes a lot more familiar and will unleash amazing features to help us analyze and present data.