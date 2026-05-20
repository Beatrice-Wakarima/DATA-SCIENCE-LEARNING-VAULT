---
title: Decorators and Context Managers
tags: [python, advanced]
created: 2026-05-20
up:: [[Python MOC]]
---

# 🎁 Decorators & Context Managers

> Decorators add behaviour to functions without changing them. Context managers handle setup and teardown automatically. Both are hallmarks of clean, professional Python.

---

## Decorators — The Concept

```python
# A decorator is a function that wraps another function

def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before the function")
        result = func(*args, **kwargs)
        print("After the function")
        return result
    return wrapper

# Apply with @ syntax
@my_decorator
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("Beatrice")
# Before the function
# Hello, Beatrice!
# After the function
```

---

## Timer Decorator — Measure Performance

```python
import time
import functools

def timer(func):
    """Measure how long a function takes"""
    @functools.wraps(func)      # Preserves function name/docstring
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"⏱️  {func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def process_large_dataset(n):
    """Simulate heavy data processing"""
    total = sum(i ** 2 for i in range(n))
    return total

result = process_large_dataset(1_000_000)
# ⏱️  process_large_dataset took 0.1823s
```

---

## Logger Decorator

```python
import logging
import functools

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")

def log_call(func):
    """Log every function call with arguments and result"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__} | args={args} kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"{func.__name__} succeeded | result={result}")
            return result
        except Exception as e:
            logging.error(f"{func.__name__} failed | error={e}")
            raise
    return wrapper

@log_call
def calculate_roi(revenue, cost):
    return ((revenue - cost) / cost) * 100

calculate_roi(150000, 100000)
# 2026-05-20 | INFO | Calling calculate_roi | args=(150000, 100000)
# 2026-05-20 | INFO | calculate_roi succeeded | result=50.0
```

---

## Retry Decorator — Auto-retry on Failure

```python
import time
import functools

def retry(max_attempts=3, delay=1):
    """Retry a function on failure"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        print(f"❌ Failed after {max_attempts} attempts: {e}")
                        raise
                    print(f"⚠️  Attempt {attempt} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def fetch_from_api(url):
    """Fetch data — will retry if connection fails"""
    import requests
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()

# Will try 3 times before giving up
data = fetch_from_api("https://api.example.com/data")
```

---

## Validate Input Decorator

```python
def validate_positive(*arg_names):
    """Ensure specified arguments are positive numbers"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import inspect
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())
            
            for name in arg_names:
                if name in params:
                    idx = params.index(name)
                    if idx < len(args):
                        value = args[idx]
                        if value <= 0:
                            raise ValueError(f"'{name}' must be positive, got {value}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_positive("revenue", "cost")
def profit_margin(revenue, cost):
    return ((revenue - cost) / revenue) * 100

print(profit_margin(500000, 300000))    # 40.0

try:
    profit_margin(-500000, 300000)      # Raises ValueError
except ValueError as e:
    print(f"Error: {e}")
```

---

## Stacking Decorators

```python
@timer
@log_call
@retry(max_attempts=3)
def run_pipeline(source):
    """This function has timing, logging AND retry!"""
    df = pd.read_csv(source)
    return len(df)

# Decorators apply bottom-up: retry → log_call → timer
```

---

## Context Managers — `with` Statement

```python
# You already use context managers!
with open("file.txt", "r") as f:
    content = f.read()
# File is automatically closed — even if an error occurs!

# Without context manager (bad practice)
f = open("file.txt", "r")
content = f.read()
f.close()           # Easy to forget! And won't run if error occurs
```

---

## Writing Your Own Context Manager

### Method 1 — Class-based
```python
class DatabaseConnection:
    """Context manager for database connections"""
    
    def __init__(self, host, database):
        self.host = host
        self.database = database
        self.connection = None
    
    def __enter__(self):
        """Setup — runs when entering `with` block"""
        print(f"🔌 Connecting to {self.database} at {self.host}")
        # self.connection = psycopg2.connect(...)  # Real DB connection
        self.connection = {"status": "connected", "db": self.database}
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Teardown — runs when leaving `with` block"""
        print(f"🔌 Closing connection to {self.database}")
        self.connection = None
        
        if exc_type:
            print(f"❌ Error occurred: {exc_val}")
        return False    # Don't suppress exceptions

# Use it
with DatabaseConnection("localhost", "sales_db") as conn:
    print(f"Running query on {conn['db']}")
    # Do database work here
# Connection automatically closed!
```

### Method 2 — Generator-based (Simpler)
```python
from contextlib import contextmanager

@contextmanager
def timer_context(name):
    """Time a block of code"""
    import time
    print(f"⏱️  Starting: {name}")
    start = time.time()
    try:
        yield                   # Code inside `with` runs here
    finally:
        elapsed = time.time() - start
        print(f"⏱️  {name} completed in {elapsed:.4f}s")

# Use it
with timer_context("Data Processing"):
    df = pd.read_csv("large_file.csv")
    df = df.dropna()
    df.to_csv("output.csv")
```

---

## Real World Example — Pipeline with Decorators & Context Managers

```python
import time
import logging
import functools
from contextlib import contextmanager
import pandas as pd

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("pipeline")

# Decorators
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} took {time.time()-start:.2f}s")
        return result
    return wrapper

def log_step(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"▶ Running: {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"✅ Done: {func.__name__}")
        return result
    return wrapper

# Context manager
@contextmanager
def pipeline_context(name):
    logger.info(f"🚀 Pipeline starting: {name}")
    start = time.time()
    try:
        yield
        logger.info(f"✅ Pipeline complete: {name} ({time.time()-start:.1f}s)")
    except Exception as e:
        logger.error(f"💥 Pipeline failed: {name} — {e}")
        raise

# Pipeline functions with decorators
@timer
@log_step
def extract(path):
    return pd.read_csv(path)

@timer
@log_step
def transform(df):
    df = df.drop_duplicates()
    df = df.dropna()
    return df

@timer
@log_step
def load(df, path):
    df.to_csv(path, index=False)
    return len(df)

# Run with context manager
with pipeline_context("Bank Marketing ETL"):
    df = extract("data/bank_marketing.csv")
    df = transform(df)
    rows = load(df, "outputs/clean.csv")
    logger.info(f"Loaded {rows:,} rows")
```

---

## Built-in Context Managers

```python
# File handling
with open("file.txt", "r") as f:
    data = f.read()

# Multiple files at once
with open("input.csv") as src, open("output.csv", "w") as dst:
    dst.write(src.read())

# Suppress specific errors
from contextlib import suppress
with suppress(FileNotFoundError):
    os.remove("temp_file.txt")  # Won't crash if file missing

# Redirect stdout
from contextlib import redirect_stdout
with open("output.txt", "w") as f:
    with redirect_stdout(f):
        print("This goes to the file, not console!")
```

---

## Quick Reference

```python
# Basic decorator
def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # before
        result = func(*args, **kwargs)
        # after
        return result
    return wrapper

# Decorator with arguments
def decorator_factory(arg):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Context manager class
class MyContext:
    def __enter__(self): return self
    def __exit__(self, *args): pass

# Context manager function
@contextmanager
def my_context():
    # setup
    yield value
    # teardown
```

---

## Previous | Next
← [[17 - Error Handling and Logging]] | → [[19 - Virtual Environments and Project Structure]]
