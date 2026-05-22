---
title: Data Sources and Extraction
tags: [data-engineering, extraction, apis, etl]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# 📥 Data Sources & Extraction

> Data extraction is the first step of every pipeline. You need to know how to pull data from APIs, databases, files, and streams reliably, with error handling and incremental loading.

---

## Types of Data Sources

```
Structured          Semi-structured      Unstructured
──────────────      ─────────────────    ────────────────
PostgreSQL          JSON APIs            PDFs
MySQL               XML feeds            Images
Snowflake           CSV/TSV files        Videos
Excel tables        Parquet files        Text documents
                    MongoDB              Audio
```

---

## Extracting from Files

```python
# src/extract/file_extractor.py
import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class FileExtractor:
    """Extract data from various file formats"""
    
    def extract_csv(self, filepath: str, **kwargs) -> pd.DataFrame:
        """Extract from CSV file"""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        df = pd.read_csv(filepath, **kwargs)
        logger.info(f"Extracted {len(df):,} rows from {path.name}")
        return df
    
    def extract_excel(self, filepath: str, sheet_name=0) -> pd.DataFrame:
        """Extract from Excel file"""
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        logger.info(f"Extracted {len(df):,} rows from Excel")
        return df
    
    def extract_parquet(self, filepath: str) -> pd.DataFrame:
        """Extract from Parquet file"""
        df = pd.read_parquet(filepath)
        logger.info(f"Extracted {len(df):,} rows from Parquet")
        return df
    
    def extract_json(self, filepath: str) -> pd.DataFrame:
        """Extract from JSON file"""
        df = pd.read_json(filepath)
        logger.info(f"Extracted {len(df):,} rows from JSON")
        return df
    
    def extract_directory(self, folder: str, pattern="*.csv") -> pd.DataFrame:
        """Extract and combine all matching files in a directory"""
        folder_path = Path(folder)
        files = list(folder_path.glob(pattern))
        
        if not files:
            raise ValueError(f"No files matching {pattern} in {folder}")
        
        dfs = []
        for file in files:
            df = pd.read_csv(file)
            df["source_file"] = file.name
            dfs.append(df)
            logger.info(f"Loaded: {file.name} ({len(df):,} rows)")
        
        combined = pd.concat(dfs, ignore_index=True)
        logger.info(f"Combined {len(files)} files: {len(combined):,} total rows")
        return combined
```

---

## Extracting from Databases

```python
# src/extract/db_extractor.py
import pandas as pd
from sqlalchemy import create_engine, text
import logging
import os

logger = logging.getLogger(__name__)

class DatabaseExtractor:
    """Extract data from SQL databases"""
    
    def __init__(self, db_url: str = None):
        url = db_url or os.getenv("SOURCE_DB_URL")
        self.engine = create_engine(url)
        logger.info("Database extractor initialised")
    
    def extract_table(self, table: str, schema: str = None) -> pd.DataFrame:
        """Extract entire table"""
        full_table = f"{schema}.{table}" if schema else table
        df = pd.read_sql_table(table, self.engine, schema=schema)
        logger.info(f"Extracted {len(df):,} rows from {full_table}")
        return df
    
    def extract_query(self, query: str, params: dict = None) -> pd.DataFrame:
        """Extract using custom SQL query"""
        df = pd.read_sql(query, self.engine, params=params)
        logger.info(f"Query returned {len(df):,} rows")
        return df
    
    def extract_incremental(self, table: str, watermark_col: str,
                             last_value) -> pd.DataFrame:
        """Extract only new/changed records since last run"""
        query = f"""
            SELECT *
            FROM {table}
            WHERE {watermark_col} > :last_value
            ORDER BY {watermark_col}
        """
        df = pd.read_sql(query, self.engine,
                         params={"last_value": last_value})
        logger.info(f"Incremental: {len(df):,} new rows since {last_value}")
        return df
    
    def extract_chunked(self, table: str, chunk_size: int = 10000):
        """Extract large tables in chunks to avoid memory issues"""
        query = f"SELECT * FROM {table}"
        total = 0
        
        for chunk in pd.read_sql(query, self.engine, chunksize=chunk_size):
            total += len(chunk)
            logger.info(f"Processing chunk: {len(chunk):,} rows (total: {total:,})")
            yield chunk
```

---

## Extracting from REST APIs

```python
# src/extract/api_extractor.py
import requests
import pandas as pd
import time
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class APIExtractor:
    """Extract data from REST APIs with retry and pagination"""
    
    def __init__(self, base_url: str, api_key: str = None,
                 rate_limit_per_min: int = 60):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.min_interval = 60 / rate_limit_per_min
        self.last_request_time = 0
        
        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            })
    
    def _rate_limit(self):
        """Enforce rate limiting between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()
    
    def get(self, endpoint: str, params: Dict = None,
            retries: int = 3) -> Dict:
        """Make GET request with retry logic"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(1, retries + 1):
            try:
                self._rate_limit()
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                return response.json()
                
            except requests.HTTPError as e:
                if response.status_code == 429:  # Rate limited
                    wait = int(response.headers.get("Retry-After", 60))
                    logger.warning(f"Rate limited. Waiting {wait}s...")
                    time.sleep(wait)
                elif response.status_code >= 500:  # Server error
                    logger.warning(f"Server error (attempt {attempt}/{retries})")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
            except requests.ConnectionError:
                logger.warning(f"Connection error (attempt {attempt}/{retries})")
                time.sleep(2 ** attempt)
        
        raise Exception(f"Failed after {retries} attempts: {url}")
    
    def get_paginated(self, endpoint: str, params: Dict = None,
                      page_key: str = "page",
                      data_key: str = "results",
                      total_key: str = "count",
                      page_size: int = 100) -> pd.DataFrame:
        """Extract all pages from paginated API"""
        all_records = []
        page = 1
        params = params or {}
        params["page_size"] = page_size
        
        while True:
            params[page_key] = page
            response = self.get(endpoint, params)
            
            records = response.get(data_key, [])
            all_records.extend(records)
            
            total = response.get(total_key, 0)
            logger.info(f"Page {page}: {len(records)} records "
                       f"({len(all_records):,}/{total:,} total)")
            
            # Check if more pages exist
            if len(all_records) >= total or not records:
                break
            page += 1
        
        df = pd.DataFrame(all_records)
        logger.info(f"Extracted {len(df):,} total records")
        return df


# Usage example
extractor = APIExtractor(
    base_url="https://api.example.com",
    api_key=os.getenv("API_KEY")
)

# Single request
data = extractor.get("customers/1")

# Paginated extraction
df = extractor.get_paginated(
    endpoint="customers",
    params={"status": "active", "country": "KE"}
)
```

---

## Extracting from Multiple Sources (Fan-out)

```python
# src/extract/multi_source_extractor.py
import pandas as pd
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Callable

logger = logging.getLogger(__name__)

def extract_parallel(sources: Dict[str, Callable],
                     max_workers: int = 4) -> Dict[str, pd.DataFrame]:
    """Extract from multiple sources in parallel"""
    results = {}
    errors = {}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all extraction jobs
        futures = {
            executor.submit(func): name
            for name, func in sources.items()
        }
        
        # Collect results as they complete
        for future in as_completed(futures):
            name = futures[future]
            try:
                results[name] = future.result()
                logger.info(f"✅ Extracted {name}: "
                           f"{len(results[name]):,} rows")
            except Exception as e:
                errors[name] = str(e)
                logger.error(f"❌ Failed to extract {name}: {e}")
    
    if errors:
        logger.warning(f"Extraction errors: {errors}")
    
    return results


# Usage
db = DatabaseExtractor()
api = APIExtractor("https://api.example.com")

datasets = extract_parallel({
    "customers":     lambda: db.extract_table("customers"),
    "transactions":  lambda: db.extract_table("transactions"),
    "products":      lambda: api.get_paginated("products"),
    "campaign_data": lambda: FileExtractor().extract_csv("data/campaign.csv")
})

customers_df = datasets["customers"]
transactions_df = datasets["transactions"]
```

---

## Watermark Management — Incremental Extraction

```python
# src/extract/watermark_manager.py
import json
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class WatermarkManager:
    """Track extraction progress for incremental loads"""
    
    def __init__(self, filepath: str = "watermarks.json"):
        self.filepath = Path(filepath)
        self.watermarks = self._load()
    
    def _load(self) -> dict:
        if self.filepath.exists():
            with open(self.filepath) as f:
                return json.load(f)
        return {}
    
    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.watermarks, f, indent=2, default=str)
    
    def get(self, source: str, default=None):
        """Get last extraction timestamp for a source"""
        value = self.watermarks.get(source, default)
        logger.info(f"Watermark [{source}]: {value}")
        return value
    
    def set(self, source: str, value):
        """Update watermark after successful extraction"""
        self.watermarks[source] = str(value)
        self._save()
        logger.info(f"Updated watermark [{source}]: {value}")
    
    def reset(self, source: str):
        """Reset watermark (force full refresh)"""
        if source in self.watermarks:
            del self.watermarks[source]
            self._save()
            logger.info(f"Reset watermark [{source}]")


# Usage in pipeline
wm = WatermarkManager("pipeline_watermarks.json")

# Get last run timestamp
last_run = wm.get("transactions", default="2020-01-01")

# Extract only new data
db = DatabaseExtractor()
new_data = db.extract_incremental(
    table="transactions",
    watermark_col="created_at",
    last_value=last_run
)

# Update watermark after successful load
if len(new_data) > 0:
    max_ts = new_data["created_at"].max()
    wm.set("transactions", max_ts)
```

---

## Real World — Bank Marketing Extraction

```python
# src/extract/bank_marketing_extractor.py
"""
Extraction layer for Bank Marketing pipeline.
Supports: CSV files, PostgreSQL source, and REST API
"""
import pandas as pd
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def extract_bank_marketing(source_type: str = "csv",
                           **kwargs) -> pd.DataFrame:
    """
    Extract bank marketing data from configured source.
    
    Args:
        source_type: 'csv', 'database', or 'api'
    Returns:
        Raw DataFrame with all source records
    """
    
    if source_type == "csv":
        filepath = kwargs.get("filepath",
                             os.getenv("DATA_PATH",
                                      "data/bank_marketing.csv"))
        logger.info(f"Extracting from CSV: {filepath}")
        df = pd.read_csv(filepath, sep=";")   # Bank dataset uses ;
        
    elif source_type == "database":
        from .db_extractor import DatabaseExtractor
        extractor = DatabaseExtractor(kwargs.get("db_url"))
        df = extractor.extract_table(
            table="raw_bank_marketing",
            schema="bronze"
        )
        
    elif source_type == "api":
        from .api_extractor import APIExtractor
        extractor = APIExtractor(
            base_url=kwargs.get("api_url"),
            api_key=kwargs.get("api_key")
        )
        df = extractor.get_paginated("campaigns/bank_marketing")
    
    else:
        raise ValueError(f"Unknown source type: {source_type}")
    
    # Log extraction stats
    logger.info(f"Extracted {len(df):,} rows, {len(df.columns)} columns")
    logger.info(f"Columns: {list(df.columns)}")
    logger.info(f"Date range: {df.shape}")
    
    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    df = extract_bank_marketing(source_type="csv")
    print(df.head())
    print(df.dtypes)
```

---

## Quick Reference

```python
# Files
pd.read_csv("file.csv")
pd.read_excel("file.xlsx", sheet_name="Sheet1")
pd.read_parquet("file.parquet")
pd.read_json("file.json")

# Database
pd.read_sql_table("table_name", engine)
pd.read_sql("SELECT ...", engine)
pd.read_sql("SELECT ...", engine, chunksize=10000)

# API
response = requests.get(url, headers=headers, params=params)
data = response.json()
df = pd.DataFrame(data["results"])

# Incremental
WHERE updated_at > :last_watermark
ORDER BY updated_at

# Parallel extraction
with ThreadPoolExecutor(max_workers=4) as ex:
    futures = {ex.submit(func): name for name, func in sources.items()}
```

---

## Previous | Next
← [[01 - Introduction to Data Engineering]] | → [[03 - Loading Data (Batch)]]
