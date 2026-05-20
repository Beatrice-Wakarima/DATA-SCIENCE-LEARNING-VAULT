---
title: Virtual Environments and Project Structure
tags: [python, advanced, best-practices]
created: 2026-05-20
up:: [[Python MOC]]
---

# 📦 Virtual Environments & Project Structure

> Every professional Python project lives in its own isolated environment. This prevents package conflicts and makes your code reproducible on any machine.

---

## The Problem Without Virtual Environments

```
Project A needs pandas==1.5.0
Project B needs pandas==2.0.0

Without venv → they conflict!
With venv    → each project has its own pandas ✅
```

---

## Creating a Virtual Environment

```bash
# Create
python -m venv venv

# Activate — Windows (Git Bash)
source venv/Scripts/activate

# Activate — Mac/Linux
source venv/bin/activate

# You'll see (venv) in your terminal prompt
(venv) $

# Deactivate
deactivate
```

---

## Installing Packages

```bash
# Always activate venv first!
source venv/Scripts/activate

# Install packages
pip install pandas numpy matplotlib seaborn
pip install requests python-dotenv
pip install scikit-learn

# Install specific version
pip install pandas==2.0.0

# Install from requirements file
pip install -r requirements.txt
```

---

## requirements.txt — Freezing Dependencies

```bash
# Generate requirements.txt from current environment
pip freeze > requirements.txt

# Install from requirements.txt (on new machine)
pip install -r requirements.txt
```

**Example `requirements.txt`:**
```
pandas==2.1.0
numpy==1.24.0
matplotlib==3.7.0
seaborn==0.12.0
requests==2.31.0
python-dotenv==1.0.0
scikit-learn==1.3.0
sqlalchemy==2.0.0
psycopg2-binary==2.9.6
apache-airflow==2.7.0
```

---

## Professional Project Structure

```
my_data_project/
│
├── 📁 data/
│   ├── raw/                    # Original, untouched data
│   ├── processed/              # Cleaned data
│   └── outputs/                # Final outputs
│
├── 📁 notebooks/               # Jupyter notebooks (exploration)
│   ├── 01_exploration.ipynb
│   └── 02_analysis.ipynb
│
├── 📁 src/                     # Source code
│   ├── __init__.py
│   ├── extract.py              # Extraction logic
│   ├── transform.py            # Transformation logic
│   ├── load.py                 # Loading logic
│   └── utils.py                # Shared utilities
│
├── 📁 tests/                   # Unit tests
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
│
├── 📁 logs/                    # Log files
│
├── 📁 config/                  # Configuration
│   └── config.yaml
│
├── .env                        # Secret keys (NEVER commit!)
├── .gitignore                  # Files to ignore in git
├── requirements.txt            # Dependencies
├── README.md                   # Project documentation
└── main.py                     # Entry point
```

---

## `.gitignore` — What NOT to Commit

```gitignore
# Virtual environment
venv/
env/
.env

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd

# Data files (often too large for git)
data/raw/
*.csv
*.xlsx
*.parquet

# Jupyter checkpoints
.ipynb_checkpoints/

# IDE files
.vscode/
.idea/

# Logs
logs/
*.log

# OS files
.DS_Store
Thumbs.db
```

---

## `.env` File — Secrets Management

```bash
# .env file (NEVER commit this!)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sales_db
DB_USER=beatrice
DB_PASSWORD=supersecret123

API_KEY=abc123xyz789
SECRET_TOKEN=my_secret_token
```

```python
# Load in Python
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
API_KEY = os.getenv("API_KEY")

print(DB_HOST)      # localhost (not hardcoded!)
```

---

## Config File with YAML

```yaml
# config/config.yaml
database:
  host: localhost
  port: 5432
  name: sales_db

pipeline:
  batch_size: 1000
  max_retries: 3
  timeout: 30

paths:
  raw_data: data/raw/
  processed: data/processed/
  outputs: data/outputs/
```

```python
import yaml

with open("config/config.yaml") as f:
    config = yaml.safe_load(f)

db_host = config["database"]["host"]
batch_size = config["pipeline"]["batch_size"]
raw_path = config["paths"]["raw_data"]
```

---

## `__init__.py` — Making Packages

```python
# src/__init__.py — makes src/ a Python package
from .extract import extract_data
from .transform import clean_data, transform_data
from .load import load_to_csv, load_to_db
from .utils import setup_logger, timer

# Now you can import cleanly:
# from src import extract_data, clean_data
```

---

## Modular Code Example

```python
# src/extract.py
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def extract_csv(filepath, **kwargs):
    """Extract data from CSV file"""
    logger.info(f"Extracting: {filepath}")
    df = pd.read_csv(filepath, **kwargs)
    logger.info(f"Extracted {len(df):,} rows")
    return df

def extract_excel(filepath, sheet_name=0):
    """Extract data from Excel file"""
    logger.info(f"Extracting Excel: {filepath}")
    df = pd.read_excel(filepath, sheet_name=sheet_name)
    logger.info(f"Extracted {len(df):,} rows")
    return df
```

```python
# src/transform.py
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def clean_strings(df, columns):
    """Standardize string columns"""
    for col in columns:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()
    return df

def remove_duplicates(df, subset=None):
    """Remove duplicate rows"""
    before = len(df)
    df = df.drop_duplicates(subset=subset)
    logger.info(f"Removed {before - len(df)} duplicates")
    return df

def handle_nulls(df, strategy="drop", fill_value=None):
    """Handle missing values"""
    if strategy == "drop":
        return df.dropna()
    elif strategy == "fill":
        return df.fillna(fill_value)
    elif strategy == "median":
        return df.fillna(df.median(numeric_only=True))
```

```python
# src/utils.py
import logging
import time
import functools
from pathlib import Path

def setup_logger(name, log_dir="logs"):
    Path(log_dir).mkdir(exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    fh = logging.FileHandler(f"{log_dir}/{name}.log")
    ch = logging.StreamHandler()
    
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"⏱️  {func.__name__}: {time.time()-start:.2f}s")
        return result
    return wrapper
```

```python
# main.py — Entry point
from src.extract import extract_csv
from src.transform import clean_strings, remove_duplicates, handle_nulls
from src.load import load_to_csv
from src.utils import setup_logger

logger = setup_logger("main_pipeline")

def run_pipeline():
    logger.info("🚀 Pipeline starting")
    
    # Extract
    df = extract_csv("data/raw/bank_marketing.csv")
    
    # Transform
    df = clean_strings(df, ["job", "education", "marital"])
    df = remove_duplicates(df)
    df = handle_nulls(df, strategy="drop")
    
    # Load
    load_to_csv(df, "data/processed/bank_clean.csv")
    
    logger.info("✅ Pipeline complete")

if __name__ == "__main__":
    run_pipeline()
```

---

## Quick Setup Script

```bash
#!/bin/bash
# setup.sh — Run once to set up new project

echo "🔧 Setting up project..."

# Create virtual environment
python -m venv venv
source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Create folder structure
mkdir -p data/{raw,processed,outputs}
mkdir -p src tests logs config notebooks

# Create placeholder files
touch src/__init__.py
touch src/extract.py src/transform.py src/load.py src/utils.py
touch main.py
touch .env
echo "venv/" >> .gitignore
echo ".env" >> .gitignore
echo "__pycache__/" >> .gitignore

echo "✅ Project ready!"
```

---

## Previous | Next
← [[18 - Decorators and Context Managers]] | → [[20 - Python for Automation]]
