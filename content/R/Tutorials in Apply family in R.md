# Tutorial on the R Apply Family

In this tutorial, you'll learn about the use of the apply functions in R, its variants, and a few of its relatives applied to different data structures.

Updated Mar 31, 2023 · 14 min read

Contents

- [A note on the R Apply Family](https://www.datacamp.com/tutorial/r-tutorial-apply-family#a-note-on-the-r-apply-family-thera)

- [The Apply Functions as Alternatives to Loops](https://www.datacamp.com/tutorial/r-tutorial-apply-family#the-apply-functions-as-alternatives-to-loops-thisp)

- [The apply() Family](https://www.datacamp.com/tutorial/r-tutorial-apply-family#the-apply\(\)-family-the%3Cc)

- [How to Use apply() in R](https://www.datacamp.com/tutorial/r-tutorial-apply-family#how-to-use-apply\(\)%C2%A0in-r-let%E2%80%99s)

- [The lapply() Function](https://www.datacamp.com/tutorial/r-tutorial-apply-family#the-lapply\(\)-function-youwa)

- [The sapply() Function](https://www.datacamp.com/tutorial/r-tutorial-apply-family#the-sapply\(\)-function-the%3Cc)

- [The rep() Function](https://www.datacamp.com/tutorial/r-tutorial-apply-family#the-rep\(\)-function-somet)

- [The mapply() Function](https://www.datacamp.com/tutorial/r-tutorial-apply-family#the-mapply\(\)-function-the%3Cc)

- [Functions Related to apply()](https://www.datacamp.com/tutorial/r-tutorial-apply-family#functions-related-to-apply\(\)-simil)

- [An Example of aggregate()](https://www.datacamp.com/tutorial/r-tutorial-apply-family#an-example-of-aggregate\(\)-consi)

- [Vectorization as an Alternative to Loops and Apply Functions?](https://www.datacamp.com/tutorial/r-tutorial-apply-family#vectorization-as-an-alternative-to-loops-and-apply-functions?-youha)

## Training more people?

Get your team access to the full DataCamp for business platform.

For a bespoke solution [book a demo](https://www.datacamp.com/business/demo-2).

[![learn r banner](https://images.datacamp.com/image/upload/f_auto,q_auto:best/v1583330891/r_2_t6hgbx.png)](https://www.datacamp.com/learn/r)

## A note on the R Apply Family

The R Apply Family is a set of functions in R that allow users to apply a function to elements of a vector, list, or matrix. However, it is considered legacy functionality and should not be used for new code. Instead, it is recommended to use the [purrr package](https://www.datacamp.com/courses/foundations-of-functional-programming-with-purrr) for all looping in R. The purrr package provides a consistent syntax for working with functions that take multiple inputs and outputs, making it easier to write and read code. Additionally, purrr offers a suite of functions that are optimized for modern computing environments, making it faster and more efficient than the Apply Family. Overall, while the R Apply Family may still work for some applications, it is advisable to use the purrr package for all new R projects.

## The Apply Functions as Alternatives to Loops

This post will show you how you can use the **R** `apply()` function, its variants such as `mapply()` and a few of `apply()'s` relatives, applied to different data structures. Of course, not all the variants can be discussed, but when possible, you will be introduced to the use of these functions in cooperation, via a couple of slightly more beefy examples.

Also, you might find it useful to look at this [introduction to R course](https://www.datacamp.com/courses/free-introduction-to-r) to better understand lists, vectors, arrays, and dataframes, though you don’t necessarily need to have completed the tutorial to follow this post!

## The `apply()` Family

The `apply()` family pertains to the R base package and is populated with functions to manipulate slices of data from matrices, arrays, lists and dataframes in a repetitive way. These functions allow crossing the data in a number of ways and avoid explicit use of loop constructs. They act on an input list, matrix or array and apply a named function with one or several optional arguments.

The called function could be:

- An aggregating function, like for example the mean, or the sum (that return a number or scalar);
- Other transforming or [subsetting functions](https://www.datacamp.com/tutorial/subsets-in-r); and
- Other vectorized functions, which yield more complex structures like lists, vectors, matrices, and arrays.

The `apply()` functions form the basis of more complex combinations and helps to perform operations with very few lines of code. More specifically, the family is made up of the `apply()`, `lapply()` , `sapply()`, `vapply()`, `mapply()`, `rapply()`, and `tapply()` functions.

But how and when should we use these?

Well, this depends on the structure of the data that you want to operate on and the format of the output that you need.

## How to Use `apply()` in R

Let’s start with the godfather of the family, `apply()`, which operates on arrays. For simplicity, the tutorial limits itself to 2D arrays, which are also known as matrices.

The R base manual tells you that it’s called as follows: `apply(X, MARGIN, FUN, ...)`

where:

- `X` is an array or a matrix if the dimension of the array is 2;
- `MARGIN` is a variable defining how the function is applied: when `MARGIN=1`, it applies over rows, whereas with `MARGIN=2`, it works over columns. Note that when you use the construct `MARGIN=c(1,2)`, it applies to both rows and columns; and
- `FUN`, which is the function that you want to apply to the data. It can be any R function, including a User Defined Function (UDF).

Now, beginners may have difficulties in visualizing what is happening, so a picture and some code will come in handy to help you to figure this out.

Let’s construct a 5 x 6 matrix and imagine you want to sum the values of each column.

You can write something like this:

`# Construct a 5 x 6 matrix my_matrix <- matrix(1:30, nrow = 5, ncol = 6)  # Calculate the sum of each column col_sums <- apply(my_matrix, 2, sum)  # Print the result print(col_sums)`

[Powered By](https://www.datacamp.com/datalab) 

The `matrix()` function creates a 5 x 6 matrix with values ranging from 1 to 30. We then use the a`pply()` function to apply the `sum()` function to each column of the matrix (`2` specifies that we want to apply the function to columns). The resulting vector of column sums is stored in the `col_sums` variable and printed to the console.

**Remember** that in R, a matrix can be seen as a collection of line vectors when you cross the matrix from top to bottom (along the vertical line 1, which specifies the dimension or margin 1), or as a list of columns vectors, spanning the matrix left to right along the dimension or margin 2.

That means that the instruction you have just entered, depicted in figure 1, translates into: “apply the function ‘sum’ to the matrix X along margin 2 (by column), summing up the values of each column.

Note that, to avoid cluttering the picture, just one of the columns is highlighted.

You end up with a line vector containing the sums of the values of each column.

The output of the above code, a line vector, would have also been given if you summed along the lines of the matrix. This is how R displays the result.

A note for the following: in most cases, R can return a value even if the latter has not been specified, or more precisely the return value of the function has not been assigned to a variable. R simply returns the last object evaluated. In practice, however, when you want to check the return value and when you need to do further operations on those return values, it is best to assign the results of a given function to a variable explicitly.

## The `lapply()` Function

You want to apply a given function to every element of a list and obtain a list as a result. When you execute `?lapply`, you see that the syntax looks like the `apply()` function.

The difference is that:

1. It can be used for other objects like dataframes, lists or vectors; and
2. The output returned is a list (which explains the “l” in the function name), which has the same number of elements as the object passed to it.

To see how this works, create a few matrices and extract from each a given column.

This is a quite common operation performed on real data when making comparisons or aggregations from different dataframes.

Our toy example, depicted in figure 2 can be coded as:

[](https://github.com/datacamp/datacamp-light "View DataCamp Light on GitHub")

- script.R

- R Console

SolutionSubmit

[](https://www.datacamp.com/?utm_source=datacamp_light&utm_campaign=powered_by_datacamp "Powered by DataCamp")

![lapply vs apply functions](https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Apply+Tutorial+R/content_content_apply2.png)

The operation is shown in the left part of figure 2.

Again, you start by specifying the object of interest, the list `Mylist`. You use the standard R selection operator `[` and then omit the first parameter (which therefore translates into “any”, that’s why you see the two commas).

Next, you specify the second parameter, which is `2`: our margin is ‘column’. So you extract the second column from all the matrices within the list.

A few notes to the code above:

- The `[` notation is the select operator. Remember, for example, that to extract all the elements of the third line of B requires: `B[3,]`;
- The `[[ ]]` notation expresses the fact that we are dealing with lists: [[2]] means the second element of the list. This is also shown in the output given by R;
- The output is a list with as many elements as the element in the input; and
- Note that you could also have extracted a single element for each matrice, like this: `lapply(MyList,"[", 1, 2)`

In the right-hand side of figure 2, you can see an alternative extraction: this time you omit the first parameter, and you get the first row from each of the matrices.

Try it yourself! Select the second column from each matrix in the list:

[](https://github.com/datacamp/datacamp-light "View DataCamp Light on GitHub")

- script.R

- R Console

SolutionSubmit

[](https://www.datacamp.com/?utm_source=datacamp_light&utm_campaign=powered_by_datacamp "Powered by DataCamp")

## The `sapply()` Function

The `sapply()` function works like `lapply()`, but it tries to simplify the output to the most elementary data structure that is possible. And indeed, `sapply()` is a ‘wrapper’ function for `lapply()`.

An example may help to understand this: let’s say that you want to repeat the extraction operation of a single element as in the last example, but now take the first element of the second row (indexes 2 and 1) for each matrix.

Applying the `lapply()` function would give us a list unless you pass `simplify=FALSE` as a parameter to `sapply()`. Then, a list will be returned. See how it works in the code chunk below:

[](https://github.com/datacamp/datacamp-light "View DataCamp Light on GitHub")

- script.R

- R Console

SolutionSubmit

[](https://www.datacamp.com/?utm_source=datacamp_light&utm_campaign=powered_by_datacamp "Powered by DataCamp")

Conversely, a function like `unlist()`, can tell `lappy()` to give you a vector!

Anyway, to avoid confusion, it is best to use these functions in their ‘native format’ and avoid conversions unless strictly necessary.

## The `rep()` Function

Something that is often used together with `apply()` functions is `rep()`. When you apply it to a vector or a factor `x`, the function replicates its values a specified number of times.

Let’s use one of the vectors that you generated above with `lapply()` into `MyList`.

This time, however, you only select the elements of the first line and first column from each elements of the list `MyList` (and you use `sapply()` to get a vector):

[](https://github.com/datacamp/datacamp-light "View DataCamp Light on GitHub")

- script.R

- R Console

Run

[](https://www.datacamp.com/?utm_source=datacamp_light&utm_campaign=powered_by_datacamp "Powered by DataCamp")

You see that the code above replicates the values of `Z` a number of times as established by `c(3,1,2)`: three times the first, one time the second and two times the third:

Handy, no?

## The `mapply()` Function

The `mapply()` function stands for ‘multivariate’ apply. Its purpose is to be able to vectorize arguments to a function that is not usually accepting vectors as arguments.

In short, `mapply()` applies a Function to Multiple List or multiple Vector Arguments.

Let’s look at a `mapply()` example where you create a 4 x 4 matrix with a call to the `rep()` function repeatedly:

[](https://github.com/datacamp/datacamp-light "View DataCamp Light on GitHub")

- script.R

- R Console

SolutionSubmit

[](https://www.datacamp.com/?utm_source=datacamp_light&utm_campaign=powered_by_datacamp "Powered by DataCamp")

But you see that there is a more efficient way to bind the results of the `rep()` function instead of with `c()`: when you call `mapply()`, you vectorize the action of the function `rep()`.

## Functions Related to `apply()`

Similarly, structured functions are occasionally used in conjunction with the element of the `apply()` family: the tutorial will only give an overview of a few of these.

### The `Sweep()` Function

The `sweep()` function is probably the closest to the `apply()` family. You use it when you want to replicate different actions on the `MARGIN` elements that you have chosen (limiting here to the matrix case).

A typical scenario occurs in clustering, where you may need to repetitively produce normalized and centered or “standardized” data.

What does this mean?

Assume you have a number of data points in a group of data. You first find the center of the data (“center of mass”) and look how disperse this data is with respect to this center. Two basic quantities will give you this information: the mean and the standard deviation.

Say your data points are the column vectors in a matrix of your data and let’s use the matrix B created at the start of this post, but now you have called it `dataPoints`.

You first find the means per column and the dispersion or standard deviation with the help of one of the `apply()` functions. And then you shift all the points with respect to their center. This means that the mean that you have found first will be used to normalize the data with respect to their standard deviation:

[](https://github.com/datacamp/datacamp-light "View DataCamp Light on GitHub")

- script.R

- R Console

Run

[](https://www.datacamp.com/?utm_source=datacamp_light&utm_campaign=powered_by_datacamp "Powered by DataCamp")

You produced the centered points with one call to `sweep()`. This function expects the following elements:

- an input array, which in this case is a matrix;
- a MARGIN, `2` to indicate the columns;
- a summary statistics (here `mean`); and
- a function to be applied. You use the arithmetic operator `“-”` for subtraction.

This means: “take the elements of the columns of the dataset MyPoints, and subtract the mean, `dataPoints_means`, from each of them”.

Now, you call `sweep()` again to divide all the values that you have just found by their own standard deviation. This step is called “normalization”. Again, you select `MARGIN=2`, and then you provide the vector of the standard deviations, `dataPoints_sdev` as an operand. Next, you pass the ‘divide by’ operator, `“/”`.

What you are asking of R is the following: “take the elements of the columns of the new object you just created, `dataPoints_Trans1`, and divide these (“/”) by their standard deviation `dataPoints_sdev`.

Of course, you could have obtained the same result more rapidly and concisely (as often is the case in R!) and without using different names, with a single line of code that contains a nested call to `sweep()`:

[](https://github.com/datacamp/datacamp-light "View DataCamp Light on GitHub")

- script.R

- R Console

Run

[](https://www.datacamp.com/?utm_source=datacamp_light&utm_campaign=powered_by_datacamp "Powered by DataCamp")

Statistically, you have just created a correlation matrix, and standardized data are at the base of several more advanced procedures on data (like dimensionality reductions via PCA, signal analysis and others).

### The `aggregate()` Function

This function is contained in the `stats` package, and you use it like this: `aggregate(x, by, FUN, ..., simplify = TRUE)`.

In other words, it works similarly to the `apply()` function: you specify the object, the function and you say whether you want to simplify, just like with the `sapply()` function. The critical difference is the use of the `by` clause, which sets the variable or dataframe field by which we want to perform the aggregation.

The next section will show you how this works.

## An Example of `aggregate()`

Consider the toy dataset called `Mydf`, which contains data about the sales of a product and where some of the values of the variable `DepPC` column repeat.

This variable classifies the data on a geographical location, like the portion of a post code (here the numbers correspond to the departments of the Île de France, the region comprising Paris).

You want to do some stats on the sales columns. These are `DProgr`, a progressive number in increasing time order, and the sales of the product (the quantity `Qty`), plus a logical variable, `Delivered`, which is logical, telling us whether the product has been delivered (T) or not (F).

First, you can do a number of very simple things to get acquainted with the data set, other than showing it all, by just typing its name (here we only have 120 records, but imagine doing this for a real file with thousands of lines!).

Let’s explore the data:

[](https://github.com/datacamp/datacamp-light "View DataCamp Light on GitHub")

- script.R

- R Console

SolutionSubmit

[](https://www.datacamp.com/?utm_source=datacamp_light&utm_campaign=powered_by_datacamp "Powered by DataCamp")

**Note** that if you want to see the number of rows and columns that the dataframe contains, you could have also called `nrow(Mydf)` and `ncol(Mydf)`.

Many other inquiries on the data are possible.

Here, you are interested in knowing where the product sells best in which department, for example. That’s why you should regroup the data by department, summing up the sales, `Qty`, for each department `DepPC` with the help of the `aggregate()` function:

[](https://github.com/datacamp/datacamp-light "View DataCamp Light on GitHub")

- script.R

- R Console

Run

[](https://www.datacamp.com/?utm_source=datacamp_light&utm_campaign=powered_by_datacamp "Powered by DataCamp")

So, `aggregate()` tells R that you wish to sum over all the `Qty` that belong to the same department.

Note that R assigned the sum to a variable ‘x’ because you didn’t say otherwise.

The output is quite readable as is, but for a higher number of departments, this might be less readable. In these cases, you can resort to some graphical output: you plot the results by using one of R’s graphical output systems together with the `aggregate()` function:

[](https://github.com/datacamp/datacamp-light "View DataCamp Light on GitHub")

- script.R

- R Console

Run

[](https://www.datacamp.com/?utm_source=datacamp_light&utm_campaign=powered_by_datacamp "Powered by DataCamp")

This gives us the sales for each department.

You might ask the same question, but only for the goods that were delivered. To do this, you first subset the data for which delivered is true (T) using the now familiar subsetting operator `"["`.

**Note** that here you assign the result to a new variable `Y`, which is a new dataframe that inherits the same columns names from the parent dataframe `Mydf`. You do this to avoid repeating the aggregate instruction within the call to the plotting for readability:

[](https://github.com/datacamp/datacamp-light "View DataCamp Light on GitHub")

- script.R

- R Console

Run

[](https://www.datacamp.com/?utm_source=datacamp_light&utm_campaign=powered_by_datacamp "Powered by DataCamp")

So you could have posed different questions to the data in a vectorized way like with `aggregate()`, and this you often do in conjunction with a convenient plotting system like `ggplot2`, so you get the jist.

Note that to get this, you only needed very few lines of code.

## Vectorization as an Alternative to Loops and Apply Functions?

You have seen some variations on the same theme, which is “act on a structured set of data in a repetitive way”. In this sense, these functions can be seen not only as an alternative to loops but also as a vectorized form of doing things.

“Vectorized” here in the loose sense, we won’t enter the debate that asks whether – and which of the – `apply()` functions are indeed vectorized or not (see for example the discussion [here](http://stackoverflow.com/questions/28983292/is-the-apply-family-really-not-vectorized)).

In practice, in order to choose which `apply()` function to use, you need to consider the following:

- The data type of the input: this is the object you will act upon (vector, matrix, array…, list, data frame or perhaps a combination of those)
- What you intend to do: the `FUN` function you want to pass
- The subsets of that data: rows, columns, or perhaps all?
- What type of data do you want to get from the function? Because you might want to perform further operations on it (and do you want a new object, or do you want to transform the input object directly?)