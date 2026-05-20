---
title: Error Handling and Logging
tags: [python, advanced, data-engineering]
created: 2026-05-20
up:: [[Python MOC]]
---

# 🛡️ Error Handling & Logging

> Production code never crashes silently. Error handling catches problems gracefully; logging records what happened so you can debug later. Non-negotiable in data engineering.

---

## Types of Errors

```python
# SyntaxError — typo in code
print("hello"           # Missing closing bracket

# NameError — undefined variable
print(undefined_var)

# TypeError — wrong data type
"text" + 5

# ValueError — right type, wrong value
int("not a number")

# IndexError — list index out of range
my_list = [1, 2, 3]
my_list[10]

# KeyError — dict key doesn't exist
my_dict = {"name": "Beatrice"}
my_dict["age"]

# FileNotFoundError
open("missing_file.csv")

# ZeroDivisionError
10 / 0
```

---

## try / except

```python
# Basic
try:
    result = 10 / 0
except ZeroDivisionError:
    print("❌ Cannot divide by zero")

# Catch specific errors
try:
    value = int("not a number")
except ValueError:
    print("❌ Invalid number format")
except TypeError:
    print("❌ Wrong data type")

# Catch multiple in one line
try:
    risky_operation()
except (ValueError, TypeError):
    print("❌ Value or Type error")

# Catch ANY exception
try:
    risky_operation()
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"   Type: {type(e).__name__}")
```

---

## try / except / else / finally

```python
try:
    df = pd.read_csv("data.csv")
    
except FileNotFoundError:
    print("❌ File not found")
    df = None
    
except pd.errors.EmptyDataError:
    print("❌ File is empty")
    df = None
    
else:
    # Runs only if NO exception occurred
    print(f"✅ Loaded {len(df):,} rows successfully")
    
finally:
    # ALWAYS runs — great for cleanup
    print("Pipeline step completed")
```

---

## Raising Exceptions

```python
def validate_salary(salary):
    if not isinstance(salary, (int, float)):
        raise TypeError(f"Salary must be a number, got {type(salary).__name__}")
    if salary < 0:
        raise ValueError("Salary cannot be negative")
    if salary < 30000:
        raise ValueError(f"Salary KES {salary:,} is below minimum wage (KES 30,000)")
    return salary

try:
    validate_salary(-5000)
except ValueError as e:
    print(f"Validation Error: {e}")
except TypeError as e:
    print(f"Type Error: {e}")
```

---

## Custom Exceptions

```python
# Define custom exceptions
class DataPipelineError(Exception):
    """Base exception for pipeline errors"""
    pass

class ExtractionError(DataPipelineError):
    """Raised when data extraction fails"""
    pass

class ValidationError(DataPipelineError):
    """Raised when data validation fails"""
    def __init__(self, message, field=None, value=None):
        super().__init__(message)
        self.field = field
        self.value = value

class TransformationError(DataPipelineError):
    """Raised when data transformation fails"""
    pass


# Use custom exceptions
def extract_data(filepath):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        raise ExtractionError(f"Source file not found: {filepath}")
    except Exception as e:
        raise ExtractionError(f"Extraction failed: {e}")

def validate_age(age):
    if age < 0 or age > 120:
        raise ValidationError(
            f"Invalid age: {age}",
            field="age",
            value=age
        )

try:
    df = extract_data("missing.csv")
except ExtractionError as e:
    print(f"Pipeline failed at extraction: {e}")
except DataPipelineError as e:
    print(f"Pipeline error: {e}")
```

---

## Logging

```python
import logging

# Basic setup
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# Log levels (lowest to highest)
logger.debug("🔍 Debug — detailed diagnostic info")
logger.info("ℹ️  Info  — general progress messages")
logger.warning("⚠️  Warning — something unexpected")
logger.error("❌ Error — something failed")
logger.critical("🔥 Critical — system may be broken")
```

---

## Logging to File

```python
import logging
from pathlib import Path

def setup_logger(name, log_file="pipeline.log", level=logging.INFO):
    """Create a logger that writes to both console and file"""
    
    Path("logs").mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # File handler
    file_handler = logging.FileHandler(f"logs/{log_file}")
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Format
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Use it
logger = setup_logger("bank_pipeline", "bank_etl.log")
logger.info("Pipeline started")
logger.debug("Loading config...")
logger.warning("Missing values detected in salary column")
logger.error("Failed to connect to database")
```

---

## Real World Example — Production ETL with Logging

```python
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime

class ETLPipeline:
    """Production ETL pipeline with full error handling and logging"""
    
    def __init__(self, name):
        self.name = name
        self.logger = self._setup_logger()
        self.stats = {"extracted": 0, "transformed": 0, "loaded": 0, "errors": 0}
    
    def _setup_logger(self):
        Path("logs").mkdir(exist_ok=True)
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        
        fh = logging.FileHandler(f"logs/{self.name}.log")
        ch = logging.StreamHandler()
        
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        fh.setFormatter(fmt)
        ch.setFormatter(fmt)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger
    
    def extract(self, filepath):
        self.logger.info(f"Extracting: {filepath}")
        try:
            df = pd.read_csv(filepath)
            self.stats["extracted"] = len(df)
            self.logger.info(f"Extracted {len(df):,} rows")
            return df
        except FileNotFoundError:
            self.logger.error(f"File not found: {filepath}")
            self.stats["errors"] += 1
            raise
        except Exception as e:
            self.logger.error(f"Extraction failed: {e}")
            self.stats["errors"] += 1
            raise
    
    def transform(self, df):
        self.logger.info("Transforming data...")
        try:
            original = len(df)
            
            # Clean
            df = df.drop_duplicates()
            self.logger.debug(f"Removed {original - len(df)} duplicates")
            
            df = df.dropna(subset=["id", "amount"])
            self.logger.debug(f"Dropped null rows. Remaining: {len(df)}")
            
            # Validate
            invalid = df[df["amount"] < 0]
            if len(invalid) > 0:
                self.logger.warning(f"Found {len(invalid)} negative amounts — removing")
                df = df[df["amount"] >= 0]
            
            self.stats["transformed"] = len(df)
            self.logger.info(f"Transformed: {len(df):,} rows retained")
            return df
            
        except KeyError as e:
            self.logger.error(f"Missing column: {e}")
            self.stats["errors"] += 1
            raise
    
    def load(self, df, output_path):
        self.logger.info(f"Loading to {output_path}")
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(output_path, index=False)
            self.stats["loaded"] = len(df)
            self.logger.info(f"✅ Loaded {len(df):,} rows to {output_path}")
        except PermissionError:
            self.logger.error(f"Permission denied: {output_path}")
            self.stats["errors"] += 1
            raise
    
    def run(self, source, destination):
        start = datetime.now()
        self.logger.info(f"🚀 Starting pipeline: {self.name}")
        
        try:
            df = self.extract(source)
            df = self.transform(df)
            self.load(df, destination)
            
            duration = (datetime.now() - start).seconds
            self.logger.info(f"✅ Pipeline complete in {duration}s | Stats: {self.stats}")
            
        except Exception as e:
            self.logger.critical(f"🔥 Pipeline failed: {e}")
            raise
        
        return df


# Run it
pipeline = ETLPipeline("bank_marketing")
result = pipeline.run(
    source="data/bank_marketing.csv",
    destination="outputs/bank_clean.csv"
)
```

---

## Quick Reference

```python
# Try/except pattern
try:
    risky_code()
except SpecificError as e:
    handle_it(e)
except (Error1, Error2):
    handle_both()
except Exception as e:
    catch_all(e)
else:
    runs_if_no_error()
finally:
    always_runs()

# Raise
raise ValueError("message")
raise CustomError("message", extra_data)

# Common exceptions
FileNotFoundError   # Missing file
ValueError          # Wrong value
TypeError           # Wrong type
KeyError            # Missing dict key
IndexError          # List out of range
ZeroDivisionError   # Division by zero
AttributeError      # Missing attribute
ImportError         # Module not found

# Logging levels
logger.debug()      # Detailed (dev only)
logger.info()       # Progress messages
logger.warning()    # Unexpected but handled
logger.error()      # Something failed
logger.critical()   # System breaking
```

---

## Previous | Next
← [[16 - Object Oriented Programming]] | → [[18 - Decorators and Context Managers]]
