# Bank Marketing Data Engineering Portfolio Project

_A comprehensive data engineering pipeline from raw CSV to PostgreSQL with monitoring and visualization_

## Project Overview

This portfolio project demonstrates end-to-end data engineering skills by building a scalable ETL pipeline for bank marketing data. The pipeline ingests raw CSV data, performs cleaning and transformation, loads data into PostgreSQL, tracks metadata, and provides real-time monitoring through a Streamlit dashboard.

### Key Technologies

- **Data Processing**: Python, Pandas
- **Database**: PostgreSQL
- **Configuration**: python-dotenv, BaseConfig pattern
- **Monitoring**: Custom metadata tracking
- **Visualization**: Streamlit dashboard
- **Future**: dbt for advanced transformations

## Project Architecture

```
bank_marketing_etl/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config/
│   ├── __init__.py
│   └── base_config.py
├── data/
│   ├── raw/
│   │   └── bank_marketing.csv
│   ├── processed/
│   │   ├── customers.csv
│   │   ├── campaigns.csv
│   │   └── economics.csv
│   └── logs/
│       └── ingestion_logs.csv
├── src/
│   ├── __init__.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── data_cleaner.py
│   │   └── data_splitter.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── schema.py
│   │   └── ingestion_tracker.py
│   └── utils/
│       ├── __init__.py
│       ├── logging_utils.py
│       └── validation.py
├── dashboard/
│   ├── __init__.py
│   ├── streamlit_app.py
│   └── dashboard_utils.py
├── scripts/
│   ├── run_pipeline.py
│   ├── setup_database.py
│   └── data_quality_check.py
└── tests/
    ├── __init__.py
    ├── test_ingestion.py
    ├── test_database.py
    └── test_validation.py
```

> [!note] Architecture Benefits This structure separates concerns, enables testing, supports scalability, and follows data engineering best practices for production systems.

# Configuration Management

_Secure, environment-aware configuration using BaseConfig pattern_

## Environment Configuration Strategy

### .env.example Template

bash

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bank_marketing
DB_USER=your_username
DB_PASSWORD=your_secure_password

# Data Paths
RAW_DATA_PATH=data/raw/bank_marketing.csv
PROCESSED_DATA_DIR=data/processed
LOG_DIR=data/logs

# Pipeline Settings
BATCH_SIZE=1000
MAX_RETRIES=3
TIMEOUT_SECONDS=300

# Dashboard Settings
STREAMLIT_PORT=8501
REFRESH_INTERVAL_SECONDS=30

# Environment
ENV=development
DEBUG=True
LOG_LEVEL=INFO
```

### BaseConfig Implementation

python

```python
# config/base_config.py
import os
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional

# Load environment variables
load_dotenv()

@dataclass
class BaseConfig:
    """Base configuration class with environment-specific overrides"""
    
    # Project structure
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    LOG_DIR: Path = DATA_DIR / "logs"
    
    # Database configuration
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_NAME: str = os.getenv("DB_NAME", "bank_marketing")
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    
    # File paths
    RAW_DATA_PATH: Path = Path(os.getenv("RAW_DATA_PATH", RAW_DATA_DIR / "bank_marketing.csv"))
    
    # Pipeline settings
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", 1000))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", 3))
    TIMEOUT_SECONDS: int = int(os.getenv("TIMEOUT_SECONDS", 300))
    
    # Dashboard settings
    STREAMLIT_PORT: int = int(os.getenv("STREAMLIT_PORT", 8501))
    REFRESH_INTERVAL_SECONDS: int = int(os.getenv("REFRESH_INTERVAL_SECONDS", 30))
    
    # Environment settings
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    def __post_init__(self):
        """Create necessary directories and validate configuration"""
        # Create directories if they don't exist
        self.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)
        
        # Validate critical settings
        if not self.DB_USER or not self.DB_PASSWORD:
            raise ValueError("Database credentials must be provided in environment variables")
        
        if not self.RAW_DATA_PATH.exists():
            raise FileNotFoundError(f"Raw data file not found: {self.RAW_DATA_PATH}")
    
    @property
    def db_connection_string(self) -> str:
        """Generate PostgreSQL connection string"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def customers_file_path(self) -> Path:
        return self.PROCESSED_DATA_DIR / "customers.csv"
    
    @property
    def campaigns_file_path(self) -> Path:
        return self.PROCESSED_DATA_DIR / "campaigns.csv"
    
    @property
    def outcomes_file_path(self) -> Path:
        return self.PROCESSED_DATA_DIR / "economics.csv"

class DevelopmentConfig(BaseConfig):
    """Development environment configuration"""
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    BATCH_SIZE: int = 100  # Smaller batches for development

class ProductionConfig(BaseConfig):
    """Production environment configuration"""
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    BATCH_SIZE: int = 5000  # Larger batches for production
    MAX_RETRIES: int = 5

class TestingConfig(BaseConfig):
    """Testing environment configuration"""
    DB_NAME: str = "bank_marketing_test"
    BATCH_SIZE: int = 10
    LOG_LEVEL: str = "ERROR"

# Configuration factory
def get_config() -> BaseConfig:
    """Get configuration based on environment"""
    env = os.getenv("ENV", "development").lower()
    
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }
    
    config_class = config_map.get(env, DevelopmentConfig)
    return config_class()

# Global configuration instance
config = get_config()
```

### Configuration Usage Pattern

python

```python
# In any module, import and use configuration
from config.base_config import config

# Use configuration values
print(f"Environment: {config.ENV}")
print(f"Database: {config.DB_NAME}")
print(f"Raw data path: {config.RAW_DATA_PATH}")

# Use connection string
import psycopg2
conn = psycopg2.connect(config.db_connection_string)
```

> [!tip] Configuration Best Practices
> 
> - Never commit `.env` files with real credentials
> - Use type hints and validation in config classes
> - Provide sensible defaults for development
> - Document all configuration options

# Data Ingestion Pipeline

_Modular ETL pipeline for processing bank marketing data_

## Pipeline Overview

The ingestion pipeline follows a clear ETL pattern:

1. **Extract**: Load raw CSV data
2. **Transform**: Clean and validate data
3. **Split**: Create normalized table structures
4. **Load**: Insert into PostgreSQL with metadata tracking

## Data Loader Module

### src/ingestion/data_loader.py

python

```python
import pandas as pd
import logging
from pathlib import Path
from typing import Optional
from config.base_config import config

logger = logging.getLogger(__name__)

class DataLoader:
    """Handles loading of raw data files"""
    
    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = file_path or config.RAW_DATA_PATH
        
    def load_raw_data(self) -> pd.DataFrame:
        """Load raw CSV data with error handling"""
        try:
            logger.info(f"Loading raw data from {self.file_path}")
            
            # Load with appropriate parameters for bank marketing dataset
            df = pd.read_csv(
                self.file_path,
                sep=';',  # Bank marketing dataset uses semicolon separator
                encoding='utf-8'
            )
            
            logger.info(f"Successfully loaded {len(df):,} rows and {len(df.columns)} columns")
            
            return df
            
        except FileNotFoundError:
            logger.error(f"Raw data file not found: {self.file_path}")
            raise
        except pd.errors.EmptyDataError:
            logger.error("Raw data file is empty")
            raise
        except Exception as e:
            logger.error(f"Error loading raw data: {str(e)}")
            raise
    
    def validate_raw_data(self, df: pd.DataFrame) -> bool:
        """Validate raw data structure and content"""
        required_columns = [
            'age', 'job', 'marital', 'education', 'default', 'housing', 'loan',
            'contact', 'month', 'day_of_week', 'duration', 'campaign', 'pdays',
            'previous', 'poutcome', 'emp.var.rate', 'cons.price.idx',
            'cons.conf.idx', 'euribor3m', 'nr.employed', 'y'
        ]
        
        # Check if all required columns are present
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            logger.error(f"Missing required columns: {missing_columns}")
            return False
        
        # Check for completely empty DataFrame
        if df.empty:
            logger.error("DataFrame is empty")
            return False
        
        # Check for reasonable data ranges
        if df['age'].min() < 0 or df['age'].max() > 120:
            logger.warning("Age values outside reasonable range")
        
        logger.info("Raw data validation passed")
        return True
```

## Data Cleaner Module

### src/ingestion/data_cleaner.py

python

```python
import pandas as pd
import numpy as np
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DataCleaner:
    """Handles data cleaning and standardization"""
    
    def __init__(self):
        self.cleaning_stats = {}
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply all cleaning transformations"""
        logger.info("Starting data cleaning process")
        original_rows = len(df)
        
        # Make a copy to avoid modifying original data
        df_clean = df.copy()
        
        # Apply cleaning steps
        df_clean = self._standardize_column_names(df_clean)
        df_clean = self._handle_missing_values(df_clean)
        df_clean = self._remove_duplicates(df_clean)
        df_clean = self._standardize_categorical_values(df_clean)
        df_clean = self._handle_outliers(df_clean)
        df_clean = self._add_derived_columns(df_clean)
        
        # Log cleaning statistics
        cleaned_rows = len(df_clean)
        self.cleaning_stats = {
            'original_rows': original_rows,
            'cleaned_rows': cleaned_rows,
            'rows_removed': original_rows - cleaned_rows,
            'removal_percentage': ((original_rows - cleaned_rows) / original_rows) * 100
        }
        
        logger.info(f"Cleaning completed: {cleaned_rows:,} rows remaining "
                   f"({self.cleaning_stats['removal_percentage']:.2f}% removed)")
        
        return df_clean
    
    def _standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names for consistency"""
        column_mapping = {
            'emp.var.rate': 'employment_variation_rate',
            'cons.price.idx': 'consumer_price_index',
            'cons.conf.idx': 'consumer_confidence_index',
            'euribor3m': 'euribor_3_month',
            'nr.employed': 'number_employed',
            'pdays': 'previous_days',
            'previous': 'previous_contacts',
            'poutcome': 'previous_outcome',
            'y': 'target'
        }
        
        df_renamed = df.rename(columns=column_mapping)
        logger.info(f"Standardized {len(column_mapping)} column names")
        
        return df_renamed
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values based on column type and business logic"""
        # Handle sentinel values (999 in previous_days means "not contacted")
        if 'previous_days' in df.columns:
            df['previous_days'] = df['previous_days'].replace(999, -1)
        
        # Fill missing previous contacts with 0
        if 'previous_contacts' in df.columns:
            df['previous_contacts'] = df['previous_contacts'].fillna(0)
        
        # Forward fill economic indicators (they change gradually)
        economic_cols = ['employment_variation_rate', 'consumer_price_index', 
                        'consumer_confidence_index', 'euribor_3_month', 'number_employed']
        
        for col in economic_cols:
            if col in df.columns:
                df[col] = df[col].fillna(method='ffill')
        
        logger.info("Missing values handled")
        return df
    
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows"""
        initial_count = len(df)
        df_dedup = df.drop_duplicates()
        duplicates_removed = initial_count - len(df_dedup)
        
        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate rows")
        
        return df_dedup
    
    def _standardize_categorical_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize categorical values for consistency"""
        # Education level standardization
        if 'education' in df.columns:
            education_mapping = {
                'basic.4y': 'basic_education',
                'basic.6y': 'basic_education',
                'basic.9y': 'basic_education',
                'high.school': 'high_school',
                'professional.course': 'professional',
                'university.degree': 'university',
                'illiterate': 'basic_education',
                'unknown': 'unknown'
            }
            df['education'] = df['education'].map(education_mapping).fillna(df['education'])
        
        # Job standardization
        if 'job' in df.columns:
            job_mapping = {
                'admin.': 'administrative',
                'blue-collar': 'blue_collar',
                'self-employed': 'self_employed'
            }
            df['job'] = df['job'].replace(job_mapping)
        
        logger.info("Categorical values standardized")
        return df
    
    def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle outliers in numerical columns"""
        # Remove impossible age values
        if 'age' in df.columns:
            initial_count = len(df)
            df = df[(df['age'] >= 18) & (df['age'] <= 100)]
            outliers_removed = initial_count - len(df)
            if outliers_removed > 0:
                logger.info(f"Removed {outliers_removed} age outliers")
        
        # Handle extreme campaign values
        if 'campaign' in df.columns:
            # Cap campaign contacts at 99th percentile
            cap_value = df['campaign'].quantile(0.99)
            df['campaign'] = df['campaign'].clip(upper=cap_value)
        
        return df
    
    def _add_derived_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add derived columns for analysis"""
        # Add customer ID
        df['customer_id'] = range(1, len(df) + 1)
        
        # Add age groups
        if 'age' in df.columns:
            df['age_group'] = pd.cut(df['age'], 
                                   bins=[0, 30, 40, 50, 60, 100], 
                                   labels=['18-30', '31-40', '41-50', '51-60', '60+'],
                                   include_lowest=True)
        
        # Convert target to numeric
        if 'target' in df.columns:
            df['target_numeric'] = df['target'].map({'yes': 1, 'no': 0})
        
        logger.info("Derived columns added")
        return df
    
    def get_cleaning_stats(self) -> Dict[str, Any]:
        """Return cleaning statistics"""
        return self.cleaning_stats
```

## Data Splitter Module

### src/ingestion/data_splitter.py

python

```python
import pandas as pd
import logging
from pathlib import Path
from typing import Tuple, Dict
from config.base_config import config

logger = logging.getLogger(__name__)

class DataSplitter:
    """Splits cleaned data into normalized table structures"""
    
    def __init__(self):
        self.split_stats = {}
    
    def split_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Split data into customers, campaigns, and outcomes tables"""
        logger.info("Starting data split process")
        
        # Create customers table
        customers_df = self._create_customers_table(df)
        
        # Create campaigns table
        campaigns_df = self._create_campaigns_table(df)
        
        # Create outcomes table
        outcomes_df = self._create_outcomes_table(df)
        
        # Log split statistics
        self.split_stats = {
            'total_records': len(df),
            'customers_records': len(customers_df),
            'campaigns_records': len(campaigns_df),
            'outcomes_records': len(outcomes_df)
        }
        
        logger.info(f"Data split completed: "
                   f"{len(customers_df)} customers, "
                   f"{len(campaigns_df)} campaigns, "
                   f"{len(outcomes_df)} outcomes")
        
        return customers_df, campaigns_df, outcomes_df
    
    def _create_customers_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create normalized customers table"""
        customer_columns = [
            'customer_id', 'age', 'job', 'marital', 'education', 
            'default', 'housing', 'loan', 'age_group'
        ]
        
        customers_df = df[customer_columns].copy()
        
        # Ensure unique customers (in case of multiple campaigns per customer)
        customers_df = customers_df.drop_duplicates(subset=['customer_id'])
        
        return customers_df
    
    def _create_campaigns_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create campaigns table with contact information"""
        campaign_columns = [
            'customer_id', 'contact', 'month', 'day_of_week', 'duration',
            'campaign', 'previous_days', 'previous_contacts', 'previous_outcome',
            'employment_variation_rate', 'consumer_price_index',
            'consumer_confidence_index', 'euribor_3_month', 'number_employed'
        ]
        
        campaigns_df = df[campaign_columns].copy()
        
        # Add campaign ID
        campaigns_df['campaign_id'] = range(1, len(campaigns_df) + 1)
        
        return campaigns_df
    
    def _create_outcomes_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create outcomes table with campaign results"""
        outcome_columns = [
            'customer_id', 'target', 'target_numeric'
        ]
        
        outcomes_df = df[outcome_columns].copy()
        
        # Add outcome ID
        outcomes_df['outcome_id'] = range(1, len(outcomes_df) + 1)
        
        return outcomes_df
    
    def save_split_data(self, customers_df: pd.DataFrame, 
                       campaigns_df: pd.DataFrame, 
                       outcomes_df: pd.DataFrame) -> Dict[str, Path]:
        """Save split data to CSV files"""
        file_paths = {}
        
        # Save customers
        customers_path = config.customers_file_path
        customers_df.to_csv(customers_path, index=False)
        file_paths['customers'] = customers_path
        logger.info(f"Customers data saved to {customers_path}")
        
        # Save campaigns
        campaigns_path = config.campaigns_file_path
        campaigns_df.to_csv(campaigns_path, index=False)
        file_paths['campaigns'] = campaigns_path
        logger.info(f"Campaigns data saved to {campaigns_path}")
        
        # Save outcomes
        outcomes_path = config.outcomes_file_path
        outcomes_df.to_csv(outcomes_path, index=False)
        file_paths['outcomes'] = outcomes_path
        logger.info(f"Outcomes data saved to {outcomes_path}")
        
        return file_paths
    
    def get_split_stats(self) -> Dict[str, int]:
        """Return split statistics"""
        return self.split_stats
```

> [!important] Data Normalization Benefits Splitting data into normalized tables improves data integrity, reduces redundancy, and enables efficient queries. This structure supports future analytics and machine learning workflows.

# Database Operations

_PostgreSQL integration with connection management and metadata tracking_

## Database Connection Module

### src/database/connection.py

python

```python
import psycopg2
import psycopg2.extras
import logging
from contextlib import contextmanager
from typing import Generator, Optional, Dict, Any
from config.base_config import config

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Manages PostgreSQL database connections"""
    
    def __init__(self, connection_string: Optional[str] = None):
        self.connection_string = connection_string or config.db_connection_string
        
    @contextmanager
    def get_connection(self) -> Generator[psycopg2.extensions.connection, None, None]:
        """Context manager for database connections"""
        conn = None
        try:
            logger.debug("Establishing database connection")
            conn = psycopg2.connect(self.connection_string)
            conn.autocommit = False
            yield conn
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()
                logger.debug("Database connection closed")
    
    @contextmanager
    def get_cursor(self, dict_cursor: bool = False) -> Generator[psycopg2.extensions.cursor, None, None]:
        """Context manager for database cursors"""
        with self.get_connection() as conn:
            cursor_class = psycopg2.extras.DictCursor if dict_cursor else None
            cursor = conn.cursor(cursor_factory=cursor_class)
            try:
                yield cursor
                conn.commit()
            except Exception as e:
                conn.rollback()
                logger.error(f"Database operation error: {e}")
                raise
            finally:
                cursor.close()
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                logger.info("Database connection test successful")
                return result[0] == 1
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Optional[Any]:
        """Execute a query and return results"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description:
                return cursor.fetchall()
            return None
    
    def execute_many(self, query: str, data: list) -> int:
        """Execute query with multiple parameter sets"""
        with self.get_cursor() as cursor:
            cursor.executemany(query, data)
            return cursor.rowcount

# Global database connection instance
db = DatabaseConnection()
```

## Database Schema Module

### src/database/schema.py

python

```python
import logging
from typing import List
from .connection import db

logger = logging.getLogger(__name__)

class SchemaManager:
    """Manages database schema creation and updates"""
    
    def create_all_tables(self) -> None:
        """Create all required tables"""
        logger.info("Creating database schema")
        
        tables = [
            self._create_customers_table(),
            self._create_campaigns_table(),
            self._create_outcomes_table(),
            self._create_ingestion_log_table()
        ]
        
        for table_sql in tables:
            try:
                db.execute_query(table_sql)
                logger.info(f"Table created successfully")
            except Exception as e:
                logger.error(f"Error creating table: {e}")
                raise
        
        logger.info("All tables created successfully")
    
    def _create_customers_table(self) -> str:
        """Create customers table SQL"""
        return """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            age INTEGER NOT NULL,
            job VARCHAR(50) NOT NULL,
            marital VARCHAR(20) NOT NULL,
            education VARCHAR(30) NOT NULL,
            default_credit VARCHAR(10) NOT NULL,
            housing_loan VARCHAR(10) NOT NULL,
            personal_loan VARCHAR(10) NOT NULL,
            age_group VARCHAR(10),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_customers_age ON customers(age);
        CREATE INDEX IF NOT EXISTS idx_customers_job ON customers(job);
        CREATE INDEX IF NOT EXISTS idx_customers_education ON customers(education);
        """
    
    def _create_campaigns_table(self) -> str:
        """Create campaigns table SQL"""
        return """
        CREATE TABLE IF NOT EXISTS campaigns (
            campaign_id SERIAL PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(customer_id),
            contact_type VARCHAR(20) NOT NULL,
            contact_month VARCHAR(10) NOT NULL,
            contact_day_of_week VARCHAR(10) NOT NULL,
            duration_seconds INTEGER NOT NULL,
            campaign_contacts INTEGER NOT NULL,
            previous_days INTEGER,
            previous_contacts INTEGER,
            previous_outcome VARCHAR(20),
            employment_variation_rate DECIMAL(5,2),
            consumer_price_index DECIMAL(6,3),
            consumer_confidence_index DECIMAL(6,2),
            euribor_3_month DECIMAL(6,3),
            number_employed DECIMAL(8,1),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_campaigns_customer_id ON campaigns(customer_id);
        CREATE INDEX IF NOT EXISTS idx_campaigns_month ON campaigns(contact_month);
        CREATE INDEX IF NOT EXISTS idx_campaigns_outcome ON campaigns(previous_outcome);
        """
    
    def _create_outcomes_table(self) -> str:
        """Create outcomes table SQL"""
        return """
        CREATE TABLE IF NOT EXISTS outcomes (
            outcome_id SERIAL PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(customer_id),
            campaign_result VARCHAR(10) NOT NULL,
            campaign_result_numeric INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_outcomes_customer_id ON outcomes(customer_id);
        CREATE INDEX IF NOT EXISTS idx_outcomes_result ON outcomes(campaign_result);
        """
    
    def _create_ingestion_log_table(self) -> str:
        """Create ingestion log table SQL"""
        return """
        CREATE TABLE IF NOT EXISTS ingestion_log (
            log_id SERIAL PRIMARY KEY,
            run_id VARCHAR(50) UNIQUE NOT NULL,
            pipeline_version VARCHAR(20),
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP,
            status VARCHAR(20) NOT NULL,
            total_records_processed INTEGER,
            customers_loaded INTEGER,
            campaigns_loaded INTEGER,
            outcomes_loaded INTEGER,
            error_message TEXT,
            processing_duration_seconds INTEGER,
            data_quality_score DECIMAL(5,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_ingestion_log_run_id ON ingestion_log(run_id);
        CREATE INDEX IF NOT EXISTS idx_ingestion_log_status ON ingestion_log(status);
        CREATE INDEX IF NOT EXISTS idx_ingestion_log_start_time ON ingestion_log(start_time);
        """
    
    def drop_all_tables(self) -> None:
        """Drop all tables (use with caution)"""
        logger.warning("Dropping all tables")
        
        tables = ['outcomes', 'campaigns', 'customers', 'ingestion_log']
        
        for table in tables:
            try:
                db.execute_query(f"DROP TABLE IF EXISTS {table} CASCADE")
                logger.info(f"Table {table} dropped")
            except Exception as e:
                logger.error(f"Error dropping table {table}: {e}")
    
    def table_exists(self, table_name: str) -> bool:
        """Check if table exists"""
        query = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = %s
        );
        """
        result = db.execute_query(query, (table_name,))
        return result[0][0] if result else False
    
    def get_table_row_count(self, table_name: str) -> int:
        """Get row count for a table"""
        if not self.table_exists(table_name):
            return 0
        
        result = db.execute_query(f"SELECT COUNT(*) FROM {table_name}")
        return result[0][0] if result else 0

schema_manager = SchemaManager()
```

## Ingestion Tracker Module

### src/database/ingestion_tracker.py

python

```python
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass
from .connection import db

logger = logging.getLogger(__name__)

@dataclass
class IngestionMetrics:
```

Retry

Claude does not have the ability to run the code it generates yet.

B

Continue

Edit

python

```python
@dataclass
class IngestionMetrics:
    """Data class for ingestion metrics"""
    run_id: str
    pipeline_version: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = "running"
    total_records_processed: int = 0
    customers_loaded: int = 0
    campaigns_loaded: int = 0
    outcomes_loaded: int = 0
    error_message: Optional[str] = None
    processing_duration_seconds: Optional[int] = None
    data_quality_score: Optional[float] = None

class IngestionTracker:
    """Tracks ingestion pipeline metadata and metrics"""
    
    def __init__(self):
        self.current_metrics: Optional[IngestionMetrics] = None
    
    def start_ingestion_run(self, run_id: str, pipeline_version: str) -> IngestionMetrics:
        """Start tracking a new ingestion run"""
        self.current_metrics = IngestionMetrics(
            run_id=run_id,
            pipeline_version=pipeline_version,
            start_time=datetime.now(),
            status="running"
        )
        
        # Insert initial record
        insert_query = """
        INSERT INTO ingestion_log (
            run_id, pipeline_version, start_time, status
        ) VALUES (%s, %s, %s, %s)
        """
        
        try:
            db.execute_query(insert_query, (
                self.current_metrics.run_id,
                self.current_metrics.pipeline_version,
                self.current_metrics.start_time,
                self.current_metrics.status
            ))
            logger.info(f"Started tracking ingestion run: {run_id}")
        except Exception as e:
            logger.error(f"Error starting ingestion tracking: {e}")
            raise
        
        return self.current_metrics
    
    def update_metrics(self, **kwargs) -> None:
        """Update current metrics"""
        if not self.current_metrics:
            raise ValueError("No active ingestion run to update")
        
        for key, value in kwargs.items():
            if hasattr(self.current_metrics, key):
                setattr(self.current_metrics, key, value)
        
        self._update_database_record()
    
    def complete_ingestion_run(self, status: str = "success", error_message: Optional[str] = None) -> None:
        """Complete the current ingestion run"""
        if not self.current_metrics:
            raise ValueError("No active ingestion run to complete")
        
        end_time = datetime.now()
        duration = int((end_time - self.current_metrics.start_time).total_seconds())
        
        self.current_metrics.end_time = end_time
        self.current_metrics.status = status
        self.current_metrics.processing_duration_seconds = duration
        self.current_metrics.error_message = error_message
        
        self._update_database_record()
        
        logger.info(f"Completed ingestion run {self.current_metrics.run_id} "
                   f"with status: {status} in {duration} seconds")
    
    def _update_database_record(self) -> None:
        """Update the database record with current metrics"""
        if not self.current_metrics:
            return
        
        update_query = """
        UPDATE ingestion_log SET
            end_time = %s,
            status = %s,
            total_records_processed = %s,
            customers_loaded = %s,
            campaigns_loaded = %s,
            outcomes_loaded = %s,
            error_message = %s,
            processing_duration_seconds = %s,
            data_quality_score = %s
        WHERE run_id = %s
        """
        
        try:
            db.execute_query(update_query, (
                self.current_metrics.end_time,
                self.current_metrics.status,
                self.current_metrics.total_records_processed,
                self.current_metrics.customers_loaded,
                self.current_metrics.campaigns_loaded,
                self.current_metrics.outcomes_loaded,
                self.current_metrics.error_message,
                self.current_metrics.processing_duration_seconds,
                self.current_metrics.data_quality_score
            ))
        except Exception as e:
            logger.error(f"Error updating ingestion metrics: {e}")
    
    def get_ingestion_history(self, limit: int = 50) -> list:
        """Get recent ingestion history"""
        query = """
        SELECT run_id, pipeline_version, start_time, end_time, status,
               total_records_processed, customers_loaded, campaigns_loaded,
               outcomes_loaded, processing_duration_seconds, data_quality_score
        FROM ingestion_log
        ORDER BY start_time DESC
        LIMIT %s
        """
        
        try:
            with db.get_cursor(dict_cursor=True) as cursor:
                cursor.execute(query, (limit,))
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching ingestion history: {e}")
            return []
    
    def get_ingestion_stats(self) -> Dict[str, Any]:
        """Get overall ingestion statistics"""
        stats_query = """
        SELECT 
            COUNT(*) as total_runs,
            COUNT(CASE WHEN status = 'success' THEN 1 END) as successful_runs,
            COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_runs,
            AVG(CASE WHEN status = 'success' THEN processing_duration_seconds END) as avg_duration,
            SUM(total_records_processed) as total_records_ever_processed,
            MAX(start_time) as last_run_time
        FROM ingestion_log
        """
        
        try:
            result = db.execute_query(stats_query)
            if result:
                row = result[0]
                return {
                    'total_runs': row[0] or 0,
                    'successful_runs': row[1] or 0,
                    'failed_runs': row[2] or 0,
                    'success_rate': (row[1] / row[0] * 100) if row[0] > 0 else 0,
                    'avg_duration_seconds': row[3] or 0,
                    'total_records_processed': row[4] or 0,
                    'last_run_time': row[5]
                }
            return {}
        except Exception as e:
            logger.error(f"Error fetching ingestion stats: {e}")
            return {}

# Global ingestion tracker instance
ingestion_tracker = IngestionTracker()
```

# Data Loading Operations

_PostgreSQL data loading with batch processing and error handling_

### src/database/data_loader.py

python

```python
import pandas as pd
import logging
from typing import Dict, List, Tuple
from .connection import db
from .schema import schema_manager

logger = logging.getLogger(__name__)

class DatabaseLoader:
    """Handles loading data into PostgreSQL tables"""
    
    def __init__(self, batch_size: int = 1000):
        self.batch_size = batch_size
        self.load_stats = {}
    
    def load_customers_data(self, customers_df: pd.DataFrame) -> int:
        """Load customers data into database"""
        logger.info(f"Loading {len(customers_df)} customer records")
        
        # Prepare data for database insertion
        customers_data = []
        for _, row in customers_df.iterrows():
            customers_data.append((
                row['customer_id'],
                row['age'],
                row['job'],
                row['marital'],
                row['education'],
                row['default'],
                row['housing'],
                row['loan'],
                row.get('age_group', None)
            ))
        
        # Insert query
        insert_query = """
        INSERT INTO customers (
            customer_id, age, job, marital, education, 
            default_credit, housing_loan, personal_loan, age_group
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (customer_id) DO UPDATE SET
            age = EXCLUDED.age,
            job = EXCLUDED.job,
            marital = EXCLUDED.marital,
            education = EXCLUDED.education,
            default_credit = EXCLUDED.default_credit,
            housing_loan = EXCLUDED.housing_loan,
            personal_loan = EXCLUDED.personal_loan,
            age_group = EXCLUDED.age_group,
            updated_at = CURRENT_TIMESTAMP
        """
        
        rows_loaded = self._batch_insert(insert_query, customers_data)
        self.load_stats['customers_loaded'] = rows_loaded
        
        logger.info(f"Successfully loaded {rows_loaded} customer records")
        return rows_loaded
    
    def load_campaigns_data(self, campaigns_df: pd.DataFrame) -> int:
        """Load campaigns data into database"""
        logger.info(f"Loading {len(campaigns_df)} campaign records")
        
        # Prepare data for database insertion
        campaigns_data = []
        for _, row in campaigns_df.iterrows():
            campaigns_data.append((
                row['customer_id'],
                row['contact'],
                row['month'],
                row['day_of_week'],
                row['duration'],
                row['campaign'],
                row.get('previous_days', None),
                row.get('previous_contacts', None),
                row.get('previous_outcome', None),
                row.get('employment_variation_rate', None),
                row.get('consumer_price_index', None),
                row.get('consumer_confidence_index', None),
                row.get('euribor_3_month', None),
                row.get('number_employed', None)
            ))
        
        # Insert query (campaigns can have multiple records per customer)
        insert_query = """
        INSERT INTO campaigns (
            customer_id, contact_type, contact_month, contact_day_of_week,
            duration_seconds, campaign_contacts, previous_days, previous_contacts,
            previous_outcome, employment_variation_rate, consumer_price_index,
            consumer_confidence_index, euribor_3_month, number_employed
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        rows_loaded = self._batch_insert(insert_query, campaigns_data)
        self.load_stats['campaigns_loaded'] = rows_loaded
        
        logger.info(f"Successfully loaded {rows_loaded} campaign records")
        return rows_loaded
    
    def load_outcomes_data(self, outcomes_df: pd.DataFrame) -> int:
        """Load outcomes data into database"""
        logger.info(f"Loading {len(outcomes_df)} outcome records")
        
        # Prepare data for database insertion
        outcomes_data = []
        for _, row in outcomes_df.iterrows():
            outcomes_data.append((
                row['customer_id'],
                row['target'],
                row['target_numeric']
            ))
        
        # Insert query
        insert_query = """
        INSERT INTO outcomes (
            customer_id, campaign_result, campaign_result_numeric
        ) VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
        """
        
        rows_loaded = self._batch_insert(insert_query, outcomes_data)
        self.load_stats['outcomes_loaded'] = rows_loaded
        
        logger.info(f"Successfully loaded {rows_loaded} outcome records")
        return rows_loaded
    
    def _batch_insert(self, query: str, data: List[Tuple]) -> int:
        """Insert data in batches for better performance"""
        total_inserted = 0
        
        # Process data in batches
        for i in range(0, len(data), self.batch_size):
            batch = data[i:i + self.batch_size]
            
            try:
                rows_affected = db.execute_many(query, batch)
                total_inserted += rows_affected
                logger.debug(f"Inserted batch {i//self.batch_size + 1}: {rows_affected} rows")
                
            except Exception as e:
                logger.error(f"Error inserting batch {i//self.batch_size + 1}: {e}")
                raise
        
        return total_inserted
    
    def load_all_data(self, customers_df: pd.DataFrame, 
                     campaigns_df: pd.DataFrame, 
                     outcomes_df: pd.DataFrame) -> Dict[str, int]:
        """Load all data tables in the correct order"""
        logger.info("Starting database loading process")
        
        try:
            # Load in dependency order
            customers_loaded = self.load_customers_data(customers_df)
            campaigns_loaded = self.load_campaigns_data(campaigns_df)
            outcomes_loaded = self.load_outcomes_data(outcomes_df)
            
            self.load_stats = {
                'customers_loaded': customers_loaded,
                'campaigns_loaded': campaigns_loaded,
                'outcomes_loaded': outcomes_loaded,
                'total_loaded': customers_loaded + campaigns_loaded + outcomes_loaded
            }
            
            logger.info("Database loading completed successfully")
            return self.load_stats
            
        except Exception as e:
            logger.error(f"Error during database loading: {e}")
            raise
    
    def verify_data_loaded(self) -> Dict[str, int]:
        """Verify data was loaded correctly"""
        verification_results = {}
        
        tables = ['customers', 'campaigns', 'outcomes']
        
        for table in tables:
            try:
                row_count = schema_manager.get_table_row_count(table)
                verification_results[table] = row_count
                logger.info(f"Table {table}: {row_count} rows")
            except Exception as e:
                logger.error(f"Error verifying table {table}: {e}")
                verification_results[table] = -1
        
        return verification_results
    
    def get_load_stats(self) -> Dict[str, int]:
        """Return loading statistics"""
        return self.load_stats

database_loader = DatabaseLoader()
```

# Pipeline Orchestration

_Main pipeline script to coordinate all ETL operations_

## Main Pipeline Runner

### scripts/run_pipeline.py

python

```python
#!/usr/bin/env python3
"""
Bank Marketing Data Pipeline Runner

Orchestrates the complete ETL process:
1. Load raw data
2. Clean and validate
3. Split into normalized tables
4. Load into PostgreSQL
5. Track ingestion metadata
"""

import logging
import sys
import uuid
from datetime import datetime
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent))

from config.base_config import config
from src.ingestion.data_loader import DataLoader
from src.ingestion.data_cleaner import DataCleaner
from src.ingestion.data_splitter import DataSplitter
from src.database.connection import db
from src.database.schema import schema_manager
from src.database.data_loader import database_loader
from src.database.ingestion_tracker import ingestion_tracker
from src.utils.logging_utils import setup_logging

logger = logging.getLogger(__name__)

class PipelineRunner:
    """Main pipeline orchestrator"""
    
    def __init__(self, pipeline_version: str = "1.0.0"):
        self.pipeline_version = pipeline_version
        self.run_id = f"RUN-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{str(uuid.uuid4())[:8]}"
        
        # Initialize components
        self.data_loader = DataLoader()
        self.data_cleaner = DataCleaner()
        self.data_splitter = DataSplitter()
    
    def run_pipeline(self) -> bool:
        """Execute the complete pipeline"""
        logger.info(f"Starting pipeline run: {self.run_id}")
        logger.info(f"Environment: {config.ENV}")
        logger.info(f"Pipeline version: {self.pipeline_version}")
        
        try:
            # Start ingestion tracking
            ingestion_tracker.start_ingestion_run(self.run_id, self.pipeline_version)
            
            # Step 1: Test database connection
            if not self._test_database_connection():
                raise Exception("Database connection failed")
            
            # Step 2: Ensure database schema exists
            self._setup_database_schema()
            
            # Step 3: Load raw data
            raw_df = self._load_raw_data()
            
            # Step 4: Clean data
            cleaned_df = self._clean_data(raw_df)
            
            # Step 5: Split data into tables
            customers_df, campaigns_df, outcomes_df = self._split_data(cleaned_df)
            
            # Step 6: Load data into database
            load_stats = self._load_to_database(customers_df, campaigns_df, outcomes_df)
            
            # Step 7: Verify data loading
            verification_results = self._verify_data_loading()
            
            # Step 8: Calculate data quality score
            quality_score = self._calculate_data_quality_score(cleaned_df)
            
            # Update tracking with final metrics
            ingestion_tracker.update_metrics(
                total_records_processed=len(raw_df),
                customers_loaded=load_stats['customers_loaded'],
                campaigns_loaded=load_stats['campaigns_loaded'],
                outcomes_loaded=load_stats['outcomes_loaded'],
                data_quality_score=quality_score
            )
            
            # Complete successful run
            ingestion_tracker.complete_ingestion_run(status="success")
            
            logger.info(f"Pipeline run {self.run_id} completed successfully")
            logger.info(f"Processed {len(raw_df):,} records")
            logger.info(f"Data quality score: {quality_score:.2f}%")
            
            return True
            
        except Exception as e:
            error_msg = f"Pipeline failed: {str(e)}"
            logger.error(error_msg)
            
            # Complete failed run
            try:
                ingestion_tracker.complete_ingestion_run(
                    status="failed", 
                    error_message=error_msg
                )
            except Exception as tracking_error:
                logger.error(f"Error updating ingestion tracking: {tracking_error}")
            
            return False
    
    def _test_database_connection(self) -> bool:
        """Test database connectivity"""
        logger.info("Testing database connection")
        
        if not db.test_connection():
            logger.error("Database connection test failed")
            return False
        
        logger.info("Database connection successful")
        return True
    
    def _setup_database_schema(self) -> None:
        """Ensure database schema exists"""
        logger.info("Setting up database schema")
        
        try:
            schema_manager.create_all_tables()
            logger.info("Database schema ready")
        except Exception as e:
            logger.error(f"Schema setup failed: {e}")
            raise
    
    def _load_raw_data(self) -> 'pd.DataFrame':
        """Load and validate raw data"""
        logger.info("Loading raw data")
        
        raw_df = self.data_loader.load_raw_data()
        
        if not self.data_loader.validate_raw_data(raw_df):
            raise ValueError("Raw data validation failed")
        
        logger.info(f"Raw data loaded: {len(raw_df):,} rows, {len(raw_df.columns)} columns")
        return raw_df
    
    def _clean_data(self, raw_df: 'pd.DataFrame') -> 'pd.DataFrame':
        """Clean and prepare data"""
        logger.info("Cleaning data")
        
        cleaned_df = self.data_cleaner.clean_data(raw_df)
        cleaning_stats = self.data_cleaner.get_cleaning_stats()
        
        logger.info(f"Data cleaning completed:")
        logger.info(f"  - Original rows: {cleaning_stats['original_rows']:,}")
        logger.info(f"  - Cleaned rows: {cleaning_stats['cleaned_rows']:,}")
        logger.info(f"  - Rows removed: {cleaning_stats['rows_removed']:,} "
                   f"({cleaning_stats['removal_percentage']:.2f}%)")
        
        return cleaned_df
    
    def _split_data(self, cleaned_df: 'pd.DataFrame') -> tuple:
        """Split data into normalized tables"""
        logger.info("Splitting data into normalized tables")
        
        customers_df, campaigns_df, outcomes_df = self.data_splitter.split_data(cleaned_df)
        
        # Save split data to CSV files
        file_paths = self.data_splitter.save_split_data(customers_df, campaigns_df, outcomes_df)
        
        split_stats = self.data_splitter.get_split_stats()
        logger.info(f"Data split completed:")
        logger.info(f"  - Customers: {split_stats['customers_records']:,}")
        logger.info(f"  - Campaigns: {split_stats['campaigns_records']:,}")
        logger.info(f"  - Outcomes: {split_stats['outcomes_records']:,}")
        
        return customers_df, campaigns_df, outcomes_df
    
    def _load_to_database(self, customers_df: 'pd.DataFrame', 
                         campaigns_df: 'pd.DataFrame', 
                         outcomes_df: 'pd.DataFrame') -> dict:
        """Load data into PostgreSQL"""
        logger.info("Loading data into database")
        
        load_stats = database_loader.load_all_data(customers_df, campaigns_df, outcomes_df)
        
        logger.info(f"Database loading completed:")
        logger.info(f"  - Customers loaded: {load_stats['customers_loaded']:,}")
        logger.info(f"  - Campaigns loaded: {load_stats['campaigns_loaded']:,}")
        logger.info(f"  - Outcomes loaded: {load_stats['outcomes_loaded']:,}")
        logger.info(f"  - Total loaded: {load_stats['total_loaded']:,}")
        
        return load_stats
    
    def _verify_data_loading(self) -> dict:
        """Verify data was loaded correctly"""
        logger.info("Verifying data loading")
        
        verification_results = database_loader.verify_data_loaded()
        
        logger.info("Data verification results:")
        for table, count in verification_results.items():
            if count >= 0:
                logger.info(f"  - {table}: {count:,} rows")
            else:
                logger.error(f"  - {table}: Verification failed")
        
        return verification_results
    
    def _calculate_data_quality_score(self, df: 'pd.DataFrame') -> float:
        """Calculate overall data quality score"""
        logger.info("Calculating data quality score")
        
        # Simple data quality metrics
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isnull().sum().sum()
        completeness_score = ((total_cells - missing_cells) / total_cells) * 100
        
        # Age validity check
        valid_ages = ((df['age'] >= 18) & (df['age'] <= 100)).sum()
        age_validity_score = (valid_ages / len(df)) * 100
        
        # Overall score (weighted average)
        overall_score = (completeness_score * 0.6) + (age_validity_score * 0.4)
        
        logger.info(f"Data quality metrics:")
        logger.info(f"  - Completeness: {completeness_score:.2f}%")
        logger.info(f"  - Age validity: {age_validity_score:.2f}%")
        logger.info(f"  - Overall score: {overall_score:.2f}%")
        
        return overall_score

def main():
    """Main entry point"""
    # Setup logging
    setup_logging()
    
    logger.info("="*60)
    logger.info("Bank Marketing Data Pipeline")
    logger.info("="*60)
    
    try:
        # Create and run pipeline
        pipeline = PipelineRunner(pipeline_version="1.0.0")
        success = pipeline.run_pipeline()
        
        if success:
            logger.info("Pipeline completed successfully! ✅")
            sys.exit(0)
        else:
            logger.error("Pipeline failed! ❌")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Utility Modules

### src/utils/logging_utils.py

python

```python
import logging
import logging.handlers
import sys
from pathlib import Path
from config.base_config import config

def setup_logging(log_file: str = None) -> None:
    """Setup logging configuration"""
    
    # Create logs directory
    config.LOG_DIR.mkdir(exist_ok=True)
    
    # Default log file
    if not log_file:
        log_file = config.LOG_DIR / f"pipeline_{config.ENV}.log"
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # Console handler
            logging.StreamHandler(sys.stdout),
            # File handler with rotation
            logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
        ]
    )
    
    # Set specific loggers
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('psycopg2').setLevel(logging.WARNING)
    
    logging.info(f"Logging configured - Level: {config.LOG_LEVEL}, File: {log_file}")
```

# Streamlit Dashboard

_Real-time monitoring dashboard for pipeline status and data quality_

## Main Dashboard Application

### dashboard/streamlit_app.py

python

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent))

from config.base_config import config
from src.database.connection import db
from src.database.schema import schema_manager
from src.database.ingestion_tracker import ingestion_tracker
from dashboard.dashboard_utils import DashboardDataLoader

# Page configuration
st.set_page_config(
    page_title="Bank Marketing Pipeline Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class PipelineDashboard:
    """Main dashboard class"""
    
    def __init__(self):
        self.data_loader = DashboardDataLoader()
    
    def run(self):
        """Main dashboard entry point"""
        st.title("📊 Bank Marketing Data Pipeline Dashboard")
        st.markdown("---")
        
        # Sidebar
        self._render_sidebar()
        
        # Main content
        self._render_main_dashboard()
    
    def _render_sidebar(self):
        """Render sidebar with controls and info"""
        st.sidebar.title("🔧 Pipeline Controls")
        
        # Environment info
        st.sidebar.info(f"Environment: {config.ENV}")
        st.sidebar.info(f"Database: {config.DB_NAME}")
        
        # Refresh controls
        st.sidebar.markdown("### 🔄 Refresh Settings")
        auto_refresh = st.sidebar.checkbox("Auto Refresh", value=True)
        refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 10, 300, 30)
        
        if st.sidebar.button("🔄 Refresh Now"):
            st.rerun()
        
        # Database connection test
        st.sidebar.markdown("### 🔌 Database Status")
        if self._test_connection():
            st.sidebar.success("✅ Connected")
        else:
            st.sidebar.error("❌ Connection Failed")
        
        # Auto refresh logic
        if auto_refresh:
            import time
            time.sleep(refresh_interval)
            st.rerun()
    
    def _test_connection(self) -> bool:
        """Test database connection"""
        try:
            return db.test_connection()
        except Exception:
            return False
    
    def _render_main_dashboard(self):
        """Render main dashboard content"""
        # Load data
        with st.spinner("Loading dashboard data..."):
            dashboard_data = self.data_loader.load_all_data()
        
        if not dashboard_data:
            st.error("Unable to load dashboard data. Please check database connection.")
            return
        
        # Key metrics row
        self._render_key_metrics(dashboard_data)
        
        # Charts and tables
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_ingestion_history(dashboard_data)
            self._render_data_quality_trend(dashboard_data)
        
        with col2:
            self._render_pipeline_performance(dashboard_data)
            self._render_table_statistics(dashboard_data)
        
        # Recent runs table
        self._render_recent_runs(dashboard_data)
    
    def _render_key_metrics(self, dashboard_data):
        """Render key metrics cards"""
        st.markdown("## 📈 Key Metrics")
        
        metrics = dashboard_data.get('metrics', {})
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "Total Records",
                f"{metrics.get('total_records_processed', 0):,}",
                delta=None
            )
        
        with col2:
            success_rate = metrics.get('success_rate', 0)
            st.metric(
                "Success Rate",
                f"{success_rate:.1f}%",
                delta=f"{success_rate - 95:.1f}%" if success_rate < 95 else None
            )
        
        with col3:
            avg_duration = metrics.get('avg_duration_seconds', 0)
            st.metric(
                "Avg Duration",
                f"{avg_duration:.1f}s",
                delta=None
            )
        
        with col4:
            total_customers = dashboard_data.get('table_stats', {}).get('customers', 0)
            st.metric(
                "Total Customers",
                f"{total_customers:,}",
                delta=None
            )
        
        with col5:
            last_run = metrics.get('last_run_time')
            if last_run:
                hours_ago = (datetime.now() - last_run).total_seconds() / 3600
                st.metric(
                    "Last Run",
                    f"{hours_ago:.1f}h ago",
                    delta=None
                )
            else:
                st.metric("Last Run", "Never", delta=None)
    
    def _render_ingestion_history(self, dashboard_data):
        """Render ingestion history chart"""
        st.markdown("### 📊 Ingestion History")
        
        history = dashboard_data.get('ingestion_history', [])
        if not history:
            st.info("No ingestion history available")
            return
        
        df_history = pd.DataFrame(history)
        df_history['start_time'] = pd.to_datetime(df_history['start_time'])
        
        # Success/failure chart
        status_counts = df_history['status'].value_counts()
        
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index
```

Retry

Claude does not have the ability to run the code it generates yet.

B

Continue

Edit

python

````python
            values=status_counts.values,
            names=status_counts.index,
            title="Pipeline Run Status",
            color_discrete_map={
                'success': '#2E8B57',
                'failed': '#DC143C',
                'running': '#FFD700'
            }
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_data_quality_trend(self, dashboard_data):
        """Render data quality trend chart"""
        st.markdown("### 📈 Data Quality Trend")
        
        history = dashboard_data.get('ingestion_history', [])
        if not history:
            st.info("No data quality history available")
            return
        
        df_history = pd.DataFrame(history)
        df_history = df_history.dropna(subset=['data_quality_score'])
        
        if df_history.empty:
            st.info("No data quality scores available")
            return
        
        df_history['start_time'] = pd.to_datetime(df_history['start_time'])
        df_history = df_history.sort_values('start_time').tail(20)
        
        fig = px.line(
            df_history,
            x='start_time',
            y='data_quality_score',
            title='Data Quality Score Over Time',
            markers=True
        )
        
        # Add quality threshold line
        fig.add_hline(
            y=95,
            line_dash="dash",
            line_color="red",
            annotation_text="Quality Threshold (95%)"
        )
        
        fig.update_layout(
            height=300,
            yaxis=dict(range=[80, 100])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_pipeline_performance(self, dashboard_data):
        """Render pipeline performance chart"""
        st.markdown("### ⚡ Pipeline Performance")
        
        history = dashboard_data.get('ingestion_history', [])
        if not history:
            st.info("No performance history available")
            return
        
        df_history = pd.DataFrame(history)
        df_history = df_history.dropna(subset=['processing_duration_seconds'])
        
        if df_history.empty:
            st.info("No performance data available")
            return
        
        df_history['start_time'] = pd.to_datetime(df_history['start_time'])
        df_history = df_history.sort_values('start_time').tail(20)
        
        fig = px.bar(
            df_history,
            x='run_id',
            y='processing_duration_seconds',
            title='Processing Duration by Run',
            color='status',
            color_discrete_map={
                'success': '#2E8B57',
                'failed': '#DC143C'
            }
        )
        
        fig.update_layout(
            height=300,
            xaxis_tickangle=-45
        )
        fig.update_xaxes(showticklabels=False)
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_table_statistics(self, dashboard_data):
        """Render table statistics"""
        st.markdown("### 📋 Table Statistics")
        
        table_stats = dashboard_data.get('table_stats', {})
        
        if not table_stats:
            st.info("No table statistics available")
            return
        
        stats_df = pd.DataFrame([
            {'Table': table.title(), 'Row Count': f"{count:,}"}
            for table, count in table_stats.items()
        ])
        
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        # Table distribution chart
        fig = px.bar(
            x=list(table_stats.keys()),
            y=list(table_stats.values()),
            title="Records by Table",
            labels={'x': 'Table', 'y': 'Row Count'}
        )
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_recent_runs(self, dashboard_data):
        """Render recent runs table"""
        st.markdown("### 🕐 Recent Pipeline Runs")
        
        history = dashboard_data.get('ingestion_history', [])
        if not history:
            st.info("No recent runs available")
            return
        
        df_history = pd.DataFrame(history)
        
        # Format for display
        display_columns = [
            'run_id', 'pipeline_version', 'start_time', 'status',
            'total_records_processed', 'processing_duration_seconds',
            'data_quality_score'
        ]
        
        df_display = df_history[display_columns].copy()
        df_display['start_time'] = pd.to_datetime(df_display['start_time']).dt.strftime('%Y-%m-%d %H:%M:%S')
        df_display = df_display.fillna('-')
        
        # Rename columns for display
        df_display.columns = [
            'Run ID', 'Version', 'Start Time', 'Status',
            'Records Processed', 'Duration (s)', 'Quality Score (%)'
        ]
        
        # Style the dataframe
        def style_status(val):
            if val == 'success':
                return 'background-color: #90EE90'
            elif val == 'failed':
                return 'background-color: #FFB6C1'
            else:
                return 'background-color: #FFFFE0'
        
        styled_df = df_display.style.applymap(style_status, subset=['Status'])
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)

# Dashboard data loader utility
### dashboard/dashboard_utils.py
```python
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import pandas as pd

from src.database.connection import db
from src.database.schema import schema_manager
from src.database.ingestion_tracker import ingestion_tracker

logger = logging.getLogger(__name__)

class DashboardDataLoader:
    """Loads data for dashboard display"""
    
    def load_all_data(self) -> Dict[str, Any]:
        """Load all dashboard data"""
        try:
            return {
                'metrics': self._load_pipeline_metrics(),
                'ingestion_history': self._load_ingestion_history(),
                'table_stats': self._load_table_statistics(),
                'data_quality': self._load_data_quality_metrics(),
                'customer_insights': self._load_customer_insights()
            }
        except Exception as e:
            logger.error(f"Error loading dashboard data: {e}")
            return {}
    
    def _load_pipeline_metrics(self) -> Dict[str, Any]:
        """Load overall pipeline metrics"""
        try:
            return ingestion_tracker.get_ingestion_stats()
        except Exception as e:
            logger.error(f"Error loading pipeline metrics: {e}")
            return {}
    
    def _load_ingestion_history(self, limit: int = 50) -> List[Dict]:
        """Load recent ingestion history"""
        try:
            return ingestion_tracker.get_ingestion_history(limit)
        except Exception as e:
            logger.error(f"Error loading ingestion history: {e}")
            return []
    
    def _load_table_statistics(self) -> Dict[str, int]:
        """Load row counts for all tables"""
        try:
            return {
                'customers': schema_manager.get_table_row_count('customers'),
                'campaigns': schema_manager.get_table_row_count('campaigns'),
                'outcomes': schema_manager.get_table_row_count('outcomes'),
                'ingestion_log': schema_manager.get_table_row_count('ingestion_log')
            }
        except Exception as e:
            logger.error(f"Error loading table statistics: {e}")
            return {}
    
    def _load_data_quality_metrics(self) -> Dict[str, Any]:
        """Load data quality metrics"""
        try:
            quality_query = """
            SELECT 
                AVG(data_quality_score) as avg_quality_score,
                MIN(data_quality_score) as min_quality_score,
                MAX(data_quality_score) as max_quality_score,
                COUNT(CASE WHEN data_quality_score < 95 THEN 1 END) as poor_quality_runs
            FROM ingestion_log
            WHERE data_quality_score IS NOT NULL
            AND start_time >= NOW() - INTERVAL '30 days'
            """
            
            result = db.execute_query(quality_query)
            if result and result[0][0] is not None:
                return {
                    'avg_quality_score': float(result[0][0]),
                    'min_quality_score': float(result[0][1]),
                    'max_quality_score': float(result[0][2]),
                    'poor_quality_runs': int(result[0][3])
                }
            return {}
        except Exception as e:
            logger.error(f"Error loading data quality metrics: {e}")
            return {}
    
    def _load_customer_insights(self) -> Dict[str, Any]:
        """Load customer demographic insights"""
        try:
            # Age distribution
            age_query = """
            SELECT age_group, COUNT(*) as count
            FROM customers
            WHERE age_group IS NOT NULL
            GROUP BY age_group
            ORDER BY age_group
            """
            
            # Job distribution
            job_query = """
            SELECT job, COUNT(*) as count
            FROM customers
            GROUP BY job
            ORDER BY count DESC
            LIMIT 10
            """
            
            # Campaign outcome rates
            outcome_query = """
            SELECT 
                campaign_result,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
            FROM outcomes
            GROUP BY campaign_result
            """
            
            age_results = db.execute_query(age_query)
            job_results = db.execute_query(job_query)
            outcome_results = db.execute_query(outcome_query)
            
            return {
                'age_distribution': age_results or [],
                'job_distribution': job_results or [],
                'outcome_rates': outcome_results or []
            }
        except Exception as e:
            logger.error(f"Error loading customer insights: {e}")
            return {}

def main():
    """Main entry point for Streamlit app"""
    dashboard = PipelineDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
````

# Database Setup Script

_Automated database initialization and schema setup_

### scripts/setup_database.py

python

```python
#!/usr/bin/env python3
"""
Database setup script for Bank Marketing Pipeline

Creates database, tables, and initial configuration
"""

import logging
import sys
import argparse
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent))

from config.base_config import config
from src.database.connection import db
from src.database.schema import schema_manager
from src.utils.logging_utils import setup_logging

logger = logging.getLogger(__name__)

def setup_database(drop_existing: bool = False):
    """Setup database schema"""
    logger.info("Starting database setup")
    
    try:
        # Test connection
        if not db.test_connection():
            raise Exception("Cannot connect to database")
        
        logger.info("Database connection successful")
        
        # Drop existing tables if requested
        if drop_existing:
            logger.warning("Dropping existing tables")
            schema_manager.drop_all_tables()
        
        # Create tables
        logger.info("Creating database schema")
        schema_manager.create_all_tables()
        
        # Verify tables were created
        tables = ['customers', 'campaigns', 'outcomes', 'ingestion_log']
        for table in tables:
            if schema_manager.table_exists(table):
                logger.info(f"✅ Table {table} created successfully")
            else:
                logger.error(f"❌ Table {table} creation failed")
        
        logger.info("Database setup completed successfully")
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        raise

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Setup Bank Marketing Pipeline Database')
    parser.add_argument('--drop', action='store_true', 
                       help='Drop existing tables before creating new ones')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        setup_logging()
    
    logger.info("="*50)
    logger.info("Bank Marketing Database Setup")
    logger.info("="*50)
    logger.info(f"Environment: {config.ENV}")
    logger.info(f"Database: {config.DB_NAME}")
    
    try:
        setup_database(drop_existing=args.drop)
        logger.info("✅ Database setup completed successfully")
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

# Project Best Practices

_Guidelines for maintainable, scalable data engineering_

## Code Quality Standards

### Modular Design Principles

- **Single Responsibility**: Each class and function has one clear purpose
- **Dependency Injection**: Configuration and connections passed as parameters
- **Error Handling**: Comprehensive try/catch with meaningful error messages
- **Logging**: Consistent logging throughout all modules
- **Testing**: Unit tests for all core functionality

### Configuration Management

python

```python
# ✅ Good: Environment-aware configuration
from config.base_config import config
connection_string = config.db_connection_string

# ❌ Bad: Hardcoded values
connection_string = "postgresql://user:pass@localhost/db"
```

### Database Operations

python

```python
# ✅ Good: Context managers for connections
with db.get_connection() as conn:
    # Database operations
    pass

# ❌ Bad: Manual connection management
conn = psycopg2.connect(...)
# Risk of connection leaks
```

### Error Handling Pattern

python

```python
# ✅ Good: Comprehensive error handling
try:
    result = risky_operation()
    logger.info("Operation completed successfully")
    return result
except SpecificException as e:
    logger.error(f"Specific error occurred: {e}")
    # Handle specific case
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

## Scalability Considerations

### Data Volume Growth

- **Batch Processing**: Process data in configurable chunks
- **Connection Pooling**: Use connection pools for high throughput
- **Indexing Strategy**: Proper database indexes for query performance
- **Partitioning**: Consider table partitioning for large datasets

### Pipeline Orchestration

- **Idempotent Operations**: Pipeline can be safely re-run
- **Checkpointing**: Ability to resume from failure points
- **Parallel Processing**: Multiple workers for CPU-intensive tasks
- **Queue Management**: Use message queues for decoupled processing

### Monitoring and Alerting

python

```python
# Built-in monitoring hooks
def monitor_pipeline_step(step_name: str, duration: float, success: bool):
    """Monitor individual pipeline steps"""
    metrics = {
        'step_name': step_name,
        'duration_seconds': duration,
        'success': success,
        'timestamp': datetime.now()
    }
    
    # Send to monitoring system
    send_metrics(metrics)
    
    # Alert on failures
    if not success:
        send_alert(f"Pipeline step {step_name} failed")
```

## Security Best Practices

### Credential Management

- **Environment Variables**: Never commit credentials to code
- **Secret Management**: Use dedicated secret management systems
- **Least Privilege**: Database users with minimal required permissions
- **Connection Encryption**: Always use SSL/TLS for database connections

### Data Privacy

python

```python
# Data anonymization for development/testing
def anonymize_customer_data(df: pd.DataFrame) -> pd.DataFrame:
    """Anonymize customer data for non-production use"""
    if config.ENV != 'production':
        # Hash or mask PII fields
        df['customer_id'] = df['customer_id'].apply(hash)
        # Remove or mask sensitive columns
        df = df.drop(['email', 'phone'], errors='ignore')
    return df
```

# Future Enhancements

_Roadmap for extending the pipeline with advanced capabilities_

## dbt Integration

### Phase 1: dbt Setup

yaml

```yaml
# dbt_project.yml
name: 'bank_marketing'
version: '1.0.0'

model-paths: ["models"]
analysis-paths: ["analysis"]
test-paths: ["tests"]
seed-paths: ["data"]
macro-paths: ["macros"]

models:
  bank_marketing:
    staging:
      materialized: view
    marts:
      materialized: table
```

### Phase 2: Data Modeling

sql

```sql
-- models/staging/stg_customers.sql
SELECT 
    customer_id,
    age,
    job,
    marital,
    education,
    CASE 
        WHEN age BETWEEN 18 AND 30 THEN 'Young Adult'
        WHEN age BETWEEN 31 AND 50 THEN 'Middle Age'
        ELSE 'Senior'
    END as life_stage,
    created_at
FROM {{ ref('customers') }}

-- models/marts/customer_lifetime_value.sql
WITH customer_metrics AS (
    SELECT 
        c.customer_id,
        c.age,
        c.job,
        COUNT(o.outcome_id) as total_interactions,
        SUM(CASE WHEN o.campaign_result = 'yes' THEN 1 ELSE 0 END) as successful_campaigns,
        AVG(camp.duration_seconds) as avg_interaction_duration
    FROM {{ ref('stg_customers') }} c
    LEFT JOIN {{ ref('outcomes') }} o ON c.customer_id = o.customer_id
    LEFT JOIN {{ ref('campaigns') }} camp ON c.customer_id = camp.customer_id
    GROUP BY c.customer_id, c.age, c.job
)
SELECT 
    *,
    CASE 
        WHEN successful_campaigns > 0 THEN 'Converted'
        WHEN total_interactions > 3 THEN 'Engaged'
        ELSE 'Cold'
    END as customer_segment
FROM customer_metrics
```

## Advanced Analytics Features

### Customer Churn Prediction

python

```python
# src/ml/churn_model.py
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

class ChurnPredictor:
    """Customer churn prediction model"""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.feature_columns = [
            'age', 'campaign_contacts', 'previous_contacts',
            'duration_seconds', 'employment_variation_rate'
        ]
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for churn prediction"""
        # Feature engineering
        df['days_since_last_contact'] = (datetime.now() - df['last_contact_date']).dt.days
        df['contact_frequency'] = df['total_contacts'] / df['customer_lifetime_days']
        
        return df[self.feature_columns + ['churn_target']]
    
    def train(self, df: pd.DataFrame):
        """Train churn prediction model"""
        features = df[self.feature_columns]
        target = df['churn_target']
        
        X_train, X_test, y_train, y_test = train_test_split(
            features, target, test_size=0.2, random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))
    
    def predict_churn_probability(self, df: pd.DataFrame) -> pd.Series:
        """Predict churn probability for customers"""
        features = df[self.feature_columns]
        return self.model.predict_proba(features)[:, 1]
```

### Real-time Streaming Integration

python

```python
# src/streaming/kafka_consumer.py
from kafka import KafkaConsumer
import json

class BankingEventConsumer:
    """Process real-time banking events"""
    
    def __init__(self, topic_name: str = 'banking-events'):
        self.consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=['localhost:9092'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
    
    def process_events(self):
        """Process incoming banking events"""
        for message in self.consumer:
            event = message.value
            
            if event['event_type'] == 'customer_interaction':
                self._update_customer_engagement(event)
            elif event['event_type'] == 'campaign_response':
                self._record_campaign_outcome(event)
    
    def _update_customer_engagement(self, event):
        """Update customer engagement metrics in real-time"""
        # Update engagement scores, last interaction time, etc.
        pass
```

## Extended Dashboard Features

### Advanced Visualizations

python

```python
# dashboard/advanced_charts.py
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_customer_journey_funnel():
    """Create customer journey funnel visualization"""
    fig = go.Figure(go.Funnel(
        y=["Initial Contact", "Follow-up", "Proposal", "Conversion"],
        x=[10000, 7500, 3000, 1200],
        textinfo="value+percent initial"
    ))
    
    fig.update_layout(title="Customer Conversion Funnel")
    return fig

def create_cohort_analysis_heatmap(df):
    """Create customer cohort retention heatmap"""
    # Process cohort data
    cohort_data = df.pivot_table(
        index='cohort_month',
        columns='period_number',
        values='retention_rate'
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=cohort_data.values,
        x=cohort_data.columns,
        y=cohort_data.index,
        colorscale='RdYlBu_r'
    ))
    
    fig.update_layout(
        title="Customer Cohort Retention Heatmap",
        xaxis_title="Period",
        yaxis_title="Cohort Month"
    )
    
    return fig
```

### A/B Testing Dashboard

python

```python
def render_ab_testing_results():
    """Render A/B testing results for marketing campaigns"""
    st.markdown("### 🧪 A/B Testing Results")
    
    # Load A/B test data
    ab_test_query = """
    SELECT 
        test_group,
        COUNT(*) as participants,
        SUM(CASE WHEN campaign_result = 'yes' THEN 1 ELSE 0 END) as conversions,
        AVG(CASE WHEN campaign_result = 'yes' THEN 1.0 ELSE 0.0 END) as conversion_rate
    FROM campaigns c
    JOIN outcomes o ON c.customer_id = o.customer_id
    WHERE test_group IS NOT NULL
    GROUP BY test_group
    """
    
    results = db.execute_query(ab_test_query)
    
    if results:
        df_results = pd.DataFrame(results, columns=[
            'Test Group', 'Participants', 'Conversions', 'Conversion Rate'
        ])
        
        # Statistical significance testing
        from scipy.stats import chi2_contingency
        
        # Create contingency table
        contingency = [[row[2], row[1]-row[2]] for row in results]
        chi2, p_value, _, _ = chi2_contingency(contingency)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(df_results)
        
        with col2:
            st.metric("Statistical Significance", 
                     "Significant" if p_value < 0.05 else "Not Significant",
                     f"p-value: {p_value:.4f}")
```

## Production Deployment

### Docker Configuration

dockerfile

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 pipeline && chown -R pipeline:pipeline /app
USER pipeline

# Default command
CMD ["python", "scripts/run_pipeline.py"]
```

### docker-compose.yml

yaml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: bank_marketing
      POSTGRES_USER: pipeline_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  pipeline:
    build: .
    depends_on:
      - postgres
    environment:
      - DB_HOST=postgres
      - DB_NAME=bank_marketing
      - DB_USER=pipeline_user
      - DB_PASSWORD=secure_password
      - ENV=production
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
  
  dashboard:
    build: .
    command: streamlit run dashboard/streamlit_app.py --server.port=8501
    depends_on:
      - postgres
    environment:
      - DB_HOST=postgres
      - DB_NAME=bank_marketing
      - DB_USER=pipeline_user
      - DB_PASSWORD=secure_password
    ports:
      - "8501:8501"

volumes:
  postgres_data:
```

### CI/CD Pipeline

yaml

```yaml
# .github/workflows/pipeline.yml
name: Data Pipeline CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: test_password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to production
      run: |
        # Deploy to cloud infrastructure
        echo "Deploying to production..."
```

This comprehensive portfolio project demonstrates professional data engineering skills including ETL pipeline design, database management, monitoring, configuration management, and scalable architecture patterns. The modular structure supports future enhancements and production deployment while maintaining code quality and operational excellence.

---

_Tags: #DataEngineering #ETL #PostgreSQL #Python #Streamlit #Portfolio #BankMarketing #Pipeline #DataQuality #Monitoring #ConfigurationManagement #BestPractices_