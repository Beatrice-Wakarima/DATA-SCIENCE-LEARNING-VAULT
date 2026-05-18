## Why Use Python in Power BI?

Using Python with Power BI introduces a whole new set of possibilities for working with data. Python turns Power BI into a platform that can do almost anything.

Here are a few examples of the types of tasks that can be performed with Python in Power BI:  
  

- **Data cleaning** - you can write Python scripts that automate some of the more repetitive data cleaning tasks that you commonly perform such as removing missing values or correcting date formats.
- **Data transformation** - Python scripts are helpful for datasets that require more extensive data transformations, which may be slow or cumbersome to do in the Power Query Editor, before they can be imported. 
- **Machine learning** - enriching your data with predictive analytics (such as regression or natural language processing), or unsupervised machine learning tasks like cluster analysis.
- **Handling of missing data** - Python gives you more options for how you want to handle missing data, such as through the use of machine learning models.
- **Advanced visualizations** - there is no restriction to the type of visualization you can add to your report when using Python. Add highly complex or customized visualizations without needing to download custom visuals in Power BI.
- **Connectivity** - Python gives you the ability to connect to almost any data source even if Power BI does not support it as one of its own built-in connections.

## What are the Limitations of Using Python in Power BI?

Some limitations in using Python with Power BI that you should keep in mind when writing your scripts are:

- Data sources added with Python must be set to public.
- Only Pandas DataFrames can be imported into Power BI using Python.
- Scripts that take longer than 30 minutes to run will time out, as will Python visuals that take more than 5 minutes to run.
- There are a limited number of Python libraries supported by Power BI Service (we’ll elaborate on this in the next section). 
- Reports using Python can only be refreshed in Power BI Service through a personal gateway (the enterprise or standard gateway is not supported).
- Python visuals do not support cross-filtering. This means that selecting an element in a Python visual will not cause other visuals to filter by that selection, thus removing some degree of interactivity in the Power BI report.

As mentioned, Power BI Service only supports a limited number of Python libraries. These same restrictions do not apply when building reports using Power BI Desktop, so keep an eye on the libraries you are using if you intend to publish your reports to Power BI Service.

Also, bear in mind that Power BI Service currently supports the Python 3.7.7 runtime. If you are writing your Python scripts in an earlier version of Python, then your code may not run correctly.

Power BI Service supports these libraries:

- Matplotlib
- NumPy
- Pandas
- Scikit-learn
- Scipy
- Seaborn
- Statsmodels
- XGBoost

It is worth noting that in order for the integration between Power BI and Python to work, a minimum of two Python libraries must be installed – Pandas and Matplotlib.

## How to Set Up Python in Power BI

Before you can write any scripts in Power BI, you will need to install the latest version of Python from the [Python website](https://www.python.org/). 

The Power BI documentation recommends that you avoid using environment managers like Anaconda since it could cause some issues with running the scripts. A possible workaround if using a custom environment in Anaconda is to activate the environment from the command line and then open Power BI Desktop from the command line, too. 

However, if you are less familiar with these aspects of programming, then it is easier to stick to  Power BI’s recommendation by just downloading Python from its website without using custom environments.

Once you have installed Python, you need to specify the correct Python file path in Power BI Desktop. From the ribbon, select ‘File’, then ‘Options and settings’, and then select ‘Options’. In the list of global options, look for ‘Python scripting’. This is where you will need to find the directory that contains the Python distribution.

You should be able to see all Python distributions installed on your computer in the drop-down selection. If you need to manually type in the file path, note that only absolute file paths are supported here, and you cannot enter a relative file path such as from the location of the Power BI report location

![Python Scripting in Power BI](https://images.datacamp.com/image/upload/v1654247675/image2_5fdc6fd4b7.png)

There are a few ways you can use Python scripts in Power BI:

- As a data source to import new data.
- To enrich an existing data source in the Power Query Editor.
- To visualize data in the Power BI report canvas.

The rest of this tutorial will cover how to use Python as a data source and to enrich an existing data source.

## Using Python as a Data Source in Power BI

In the Home tab of the ribbon, select ‘Get data’ to bring up the full list of data connections. Select the ‘Other’ category and find ‘Python script’ on the list. This will allow you to write a Python script to import a dataset. I find this to be particularly useful when connecting to a data source that is not supported in Power BI’s list of connections, or even a dataset that requires extensive data transformation before importing (such as from an API).

![Using Python as a Data Source in Power BI](https://images.datacamp.com/image/upload/v1654247675/image6_cf1be98278.png)

A dialogue box will pop up where you can enter your Python code. In this example, we will be using the Scikit-Learn library to load the Iris dataset that we will also use in the next section. Remember that Power BI only allows you to import Pandas DataFrames, so we must convert the dataset using ‘pd.DataFrame’ first.

![Python Script in Power BI](https://images.datacamp.com/image/upload/v1654247675/image4_565298833c.png)

In the next window, select the table called ‘df’ which contains the data. This will now allow you to load this dataset to the data model just like any other data source in Power BI. 

![Navigator in Power BI Screenshot](https://images.datacamp.com/image/upload/v1654247675/image5_69985e373d.png)

## K-Means Clustering in Power BI Using Python

K-Means clustering is an unsupervised machine learning technique that allows you to find groups of data points that are similar to each other – these are the clusters. This technique is particularly useful to businesses in marketing and customer service to better understand their customers.

Power BI has the ability to perform cluster analysis on your data without the need for Python. However, it is somewhat restrictive in that it determines the number of clusters to split the data into and does not allow you to change it. This kind of situation makes Python the perfect solution, as you now have the flexibility to write a script according to your own requirements.

From within the Power Query Editor, select the Transform tab in the ribbon and then select ‘Run Python Script’. This brings up almost the same dialogue box we had when importing the dataset, except here, there is a placeholder for our current dataset called ‘dataset’.

![Run Python Script Power BI Screenshot](https://images.datacamp.com/image/upload/v1654247675/image7_4419dc34ae.png)

Selecting ‘OK’ will import a collapsed table. You now need to expand the Value column out to select which columns you would like to include in the query. Select all columns, including our new ‘Cluster’ column that was just created from the script above and be sure to uncheck the box that says ‘Use original column name as prefix'.

![Power BI Use Original Column Name as Prefix](https://images.datacamp.com/image/upload/v1654247675/image1_32452dbbd2.png)

In the end, we are left with a dataset that contains all the original columns plus an additional column that shows the cluster to which each row of the data is assigned. In this example, we chose to split the data into 4 clusters, and so there should be cluster labels from 0 to 3.

![Splitting the Data into 4 Clusters Power BI](https://images.datacamp.com/image/upload/v1654247676/image3_2bbd64f6e4.png)