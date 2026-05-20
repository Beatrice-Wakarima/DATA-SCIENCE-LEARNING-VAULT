---
title: Matplotlib and Seaborn
tags: [python, visualization, data-science]
created: 2026-05-20
up:: [[Python MOC]]
---

# 📊 Matplotlib & Seaborn

> Visualizing data is as important as analyzing it. Matplotlib is the foundation; Seaborn makes beautiful statistical charts with less code.

---

## Installation & Import

```python
pip install matplotlib seaborn

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
```

---

## Matplotlib Basics

### Line Chart
```python
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
sales = [420, 385, 510, 490, 620, 580, 450, 730, 695, 810, 750, 920]

plt.figure(figsize=(12, 5))
plt.plot(months, sales, color="#c9a84c", linewidth=2.5, marker="o", markersize=6)
plt.title("Monthly Sales 2026", fontsize=16, fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Sales (KES Thousands)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("sales_trend.png", dpi=150)
plt.show()
```

---

### Bar Chart
```python
departments = ["Engineering", "Analytics", "Management", "Sales"]
headcount = [25, 18, 8, 30]
colors = ["#1a1a2e", "#c9a84c", "#e8c97a", "#8a8a8a"]

plt.figure(figsize=(10, 6))
bars = plt.bar(departments, headcount, color=colors, edgecolor="white", linewidth=0.5)

# Add value labels on bars
for bar, val in zip(bars, headcount):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             str(val), ha="center", fontweight="bold")

plt.title("Headcount by Department", fontsize=16, fontweight="bold")
plt.ylabel("Number of Employees")
plt.tight_layout()
plt.show()
```

---

### Pie Chart
```python
labels = ["Engineering", "Analytics", "Management", "Sales"]
sizes = [25, 18, 8, 30]
colors = ["#1a1a2e", "#c9a84c", "#e8c97a", "#8a8a8a"]
explode = (0, 0.05, 0, 0)  # Highlight Analytics

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, colors=colors, explode=explode,
        autopct="%1.1f%%", startangle=90,
        textprops={"fontsize": 12})
plt.title("Headcount Distribution", fontsize=16, fontweight="bold")
plt.show()
```

---

### Scatter Plot
```python
np.random.seed(42)
experience = np.random.randint(1, 15, 50)
salary = experience * 8000 + np.random.randint(-10000, 20000, 50)

plt.figure(figsize=(10, 6))
plt.scatter(experience, salary, color="#c9a84c", alpha=0.7, s=80, edgecolors="#1a1a2e")
plt.title("Experience vs Salary", fontsize=16, fontweight="bold")
plt.xlabel("Years of Experience")
plt.ylabel("Annual Salary (KES)")
plt.grid(True, alpha=0.3)

# Add trend line
z = np.polyfit(experience, salary, 1)
p = np.poly1d(z)
plt.plot(sorted(experience), p(sorted(experience)), "r--", alpha=0.8, label="Trend")
plt.legend()
plt.tight_layout()
plt.show()
```

---

### Histogram
```python
np.random.seed(42)
salaries = np.random.normal(95000, 25000, 500)

plt.figure(figsize=(10, 6))
plt.hist(salaries, bins=30, color="#c9a84c", edgecolor="#1a1a2e", alpha=0.8)
plt.axvline(np.mean(salaries), color="red", linestyle="--", linewidth=2, label=f"Mean: KES {np.mean(salaries):,.0f}")
plt.axvline(np.median(salaries), color="blue", linestyle="--", linewidth=2, label=f"Median: KES {np.median(salaries):,.0f}")
plt.title("Salary Distribution", fontsize=16, fontweight="bold")
plt.xlabel("Salary (KES)")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.show()
```

---

## Subplots — Multiple Charts

```python
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Sales Dashboard 2026", fontsize=18, fontweight="bold")

# Chart 1 — Line
axes[0, 0].plot(months, sales, color="#c9a84c", marker="o")
axes[0, 0].set_title("Monthly Sales Trend")
axes[0, 0].set_ylabel("KES Thousands")

# Chart 2 — Bar
axes[0, 1].bar(departments, headcount, color="#1a1a2e")
axes[0, 1].set_title("Headcount by Dept")

# Chart 3 — Scatter
axes[1, 0].scatter(experience, salary, alpha=0.6, color="#c9a84c")
axes[1, 0].set_title("Experience vs Salary")

# Chart 4 — Histogram
axes[1, 1].hist(salaries, bins=20, color="#e8c97a", edgecolor="white")
axes[1, 1].set_title("Salary Distribution")

plt.tight_layout()
plt.savefig("dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
```

---

## Seaborn — Statistical Charts Made Easy

```python
import seaborn as sns

# Set style
sns.set_theme(style="darkgrid", palette="muted")

# Sample data
df = pd.DataFrame({
    "department": ["Engineering"]*25 + ["Analytics"]*18 + ["Sales"]*30,
    "salary": np.concatenate([
        np.random.normal(115000, 15000, 25),
        np.random.normal(95000, 12000, 18),
        np.random.normal(85000, 10000, 30)
    ]),
    "performance": np.random.choice(["Excellent","Good","Average"], 73)
})
```

### Box Plot — Distribution by Group
```python
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="department", y="salary", palette=["#1a1a2e","#c9a84c","#e8c97a"])
plt.title("Salary Distribution by Department", fontsize=15, fontweight="bold")
plt.ylabel("Annual Salary (KES)")
plt.tight_layout()
plt.show()
```

### Heatmap — Correlation Matrix
```python
# Correlation heatmap
numeric_df = df[["salary"]].copy()
numeric_df["experience"] = np.random.randint(1, 15, len(df))
numeric_df["performance_score"] = np.random.randint(60, 100, len(df))
numeric_df["tenure"] = np.random.randint(1, 10, len(df))

plt.figure(figsize=(8, 6))
sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f",
            cmap="YlOrBr", linewidths=0.5,
            annot_kws={"size": 12})
plt.title("Correlation Matrix", fontsize=15, fontweight="bold")
plt.tight_layout()
plt.show()
```

### Count Plot
```python
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x="department", hue="performance",
              palette=["#1a1a2e", "#c9a84c", "#e8c97a"])
plt.title("Performance by Department", fontsize=15, fontweight="bold")
plt.tight_layout()
plt.show()
```

### Pair Plot — All vs All
```python
sns.pairplot(numeric_df, diag_kind="kde",
             plot_kws={"alpha": 0.6, "color": "#c9a84c"})
plt.suptitle("Pairwise Relationships", y=1.02)
plt.show()
```

---

## Chart Styling Cheatsheet

```python
# Figure size
plt.figure(figsize=(width, height))

# Colors
color="#c9a84c"                 # Hex code
color="navy"                    # Named color

# Title & Labels
plt.title("Title", fontsize=16, fontweight="bold")
plt.xlabel("X Label", fontsize=12)
plt.ylabel("Y Label", fontsize=12)

# Grid
plt.grid(True, alpha=0.3)

# Legend
plt.legend(loc="upper left", fontsize=10)

# Annotations
plt.annotate("Peak", xy=(x, y), xytext=(x+1, y+1000),
             arrowprops=dict(arrowstyle="->"))

# Save
plt.savefig("chart.png", dpi=150, bbox_inches="tight")

# Show
plt.tight_layout()
plt.show()
```

---

## Real World Example — Executive Dashboard

```python
import matplotlib.pyplot as plt
import numpy as np

months = ["Jan","Feb","Mar","Apr","May","Jun"]
revenue = [420, 385, 510, 490, 620, 580]
costs = [280, 260, 340, 320, 410, 380]
profit = [r - c for r, c in zip(revenue, costs)]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.patch.set_facecolor("#0d0d1a")

# Revenue vs Cost
ax1.set_facecolor("#1a1a2e")
ax1.plot(months, revenue, color="#c9a84c", marker="o", linewidth=2.5, label="Revenue")
ax1.plot(months, costs, color="#e8c97a", marker="s", linewidth=2.5, linestyle="--", label="Costs")
ax1.fill_between(months, revenue, costs, alpha=0.1, color="#c9a84c")
ax1.set_title("Revenue vs Costs (KES K)", color="white", fontsize=13, fontweight="bold")
ax1.legend()
ax1.tick_params(colors="white")

# Profit bars
colors = ["#c9a84c" if p > 0 else "red" for p in profit]
ax2.set_facecolor("#1a1a2e")
ax2.bar(months, profit, color=colors)
ax2.set_title("Monthly Profit (KES K)", color="white", fontsize=13, fontweight="bold")
ax2.axhline(0, color="white", linewidth=0.8)
ax2.tick_params(colors="white")

plt.tight_layout()
plt.savefig("executive_dashboard.png", dpi=150, facecolor="#0d0d1a")
plt.show()
```

---

## Previous | Next
← [[12 - NumPy]] | → [[14 - Working with APIs]]
