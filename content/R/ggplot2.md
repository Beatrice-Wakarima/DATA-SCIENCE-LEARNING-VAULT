# ggplot2: Grammar of Graphics in R

#R #DataVisualization #ggplot2 #DataScience #Statistics

## Overview

**ggplot2** is R's most popular data visualization package, based on the Grammar of Graphics. It allows you to build plots layer by layer, making it both powerful and intuitive for creating complex visualizations.

**Key Concept**: Every ggplot has three essential components:

- **Data**: The dataset you want to visualize
- **Aesthetics (aes)**: How variables map to visual properties
- **Geometries (geom)**: The type of plot/visualization

## Installation and Loading

```r
# Install ggplot2 (if not already installed)
install.packages("ggplot2")

# Load the library
library(ggplot2)

# ggplot2 is also part of the tidyverse
library(tidyverse)
```

## Basic Syntax Structure

```r
ggplot(data = <DATA>) + 
  <GEOM_FUNCTION>(mapping = aes(<MAPPINGS>)) +
  <OTHER_LAYERS>
```

## Essential Components

### 1. Data Layer

The foundation of every ggplot - your dataset.

```r
# Using built-in mtcars dataset
ggplot(data = mtcars)
```

### 2. Aesthetic Mappings [[Data Mapping]]

Map variables to visual properties like position, color, size, shape.

```r
# Common aesthetic mappings
ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point()

# Multiple aesthetics
ggplot(mtcars, aes(x = wt, y = mpg, color = factor(cyl), size = hp)) +
  geom_point()
```

**Common Aesthetics**:

- `x`, `y`: Position on axes
- `color`: Color of points/lines
- `fill`: Fill color for bars, areas
- `size`: Size of points/lines
- `shape`: Shape of points
- `alpha`: Transparency (0-1)

### 3. Geometric Objects (geoms) [[Plot Types]]

The visual representation of your data.

## Common Geoms and Plot Types

### Scatter Plots

```r
# Basic scatter plot
ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point()

# With color grouping
ggplot(mtcars, aes(x = wt, y = mpg, color = factor(cyl))) +
  geom_point(size = 3, alpha = 0.7)
```

### Line Plots [[Time Series]]

```r
# Line plot
ggplot(economics, aes(x = date, y = unemploy)) +
  geom_line()

# Multiple lines
ggplot(economics_long, aes(x = date, y = value01, color = variable)) +
  geom_line()
```

### Bar Charts [[Categorical Data]]

```r
# Bar chart (counts)
ggplot(diamonds, aes(x = cut)) +
  geom_bar()

# Bar chart with specified values
df <- data.frame(
  category = c("A", "B", "C"),
  values = c(23, 45, 56)
)
ggplot(df, aes(x = category, y = values)) +
  geom_col()
```

### Histograms [[Distributions]]

```r
# Histogram
ggplot(mtcars, aes(x = mpg)) +
  geom_histogram(bins = 15, fill = "skyblue", alpha = 0.7)

# With density curve overlay
ggplot(mtcars, aes(x = mpg)) +
  geom_histogram(aes(y = after_stat(density)), alpha = 0.7) +
  geom_density(color = "red", size = 1)
```

### Box Plots [[Statistical Summaries]]

```r
# Box plot
ggplot(mtcars, aes(x = factor(cyl), y = mpg)) +
  geom_boxplot()

# Box plot with points
ggplot(mtcars, aes(x = factor(cyl), y = mpg)) +
  geom_boxplot() +
  geom_jitter(width = 0.2, alpha = 0.6)
```

## Customization Layers

### Labels and Titles

```r
ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point() +
  labs(
    title = "Fuel Efficiency vs Weight",
    subtitle = "Motor Trend Car Road Tests",
    x = "Weight (1000 lbs)",
    y = "Miles per Gallon",
    caption = "Data: mtcars dataset"
  )
```

### Themes [[Plot Styling]]

```r
# Built-in themes
ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point() +
  theme_minimal()

# Other themes: theme_bw(), theme_classic(), theme_dark()

# Custom theme modifications
ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point() +
  theme_minimal() +
  theme(
    plot.title = element_text(size = 16, face = "bold"),
    axis.text = element_text(size = 12),
    panel.grid.minor = element_blank()
  )
```

### Colors and Scales [[Color Theory]]

```r
# Manual color specification
ggplot(mtcars, aes(x = wt, y = mpg, color = factor(cyl))) +
  geom_point() +
  scale_color_manual(values = c("red", "blue", "green"))

# Color brewer palettes
ggplot(mtcars, aes(x = wt, y = mpg, color = factor(cyl))) +
  geom_point() +
  scale_color_brewer(type = "qual", palette = "Set1")

# Viridis color scale (colorblind friendly)
ggplot(mtcars, aes(x = wt, y = mpg, color = hp)) +
  geom_point() +
  scale_color_viridis_c()
```

## Advanced Features

### Faceting [[Small Multiples]]

Create multiple plots based on categorical variables.

```r
# Facet wrap
ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point() +
  facet_wrap(~cyl, ncol = 2)

# Facet grid
ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point() +
  facet_grid(vs ~ am, labeller = label_both)
```

### Statistical Transformations

```r
# Adding trend line
ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point() +
  geom_smooth(method = "lm", se = TRUE)

# Multiple smoothers
ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point() +
  geom_smooth(method = "lm", color = "red") +
  geom_smooth(method = "loess", color = "blue")
```

### Coordinate Systems

```r
# Flip coordinates
ggplot(mtcars, aes(x = factor(cyl), y = mpg)) +
  geom_boxplot() +
  coord_flip()

# Polar coordinates (for pie charts)
df <- data.frame(category = c("A", "B", "C"), values = c(30, 40, 30))
ggplot(df, aes(x = "", y = values, fill = category)) +
  geom_bar(stat = "identity", width = 1) +
  coord_polar("y", start = 0) +
  theme_void()
```

## Useful Functions and Tips

### Saving Plots

```r
# Save the last plot
ggsave("my_plot.png", width = 8, height = 6, dpi = 300)

# Save specific plot
p <- ggplot(mtcars, aes(x = wt, y = mpg)) + geom_point()
ggsave("scatter.pdf", plot = p, width = 10, height = 8)
```

### Combining Plots [[patchwork]]

```r
library(patchwork)

p1 <- ggplot(mtcars, aes(x = wt, y = mpg)) + geom_point()
p2 <- ggplot(mtcars, aes(x = hp, y = mpg)) + geom_point()

# Side by side
p1 + p2

# Stacked
p1 / p2
```

## Common Patterns and Workflows

### Exploratory Data Analysis Pipeline

```r
# Load data
data("diamonds")

# Quick overview plot
diamonds %>%
  ggplot(aes(x = carat, y = price, color = cut)) +
  geom_point(alpha = 0.3) +
  scale_y_log10() +
  facet_wrap(~cut) +
  theme_minimal() +
  labs(title = "Diamond Prices by Carat and Cut Quality")
```

### Customizing for Publication

```r
# Professional looking plot
ggplot(mtcars, aes(x = wt, y = mpg, color = factor(cyl))) +
  geom_point(size = 3, alpha = 0.8) +
  geom_smooth(method = "lm", se = FALSE, linetype = "dashed") +
  scale_color_viridis_d(name = "Cylinders") +
  labs(
    title = "Fuel Efficiency Decreases with Vehicle Weight",
    x = "Weight (1000 lbs)",
    y = "Miles per Gallon"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
    legend.position = "bottom",
    panel.grid.minor = element_blank()
  )
```

## Related Topics

- [[Data Visualization Principles]]
- [[R Data Manipulation]] with dplyr
- [[Color Theory in Data Visualization]]
- [[Statistical Graphics]]
- [[Reproducible Research]] with R Markdown

## References

- [Official ggplot2 documentation](https://ggplot2.tidyverse.org/)
- [R for Data Science - Data Visualization](https://r4ds.had.co.nz/data-visualisation.html)
- [ggplot2 Cheat Sheet](https://rstudio.com/wp-content/uploads/2015/03/ggplot2-cheatsheet.pdf)
- Wickham, H. (2016). _ggplot2: Elegant Graphics for Data Analysis_. Springer.

---

_Created: [[Today's Date]]_  
_Tags: #R #ggplot2 #DataVisualization #Grammar-of-Graphics_