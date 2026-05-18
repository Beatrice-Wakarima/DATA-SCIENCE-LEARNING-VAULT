# Subsetting Datasets in R

Subsetting datasets is a crucial skill for any data professional. Learn and practice subsetting data in this quick interactive tutorial!

Oct 8, 2018 · 6 min read

Contents

- [Subsetting Rows and Columns by Index](https://www.datacamp.com/tutorial/subsetting-datasets-r#subsetting-rows-and-columns-by-index-onewa)

- [Subsetting Rows and Columns by Name](https://www.datacamp.com/tutorial/subsetting-datasets-r#subsetting-rows-and-columns-by-name-inr,t)

- [Subsetting Rows and Columns by Value](https://www.datacamp.com/tutorial/subsetting-datasets-r#subsetting-rows-and-columns-by-value-subse)

- [Practice Exercises](https://www.datacamp.com/tutorial/subsetting-datasets-r#practice-exercises-%3Cstro)

## Training more people?

Get your team access to the full DataCamp for business platform.

For a bespoke solution [book a demo](https://www.datacamp.com/business/demo-2).

- [Subsetting Rows and Columns by Index](https://www.datacamp.com/tutorial/subsetting-datasets-r#subsetting-rows-and-columns-by-index)
- [Subsetting Rows and Columns by Name](https://www.datacamp.com/tutorial/subsetting-datasets-r#subsetting-rows-and-columns-by-name)
- [Subsetting Rows and Columns by Value](https://www.datacamp.com/tutorial/subsetting-datasets-r#subsetting-rows-and-columns-by-value)
- [Practice Exercises](https://www.datacamp.com/tutorial/subsetting-datasets-r#practice-exercises)

Whether you're comparing how different demographics respond to marketing campaigns, zooming in on a specific time frame, or pulling information about a select few products from the inventory, subsetting datasets enables you to extract useful observations in your dataset. R is a great tool that makes subsetting data easy and intuitive. By the end of this tutorial, you'll have the know-how to extract the information you want from your dataset.

Subsetting your data does not change the content of your data, but simply selects the portion most relevant to the goal you have in mind. In general, there are three ways to subset the rows and columns of your dataset—by index, by name, and by value.

## Subsetting Rows and Columns by Index

One way to subset your rows and columns is by your dataset's indices. This is the same as describing your rows and columns as "the first row", "all rows in second and fifth columns", or "the first row in second to fifth columns". Let's specify such phrases using a dataset called `iris` in R. From its [documentation](https://www.rdocumentation.org/packages/datasets/versions/3.5.1/topics/iris), "[t]his famous (Fisher's or Anderson's) iris dataset gives the measurements in centimeters of the variables sepal length and width and petal length and width, respectively, for 50 flowers from each of 3 species of iris. The species are _Iris setosa, versicolor_, and _virginica_."

To subset your data, square brackets are used after your dataset object. The rows of your dataset are specified as the first element inside the square brackets, and the columns of your dataset are specified as the second, separated by a comma:

```
data[rows, columns]
```

## Subsetting Rows and Columns by Name

In R, the rows and columns of your dataset have name attributes. Row names are rarely used and by default provide indices—integers numbering from 1 to the number of rows of your dataset—just like what you saw in the previous section. In fact, if you called `rownames()` on the `iris` dataset, you will see that these are just indexed from 1 to 150:

```
 > rownames(iris)
[1] "1"   "2"   "3"   "4"   "5"   "6"   "7"   "8"   "9"   "10"  "11"  "12"  "13"  "14"
[15] "15"  "16"  "17"  "18"  "19"  "20"  "21"  "22"  "23"  "24"  "25"  "26"  "27"  "28"
[29] "29"  "30"  "31"  "32"  "33"  "34"  "35"  "36"  "37"  "38"  "39"  "40"  "41"  "42"
[43] "43"  "44"  "45"  "46"  "47"  "48"  "49"  "50"  "51"  "52"  "53"  "54"  "55"  "56"
[57] "57"  "58"  "59"  "60"  "61"  "62"  "63"  "64"  "65"  "66"  "67"  "68"  "69"  "70"
[71] "71"  "72"  "73"  "74"  "75"  "76"  "77"  "78"  "79"  "80"  "81"  "82"  "83"  "84"
[85] "85"  "86"  "87"  "88"  "89"  "90"  "91"  "92"  "93"  "94"  "95"  "96"  "97"  "98"
[99] "99"  "100" "101" "102" "103" "104" "105" "106" "107" "108" "109" "110" "111" "112"
[113] "113" "114" "115" "116" "117" "118" "119" "120" "121" "122" "123" "124" "125" "126"
[127] "127" "128" "129" "130" "131" "132" "133" "134" "135" "136" "137" "138" "139" "140"
[141] "141" "142" "143" "144" "145" "146" "147" "148" "149" "150"

> nrow(iris)
[1] 150
```

Row names are more common in smaller datasets and are used to make observations in your dataset easily identifiable. For example, for a small dataset containing health information of a doctor's patients, the row names of this dataset could be the full names of the patients.

Column names on the other hand, are ubiquitous to almost any dataset. You can access these with the `colnames()` function or the `names()` function:

```
colnames(iris)
[1] "Sepal.Length" "Sepal.Width"  "Petal.Length" "Petal.Width"  "Species"     

names(iris)
[1] "Sepal.Length" "Sepal.Width"  "Petal.Length" "Petal.Width"  "Species"
```

To subset your dataset by the names of your rows and columns, simply use the square brackets again, prefixed by your dataset object:

It's important to note that both the row and column names are **characters**, so using single or double quotes is absolutely necessary!

## Subsetting Rows and Columns by Value

Subsetting your rows and columns by value often allows the most flexibility. For example, you can extract the data on _Iris setosa_ using a conditional statement like this:

```
> iris[iris$Species == "setosa", ]
Sepal.Length Sepal.Width Petal.Length Petal.Width Species
1           5.1         3.5          1.4         0.2  setosa
2           4.9         3.0          1.4         0.2  setosa
3           4.7         3.2          1.3         0.2  setosa
4           4.6         3.1          1.5         0.2  setosa

...

47          5.1         3.8          1.6         0.2  setosa
48          4.6         3.2          1.4         0.2  setosa
49          5.3         3.7          1.5         0.2  setosa
50          5.0         3.3          1.4         0.2  setosa
```

Conditional statements like `iris$Species == "setosa"` belong in the row element in the square brackets (i.e., the first element before the comma). In addition to the conditional statement in the first element, you can specify columns by index or name in the second element. In the console below, try selecting just the sepal measurements of _Iris setosa_:

### Recap

In this tutorial, you:

- Learned about subsetting your data frame by index. Rows and columns are indexed as integers from 1 to the number of rows and columns, respectively.
- Learned about subsetting your data frame by name. You learned that row names are rarely specified, and that column names are of character types.
- Learned to use conditional statements in the row element inside square brackets to subset your data frame by value.
- Learned to combine these methods to allow more flexible subsetting (e.g., using conditionals for rows and subsetting by index or name for columns).

Below are some exercises to help reinforce what you've learned. Practice makes perfect, so give these a try!