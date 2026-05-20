---
title: PySpark Basics
tags: [python, pyspark, big-data, data-engineering]
created: 2026-05-20
up:: [[Python MOC]]
---

# ⚡ PySpark Basics

> PySpark is Python's interface to Apache Spark — the engine for processing massive datasets that don't fit in memory. When Pandas hits its limits, PySpark takes over.

---

## When to Use PySpark vs Pandas

| Scenario | Use |
|---|---|
| Dataset < 1GB | Pandas |
| Dataset 1GB - 10GB | Pandas (with chunking) or PySpark |
| Dataset > 10GB | PySpark |
| Distributed cluster | PySpark |
| Real-time streaming | PySpark Streaming |
| Databricks / EMR | PySpark |

---

## Installation

```bash
pip install pyspark

# Or use Databricks / Google Colab (pre-installed)
```

---

## SparkSession — The Entry Point

```python
from pyspark.sql import SparkSession

# Create (or get existing) Spark session
spark = SparkSession.builder \
    .appName("Beatrice Builds Pipeline") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()

print(spark.version)    # 3.x.x
spark.sparkContext.setLogLevel("ERROR")     # Reduce noisy logs
```

---

## Creating DataFrames

```python
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

spark = SparkSession.builder.appName("demo").getOrCreate()

# From Python list
data = [
    ("Beatrice", "Engineering", 120000, 5),
    ("John", "Analytics", 95000, 3),
    ("Alice", "Engineering", 110000, 4),
    ("Bob", "Analytics", 85000, 2)
]

columns = ["name", "department", "salary", "years_exp"]
df = spark.createDataFrame(data, columns)
df.show()
# +--------+-----------+------+---------+
# |    name| department|salary|years_exp|
# +--------+-----------+------+---------+
# |Beatrice|Engineering|120000|        5|
# ...

# From CSV
df = spark.read.csv("data/bank_marketing.csv", header=True, inferSchema=True)

# With explicit schema (recommended for large files)
schema = StructType([
    StructField("age", IntegerType(), True),
    StructField("job", StringType(), True),
    StructField("balance", FloatType(), True),
    StructField("y", StringType(), True)
])
df = spark.read.csv("data/bank_marketing.csv", header=True, schema=schema)

# From Parquet (best format for big data)
df = spark.read.parquet("data/transactions.parquet")

# From JSON
df = spark.read.json("data/customers.json")
```

---

## Exploring Data

```python
df.show(5)                  # Print first 5 rows
df.show(5, truncate=False)  # Don't truncate columns
df.printSchema()            # Column names and types
df.columns                  # List of column names
df.count()                  # Number of rows
df.dtypes                   # Column data types
df.describe().show()        # Statistics
df.summary().show()         # Detailed summary
```

---

## Selecting & Filtering

```python
from pyspark.sql import functions as F

# Select columns
df.select("name", "salary").show()
df.select(df.name, df.salary).show()

# Filter rows
df.filter(df.salary > 100000).show()
df.filter("salary > 100000").show()         # SQL-style string

# Multiple conditions
df.filter(
    (df.department == "Engineering") &
    (df.years_exp >= 4)
).show()

# Where (alias for filter)
df.where(df.salary.between(80000, 120000)).show()

# isin
df.filter(df.department.isin(["Engineering", "Analytics"])).show()

# isNull / isNotNull
df.filter(df.email.isNull()).show()
df.filter(df.email.isNotNull()).show()
```

---

## Adding & Transforming Columns

```python
from pyspark.sql import functions as F

# Add new column
df = df.withColumn("annual_bonus", df.salary * 0.10)
df = df.withColumn("total_comp", df.salary + df.annual_bonus)

# Conditional column (like Excel IF)
df = df.withColumn("seniority",
    F.when(df.years_exp >= 7, "Senior")
     .when(df.years_exp >= 4, "Mid")
     .otherwise("Junior")
)

# String operations
df = df.withColumn("name_upper", F.upper(df.name))
df = df.withColumn("name_length", F.length(df.name))

# Date operations
df = df.withColumn("hire_date", F.to_date(df.hire_date_str, "yyyy-MM-dd"))
df = df.withColumn("hire_year", F.year(df.hire_date))
df = df.withColumn("months_employed", F.months_between(F.current_date(), df.hire_date))

# Rename column
df = df.withColumnRenamed("years_exp", "experience")

# Drop column
df = df.drop("temp_column")
df = df.drop("col1", "col2")
```

---

## Aggregations

```python
from pyspark.sql import functions as F

# Basic aggregation
df.agg(
    F.count("*").alias("total_rows"),
    F.sum("salary").alias("total_payroll"),
    F.avg("salary").alias("avg_salary"),
    F.max("salary").alias("max_salary"),
    F.min("salary").alias("min_salary")
).show()

# GroupBy
dept_stats = df.groupBy("department").agg(
    F.count("*").alias("headcount"),
    F.round(F.avg("salary"), 0).alias("avg_salary"),
    F.sum("salary").alias("total_payroll"),
    F.max("years_exp").alias("max_experience")
)
dept_stats.show()

# Multiple groupBy columns
df.groupBy("department", "seniority").agg(
    F.count("*").alias("count"),
    F.avg("salary").alias("avg_salary")
).orderBy("department", "avg_salary").show()
```

---

## Joins

```python
# Sample DataFrames
customers = spark.createDataFrame([
    (1, "Beatrice", "Gold"),
    (2, "John", "Silver"),
    (3, "Alice", "Platinum")
], ["customer_id", "name", "tier"])

transactions = spark.createDataFrame([
    (1, 1, 45000, "deposit"),
    (2, 1, 10000, "withdrawal"),
    (3, 2, 25000, "deposit"),
    (4, 3, 100000, "deposit")
], ["txn_id", "customer_id", "amount", "type"])

# Inner join
result = customers.join(transactions, on="customer_id", how="inner")
result.show()

# Left join
result = customers.join(transactions, on="customer_id", how="left")

# Join on multiple columns
result = df1.join(df2, on=["customer_id", "date"], how="inner")

# Join with different column names
result = df1.join(df2, df1.cust_id == df2.customer_id, how="inner")
```

---

## SQL on Spark DataFrames

```python
# Register as temporary SQL view
df.createOrReplaceTempView("employees")
transactions.createOrReplaceTempView("transactions")

# Run SQL queries!
result = spark.sql("""
    SELECT 
        e.department,
        COUNT(*) AS headcount,
        ROUND(AVG(e.salary), 0) AS avg_salary,
        SUM(t.amount) AS total_transactions
    FROM employees e
    LEFT JOIN transactions t ON e.id = t.customer_id
    GROUP BY e.department
    ORDER BY avg_salary DESC
""")
result.show()
```

---

## Handling Missing Values

```python
# Check nulls
from pyspark.sql import functions as F
df.select([F.count(F.when(F.col(c).isNull(), c)).alias(c) for c in df.columns]).show()

# Drop nulls
df.dropna()                             # Drop rows with any null
df.dropna(subset=["name", "salary"])    # Only if these cols are null
df.dropna(thresh=3)                     # Keep rows with at least 3 non-null

# Fill nulls
df.fillna(0)                                    # Fill all with 0
df.fillna({"salary": 0, "tier": "Unknown"})     # Fill specific columns
df.fillna(df.approxQuantile("salary", [0.5], 0)[0])  # Fill with median
```

---

## Writing Data

```python
# CSV
df.write.csv("outputs/employees", header=True, mode="overwrite")

# Parquet (recommended — compressed, fast)
df.write.parquet("outputs/employees.parquet", mode="overwrite")

# Partitioned by column (great for large datasets)
df.write.partitionBy("department").parquet("outputs/employees_partitioned")

# Single file (careful with large data!)
df.coalesce(1).write.csv("outputs/single_file.csv", header=True)

# To database via JDBC
df.write.jdbc(
    url="jdbc:postgresql://localhost:5432/sales_db",
    table="employees_clean",
    mode="overwrite",
    properties={"user": "beatrice", "password": "secret", "driver": "org.postgresql.Driver"}
)
```

---

## PySpark vs Pandas Cheatsheet

| Operation | Pandas | PySpark |
|---|---|---|
| Read CSV | `pd.read_csv()` | `spark.read.csv()` |
| Show data | `df.head()` | `df.show()` |
| Filter | `df[df.col > 5]` | `df.filter(df.col > 5)` |
| New column | `df["new"] = x` | `df.withColumn("new", x)` |
| GroupBy | `df.groupby().agg()` | `df.groupBy().agg()` |
| Sort | `df.sort_values()` | `df.orderBy()` |
| Count | `len(df)` | `df.count()` |
| Nulls | `df.fillna()` | `df.fillna()` |
| Write CSV | `df.to_csv()` | `df.write.csv()` |
| SQL | Not native | `spark.sql()` |

---

## Real World Example — Bank Marketing at Scale

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("BankMarketing").getOrCreate()

# Load large dataset
df = spark.read.csv("data/bank_marketing_large.csv",
                    header=True, inferSchema=True)
print(f"Total records: {df.count():,}")

# Clean
df = df.dropna(subset=["age", "job", "balance"])
df = df.filter(df.age.between(18, 70))
df = df.filter(df.balance >= 0)

# Feature engineering
df = df.withColumn("balance_segment",
    F.when(df.balance > 10000, "High")
     .when(df.balance > 1000, "Medium")
     .otherwise("Low")
)

# Campaign analysis
campaign_stats = df.groupBy("job", "balance_segment").agg(
    F.count("*").alias("contacts"),
    F.sum(F.when(F.col("y") == "yes", 1).otherwise(0)).alias("subscriptions"),
    F.round(
        F.sum(F.when(F.col("y") == "yes", 1).otherwise(0)) * 100.0 / F.count("*"), 2
    ).alias("conversion_rate_pct")
).orderBy("conversion_rate_pct", ascending=False)

campaign_stats.show(20)

# Save results
campaign_stats.write.parquet("outputs/campaign_stats.parquet", mode="overwrite")
print("✅ Analysis complete!")

spark.stop()
```

---

## Previous | Next
← [[22 - FastAPI — Building Data APIs]] | → [[24 - Python + Docker]]
