# R Programming Basics

#programming #r-language #data-science #statistics #analytics

## Overview

**R** is a programming language and free software environment for statistical computing and graphics. Developed in the early 1990s, it's become the de facto standard for statistical analysis and data visualization.

> [!quote] R Philosophy "R is a language and environment for statistical computing and graphics. It provides a wide variety of statistical and graphical techniques."

**Created by:** Ross Ihaka and Robert Gentleman **First Release:** 1993 **License:** GNU General Public License **Paradigm:** Multi-paradigm (array, object-oriented, functional, procedural)

## Why Learn R?

### Strengths

- 📊 **Statistical Analysis**: Built specifically for statistics
- 📈 **Data Visualization**: Exceptional plotting capabilities with [[ggplot2]]
- 📦 **Package Ecosystem**: 18,000+ packages on [[CRAN]]
- 🔬 **Research Community**: Widely used in academia and research
- 💰 **Free & Open Source**: No licensing costs

### Common Use Cases

- [[Statistical Analysis]]
- [[Data Science]] and [[Machine Learning]]
- [[Bioinformatics]] and genomics
- [[Time Series Analysis]]
- [[Survey Analysis]]
- Academic research and reporting

---

## Installation & Setup

### Installing R

bash

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install r-base r-base-dev

# macOS (using Homebrew)
brew install --cask r

# Windows: Download from https://cran.r-project.org/
```

### Installing RStudio

- **RStudio Desktop**: Free IDE for R
- **Download**: [https://www.rstudio.com/products/rstudio/download/](https://www.rstudio.com/products/rstudio/download/)
- **Alternative IDEs**: [[VSCode with R]], [[Emacs ESS]], [[Vim-R]]

### First R Session

r

```r
# Check R version
R.version.string

# Get help
?help
help.start()

# Basic calculation
2 + 2
```

---

## Data Types & Structures

#r/data-types

### Atomic Data Types

|Type|Description|Example|Test Function|
|---|---|---|---|
|**numeric**|Numbers (double)|`3.14`|`is.numeric()`|
|**integer**|Whole numbers|`42L`|`is.integer()`|
|**character**|Text strings|`"hello"`|`is.character()`|
|**logical**|Boolean values|`TRUE`, `FALSE`|`is.logical()`|
|**complex**|Complex numbers|`1+2i`|`is.complex()`|

r

```r
# Creating different data types
num_var <- 3.14
int_var <- 42L
char_var <- "Hello World"
log_var <- TRUE
complex_var <- 1+2i

# Check type
class(num_var)     # "numeric"
typeof(int_var)    # "integer"
str(char_var)      # chr "Hello World"
```

### Data Structures

#### 1. Vectors

**One-dimensional arrays of same data type**

r

```r
# Creating vectors
numbers <- c(1, 2, 3, 4, 5)
names <- c("Alice", "Bob", "Charlie")
flags <- c(TRUE, FALSE, TRUE)

# Vector operations
numbers * 2                    # Element-wise multiplication
numbers + c(10, 20, 30, 40, 50) # Element-wise addition
length(numbers)                # Vector length
numbers[1]                     # First element (1-indexed!)
numbers[c(1, 3, 5)]           # Multiple elements
numbers[-2]                    # All except 2nd element

# Named vectors
ages <- c(Alice = 25, Bob = 30, Charlie = 35)
ages["Alice"]                  # Access by name
```

#### 2. Lists

**Ordered collections that can hold different data types**

r

```r
# Creating lists
person <- list(
    name = "Alice",
    age = 25,
    married = TRUE,
    children = c("Emma", "Jack")
)

# Accessing list elements
person$name              # "Alice"
person[["age"]]          # 25
person[[2]]              # 25 (by position)
person["married"]        # Returns list with one element
person[c("name", "age")] # Multiple elements

# Adding elements
person$city <- "New York"
person[["salary"]] <- 75000
```

#### 3. Matrices

**Two-dimensional arrays of same data type**

r

```r
# Creating matrices
mat1 <- matrix(1:12, nrow = 3, ncol = 4)
mat2 <- matrix(1:12, nrow = 3, byrow = TRUE)

# Matrix operations
dim(mat1)           # Dimensions
nrow(mat1)          # Number of rows
ncol(mat1)          # Number of columns
mat1[2, 3]          # Element at row 2, col 3
mat1[2, ]           # Entire row 2
mat1[, 3]           # Entire column 3
mat1 %*% t(mat1)    # Matrix multiplication

# Named rows and columns
rownames(mat1) <- c("Row1", "Row2", "Row3")
colnames(mat1) <- c("Col1", "Col2", "Col3", "Col4")
```

#### 4. Data Frames

**Most important! Like a table/spreadsheet**

r

```r
# Creating data frames
df <- data.frame(
    name = c("Alice", "Bob", "Charlie"),
    age = c(25, 30, 35),
    salary = c(50000, 60000, 70000),
    married = c(TRUE, FALSE, TRUE),
    stringsAsFactors = FALSE  # Keep characters as characters
)

# Exploring data frame
head(df)            # First 6 rows
tail(df)            # Last 6 rows
str(df)             # Structure
summary(df)         # Summary statistics
dim(df)             # Dimensions
names(df)           # Column names
rownames(df)        # Row names

# Accessing data frame elements
df$name             # Column by name
df[["age"]]         # Column by name (alternative)
df[, "salary"]      # Column by name
df[2, ]             # Row 2
df[, 2]             # Column 2
df[1:2, c("name", "age")]  # Subset rows and columns

# Adding columns
df$department <- c("IT", "HR", "Finance")
df[["bonus"]] <- df$salary * 0.1
```

#### 5. Factors

**Categorical variables with levels**

r

```r
# Creating factors
gender <- factor(c("Male", "Female", "Female", "Male"))
education <- factor(
    c("High School", "Bachelor", "Master", "Bachelor"),
    levels = c("High School", "Bachelor", "Master", "PhD"),
    ordered = TRUE
)

# Factor properties
levels(gender)      # Available categories
nlevels(gender)     # Number of levels
table(gender)       # Frequency table

# Converting factors
as.numeric(education)        # Convert to numbers
as.character(gender)         # Convert to characters
```

---

## Variables & Assignment

#r/variables

### Assignment Operators

r

```r
# Three ways to assign (prefer <-)
x <- 10        # Preferred
x = 10         # Also works
10 -> x        # Unusual but valid

# Multiple assignment
a <- b <- c <- 5

# Assignment in function calls
mean(scores <- c(85, 90, 78, 92))  # Assigns and uses
```

### Variable Naming Rules

r

```r
# Valid names
my_variable <- 1
MyVariable <- 2
my.variable <- 3
variable123 <- 4

# Invalid names (will cause errors)
# 123variable <- 5    # Can't start with number
# my-variable <- 6    # Hyphens not allowed
# for <- 7            # Reserved word
```

### Environment & Scope

r

```r
# List all objects
ls()                    # Current environment
objects()               # Same as ls()

# Remove objects
rm(x)                   # Remove specific object
rm(list = ls())         # Remove all objects

# Check if object exists
exists("my_variable")

# Global vs local scope
global_var <- "I'm global"

my_function <- function() {
    local_var <- "I'm local"
    global_var <<- "Modified global"  # Global assignment
    return(local_var)
}
```

---

## Operators

#r/operators

### Arithmetic Operators

r

```r
x <- 10
y <- 3

x + y    # Addition (13)
x - y    # Subtraction (7)
x * y    # Multiplication (30)
x / y    # Division (3.333333)
x %/% y  # Integer division (3)
x %% y   # Modulus (1)
x ^ y    # Exponentiation (1000)
x ** y   # Alternative exponentiation (1000)
```

### Comparison Operators

r

```r
x == y   # Equal to (FALSE)
x != y   # Not equal to (TRUE)
x > y    # Greater than (TRUE)
x < y    # Less than (FALSE)
x >= y   # Greater than or equal (TRUE)
x <= y   # Less than or equal (FALSE)

# Vector comparisons
c(1, 2, 3) == c(1, 5, 3)  # Element-wise: TRUE FALSE TRUE
```

### Logical Operators

r

```r
TRUE & FALSE   # AND (FALSE)
TRUE | FALSE   # OR (TRUE)
!TRUE          # NOT (FALSE)

# Vectorized logical operators
c(T, F, T) & c(T, T, F)    # Element-wise AND: TRUE FALSE FALSE
c(T, F, T) | c(T, T, F)    # Element-wise OR: TRUE TRUE TRUE

# Short-circuit operators (for single values)
TRUE && FALSE   # AND with short-circuiting
TRUE || FALSE   # OR with short-circuiting
```

### Special Operators

r

```r
# %in% operator (very useful!)
"apple" %in% c("apple", "banana", "orange")  # TRUE
c(1, 2) %in% c(1, 2, 3, 4)                   # TRUE TRUE

# Assignment operators
x <- 5
x <<- 5    # Global assignment

# Other useful operators
1:10       # Sequence operator
x$y        # List/data frame accessor
x[[1]]     # List accessor
```

---

## Control Flow

#r/control-flow

### Conditional Statements

#### if/else

r

```r
# Basic if statement
x <- 10
if (x > 5) {
    print("x is greater than 5")
}

# if-else
if (x > 15) {
    print("x is large")
} else {
    print("x is not that large")
}

# if-else if-else
score <- 85
if (score >= 90) {
    grade <- "A"
} else if (score >= 80) {
    grade <- "B"
} else if (score >= 70) {
    grade <- "C"
} else {
    grade <- "F"
}

# Vectorized ifelse (very useful!)
scores <- c(95, 85, 75, 65)
grades <- ifelse(scores >= 90, "A",
                 ifelse(scores >= 80, "B", 
                        ifelse(scores >= 70, "C", "F")))

# Multiple condition ifelse with dplyr::case_when() (more readable)
# See [[dplyr]] notes for case_when examples
```

#### switch statement

r

```r
# switch with character
day <- "Monday"
activity <- switch(day,
    "Monday" = "Start of work week",
    "Friday" = "TGIF!",
    "Saturday" = "Weekend!",
    "Sunday" = "Weekend!",
    "Regular day"  # default
)

# switch with numeric
switch(3, "one", "two", "three", "four")  # Returns "three"
```

### Loops

#### for loops

r

```r
# Basic for loop
for (i in 1:5) {
    print(paste("Iteration:", i))
}

# Loop over vectors
fruits <- c("apple", "banana", "orange")
for (fruit in fruits) {
    print(paste("I like", fruit))
}

# Loop over data frame rows
for (i in 1:nrow(df)) {
    print(paste(df$name[i], "is", df$age[i], "years old"))
}

# Nested loops
for (i in 1:3) {
    for (j in 1:2) {
        print(paste("i =", i, ", j =", j))
    }
}
```

#### while loops

r

```r
# Basic while loop
count <- 1
while (count <= 5) {
    print(paste("Count:", count))
    count <- count + 1
}

# while with condition
x <- 10
while (x > 0) {
    print(x)
    x <- x - 2
}
```

#### repeat loops

r

```r
# repeat with break
x <- 1
repeat {
    print(x)
    x <- x + 1
    if (x > 5) break
}
```

### Loop Control

r

```r
# next (equivalent to continue)
for (i in 1:10) {
    if (i %% 2 == 0) next  # Skip even numbers
    print(i)
}

# break
for (i in 1:10) {
    if (i > 5) break
    print(i)
}
```

---

## Functions

#r/functions

### Built-in Functions

#### Mathematical Functions

r

```r
# Basic math
abs(-5)          # Absolute value (5)
sqrt(16)         # Square root (4)
exp(1)           # Exponential (2.718...)
log(10)          # Natural logarithm
log10(100)       # Base-10 logarithm (2)
round(3.14159, 2) # Round to 2 decimals (3.14)
ceiling(3.2)     # Round up (4)
floor(3.8)       # Round down (3)

# Trigonometric
sin(pi/2)        # Sine (1)
cos(0)           # Cosine (1)
tan(pi/4)        # Tangent (1)

# Statistical functions
numbers <- c(1, 2, 3, 4, 5, NA)
sum(numbers, na.rm = TRUE)      # Sum (15)
mean(numbers, na.rm = TRUE)     # Mean (3)
median(numbers, na.rm = TRUE)   # Median (3)
var(numbers, na.rm = TRUE)      # Variance
sd(numbers, na.rm = TRUE)       # Standard deviation
min(numbers, na.rm = TRUE)      # Minimum (1)
max(numbers, na.rm = TRUE)      # Maximum (5)
range(numbers, na.rm = TRUE)    # Min and max
quantile(numbers, na.rm = TRUE) # Quartiles
```

#### String Functions

r

```r
# Basic string operations
text <- "Hello World"
nchar(text)                    # Number of characters (11)
toupper(text)                  # "HELLO WORLD"
tolower(text)                  # "hello world"
substr(text, 1, 5)            # "Hello"
substring(text, 7)            # "World"

# String manipulation
paste("Hello", "World")        # "Hello World"
paste0("Hello", "World")       # "HelloWorld"
paste(c("A", "B"), 1:2, sep = "-")  # "A-1" "B-2"

# Pattern matching
grep("World", c("Hello World", "Goodbye"))  # 1 (index)
grepl("World", c("Hello World", "Goodbye")) # TRUE FALSE
gsub("World", "Universe", text)             # "Hello Universe"
```

### Creating Custom Functions

r

```r
# Basic function
my_function <- function(x, y) {
    result <- x + y
    return(result)  # return() is optional for last expression
}

# Function with default arguments
greet <- function(name, greeting = "Hello") {
    paste(greeting, name)
}
greet("Alice")                 # "Hello Alice"
greet("Bob", "Hi")            # "Hi Bob"

# Function with ... (dot-dot-dot) arguments
my_summary <- function(x, ...) {
    list(
        mean = mean(x, ...),
        median = median(x, ...),
        sd = sd(x, ...)
    )
}
my_summary(c(1, 2, 3, NA), na.rm = TRUE)

# Anonymous functions (lambda functions)
sapply(1:5, function(x) x^2)   # Square each number
# Or with new R 4.1+ syntax:
sapply(1:5, \(x) x^2)
```

### Function Environments & Scope

r

```r
# Lexical scoping
x <- 10
my_func <- function() {
    x <- 20    # Local x
    inner_func <- function() {
        x      # Uses local x from my_func (20)
    }
    inner_func()
}
my_func()  # Returns 20

# Global assignment within function
modify_global <- function() {
    global_var <<- "Changed from function"
}
```

---

## Data Import & Export

#r/data-io

### Reading Data

#### CSV Files

r

```r
# Basic CSV reading
df <- read.csv("data.csv")
df <- read.csv("data.csv", stringsAsFactors = FALSE)
df <- read.csv("data.csv", header = TRUE, sep = ",")

# More modern approach with readr package
library(readr)
df <- read_csv("data.csv")  # Faster and more consistent
df <- read_csv2("data.csv") # European format (semicolon separator)
```

#### Excel Files

r

```r
# Using readxl package
library(readxl)
df <- read_excel("data.xlsx")
df <- read_excel("data.xlsx", sheet = "Sheet2")
df <- read_excel("data.xlsx", range = "A1:D100")

# List sheets in Excel file
excel_sheets("data.xlsx")
```

#### Other Formats

r

```r
# Tab-separated values
df <- read.table("data.txt", header = TRUE, sep = "\t")
df <- read.delim("data.txt")  # Default is tab-separated

# Fixed-width files
df <- read.fwf("data.txt", widths = c(10, 5, 8))

# JSON files
library(jsonlite)
data <- fromJSON("data.json")

# RDS files (R's native format)
df <- readRDS("data.rds")

# R workspace
load("workspace.RData")
```

### Writing Data

r

```r
# CSV files
write.csv(df, "output.csv", row.names = FALSE)
write_csv(df, "output.csv")  # readr version

# Excel files
library(writexl)
write_xlsx(df, "output.xlsx")

# RDS files (preserves R data types)
saveRDS(df, "data.rds")

# R workspace (all objects)
save.image("workspace.RData")
save(df, my_list, file = "selected_objects.RData")
```

### Working with URLs

r

```r
# Read directly from URL
url <- "https://raw.githubusercontent.com/user/repo/main/data.csv"
df <- read.csv(url)

# Download file first
download.file(url, "local_data.csv")
df <- read.csv("local_data.csv")
```

---

## Data Manipulation Basics

#r/data-manipulation

### Base R Data Operations

#### Subsetting Data Frames

r

```r
# By column
df$name                    # Single column as vector
df["name"]                 # Single column as data frame
df[c("name", "age")]      # Multiple columns

# By row
df[1, ]                   # First row
df[1:3, ]                 # First three rows
df[c(1, 3, 5), ]         # Specific rows

# Conditional subsetting
df[df$age > 25, ]         # Rows where age > 25
df[df$name == "Alice", ]  # Rows where name is "Alice"
df[df$age > 25 & df$married == TRUE, ]  # Multiple conditions

# Using subset() function (more readable)
subset(df, age > 25)
subset(df, age > 25 & married == TRUE, select = c(name, age))
```

#### Adding/Modifying Columns

r

```r
# Add new column
df$new_column <- "some value"
df$age_group <- ifelse(df$age < 30, "Young", "Old")

# Modify existing column
df$age <- df$age + 1
df$name <- toupper(df$name)

# Transform multiple columns
df[c("age", "salary")] <- df[c("age", "salary")] * 1.1
```

#### Sorting

r

```r
# Sort by single column
df_sorted <- df[order(df$age), ]          # Ascending
df_sorted <- df[order(-df$age), ]         # Descending

# Sort by multiple columns
df_sorted <- df[order(df$age, -df$salary), ]  # Age asc, salary desc

# Using with()
df_sorted <- df[with(df, order(age, -salary)), ]
```

#### Aggregation

r

```r
# Summary statistics by group
aggregate(salary ~ married, data = df, mean)
aggregate(cbind(age, salary) ~ married, data = df, mean)

# Using by()
by(df$salary, df$married, mean)

# Using tapply()
tapply(df$salary, df$married, mean)
tapply(df$salary, list(df$married, df$department), mean)
```

### Modern Approaches

> [!tip] Modern Data Manipulation For more efficient and readable data manipulation, consider learning [[dplyr]] and [[tidyr]] from the [[tidyverse]]. These packages provide more intuitive syntax for data manipulation tasks.

---

## Basic Statistics

#r/statistics

### Descriptive Statistics

r

```r
# Sample data
data <- c(23, 25, 28, 30, 32, 35, 38, 40, 42, 45)

# Central tendency
mean(data)                    # Arithmetic mean
median(data)                  # Median
Mode <- function(x) {         # Mode (custom function)
    ux <- unique(x)
    ux[which.max(tabulate(match(x, ux)))]
}

# Dispersion
var(data)                     # Variance
sd(data)                      # Standard deviation
range(data)                   # Min and max
diff(range(data))             # Range as single value
IQR(data)                     # Interquartile range

# Distribution shape
library(moments)
skewness(data)                # Skewness
kurtosis(data)                # Kurtosis

# Quantiles
quantile(data)                # 0%, 25%, 50%, 75%, 100%
quantile(data, c(0.1, 0.9))   # 10th and 90th percentiles
```

### Frequency Tables

r

```r
# Simple frequency table
colors <- c("red", "blue", "red", "green", "blue", "red")
table(colors)

# Cross-tabulation
df <- data.frame(
    gender = c("M", "F", "M", "F", "M", "F"),
    education = c("HS", "College", "College", "HS", "Graduate", "College")
)
table(df$gender, df$education)

# Proportions
prop.table(table(colors))     # Proportions
prop.table(table(df$gender, df$education), 1)  # Row proportions
prop.table(table(df$gender, df$education), 2)  # Column proportions
```

### Statistical Tests

#### t-tests

r

```r
# One-sample t-test
data <- rnorm(30, mean = 100, sd = 15)
t.test(data, mu = 100)        # Test if mean equals 100

# Two-sample t-test
group1 <- rnorm(20, mean = 100, sd = 10)
group2 <- rnorm(25, mean = 105, sd = 12)
t.test(group1, group2)        # Welch's t-test (default)
t.test(group1, group2, var.equal = TRUE)  # Student's t-test

# Paired t-test
before <- c(120, 135, 128, 140, 132)
after <- c(118, 130, 125, 138, 130)
t.test(before, after, paired = TRUE)
```

#### Chi-square Tests

r

```r
# Chi-square goodness of fit
observed <- c(20, 25, 15, 40)
expected <- c(25, 25, 25, 25)
chisq.test(observed, p = expected/sum(expected))

# Chi-square test of independence
contingency_table <- matrix(c(10, 15, 20, 25), nrow = 2)
chisq.test(contingency_table)
```

#### Correlation

r

```r
# Correlation matrix
numeric_data <- mtcars[, c("mpg", "hp", "wt")]
cor(numeric_data)                    # Pearson correlation
cor(numeric_data, method = "spearman")  # Spearman correlation

# Correlation test
cor.test(mtcars$mpg, mtcars$hp)      # Test significance
```

---

## Basic Plotting

#r/plotting #r/visualization

### Base R Plots

#### Scatter Plots

r

```r
# Basic scatter plot
plot(mtcars$hp, mtcars$mpg)
plot(mtcars$hp, mtcars$mpg, 
     xlab = "Horsepower", 
     ylab = "Miles per Gallon",
     main = "MPG vs Horsepower",
     col = "blue",
     pch = 19)  # Point character

# Add trend line
abline(lm(mpg ~ hp, data = mtcars), col = "red")
```

#### Line Plots

r

```r
# Basic line plot
x <- 1:10
y <- x^2
plot(x, y, type = "l")           # type = "l" for lines
plot(x, y, type = "b")           # type = "b" for both points and lines

# Multiple lines
plot(x, x^2, type = "l", col = "red", ylim = c(0, 100))
lines(x, x^1.5, col = "blue")
legend("topleft", c("x²", "x^1.5"), col = c("red", "blue"), lty = 1)
```

#### Bar Plots

r

```r
# Simple bar plot
counts <- table(mtcars$cyl)
barplot(counts)
barplot(counts, 
        main = "Number of Cars by Cylinder",
        xlab = "Cylinders",
        ylab = "Count",
        col = c("red", "green", "blue"))

# Stacked bar plot
counts_matrix <- table(mtcars$cyl, mtcars$gear)
barplot(counts_matrix, col = rainbow(3), legend = TRUE)
```

#### Histograms

r

```r
# Basic histogram
hist(mtcars$mpg)
hist(mtcars$mpg, 
     breaks = 20,
     main = "Distribution of MPG",
     xlab = "Miles per Gallon",
     col = "lightblue",
     border = "black")

# Add normal curve
hist(mtcars$mpg, freq = FALSE, col = "lightblue")
curve(dnorm(x, mean = mean(mtcars$mpg), sd = sd(mtcars$mpg)), 
      add = TRUE, col = "red", lwd = 2)
```

#### Box Plots

r

```r
# Single box plot
boxplot(mtcars$mpg)

# Box plots by group
boxplot(mpg ~ cyl, data = mtcars,
        main = "MPG by Number of Cylinders",
        xlab = "Cylinders",
        ylab = "Miles per Gallon",
        col = c("red", "green", "blue"))
```

### Plot Customization

r

```r
# Comprehensive plot customization
plot(mtcars$hp, mtcars$mpg,
     main = "Fuel Efficiency vs Engine Power",
     sub = "Data from 1974 Motor Trend",
     xlab = "Gross Horsepower",
     ylab = "Miles per Gallon",
     col = as.factor(mtcars$cyl),     # Color by cylinder
     pch = 19,                        # Solid circles
     cex = 1.2,                       # Point size
     xlim = c(50, 350),
     ylim = c(10, 35))

# Add legend
legend("topright", 
       legend = c("4 cyl", "6 cyl", "8 cyl"),
       col = 1:3,
       pch = 19,
       title = "Cylinders")

# Add grid
grid(col = "gray", lty = "dotted")
```

### Multiple Plots

r

```r
# 2x2 layout
par(mfrow = c(2, 2))
plot(mtcars$hp, mtcars$mpg, main = "MPG vs HP")
plot(mtcars$wt, mtcars$mpg, main = "MPG vs Weight")
hist(mtcars$mpg, main = "MPG Distribution")
boxplot(mpg ~ cyl, data = mtcars, main = "MPG by Cylinders")

# Reset to single plot
par(mfrow = c(1, 1))
```

> [!tip] Advanced Visualization For more sophisticated and publication-ready graphics, learn [[ggplot2]], which provides a grammar of graphics approach to visualization.

---

## Package Management

#r/packages

### Installing Packages

r

```r
# From CRAN
install.packages("dplyr")
install.packages(c("ggplot2", "readr", "tidyr"))

# From Bioconductor
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install("GenomicFeatures")

# From GitHub
if (!requireNamespace("devtools", quietly = TRUE))
    install.packages("devtools")
devtools::install_github("username/packagename")

# Install specific version
devtools::install_version("ggplot2", version = "3.3.0")
```

### Loading Packages

r

```r
# Load package
library(dplyr)          # Preferred method
require(dplyr)          # Alternative (returns TRUE/FALSE)

# Load without attaching to namespace
dplyr::filter(mtcars, cyl == 4)

# Check if package is installed
if (requireNamespace("dplyr", quietly = TRUE)) {
    library(dplyr)
} else {
    install.packages("dplyr")
    library(dplyr)
}
```

### Package Information

r

```r
# List installed packages
installed.packages()
library()

# Get package information
packageDescription("ggplot2")
packageVersion("dplyr")

# Update packages
update.packages()
update.packages(ask = FALSE)  # Update without prompting

# Remove packages
remove.packages("packagename")

# Check for package updates
old.packages()
```

### Essential Packages to Know

#### [[Tidyverse]]

r

```r
# Meta-package including dplyr, ggplot2, tidyr, readr, etc.
install.packages("tidyverse")
library(tidyverse)
```

#### Data Manipulation

- [[dplyr]]: Data frame manipulation
- [[tidyr]]: Data reshaping and tidying
- [[data.table]]: High-performance data manipulation
- [[stringr]]: String manipulation

#### Visualization

- [[ggplot2]]: Grammar of graphics
- [[plotly]]: Interactive plots
- [[lattice]]: Trellis graphics
- [[RColorBrewer]]: Color palettes

#### Statistical Analysis

- [[broom]]: Tidy statistical output
- [[caret]]: Classification and regression training
- [[randomForest]]: Random forest algorithm
- [[survival]]: Survival analysis

#### Data Import/Export

- [[readr]]: Fast CSV reading
- [[readxl]]: Excel files
- [[haven]]: SPSS, Stata, SAS files
- [[DBI]] + [[RSQLite]]: Database connections

---

## Working Directory & File Paths

#r/file-management

### Getting Oriented

r

```r
# Current working directory
getwd()

# Set working directory
setwd("/path/to/your/project")
setwd("C:/Users/YourName/Documents/R_Projects")  # Windows
setwd("~/Documents/R_Projects")                   # Mac/Linux

# List files in directory
list.files()
list.files(pattern = "\\.csv$")  # Only CSV files
list.files(recursive = TRUE)     # Include subdirectories

# File and directory operations
file.exists("data.csv")
dir.exists("data_folder")
dir.create("new_folder")
file.copy("source.csv", "backup.csv")
file.remove("old_file.csv")
```

### Working with Paths

r

```r
# Build file paths (works across operating systems)
file.path("data", "raw", "dataset.csv")

# Get file information
file.info("data.csv")

# Basename and dirname
basename("/path/to/file.csv")    # "file.csv"
dirname("/path/to/file.csv")     # "/path/to"

# File extensions
tools::file_ext("data.csv")      # "csv"
tools::file_path_sans_ext("data.csv")  # "data"
```

> [!tip] Best Practice Use [[RStudio Projects]] or the [[here]] package for better path management in projects.

---

## Debugging & Error Handling

#r/debugging #r/error-handling

### Common Error Types

r

```r
# Syntax errors (caught before execution)
# Missing parenthesis, brackets, etc.

# Runtime errors
x <- "hello"
x + 5  # Error: non-numeric argument to binary operator

# Logical errors (code runs but produces wrong result)
mean(c(1, 2, 3, NA))          # Returns NA (forgot na.rm = TRUE)
mean(c(1, 2, 3, NA), na.rm = TRUE)  # Correct: returns 2
```

### Debugging Techniques

r

```r
# Print debugging
my_function <- function(x, y) {
    print(paste("x =", x, "y =", y))  # Debug print
    result <- x * y
    print(paste("result =", result))   # Debug print
    return(result)
}

# Using browser() for interactive debugging
my_function <- function(x, y) {
    browser()  # Stops execution here for inspection
    result <- x * y
    return(result)
}

# Debug a function
debug(my_function)    # Enter debug mode
my_function(3, 4)     # Will stop at each line
undebug(my_function)  # Exit debug mode

# Trace function calls
trace(my_function)
untrace(my_function)
```

### Error Handling

r

```r
# try() - continues execution even if error occurs
result <- try(log("not a number"), silent = TRUE)
if (inherits(result, "try-error")) {
    print("An error occurred")
}

# tryCatch() - more sophisticated error handling
safe_division <- function(x, y) {
    tryCatch({
        if (y == 0) stop("Division by zero!")
        return(x / y)
    }, error = function(e) {
        message("Error caught: ", e$message)
        return(NA)
    }, warning = function(w) {
        message("Warning: ", w$message)
    })
}

safe_division(10, 0)  # Returns NA with message
safe_division(10, 2)  # Returns 5

# stop() - throw custom errors
validate_input <- function(x) {
    if (!is.numeric(x)) {
        stop("Input must be numeric")
    }
    if (any(x < 0)) {
        stop("All values must be non-negative")
    }
}

# warning() - issue warnings
risky_function <- function(x) {
    if (x > 100) {
        warning("Large input value might cause issues")
    }
    return(x^2)
}
```

---

## Best Practices & Style Guide

#r/best-practices #r/style-guide

### Naming Conventions

r

```r
# Variables and functions: use snake_case
my_variable <- 10
calculate_mean <- function(x) mean(x, na.rm = TRUE)

# Constants: use UPPER_CASE
MAX_ITERATIONS <- 1000
DEFAULT_TIMEOUT <- 30

# Avoid single letter names (except for loops)
# Good
student_ages <- c(20, 21, 19, 22)
for (i in seq_along(student_ages)) {
    # process
}

# Avoid
x <- c(20, 21, 19, 22)  # What is x?
```

### Code Organization

r

```r
# Use consistent spacing
# Good
result <- my_function(x = 5, y = 10)
if (condition) {
    do_something()
}

# Avoid
result<-my_function(x=5,y=10)
if(condition){
do_something()
}

# Line length: aim for < 80 characters
# Break long lines sensibly
long_function_call <- some_function(
    parameter_one = "value_one",
    parameter_two = "value_two",
    parameter_three = "value_three"
)

# Comment your code
# Calculate customer lifetime value
customer_ltv <- customer_data %>%
    group_by(customer_id) %>%
    summarise(
        total_spent = sum(order_value),
        order_count = n(),
        avg_order_value = mean(order_value)
    )
```

### Function Design

r

```r
# Good function design principles

# 1. Single responsibility
calculate_mean <- function(x, remove_na = TRUE) {
    if (remove_na) {
        x <- x[!is.na(x)]
    }
    sum(x) / length(x)
}

# 2. Clear parameter names with defaults
read_sales_data <- function(file_path, 
                           skip_rows = 0, 
                           date_format = "%Y-%m-%d") {
    # Function body
}

# 3. Input validation
safe_sqrt <- function(x) {
    if (!is.numeric(x)) {
        stop("Input must be numeric")
    }
    if (any(x < 0, na.rm = TRUE)) {
        warning("Negative values will return NaN")
    }
    sqrt(x)
}

# 4. Consistent return types
get_summary_stats <- function(x) {
    list(
        mean = mean(x, na.rm = TRUE),
        median = median(x, na.rm = TRUE),
        sd = sd(x, na.rm = TRUE),
        n = length(x[!is.na(x)])
    )
}
```

### Project Structure

```
my_r_project/
├── data/
│   ├── raw/           # Original, immutable data
│   ├── processed/     # Cleaned data
│   └── external/      # Third-party data
├── R/
│   ├── functions.R    # Custom functions
│   ├── analysis.R     # Main analysis
│   └── visualization.R # Plotting code
├── outputs/
│   ├── figures/       # Plots and charts
│   └── tables/        # Summary tables
├── docs/
│   └── analysis_report.Rmd
├── my_project.Rproj   # RStudio project file
└── README.md
```

---

## Common Gotchas & Pitfalls

#r/gotchas #r/common-mistakes

### Indexing (1-based vs 0-based)

r

```r
# R uses 1-based indexing (unlike Python/Java)
my_vector <- c("a", "b", "c", "d")
my_vector[1]    # "a" (first element)
my_vector[0]    # character(0) (empty)

# This trips up programmers from other languages!
```

### Factor Behavior

r

```r
# Factors can be tricky
f <- factor(c("low", "medium", "high"))
f[1] <- "very high"  # Warning! Creates NA

# Convert to character first
f <- as.character(f)
f[1] <- "very high"  # Now it works

# Or specify all levels upfront
f <- factor(c("low", "medium", "high"), 
           levels = c("low", "medium", "high", "very high"))
```

### Logical Subsetting with NA

r

```r
# NA in logical subsetting can cause issues
x <- c(1, 2, NA, 4, 5)
x[x > 3]        # Returns: 4 5 NA (NA comparison returns NA)
x[x > 3 & !is.na(x)]  # Correct: 4 5

# Use which() to avoid NA issues
x[which(x > 3)] # Returns: 4 5
```

### Floating Point Precision

r

```r
# Floating point arithmetic can be imprecise
0.1 + 0.2 == 0.3    # FALSE (surprising!)
0.1 + 0.2           # 0.30000000000000004

# Use all.equal() for floating point comparisons
all.equal(0.1 + 0.2, 0.3)  # TRUE
```

### String vs Factor Confusion

r

```r
# read.csv() used to convert strings to factors by default
df <- read.csv("data.csv")  # Old behavior
df <- read.csv("data.csv", stringsAsFactors = FALSE)  # Better

# Modern solution: use readr
df <- readr::read_csv("data.csv")  # Always keeps strings as strings
```

### Vectorization Misunderstanding

r

```r
# R operations are vectorized
c(1, 2, 3) + c(10, 20, 30)  # Element-wise: 11 22 33
c(1, 2, 3) + 10              # Recycling: 11 12 13

# But recycling can be dangerous with different lengths
c(1, 2, 3, 4) + c(10, 20)   # Warning: 11 22 13 24 (recycled)

# Length mismatch warnings are your friend!
```

---

## Next Steps & Advanced Topics

#r/advanced #r/learning-path

### Immediate Next Steps

1. **Master the [[Tidyverse]]**: More intuitive data manipulation
2. **Learn [[ggplot2]]**: Professional data visualization
3. **Practice with real datasets**: [[Kaggle]], built-in datasets
4. **Set up [[RStudio Projects]]**: Better project management

### Intermediate Topics

- [[R Markdown]]: Reproducible reports and documents
- [[Shiny]]: Interactive web applications
- [[Statistical Modeling]]: lm(), glm(), mixed effects
- [[Time Series Analysis]]: ts objects, forecasting
- [[Text Mining]]: tm package, sentiment analysis

### Advanced Topics

- [[R Package Development]]: Creating your own packages
- [[Advanced Statistics]]: Bayesian methods, machine learning
- [[High Performance R]]: Rcpp, parallel computing
- [[Spatial Analysis]]: sf package, mapping
- [[Big Data in R]]: sparklyr, data.table optimization

### Resources for Learning

#### Documentation

- [[R Documentation]] - [https://www.r-project.org/other-docs.html](https://www.r-project.org/other-docs.html)
- [[R-bloggers]] - [https://www.r-bloggers.com/](https://www.r-bloggers.com/)
- [[Stack Overflow R]] - Tag: [r]

#### Books (Free Online)

- [[R for Data Science]] - [https://r4ds.had.co.nz/](https://r4ds.had.co.nz/)
- [[Advanced R]] - [https://adv-r.hadley.nz/](https://adv-r.hadley.nz/)
- [[R Graphics Cookbook]] - [https://r-graphics.org/](https://r-graphics.org/)
- [[Hands-On Programming with R]] - [https://rstudio-education.github.io/hopr/](https://rstudio-education.github.io/hopr/)

#### Practice Datasets

r

```r
# Built-in datasets
data()                  # List all available datasets
head(mtcars)           # Motor trend car data
head(iris)             # Flower measurements
head(diamonds)         # Diamond characteristics (ggplot2)

# Load specific dataset
data(mtcars)
?mtcars                # Dataset documentation
```

#### Cheat Sheets

- [[RStudio Cheat Sheets]] - [https://rstudio.com/resources/cheatsheets/](https://rstudio.com/resources/cheatsheets/)
- [[Base R Cheat Sheet]]
- [[dplyr Cheat Sheet]]
- [[ggplot2 Cheat Sheet]]

---

## Keyboard Shortcuts (RStudio)

#r/shortcuts #rstudio

### Essential Shortcuts

|Shortcut|Action|
|---|---|
|`Ctrl + Enter`|Run current line/selection|
|`Ctrl + Shift + Enter`|Run entire script|
|`Ctrl + Shift + S`|Source entire script|
|`Tab`|Auto-complete|
|`Ctrl + 1`|Move cursor to Source pane|
|`Ctrl + 2`|Move cursor to Console pane|
|`Ctrl + L`|Clear console|
|`Ctrl + Shift + C`|Comment/uncomment lines|
|`Ctrl + Shift + R`|Insert section header|
|`Ctrl + Shift + M`|Insert pipe operator `%>%`|
|`Alt + -`|Insert assignment operator `<-`|

### Navigation Shortcuts

|Shortcut|Action|
|---|---|
|`Ctrl + .`|Go to file/function|
|`Ctrl + F`|Find in current file|
|`Ctrl + Shift + F`|Find in files|
|`F2`|Go to function definition|
|`Ctrl + Shift + .`|Show document outline|

---

## Quick Reference Cards

### Data Types Quick Check

r

```r
# Check data type
is.numeric(x)
is.character(x)
is.logical(x)
is.factor(x)
is.data.frame(x)
is.list(x)
is.matrix(x)

# Convert data types
as.numeric(x)
as.character(x)
as.logical(x)
as.factor(x)
as.data.frame(x)
```

### Common Statistical Functions

r

```r
# Descriptive statistics
summary(x)       # Five-number summary + mean
describe(x)      # Detailed statistics (psych package)
stat.desc(x)     # Detailed statistics (pastecs package)

# Distribution functions (example with normal)
dnorm(x)         # Density
pnorm(x)         # Cumulative probability
qnorm(p)         # Quantile
rnorm(n)         # Random numbers

# Replace 'norm' with other distributions:
# unif, binom, pois, t, chisq, f, etc.
```

### Data Frame Operations

r

```r
# Quick data frame exploration
head(df, 10)     # First 10 rows
tail(df, 5)      # Last 5 rows
glimpse(df)      # dplyr version of str()
str(df)          # Structure
summary(df)      # Summary of all columns
dim(df)          # Dimensions
nrow(df)         # Number of rows
ncol(df)         # Number of columns
names(df)        # Column names
```

---

## Practical Examples

#r/examples #r/practice

### Example 1: Data Analysis Workflow

r

```r
# 1. Load packages
library(tidyverse)

# 2. Load data
df <- read_csv("sales_data.csv")

# 3. Explore data
glimpse(df)
summary(df)
head(df)

# 4. Clean data
df_clean <- df %>%
    filter(!is.na(sales_amount)) %>%
    mutate(
        date = as.Date(date),
        sales_amount = as.numeric(sales_amount)
    )

# 5. Analyze
monthly_sales <- df_clean %>%
    mutate(month = format(date, "%Y-%m")) %>%
    group_by(month) %>%
    summarise(
        total_sales = sum(sales_amount),
        avg_sales = mean(sales_amount),
        n_transactions = n()
    )

# 6. Visualize
ggplot(monthly_sales, aes(x = month, y = total_sales)) +
    geom_col() +
    theme_minimal() +
    labs(title = "Monthly Sales Trend")

# 7. Export results
write_csv(monthly_sales, "monthly_sales_summary.csv")
```

### Example 2: Statistical Analysis

r

```r
# Load built-in dataset
data(mtcars)

# Research question: Does weight affect fuel efficiency?

# Exploratory analysis
plot(mtcars$wt, mtcars$mpg)
cor(mtcars$wt, mtcars$mpg)

# Linear regression
model <- lm(mpg ~ wt, data = mtcars)
summary(model)

# Model diagnostics
par(mfrow = c(2, 2))
plot(model)

# Predictions
new_cars <- data.frame(wt = c(2.5, 3.5, 4.5))
predictions <- predict(model, new_cars, interval = "confidence")
print(predictions)
```

### Example 3: Text Analysis

r

```r
# Simple text analysis
library(stringr)

text <- c("Hello world", "R is great", "Data science rocks")

# Basic text operations
str_length(text)                    # Character count
str_to_upper(text)                  # Convert to uppercase
str_detect(text, "R")               # Detect pattern
str_extract(text, "\\w+")           # Extract first word
str_replace(text, "R", "Python")    # Replace pattern

# Word frequency
words <- unlist(str_split(text, " "))
word_freq <- table(tolower(words))
sort(word_freq, decreasing = TRUE)
```

---

## Tags & References

#r-programming #data-analysis #statistics #programming-fundamentals #data-science #analytics #visualization #statistical-computing

## Related Notes

- [[Statistics Fundamentals]]
- [[Data Science Workflow]]
- [[Statistical Analysis]]
- [[Data Visualization]]
- [[Programming Best Practices]]
- [[Reproducible Research]]

---

_This guide provides a comprehensive foundation in R programming. Continue learning by exploring the [[Tidyverse]], building real projects, and practicing with diverse datasets. Remember: the best way to learn R is by using it for real analysis tasks!_