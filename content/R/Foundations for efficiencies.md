# R Programming: Foundation for Efficiencies

#R #Performance #Optimization #BestPractices #Programming #DataScience

## Overview

Building efficient R code requires understanding fundamental concepts that impact performance, memory usage, and code maintainability. This foundation focuses on core principles and practices that make R programming more efficient from the ground up.

## Core Efficiency Principles

### 1. Vectorization [[Vector Operations]]

R is designed for vectorized operations - operations that work on entire vectors at once rather than individual elements.

```r
# Inefficient: Using loops
n <- 1000000
x <- numeric(n)
system.time({
  for(i in 1:n) {
    x[i] <- i^2
  }
})

# Efficient: Vectorized operation
system.time({
  x <- (1:n)^2
})

# Vectorized functions are much faster
system.time(sqrt(1:1000000))  # Fast
system.time(sapply(1:1000000, sqrt))  # Much slower
```

**Key Vectorized Functions:**

- Mathematical: `+`, `-`, `*`, `/`, `^`, `sqrt()`, `log()`, `exp()`
- Logical: `&`, `|`, `!`, `==`, `!=`, `<`, `>`
- String: `paste()`, `substr()`, `nchar()`, `grepl()`

### 2. Memory Management [[Memory Optimization]]

Efficient memory usage prevents crashes and improves performance.

```r
# Pre-allocate vectors instead of growing them
# Inefficient: Growing vectors
result <- numeric(0)
for(i in 1:10000) {
  result <- c(result, i^2)  # Bad: copies entire vector each time
}

# Efficient: Pre-allocation
result <- numeric(10000)  # Pre-allocate
for(i in 1:10000) {
  result[i] <- i^2  # Good: direct assignment
}

# Even better: Vectorized
result <- (1:10000)^2
```

**Memory Management Functions:**

```r
# Check memory usage
object.size(my_data)
memory.size()  # Windows only
gc()  # Garbage collection

# Monitor memory during operations
library(pryr)
mem_used()
mem_change(x <- 1:1000000)
```

### 3. Data Structure Selection [[Data Structures]]

Choose the right data structure for your use case.

```r
# Vectors: Fastest for single data type
x <- 1:1000000

# Lists: Flexible but slower
lst <- as.list(1:1000)

# Data frames: Good balance for mixed data types
df <- data.frame(
  id = 1:1000,
  value = rnorm(1000),
  category = sample(letters[1:5], 1000, replace = TRUE)
)

# Matrices: Fast for numeric data
mat <- matrix(rnorm(1000000), nrow = 1000)

# Performance comparison
library(microbenchmark)
microbenchmark(
  vector = sum(x),
  list = sum(unlist(lst)),
  dataframe = sum(df$value),
  matrix = sum(mat),
  times = 100
)
```

## Efficient Data Manipulation

### Using data.table for Large Data [[data.table]]

```r
library(data.table)

# Convert to data.table for speed
dt <- as.data.table(df)

# Fast aggregation
system.time(
  dt[, .(mean_value = mean(value)), by = category]
)

# Compare with base R
system.time(
  aggregate(value ~ category, data = df, FUN = mean)
)

# Fast filtering and selection
dt[category %in% c("a", "b") & value > 0, .(id, value)]
```

### dplyr with Efficiency Mindset [[dplyr]]

```r
library(dplyr)

# Chain operations efficiently
result <- df %>%
  filter(value > 0) %>%           # Filter early
  select(id, value, category) %>% # Select only needed columns
  group_by(category) %>%
  summarise(
    mean_val = mean(value),
    count = n(),
    .groups = 'drop'
  )

# Use .data pronoun for programming
filter_column <- function(data, col, threshold) {
  data %>%
    filter(.data[[col]] > threshold)
}
```

## Function Writing Efficiency [[Function Design]]

### Efficient Function Design

```r
# Good function design principles
calculate_stats <- function(x, na.rm = TRUE) {
  # Input validation
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  
  # Early return for empty input
  if (length(x) == 0) {
    return(list(mean = NA, sd = NA, n = 0))
  }
  
  # Efficient computation
  list(
    mean = mean(x, na.rm = na.rm),
    sd = sd(x, na.rm = na.rm),
    n = length(x)
  )
}

# Use environment-specific optimizations
fast_variance <- function(x) {
  n <- length(x)
  if (n < 2) return(NA)
  
  # Use built-in C functions when possible
  .Call(C_var, x, na.rm = FALSE)  # Example of calling C code
}
```

### Avoiding Common Pitfalls

```r
# DON'T: Use apply() on data frames (converts to matrix)
# DO: Use lapply() or specialized functions

# DON'T: 
df %>% apply(2, mean)  # Slow, type conversion

# DO:
df %>% summarise(across(where(is.numeric), mean))  # Fast, type-safe

# DON'T: Unnecessary function calls in loops
for(i in 1:nrow(df)) {
  # length(df) calculated every iteration
  if(i <= length(df)) { ... }
}

# DO: Calculate once
n <- nrow(df)
for(i in 1:n) {
  # Use pre-calculated value
}
```

## Profiling and Benchmarking [[Performance Analysis]]

### Finding Bottlenecks

```r
# Profile your code
library(profvis)

profvis({
  # Your code here
  result <- df %>%
    group_by(category) %>%
    summarise(mean_val = mean(value))
})

# Benchmark alternatives
library(microbenchmark)

microbenchmark(
  base_r = aggregate(value ~ category, df, mean),
  dplyr = df %>% group_by(category) %>% summarise(mean_val = mean(value)),
  data_table = dt[, .(mean_val = mean(value)), by = category],
  times = 100
)
```

### System Monitoring

```r
# Track execution time
system.time({
  # Your code
})

# Memory usage tracking
library(pryr)
mem_change({
  large_object <- matrix(rnorm(1e6), nrow = 1000)
})

# Line-by-line profiling
library(lineprof)
l <- lineprof(your_function())
shine(l)  # Interactive profiler
```

## I/O Efficiency [[File Operations]]

### Fast Data Reading

```r
# For large CSV files
library(data.table)
dt <- fread("large_file.csv")  # Fastest

library(readr)
df <- read_csv("large_file.csv")  # Fast with good defaults

# For specific columns only
dt <- fread("large_file.csv", select = c("col1", "col2", "col5"))

# For compressed files
library(vroom)
df <- vroom("large_file.csv.gz")  # Handles compression automatically
```

### Efficient Writing

```r
# Fast writing
fwrite(dt, "output.csv")  # data.table - fastest
write_csv(df, "output.csv")  # readr - good speed with features

# For multiple files
library(purrr)
split_data <- split(df, df$category)
iwalk(split_data, ~ write_csv(.x, paste0("data_", .y, ".csv")))
```

## Parallel Processing Foundation [[Parallel Computing]]

### Basic Parallelization

```r
library(parallel)

# Detect available cores
cores <- detectCores() - 1  # Leave one core free

# Parallel lapply
cl <- makeCluster(cores)
result <- parLapply(cl, data_list, function(x) {
  # Your function here
  mean(x)
})
stopCluster(cl)

# Using foreach
library(foreach)
library(doParallel)

registerDoParallel(cores)
result <- foreach(i = 1:1000, .combine = 'c') %dopar% {
  expensive_calculation(i)
}
```

### When to Parallelize

```r
# Rule of thumb: Parallelize if task takes > 1 second
# and can be broken into independent chunks

# Good candidates:
# - Independent iterations
# - Bootstrap sampling
# - Cross-validation folds
# - Monte Carlo simulations

# Bad candidates:
# - Sequential dependencies
# - Small, fast operations
# - I/O heavy tasks
```

## Code Organization for Efficiency [[Code Structure]]

### Project Structure

```r
# Efficient project organization
project/
├── R/
│   ├── utils.R        # Helper functions
│   ├── data_prep.R    # Data preprocessing
│   └── analysis.R     # Main analysis
├── data/
│   ├── raw/          # Original data
│   └── processed/    # Cleaned data
├── output/
└── config.R          # Configuration parameters
```

### Environment Management

```r
# Load packages efficiently
required_packages <- c("dplyr", "ggplot2", "data.table")
lapply(required_packages, require, character.only = TRUE)

# Or use pacman for automatic installation
if (!require(pacman)) install.packages("pacman")
pacman::p_load(dplyr, ggplot2, data.table)

# Set global options for efficiency
options(
  stringsAsFactors = FALSE,  # Avoid automatic factor conversion
  scipen = 999,              # Avoid scientific notation
  digits = 4                 # Control decimal places
)
```

## Performance Best Practices Checklist

### Pre-Development

- [ ] Choose appropriate data structures
- [ ] Plan for expected data sizes
- [ ] Identify potential bottlenecks
- [ ] Consider memory constraints

### During Development

- [ ] Use vectorized operations
- [ ] Pre-allocate objects
- [ ] Avoid growing objects in loops
- [ ] Filter/select early in pipelines
- [ ] Use appropriate packages (data.table, dplyr)

### Post-Development

- [ ] Profile code to find bottlenecks
- [ ] Benchmark different approaches
- [ ] Test with realistic data sizes
- [ ] Document performance considerations

## Common Performance Patterns

### Fast Groupwise Operations

```r
# Pattern: Group-wise statistics
library(data.table)

# Fast aggregation
dt[, .(
  mean_val = mean(value),
  median_val = median(value),
  count = .N
), by = .(group1, group2)]

# Rolling operations
dt[, rolling_mean := frollmean(value, n = 5), by = group]
```

### Efficient Joins

```r
# Use data.table for large joins
setkey(dt1, key_col)
setkey(dt2, key_col)
result <- dt1[dt2]  # Fast join

# Index-based operations
dt[value > threshold, .SD, .SDcols = c("col1", "col2")]
```

## Related Topics

- [[Advanced R Programming]]
- [[Memory Management in R]]
- [[Parallel Computing with R]]
- [[Data.table Advanced Usage]]
- [[Code Profiling and Optimization]]
- [[R Package Development]]

## References

- [Advanced R by Hadley Wickham](http://adv-r.had.co.nz/)
- [Efficient R Programming](https://csgillespie.github.io/efficientR/)
- [data.table documentation](https://rdatatable.gitlab.io/data.table/)
- [R Performance Tips](https://www.r-bloggers.com/r-performance-tips/)

---

_Created: [[Today's Date]]_  
_Tags: #R #Performance #Efficiency #BestPractices #Optimization_