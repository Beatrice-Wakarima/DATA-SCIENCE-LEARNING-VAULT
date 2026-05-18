# Merging Datasets in R

In this tutorial, you'll learn to join multiple datasets in R.

Oct 29, 2018 · 8 min read

Contents

- [Concatenating Datasets](https://www.datacamp.com/tutorial/merging-datasets-r#concatenating-datasets-atthe)

- [Primary Key and Foreign Keys](https://www.datacamp.com/tutorial/merging-datasets-r#primary-key-and-foreign-keys-thefi)

- [Types of Joins](https://www.datacamp.com/tutorial/merging-datasets-r#types-of-joins-there)

- [Missing Keys](https://www.datacamp.com/tutorial/merging-datasets-r#missing-keys-suppo)

- [Final Thoughts](https://www.datacamp.com/tutorial/merging-datasets-r#final-thoughts-inthe)

## Training more people?

Get your team access to the full DataCamp for business platform.

For a bespoke solution [book a demo](https://www.datacamp.com/business/demo-2).

In the applied setting, data are hosted on different servers and exist in many different files. When the data you need come from multiple sources, it's essential to know how to aggregate them so that you lose as little information as possible and make pairings that actually make sense given the structure of your data.

This tutorial will walk you through:

- Merging datasets horizontally and vertically
- What primary keys are and how they add structure to your data
- Different types of joins (e.g., left-join, inner-join, full-join) and how to choose among them
- A common problem to watch out for and how to resolve it

## Concatenating Datasets

At the high level, there are two ways you can merge datasets; you can add information by adding more rows or by adding more columns to your dataset. In general, when you have datasets that have the same set of columns or have the same set of observations, you can concatenate them vertically or horizontally, respectively. Let's learn by seeing some examples.

### Adding datasets vertically

When you have multiple datasets that have the same set of columns, you can concatenate one dataset to another, vertically. That is, _keeping the columns_ of your dataset, you can _add more rows_ to it. Having such information in one file will make it easier for you to aggregate and see the bigger picture without the hassle of switching back and forth between multiple files and losing track of them.

#### Dataset 1

|Make|Num models|
|---|---|
|Honda|63|
|BMW|10|

#### Dataset 2

|Make|Num models|
|---|---|
|Ford|26|
|Tesla|4|

It's important to note that if you have the same observation across multiple datasets and you concatenate them vertically using `rbind()`, you'll end up with duplicate observations in your table. And though the two datasets must have the same set of variables (i.e., columns), they don't have to be in the same order. See for yourself in the console below!

In your workspace, there are two datasets called `dataset1` and `dataset2` you saw above. Try reordering the columns of `dataset1`. Call `rbind()` on `dataset1` and `dataset2` as well as `reordered_dataset1` and `dataset2`.

[](https://github.com/datacamp/datacamp-light "View DataCamp Light on GitHub")

- script.R

- R Console

Run

[](https://www.datacamp.com/?utm_source=datacamp_light&utm_campaign=powered_by_datacamp "Powered by DataCamp")

After `rbind()`, your results should have information on all four car makes in one table like this:

#### Vertically concatenated dataset

|Make|Num models|
|---|---|
|Honda|63|
|BMW|10|
|Ford|26|
|Tesla|4|

## Start Learning R For Free

[

See More



](https://www.datacamp.com/courses-all?technology=r)

### [Introduction to R](https://www.datacamp.com/courses/free-introduction-to-r)

BeginnerSkill Level

4 hr

2.7M learners

Master the basics of data analysis in R, including vectors, lists, and data frames, and practice R with real data sets.

[

See Details

](https://www.datacamp.com/courses/free-introduction-to-r)

### [Intermediate R](https://www.datacamp.com/courses/intermediate-r)

BeginnerSkill Level

6 hr

598.6K learners

Continue your journey to becoming an R ninja by learning about conditional statements, loops, and vector functions.

[

See Details

](https://www.datacamp.com/courses/intermediate-r)

### Adding datasets horizontally

When you have datasets representing the same set of observations, you can concatenate such datasets horizontally. This time, _keeping the rows_ of your dataset, you can _add more columns_ to it. In such cases, you should check that the order of the observations are the same. If your datasets have a different amount of rows, or they have the same number of rows, but the rows are ordered inconsistently, you can pair one set of columns with the other set in a way that doesn't make sense.

Let's extend the example above for an example. Suppose you have two data files, one containing the car make and number of unique models offered, and another containing the car make and total sales:

#### Number of unique models offered

|Make|Num models|
|---|---|
|Honda|63|
|BMW|10|
|Ford|26|
|Tesla|4|

#### Total sales

|Make|Sales|
|---|---|
|Ford|119157|
|BMW|25908|
|Honda|188328|
|Tesla|29975|

It's important to note that if you have the same observation across multiple datasets and you concatenate them horizontally using `cbind()` , you'll end up with redundant columns in your table. And though the two datasets contain related information, ordering of rows matter!

In the console below, call `cbind()` on `models` and `sales` and print out the result:

[](https://github.com/datacamp/datacamp-light "View DataCamp Light on GitHub")

- script.R

- R Console

Run

[](https://www.datacamp.com/?utm_source=datacamp_light&utm_campaign=powered_by_datacamp "Powered by DataCamp")

You should have gotten something like this:

#### Models & Sales

|Make|Num models|Make|Sales|
|---|---|---|---|
|Honda|63|Ford|119157|
|BMW|10|BMW|25908|
|Ford|26|Honda|188328|
|Tesla|4|Tesla|29975|

Do you see the problem here? This data is not tidy!

According to the principles of tidy data taught in [this foundational course](https://www.datacamp.com/courses/cleaning-data-in-r), each observation of a dataset should be represented in a unique row. And what if you had information only on some of the rows in one dataset and wanted to add information only for those you have more information on? Put another way, what if you wanted to add more columns from one dataset to another, but these datasets don't have the same number of observations?

## Primary Key and Foreign Keys

The first step when looking to combine datasets is to look for the _primary key_ of your dataset. The primary key is the column or set of columns that uniquely identifies each observation in your dataset. In the example with car makes, the number of unique models offered, and total sales, the primary key of your datasets is the `make` column.

Now, we can perform _joins_, the standard way to merge datasets into a single table.

## Types of Joins

There are many types of joins. You can learn how to augment columns from one dataset with columns from another with mutating joins, how to filter one dataset against another with filtering joins, and how to sift through datasets with set operations in the [Joining Data in R with dplyr](https://www.datacamp.com/courses/joining-data-in-r-with-dplyr) course. Below are some of the most common.

`left_join(x, y)`: returns all rows from `x`, and all columns from `x` and `y`. Rows in `x` with no match in `y` will have `NA` values in the new columns. If there are multiple matches between `x` and `y`, all combinations of the matches are returned.

`inner_join(x, y)`: returns all rows from `x` where there are matching values in `y`, and all columns from `x` and `y`. If there are multiple matches between `x` and `y`, all combinations of the matches are returned.

`full_join(x, y)`: returns all rows and all columns from both `x` and `y`. Where there are not matching values, the function returns `NA` for the one missing.

The joins mentioned above are examples of mutating joins since they combine variables from two datasets.

## Missing Keys

Suppose you have two datasets. The first dataset is called `size` and contains the names of people and their shirt size:

 `> size name size 1  Tom    M 2  Dan   XL 3 Keil    S`

[Powered By](https://www.datacamp.com/datalab) 

The second dataset is called `color` and contains the people's surnames, shirt color preferences, and stores some information in the `row.names` attribute:

 `> color      surname color Tom     Jeon  <NA> Dan    Smith  Dark Bob McLadden Light`

[Powered By](https://www.datacamp.com/datalab) 

Notice what could go wrong here? Two-table joins can get complicated when there are missing keys or duplicate keys. In this example, [R's data frames](https://www.datacamp.com/tutorial/intro-data-frame-r) store important information in the `row.names` attribute. When this is the case, you won't be able to access the key with a join function, as join functions can only access columns of the data frame.

The trick to easily fix this problem is to use the `rownames_to_column()` function from the `tibble` package. It returns a copy of your dataset with the row names added to the data as a column. The first argument to `rownames_to_column()` is your data frame object and the second argument is a string specifying the name of the column you want to add.

Try exploring in the console below. Datasets `size` and `color` are pre-loaded on your workspace.

[](https://github.com/datacamp/datacamp-light "View DataCamp Light on GitHub")

- script.R

- R Console

Run

[](https://www.datacamp.com/?utm_source=datacamp_light&utm_campaign=powered_by_datacamp "Powered by DataCamp")