# Utilities in R Tutorial

Learn about several useful functions for data structure manipulation, nested-lists, regular expressions, and working with times and dates in the R programming language.

Feb 7, 2020 · 14 min read

Contents

- [Mathematical Functions](https://www.datacamp.com/tutorial/utilities-in-r#mathematical-functions-let's)

- [Functions for Data Structures](https://www.datacamp.com/tutorial/utilities-in-r#functions-for-data-structures-nowle)

- [Regular Expressions](https://www.datacamp.com/tutorial/utilities-in-r#regular-expressions-aloto)

- [Time and Dates](https://www.datacamp.com/tutorial/utilities-in-r#time-and-dates-timea)

- [Conclusion](https://www.datacamp.com/tutorial/utilities-in-r#conclusion-congr)

## Training more people?

Get your team access to the full DataCamp for business platform.

For a bespoke solution [book a demo](https://www.datacamp.com/business/demo-2).

In this tutorial, you are going to learn about several functions and utilities that are easy and often used in the R programming language. First, we'll discuss some mathematical related functions. Then you will look at functions that relate more closely to R's data structure like manipulating nested-list, regular expressions, time, and dates.

## Mathematical Functions

Let's look at the following cells of code that uses several mathematical functions.

You will first define two vectors, namely `x` and `y` that comprises of both positive and negative values.

`x <- c(1.1, -2.3, -4.5) y <- c(2.4,-44, -2.2)`

[Powered By](https://www.datacamp.com/datalab) 

`print(x)`

[Powered By](https://www.datacamp.com/datalab) 

`[1]  1.1 -2.3 -4.5`

[Powered By](https://www.datacamp.com/datalab) 

`print(y)`

[Powered By](https://www.datacamp.com/datalab) 

`[1]   2.4 -44.0  -2.2`

[Powered By](https://www.datacamp.com/datalab) 

Let's take these two vectors `x` and `y`:

- Take the absolute values of them,
- Round them up to zero decimal places,
- Sum them up each and
- Finally, take the average of both.

`mean(c(sum(round(abs(x))),sum(round(abs(y)))))`

[Powered By](https://www.datacamp.com/datalab) 

`27.5`

[Powered By](https://www.datacamp.com/datalab) 

How about you break the above line of code into small pieces and take a microscopic look into each function.

- The `abs()` function simply considers the positive or an absolute value of the elements of the vector `x` and `y`.

For example, on applying the `abs()` function of `x` and `y`, you would expect all positive values, as shown below.

`abs(x)`

[Powered By](https://www.datacamp.com/datalab) 

1. 1.1
2. 2.3
3. 4.5

`abs(y)`

[Powered By](https://www.datacamp.com/datalab) 

1. 2.4
2. 44
3. 2.2

- The next function in the list is the `round()` function. That does nothing but rounds the input. It takes an extra argument, where you can specify how many decimal places you would like the input to be rounded to. In a general setting, the `round()` function rounds the input to zero decimal places.

For example, after you apply the `round()` function to the vectors `x` and `y`, the output would look the one shown below:

`round(x)`

[Powered By](https://www.datacamp.com/datalab) 

1. 1
2. -2
3. -4

`round(y)`

[Powered By](https://www.datacamp.com/datalab) 

1. 2
2. -44
3. -2

- While the `sum()` function will simply compute the sum of the elements of the vector or matrix. For example, if you pass a row-vector as an argument to the sum function, the sum of all the row-vector elements will be returned as a scalar.

In this case, vector `x` and `y` are passed to the `sum()` function. Hence, R simply calculates the sum of the vector elements and returns a scalar as an output.

`sum(abs(round(x)))`

[Powered By](https://www.datacamp.com/datalab) 

`7`

[Powered By](https://www.datacamp.com/datalab) 

`sum(abs(round(y)))`

[Powered By](https://www.datacamp.com/datalab) 

 `48`

[Powered By](https://www.datacamp.com/datalab) 

- Finally, the `mean()` or the `average()` function will calculate the arithmetic mean. It will take the average of a set of numerical values, add them together, and divide them by the number of terms in the set.

In this case, the input to the `mean()` function is a row vector of length two containing numbers `7` and `48`. So, the mean of these two values would be the sum of these values divided by the number of elements, i.e., 2.

`mean(c(7,48))`

[Powered By](https://www.datacamp.com/datalab) 

`27.5`

[Powered By](https://www.datacamp.com/datalab) 

This was still pretty easy. Isn't it?

Let's now move onto the next and most interesting segment of this tutorial!

## Functions for Data Structures

Now let's look at some of the data structures like list and vectors. Different ways in which you can operate on `list` data structure, reversing a `list`, and how you can convert a list to a vector and vice-versa.

The below function is a `list()`, or you can say it is a `list of lists`, also known as a nested-list. It creates a list of elements that can comprise of logical values, numerical values, and strings.

In the below example, there are three lists inside a list, namely `log`, `ch`, and `int_vec`. Each of them has a data type or an R object of logical, numeric, and string/character.

`list_define <- list(log = TRUE, ch = "hello_datacamp", int_vec = sort(rep(seq(8,2, by = -2), times = 2)))`

[Powered By](https://www.datacamp.com/datalab) 

`list_define`

[Powered By](https://www.datacamp.com/datalab) 

$log

TRUE

$ch

'hello_datacamp'

$int_vec

1. 2
2. 2
3. 4
4. 4
5. 6
6. 6
7. 8
8. 8

- `log` is simply a logical operator, TRUE or FALSE
- `ch` is a character string `hello_datacamp`
- `int_vec` is a sequence of numerical values.

Since the `log` and `ch` are pretty straightforward, let's have a closer look at `int_vec`.

`int_vec = sort(rep(seq(8,2, by = -2), times = 2))`

[Powered By](https://www.datacamp.com/datalab) 

`int_vec`

[Powered By](https://www.datacamp.com/datalab) 

1. 2
2. 2
3. 4
4. 4
5. 6
6. 6
7. 8
8. 8

Let's understand the above expression step-by-step.

The `seq` function that produces a sequence of numbers in descending order ranging from 8 to 2.

Syntax of `seq()` function is given as: seq(x1,x2, by = y)

The first two arguments `x1` and `x2` tells R the range of the sequence, i.e., where to start and end the sequence. The `by` argument specifies the amount of increment or decrement of the sequence at each interval.

For example, the below line of code will generate a sequence starting from 100 to 200 with an increment step of 20.

`seq(100,200, by = 20)`

[Powered By](https://www.datacamp.com/datalab) 

1. 100
2. 120
3. 140
4. 160
5. 180
6. 200

In [our](https://www.datacamp.com/tutorial/utilities-in-r#our) example, the sequence function will output a sequence from 8 till 2 (inclusive) with a decrement step of 2, which returns a vector of length 4.

`a = seq(8,2, by = -2)`

[Powered By](https://www.datacamp.com/datalab) 

`a`

[Powered By](https://www.datacamp.com/datalab) 

1. 8
2. 6
3. 4
4. 2

Let's now understand the `rep` function.

It can repeat the input argument, which is usually a vector or a list using the `times` function, which takes an integer as an argument and repeats that many times through the input or the sequence. The `rep` function takes in two arguments: the input and the number of times you want the input to repeat or replicated.

Applying the `rep` function on [our](https://www.datacamp.com/tutorial/utilities-in-r#our) example, which is a vector of length 4 yields an output vector of length 8.

`b = rep(a, times = 2)`

[Powered By](https://www.datacamp.com/datalab) 

If you want each element of the vector or list to be repeated instead of the complete vector, then there is an alternative to `times`, i.e., by using the `each` argument.

The apparent difference by using `times` and `each` is that pattern in which each element occurs is not the same.

`rep(a, each = 2)`

[Powered By](https://www.datacamp.com/datalab) 

1. 8
2. 8
3. 6
4. 6
5. 4
6. 4
7. 2
8. 2

Last but not least, the `sort()` function. It is a self-explanatory and a generic function used for sorting many data structures like a vector or list. It is not limited to only numerical values but can also be used on logical values, and characters. By default, it sorts the elements in ascending order.

Let's put the output of the `rep` function to the `sort` function to arrive at the final output.

`sort(b)`

[Powered By](https://www.datacamp.com/datalab) 

1. 2
2. 2
3. 4
4. 4
5. 6
6. 6
7. 8
8. 8

Great! So you were successful in solving the lengthy-expression `int_vec`, which was inside the list `list_define` in such an easy manner.

Further, let's find out the contents of the list `list_define` for which you will make use of the `str()` function. The `str()` function in R allows you to display the structure of R objects.

`str(list_define)`

[Powered By](https://www.datacamp.com/datalab) 

`List of 3  $ log    : logi TRUE  $ ch     : chr "hello_datacamp"  $ int_vec: num [1:8] 2 2 4 4 6 6 8 8`

[Powered By](https://www.datacamp.com/datalab) 

Let's look at some of the cool R expressions:

- `is` function can be used to check the type of your data structure, which returns a logical and can come handy when dealing with conditional statements.

`is.list(list_define) #returns true if the argument passed is a list.`

[Powered By](https://www.datacamp.com/datalab) 

`TRUE`

[Powered By](https://www.datacamp.com/datalab) 

Whereas, it returns FALSE if a vector, which is not a list, is passed as shown in the cell below.

`is.list(c(1,2,3)) #returns false since you passed a vector.`

[Powered By](https://www.datacamp.com/datalab) 

`FALSE`

[Powered By](https://www.datacamp.com/datalab) 

- Converting a vector to a list is so simple in R. All you need to do is use the `as` function followed by `.list()`, and pass the vector as an argument. That's all it takes to convert a vector to a list.

`vec_to_list <- as.list(c(1,2,3))`

[Powered By](https://www.datacamp.com/datalab) 

`is.list(vec_to_list) #verify it with is.list()`

[Powered By](https://www.datacamp.com/datalab) 

`TRUE`

[Powered By](https://www.datacamp.com/datalab) 

- On the other hand, a list can be unrolled into a vector by using the `unlist` function. R does this conversion by simply flattening the entire list structure and finally outputting a single vector.

`list_to_vec <- unlist(vec_to_list)`

[Powered By](https://www.datacamp.com/datalab) 

`list_to_vec`

[Powered By](https://www.datacamp.com/datalab) 

1. 1
2. 2
3. 3

Similar to `is.list()`, you can use `is.vector()` to find out whether the given argument is a vector or not.

`is.vector(list_to_vec)`

[Powered By](https://www.datacamp.com/datalab) 

`TRUE`

[Powered By](https://www.datacamp.com/datalab) 

Let's convert the big list `list_define` to a vector. Point to note here is that a vector can only contain a single data type or R object. Hence, both the `logical` as well as `numerical` values will be converted to strings.

`unlist(list_define)`

[Powered By](https://www.datacamp.com/datalab) 

log

'TRUE'

ch

'hello_datacamp'

int_vec1

'2'

int_vec2

'2'

int_vec3

'4'

int_vec4

'4'

int_vec5

'6'

int_vec6

'6'

int_vec7

'8'

int_vec8

'8'

Before moving onto the next topic, let's look at the `append()` and `rev()` function.

- As the name suggests, `append()` function allows you to append or add two or more vector or a list to an existing or a new vector or list.

Let's try out the `append()` function on the `list_define` list. You would notice that the list will now consist of 6 elements instead of 3 since you appended the same list with itself.

`str(append(list_define, list_define))`

[Powered By](https://www.datacamp.com/datalab) 

`List of 6  $ log    : logi TRUE  $ ch     : chr "hello_datacamp"  $ int_vec: num [1:8] 2 2 4 4 6 6 8 8  $ log    : logi TRUE  $ ch     : chr "hello_datacamp"  $ int_vec: num [1:8] 2 2 4 4 6 6 8 8`

[Powered By](https://www.datacamp.com/datalab) 

- Finally, let's reverse or change the order of the `list_define` list with the help of the `rev()` function in R.

`str(rev(list_define))`

[Powered By](https://www.datacamp.com/datalab) 

`List of 3  $ int_vec: num [1:8] 2 2 4 4 6 6 8 8  $ ch     : chr "hello_datacamp"  $ log    : logi TRUE`

[Powered By](https://www.datacamp.com/datalab) 

## Regular Expressions

A lot of people find regular expression a complex topic to learn. However, it is an essential topic not only in R but across various programming languages like Python. Many programming languages, including R, provide in-built regular expression capability.

A regular expression can be used in so many applications, and it comes in handy, especially when you want to preprocess text data. It is used in various Natural Language Processing (NLP) problems.

It is also used in query search engines and text editors.

Regular expressions, also known as `regex` or `regexp` or `rational operators`, are a sequence of characters that define a search pattern. Generally, these search patterns are used by various string searching algorithms for finding a pattern or finding and replacing the pattern or filtering a matched pattern.

Let's start this topic by understanding the use of `grep()` and `grepl()` function.

For simplicity, let's define a row-vector `animals_regex` of length 5 on which you will learn to apply regex patterns.

`animals_regex <- c('cat','dog','cheetah','lion','mice')`

[Powered By](https://www.datacamp.com/datalab) 

First, let's understand the `grepl()` function. The `grepl()` function returns a logical output meaning that if the string matches the pattern, then it returns TRUE else FALSE.

Below is a straightforward and intuitive syntax of the `grepl()` function where the first argument is the pattern you want to match while the second argument is the string or the input from which you want to find or filter the pattern. You can ignore the remaining arguments for now. grepl(pattern, x, ignore.case = FALSE, perl = FALSE, fixed = FALSE, useBytes = FALSE) Let's find out which out of the above five animals have a `c` in them with the help of the `grepl()` function.

In this case, you are looking for the animals which have `c` in them, which directly means that the pattern here is nothing but `c` itself.

`grepl(pattern = 'c', x = animals_regex)`

[Powered By](https://www.datacamp.com/datalab) 

1. TRUE
2. FALSE
3. TRUE
4. FALSE
5. TRUE

From the above output, you can observe that, since there is a `c` in cat, cheetah, and mice, so a TRUE is returned for those indices in the vector `animals_regex`, while FALSE was returned for the ones which did not match with the pattern `c`.

Let's find out the elements that start with `c` and not just have a character `c` in their name.

To achieve this, all you need to do is use a $^$ (caret) sign at the beginning of the pattern you would like to find.

``grepl(pattern = '^c', x = animals_regex) #only cat and cheetah start with `c`.``

[Powered By](https://www.datacamp.com/datalab) 

1. TRUE
2. FALSE
3. TRUE
4. FALSE
5. FALSE

So from the above output, you can see that since only cat and cheetah start with a `c`, hence, only those positions are returned as TRUE.

Similar to the $^$ sign, the `$` sign can be used at the end of the pattern you would like to find to match the elements that end with the specified pattern. To find out an animal that ends with an `n`, you can simply use `n`, followed by the `$` sign.

``grepl(pattern = 'n$', x = animals_regex) #only lion ends with an `n`.``

[Powered By](https://www.datacamp.com/datalab) 

1. FALSE
2. FALSE
3. FALSE
4. TRUE
5. FALSE

**Note:** To learn more about regular expressions, simply type `?regex` in jupyter notebook code cell and documentation on regex will pop-up. Also, if you want to learn more about regular expressions, you could go through [this source](https://regexr.com/), which provides you a tool to design your search patterns and then allows you to test it on your input strings.

- Similar to the `grepl()` function, there is a `grep()` function, which instead of the logical output, returns the index of the vector/matrix that matches the given pattern.

The syntax of `grep()` function is exactly same as the `grepl()` function and is given as: grep(pattern, x, ignore.case = FALSE, perl = FALSE, value = FALSE, fixed = FALSE, useBytes = FALSE, invert = FALSE) Let's take the same example as [above](https://www.datacamp.com/tutorial/utilities-in-r#above) but this time apply the `grep()` function on it!

`grep(pattern = 'c', x = animals_regex)`

[Powered By](https://www.datacamp.com/datalab) 

1. 1
2. 3
3. 5

As you would expect, the above output returns the index of the elements cat, cheetah, and mice, and not TRUE/FALSE. And that's pretty much about it!

Let's use the `which` function to compare the `grep()` and `grepl()` function. The `which()` function simply returns the indices of the vector for the `TRUE` indices of a logical object.

Now if you connect the dots, you would have understood that since the `grepl()` function has the capability to return a logical object, it will be simply passed to the `which()` function which will then convert the output similar to what you would expect from a `grep()` function.

`which(grepl(pattern = 'c', x = animals_regex))`

[Powered By](https://www.datacamp.com/datalab) 

1. 1
2. 3
3. 5

Similar to the `grepl()` function, the `grep()` function also knows how to handle different types of regular expression patterns.

If you apply the `grep()` function to find out the elements in animals_regex vector that end with `n`, you would expect an output of 4 since only `lion` ends with `n` as shown below.

`grep(pattern = 'n$', x = animals_regex)`

[Powered By](https://www.datacamp.com/datalab) 

`4`

[Powered By](https://www.datacamp.com/datalab) 

Well done!

You have learned some basics of regular expressions like how you can filter out the elements from a vector that matches the given pattern. However, R is not limited to just pattern matching. It has a handful of functions, and out of which `sub()` function is one of them.

The `sub()` function, instead of filtering the matched pattern, replaces the matches with other strings. Let's understand it more deeply!

- The `sub()` function primarily takes three arguments as an input that are:
    - **pattern** which you would like to match or the regular expression,
    - **replacement** value which will be placed at the matched element of the vector and,
    - **x** the input vector string on which you will apply the regex.

The syntax is given as: sub(pattern, replacement, x, ignore.case = FALSE, perl = FALSE,fixed = FALSE, useBytes = FALSE) This time also let's take the same example as [above](https://www.datacamp.com/tutorial/utilities-in-r#above) to understand its functionality!

`sub(pattern = 'c', replacement = 'a', x = animals_regex)`

[Powered By](https://www.datacamp.com/datalab) 

1. 'aat'
2. 'dog'
3. 'aheetah'
4. 'lion'
5. 'miae'

From the above output, you can observe that the `cat` string gets replaced with `aat`, the `cheetah` string gets replaced to `aheetah`, and the `mice` string gets converted to `miae`. For these elements, the pattern was successfully matched.

Also, note that the `sub()` looks for only the first match in the string, which means that if there are two `c` in a string, only the first occurrence of `c` will be replaced with `a` while the second one will remain unchanged.

If you still want to replace every single match of a pattern in a vector string better, use the `gsub()` function, which is out of the scope of this tutorial!

Before moving on to the next topic, let's try one more interesting expression.

This time you will make use of the `|` (or) operator which will try to match any of the defined patterns and if it matches, replace it with `-`. Remember, since you use `gsub()` function, it will replace every single match of a pattern in a string.

``gsub(pattern = 'c|d|l', replacement = '-', x = animals_regex) #animals with `c`,`d`,`l` gets replaced with `-`.``

[Powered By](https://www.datacamp.com/datalab) 

1. '-at'
2. '-og'
3. '-heetah'
4. '-ion'
5. 'mi-e'

Let's move onto the final topic of today's tutorial, i.e., Time and Dates!

## Time and Dates

Time and date information can be quite useful in various scenarios. For example, let's say you are working on a Computer Vision related problem and you would like to find out the FPS (frames per second) at which your algorithm is running. In such a use-case, you could use the Time object to find out the processing speed of your computer vision algorithm. For other specific problems like time-series forecasting and seasonality studies, R's potential can be used to the full extent.

For starters, let's quickly print today's date using R with a simple command `Sys.Date()`. Here Sys refers to the system, which means it returns systems approximation of date.

`Sys.Date()`

[Powered By](https://www.datacamp.com/datalab) 

2020-02-04

Simple, isn't it?

R's time and dates belong to `Date` object, or you can say that the data type is `Date`. It can be verified using the `class` function that you learned in [Data Types in R](https://www.datacamp.com/tutorial/data-types-in-r) tutorial.

Similar to the Date function, you have a `time()` function which returns the systems current time, in fact, it returns both the time and date as an output.

`Sys.time()`

[Powered By](https://www.datacamp.com/datalab) 

`[1] "2020-02-04 02:05:04 IST"`

[Powered By](https://www.datacamp.com/datalab) 

### Creating Date Objects

You learned how to get the current date and time. Let's now find out how you can create dates for other days by passing a mere string as an argument.

To create a date object for 10th May 1993, you will use the following syntax:

`date_may <- as.Date('1993-05-10') #converts character string to a date object`

[Powered By](https://www.datacamp.com/datalab) 

`date_may`

[Powered By](https://www.datacamp.com/datalab) 

1993-05-10

`class(date_may)`

[Powered By](https://www.datacamp.com/datalab) 

`'Date'`

[Powered By](https://www.datacamp.com/datalab) 

One important point to note here is that the R's `Date` function by default expects you to enter the date in `YYYY-MM-DD` format if you try to interchange the year with the month or day it would result in an error. Let's try it out!

`date_may <- as.Date('05-1993-10') #R follows the ISO date format by default`

[Powered By](https://www.datacamp.com/datalab) 

`Error in charToDate(x): character string is not in a standard unambiguous format Traceback:  1. as.Date("05-1993-10")  2. as.Date.character("05-1993-10")  3. charToDate(x)  4. stop("character string is not in a standard unambiguous format")`

[Powered By](https://www.datacamp.com/datalab) 

But the good thing is, you could change the format explicitly by passing an argument `format` and customize it accordingly.

`date_may <- as.Date('05-1993-10', format = '%m-%Y-%d')`

[Powered By](https://www.datacamp.com/datalab) 

The `as.Date()` function will accept different date formats, but at the end, it will convert it back to the ISO date format, you can see that by printing the `date_may` variable.

`date_may`

[Powered By](https://www.datacamp.com/datalab) 

1993-05-10

`date_may <- as.Date('05-10-1993', format = '%m-%d-%Y')`

[Powered By](https://www.datacamp.com/datalab) 

`date_may`

[Powered By](https://www.datacamp.com/datalab) 

1993-05-10

### Date Arithmetic

Wouldn't it be awesome if you could apply mathematical operations like addition and subtraction to the Date objects in R?

Let's add 1 to the `date_may` variable, and you would observe that it will show you one day later date.

`date_may + 1`

[Powered By](https://www.datacamp.com/datalab) 

1993-05-11

Great, so as you can see from the above output, adding one changed the date to 11th May 1993 from 10th May 1993. Similarly, you could subtract one from the date.

Let's say you want to find out the time difference between you and your elder sibling's date of birth.

`elder_sib <- as.Date('1989-03-21')`

[Powered By](https://www.datacamp.com/datalab) 

`date_may - elder_sib`

[Powered By](https://www.datacamp.com/datalab) 

`Time difference of 1511 days`

[Powered By](https://www.datacamp.com/datalab) 

## Conclusion

Congratulations on finishing the tutorial.