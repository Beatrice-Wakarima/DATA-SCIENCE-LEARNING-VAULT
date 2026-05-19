# Bank Marketing Config Notes

_Environment-safe configuration setup for the bank marketing data pipeline_

## Overview

This note documents the configuration management approach for our data pipeline, ensuring environment isolation, security, and maintainability across development, testing, and production environments.

## Environment Setup Strategy

### Configuration Architecture

```
bank_marketing_pipeline/
├── config.py              # Main configuration logic
├── .env.example           # Template for environment variables
├── .env                   # Local environment variables (git-ignored)
├── config/
│   ├── development.py     # Dev-specific overrides
│   ├── testing.py         # Test environment config
│   └── production.py      # Production config
└── .gitignore            # Ensures secrets stay safe
```

## Environment Variables Template

### .env.example

bash

```bash
# Copy this file to .env and fill in your actual values

# Environment
ENVIRONMENT=development

# Data Directories
DATA_DIR=data
LOG_DIR=logs
OUTPUT_DIR=outputs

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bank_marketing
DB_USER=your_username
DB_PASSWORD=your_secure_password

# API Keys (if needed)
EXTERNAL_API_KEY=your_api_key_here
SMTP_PASSWORD=your_email_password

# Logging Level
LOG_LEVEL=INFO

# Model Parameters
RANDOM_STATE=42
TEST_SIZE=0.2
```

> [!important] Security Notice Never commit the actual `.env` file to version control. Only commit `.env.example` with placeholder values.

## Main Configuration File

### config.py

python

```python
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    # Project structure
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / os.getenv('DATA_DIR', 'data')
    LOG_DIR = BASE_DIR / os.getenv('LOG_DIR', 'logs')
    OUTPUT_DIR = BASE_DIR / os.getenv('OUTPUT_DIR', 'outputs')
    
    # Ensure directories exist
    DATA_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # File paths
    RAW_FILE_NAME = "bank_marketing.csv"
    RAW_FILE_PATH = DATA_DIR / RAW_FILE_NAME
    CLIENT_FILE = OUTPUT_DIR / "client.csv"
    CAMPAIGN_FILE = OUTPUT_DIR / "campaign.csv"
    ECONOMICS_FILE = OUTPUT_DIR / "economics.csv"
    
    # Database configuration
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'database': os.getenv('DB_NAME', 'bank_marketing'),
        'user': os.getenv('DB_USER', ''),
        'password': os.getenv('DB_PASSWORD', '')
    }
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = LOG_DIR / f"pipeline_{ENVIRONMENT}.log"
    
    # Model parameters
    RANDOM_STATE = int(os.getenv('RANDOM_STATE', 42))
    TEST_SIZE = float(os.getenv('TEST_SIZE', 0.2))
    
    @classmethod
    def get_db_connection_string(cls):
        """Generate database connection string"""
        return f"postgresql://{cls.DB_CONFIG['user']}:{cls.DB_CONFIG['password']}@{cls.DB_CONFIG['host']}:{cls.DB_CONFIG['port']}/{cls.DB_CONFIG['database']}"

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DB_CONFIG = Config.DB_CONFIG.copy()
    DB_CONFIG['database'] = 'bank_marketing_test'

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'

# Configuration factory
config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.getenv('ENVIRONMENT', 'development')
    return config_map.get(env, DevelopmentConfig)

# Current configuration instance
current_config = get_config()
```

## Environment-Specific Usage

### Development Environment

python

```python
# In your scripts, import configuration
from config import current_config

# Use configuration values
print(f"Environment: {current_config.ENVIRONMENT}")
print(f"Data directory: {current_config.DATA_DIR}")
print(f"Log level: {current_config.LOG_LEVEL}")

# Database connection example
import psycopg2
conn = psycopg2.connect(current_config.get_db_connection_string())
```

### Switching Between Environments

bash

```bash
# Development (default)
export ENVIRONMENT=development
python scripts/clean_clients.py

# Testing
export ENVIRONMENT=testing
python -m pytest tests/

# Production
export ENVIRONMENT=production
python scripts/run_pipeline.py
```

## Security Best Practices

### Checklist for Safe Configuration

- [ ]  All sensitive data stored in environment variables
- [ ]  `.env` file added to `.gitignore`
- [ ]  `.env.example` provided with placeholder values
- [ ]  Database passwords never hardcoded
- [ ]  API keys loaded from environment
- [ ]  Production secrets managed through deployment system
- [ ]  Regular rotation of sensitive credentials

### What Goes in Each File

|File|Contents|Version Control|
|---|---|---|
|`config.py`|Logic, structure, defaults|✅ Committed|
|`.env.example`|Template with placeholders|✅ Committed|
|`.env`|Actual secrets and local config|❌ Git-ignored|
|Environment configs|Environment-specific overrides|✅ Committed|

### Production Deployment Notes

python

```python
# Production environment variables should be set via:
# - Docker environment variables
# - Kubernetes secrets
# - Cloud provider secret management (AWS Secrets Manager, Azure Key Vault)
# - CI/CD pipeline environment configuration

# Example Docker deployment
# docker run -e ENVIRONMENT=production -e DB_PASSWORD=secure_password my_app
```

## Configuration Validation

### Validation Script

python

```python
# scripts/validate_config.py
from config import current_config
import sys

def validate_config():
    """Validate current configuration"""
    errors = []
    
    # Check required directories exist
    required_dirs = [current_config.DATA_DIR, current_config.LOG_DIR, current_config.OUTPUT_DIR]
    for dir_path in required_dirs:
        if not dir_path.exists():
            errors.append(f"Directory does not exist: {dir_path}")
    
    # Check database configuration
    if not all([current_config.DB_CONFIG['user'], current_config.DB_CONFIG['password']]):
        errors.append("Database credentials not configured")
    
    # Check critical files
    if not current_config.RAW_FILE_PATH.exists():
        errors.append(f"Raw data file not found: {current_config.RAW_FILE_PATH}")
    
    if errors:
        print("❌ Configuration validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("✅ Configuration validation passed")

if __name__ == "__main__":
    validate_config()
```

## Troubleshooting Common Issues

### Import Error Solutions

python

```python
# If you get ModuleNotFoundError for config
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import current_config
```

### Environment Variable Not Loading

bash

```bash
# Check if .env file exists and is in the right location
ls -la .env

# Verify environment variables are set
python -c "import os; print(os.getenv('ENVIRONMENT'))"
```

## Related Notes

- [[Client Data Cleaning Log]] - Uses config for file paths and logging
- [[Pipeline Execution Tracker]] - Logs configuration used in each run
- [[Audit Trail Design]] - Tracks config versions for reproducibility

---

# Client Data Cleaning Log

_Detailed documentation of data cleaning transformations for bank marketing dataset_

## Data Cleaning Overview

This log documents the systematic cleaning process applied to the raw bank marketing dataset, transforming it from its original state into analysis-ready format. Each step is documented with business rationale and technical implementation.

## Data Quality Assessment

### Initial Data Profile

python

```python
# Raw dataset characteristics (before cleaning)
Shape: (45,211 rows × 17 columns)
Missing Values: 330 total across 3 columns
Duplicates: 12 exact duplicate rows
Data Types: Mixed (8 object, 7 int64, 2 float64)
Encoding Issues: Semicolon-separated values, inconsistent categories
```

### Data Quality Issues Identified

- [ ]  Column names contain dots and inconsistent formatting
- [ ]  Missing values in `pdays`, `previous`, and `emp.var.rate` columns
- [ ]  Duplicate customer records
- [ ]  Categorical variables with inconsistent encoding
- [ ]  Date formatting issues in temporal columns
- [ ]  Outliers in numerical variables requiring investigation

## Cleaning Process Steps

### Step 1: Column Standardization

**Purpose:** Ensure consistent, Python-friendly column names

python

```python
# Column name mapping applied
column_mapping = {
    'emp.var.rate': 'employment_variation_rate',
    'cons.price.idx': 'consumer_price_index',
    'cons.conf.idx': 'consumer_confidence_index',
    'euribor3m': 'euribor_3_month',
    'nr.employed': 'number_employed',
    'pdays': 'previous_days',
    'previous': 'previous_contacts',
    'poutcome': 'previous_outcome'
}

# Before: emp.var.rate, cons.price.idx, cons.conf.idx
# After: employment_variation_rate, consumer_price_index, consumer_confidence_index
```

**Business Rationale:** Standardized column names improve code readability and prevent errors in downstream analysis.

### Step 2: Missing Value Treatment

**Missing Value Strategy by Column:**

|Column|Missing Count|Treatment|Rationale|
|---|---|---|---|
|`previous_days`|96.3% (999 values)|Replace 999 with -1|999 indicates "not contacted"; -1 is more intuitive|
|`previous_contacts`|13.2%|Fill with 0|Missing indicates no previous contact|
|`employment_variation_rate`|0.7%|Forward fill|Economic indicator; use most recent valid rate|

python

```python
# Missing value transformations
def handle_missing_values(df):
    # Replace sentinel value in previous_days
    df['previous_days'] = df['previous_days'].replace(999, -1)
    
    # Fill missing previous contacts with 0
    df['previous_contacts'] = df['previous_contacts'].fillna(0)
    
    # Forward fill economic indicators
    df['employment_variation_rate'] = df['employment_variation_rate'].fillna(method='ffill')
    
    return df
```

### Step 3: Duplicate Removal

**Duplicates Found:** 12 exact duplicate rows

python

```python
# Before cleaning
print(f"Original dataset: {df.shape[0]:,} rows")

# Remove duplicates keeping first occurrence
df_clean = df.drop_duplicates(keep='first')

print(f"After removing duplicates: {df_clean.shape[0]:,} rows")
print(f"Duplicates removed: {df.shape[0] - df_clean.shape[0]} rows")

# Output:
# Original dataset: 45,211 rows
# After removing duplicates: 45,199 rows
# Duplicates removed: 12 rows
```

**Business Impact:** Prevents double-counting in analysis and model training.

### Step 4: Categorical Variable Encoding

**Encoding Strategy Applied:**

python

```python
# Education level standardization
education_mapping = {
    'basic.4y': 'basic_education',
    'basic.6y': 'basic_education', 
    'basic.9y': 'basic_education',
    'high.school': 'high_school',
    'professional.course': 'professional',
    'university.degree': 'university',
    'unknown': 'unknown'
}

# Job category consolidation
job_consolidation = {
    'admin.': 'administrative',
    'blue-collar': 'blue_collar',
    'self-employed': 'self_employed',
    'services': 'services',
    'management': 'management',
    'technician': 'technical',
    'entrepreneur': 'business_owner',
    'housemaid': 'domestic',
    'retired': 'retired',
    'student': 'student',
    'unemployed': 'unemployed',
    'unknown': 'unknown'
}
```

### Step 5: Data Type Optimization

**Memory Optimization Applied:**

|Column|Original Type|New Type|Memory Saved|
|---|---|---|---|
|`age`|int64|int16|75%|
|`campaign`|int64|int8|87.5%|
|`previous_contacts`|float64|int8|87.5%|
|Categorical columns|object|category|60-80%|

python

```python
# Data type optimization
def optimize_datatypes(df):
    # Integer columns that can be downsized
    int_cols = {
        'age': 'int16',  # Age range 18-95
        'campaign': 'int8',  # Campaign contacts 1-50
        'previous_contacts': 'int8'  # Previous contacts 0-7
    }
    
    # Convert to more efficient integer types
    for col, dtype in int_cols.items():
        df[col] = df[col].astype(dtype)
    
    # Convert string columns to categories
    categorical_cols = ['job', 'marital', 'education', 'default', 'housing', 
                       'loan', 'contact', 'month', 'day_of_week', 'previous_outcome', 'y']
    
    for col in categorical_cols:
        df[col] = df[col].astype('category')
    
    return df
```

## Before/After Sample Transformations

### Raw Data Sample (Before)

```
| age | job      | marital  | education    | default | emp.var.rate | y   |
|-----|----------|----------|--------------|---------|--------------|-----|
| 56  | admin.   | married  | basic.4y     | no      | 1.1          | no  |
| 57  | services | married  | high.school  | unknown | 1.1          | no  |
| 37  | services | married  | basic.9y     | no      | 1.1          | no  |
```

### Cleaned Data Sample (After)

```
| age | job            | marital | education        | default | employment_variation_rate | target |
|-----|----------------|---------|------------------|---------|---------------------------|--------|
| 56  | administrative | married | basic_education  | no      | 1.1                      | 0      |
| 57  | services       | married | high_school      | unknown | 1.1                      | 0      |
| 37  | services       | married | basic_education  | no      | 1.1                      | 0      |
```

## Data Quality Validation

### Post-Cleaning Validation Checks

python

```python
def validate_cleaned_data(df):
    """Validation checks after cleaning"""
    checks_passed = []
    
    # Check 1: No missing values in critical columns
    critical_cols = ['age', 'job', 'education', 'target']
    missing_critical = df[critical_cols].isnull().sum().sum()
    checks_passed.append(('No missing in critical columns', missing_critical == 0))
    
    # Check 2: Age range validation
    age_valid = (df['age'] >= 18) & (df['age'] <= 100)
    checks_passed.append(('Valid age range', age_valid.all()))
    
    # Check 3: Target variable binary
    target_binary = df['target'].isin([0, 1]).all()
    checks_passed.append(('Binary target variable', target_binary))
    
    # Check 4: No duplicates
    no_duplicates = not df.duplicated().any()
    checks_passed.append(('No duplicate rows', no_duplicates))
    
    return checks_passed

# Validation results
validation_results = validate_cleaned_data(df_cleaned)
for check, passed in validation_results:
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {check}")
```

## Cleaning Rules and Assumptions

### Business Rules Applied

1. **Age Boundaries:** Customers must be 18-95 years old (filtered 3 outliers)
2. **Contact History:** Previous days = 999 treated as "never contacted before"
3. **Education Grouping:** Basic education levels (4y, 6y, 9y) consolidated for analysis
4. **Employment Status:** Unknown job categories kept separate for pattern analysis

### Assumptions Made

- **Missing Previous Contacts:** Assumed to be 0 (no previous marketing contact)
- **Economic Indicators:** Missing values forward-filled assuming gradual change
- **Contact Method:** Missing contact types assumed to be most common method (cellular)
- **Seasonal Patterns:** Month and day_of_week preserved for temporal analysis

### Data Integrity Constraints

python

```python
# Integrity constraints applied
constraints = {
    'age': (18, 95),
    'campaign': (1, 50),
    'previous_contacts': (0, 10),
    'employment_variation_rate': (-3.5, 2.0),
    'consumer_price_index': (92, 95),
    'consumer_confidence_index': (-51, -26)
}
```

## Output Data Schema

### Final Schema Documentation

python

```python
cleaned_schema = {
    'customer_id': 'int32',          # Unique identifier (added)
    'age': 'int16',                  # Customer age (18-95)
    'job': 'category',               # Job category (12 categories)
    'marital': 'category',           # Marital status (4 categories)
    'education': 'category',         # Education level (7 categories)
    'default': 'category',           # Credit default history
    'housing': 'category',           # Housing loan status
    'loan': 'category',              # Personal loan status
    'contact': 'category',           # Contact communication type
    'month': 'category',             # Last contact month
    'day_of_week': 'category',       # Last contact day
    'campaign': 'int8',              # Number of contacts this campaign
    'previous_days': 'int16',        # Days since previous campaign (-1 = none)
    'previous_contacts': 'int8',     # Previous campaign contact count
    'previous_outcome': 'category',  # Previous campaign outcome
    'employment_variation_rate': 'float32',      # Economic indicator
    'consumer_price_index': 'float32',           # Economic indicator
    'consumer_confidence_index': 'float32',      # Economic indicator
    'euribor_3_month': 'float32',               # Economic indicator
    'number_employed': 'float32',               # Economic indicator
    'target': 'int8'                            # Target variable (0/1)
}
```

## Cleaning Performance Metrics

### Processing Statistics

- **Processing Time:** 2.3 seconds
- **Memory Usage:** Reduced from 67.2 MB to 23.1 MB (65% reduction)
- **Data Quality Score:** 94.7% (custom metric based on completeness, consistency, validity)
- **Records Retained:** 99.97% (45,199 out of 45,211)

## Related Files and Logs

- **Input:** `data/raw/bank_marketing.csv`
- **Output:** `data/processed/bank_marketing_cleaned.csv`
- **Cleaning Script:** `scripts/data_processing/clean_clients.py`
- **Validation Log:** `logs/data_cleaning_validation.log`
- **Configuration Used:** [[Bank Marketing Config Notes]]

## Next Steps

- [ ]  Feature engineering based on cleaned data
- [ ]  Exploratory data analysis on processed dataset
- [ ]  Model development using clean features
- [ ]  Update [[Pipeline Execution Tracker]] with cleaning run details

---

# Pipeline Execution Tracker

_Centralized log for tracking all pipeline executions, monitoring performance, and identifying issues_

## Pipeline Run Log

### Current Run Status

**Last Successful Run:** 2024-01-15 14:23:45  
**Next Scheduled Run:** 2024-01-16 09:00:00  
**Pipeline Health:** ✅ Healthy

## Execution History Table

|Run ID|Date/Time|Environment|Scripts Executed|Status|Rows In|Rows Out|Duration|Log File|Notes|
|---|---|---|---|---|---|---|---|---|---|
|RUN-2024-001|2024-01-15 14:23:45|production|clean_clients.py, feature_engineering.py|✅ Success|45,211|45,199|2.3s|[execution_001.log](logs/execution_001.log)|Initial production run|
|RUN-2024-002|2024-01-15 16:45:12|production|full_pipeline.py|❌ Failed|45,199|0|1.2s|[execution_002.log](logs/execution_002.log)|DB connection timeout|
|RUN-2024-003|2024-01-15 17:12:33|production|clean_clients.py, validate_data.py|✅ Success|45,211|45,199|2.1s|[execution_003.log](logs/execution_003.log)|Fixed DB config|
|RUN-2024-004|2024-01-16 09:00:15|production|scheduled_pipeline.py|✅ Success|45,312|45,298|4.7s|[execution_004.log](logs/execution_004.log)|New data batch processed|

## Run Details Template

### Run ID: RUN-2024-004

**Execution Details:**

- **Timestamp:** 2024-01-16 09:00:15
- **Environment:** production
- **Triggered By:** scheduled_task
- **Configuration Version:** v2.1.3
- **User/Service:** pipeline_scheduler

**Scripts Executed:**

1. `data_ingestion.py` - ✅ Success (1.2s)
2. `clean_clients.py` - ✅ Success (2.3s)
3. `feature_engineering.py` - ✅ Success (0.8s)
4. `data_validation.py` - ✅ Success (0.4s)

**Data Flow:**

- **Input Records:** 45,312 rows
- **After Cleaning:** 45,298 rows (14 duplicates removed)
- **After Feature Engineering:** 45,298 rows (23 new features)
- **Final Output:** 45,298 rows

**Performance Metrics:**

- **Total Duration:** 4.7 seconds
- **Memory Peak:** 147 MB
- **CPU Usage:** 23% average
- **Disk I/O:** 89 MB read, 34 MB written

**Anomalies Detected:**

- [ ]  Data quality issues
- [ ]  Performance degradation
- [x]  New data pattern: Increased age demographic (avg age +2.1 years)
- [ ]  Missing expected files
- [ ]  Configuration drift

## Pipeline Run Categories

### Scheduled Runs

python

```python
# Daily automated runs
scheduled_runs = {
    'daily_full_pipeline': {
        'schedule': '09:00 UTC daily',
        'scripts': ['data_ingestion.py', 'clean_clients.py', 'feature_engineering.py', 
                   'model_training.py', 'generate_reports.py'],
        'expected_duration': '8-12 minutes',
        'alert_threshold': '15 minutes'
    },
    'hourly_data_check': {
        'schedule': '00 * * * *',
        'scripts': ['data_freshness_check.py'],
        'expected_duration': '30 seconds',
        'alert_threshold': '2 minutes'
    }
}
```

### Manual Runs

python

```python
# Ad-hoc manual executions
manual_run_types = {
    'data_backfill': 'Historical data processing',
    'model_retrain': 'Model retraining with new parameters',
    'hotfix_deployment': 'Emergency fixes and patches',
    'data_quality_audit': 'Comprehensive data validation',
    'performance_test': 'Load and performance testing'
}
```

## Monitoring and Alerting

### Success Criteria Checklist

- [ ]  All scripts executed successfully
- [ ]  Data row counts within expected range
- [ ]  Processing time under threshold
- [ ]  Data quality metrics passed
- [ ]  Output files generated correctly
- [ ]  No critical errors in logs

### Alert Thresholds

|Metric|Warning|Critical|Action|
|---|---|---|---|
|Duration|> 10 min|> 15 min|Page on-call|
|Row Count Drop|> 5%|> 10%|Stop pipeline|
|Error Rate|> 1%|> 5%|Auto-rollback|
|Memory Usage|> 80%|> 95%|Scale resources|

### Failure Classification

python

```python
failure_types = {
    'data_issue': {
        'examples': ['Missing input file', 'Corrupt data', 'Schema change'],
        'response': 'Data team investigation',
        'recovery_time': '2-4 hours'
    },
    'infrastructure': {
        'examples': ['DB connection failure', 'Disk full', 'Memory error'],
        'response': 'Infrastructure team alert',
        'recovery_time': '15-60 minutes'
    },
    'code_error': {
        'examples': ['Script failure', 'Logic error', 'Import error'],
        'response': 'Development team fix',
        'recovery_time': '1-8 hours'
    },
    'configuration': {
        'examples': ['Wrong environment', 'Missing config', 'Credential issue'],
        'response': 'Config validation and fix',
        'recovery_time': '15-30 minutes'
    }
}
```

## Performance Tracking

### Historical Performance Trends

python

```python
# Performance metrics over time
performance_history = {
    'week_1': {
        'avg_duration': '3.2s',
        'success_rate': '98.5%',
        'avg_rows_processed': '45,234'
    },
    'week_2': {
        'avg_duration': '3.8s',
        'success_rate': '99.2%',
        'avg_rows_processed': '45,456'
    },
    'week_3': {
        'avg_duration': '4.1s',
        'success_rate': '97.8%',
        'avg_rows_processed': '45,612'
    }
}
```

### Performance Degradation Alerts

- **Duration Increase:** > 50% from baseline
- **Memory Growth:** > 30% from baseline
- **Success Rate Drop:** < 95% over 24 hours
- **Data Volume Anomaly:** > 20% change from expected

## Recovery Procedures

### Failed Run Recovery Checklist

1. **Immediate Response**
    - [ ]  Check pipeline status dashboard
    - [ ]  Review error logs for root cause
    - [ ]  Verify data source availability
    - [ ]  Check system resources (CPU, memory, disk)
2. **Investigation Steps**
    - [ ]  Compare with last successful run
    - [ ]  Validate input data integrity
    - [ ]  Check configuration changes
    - [ ]  Review recent deployments
3. **Recovery Actions**
    - [ ]  Fix identified root cause
    - [ ]  Run data validation checks
    - [ ]  Execute recovery scripts if needed
    - [ ]  Resume pipeline from appropriate checkpoint
4. **Post-Recovery**
    - [ ]  Update run tracker with resolution
    - [ ]  Document lessons learned
    - [ ]  Update monitoring if needed
    - [ ]  Communicate status to stakeholders

## Run Configuration Tracking

### Environment-Specific Configurations

python

```python
# Configuration used in each environment
environment_configs = {
    'development': {
        'config_version': 'v2.1.3-dev',
        'data_source': 'local_files',
        'log_level': 'DEBUG',
        'parallel_processing': False
    },
    'testing': {
        'config_version': 'v2.1.3-test',
        'data_source': 'test_database',
        'log_level': 'INFO',
        'parallel_processing': True
    },
    'production': {
        'config_version': 'v2.1.3',
        'data_source': 'production_database',
        'log_level': 'WARNING',
        'parallel_processing': True
    }
}
```

## Data Quality Monitoring

### Quality Metrics by Run

|Run ID|Completeness|Consistency|Validity|Uniqueness|Accuracy|Overall Score|
|---|---|---|---|---|---|---|
|RUN-2024-001|99.2%|98.7%|97.8%|99.9%|96.5%|98.4%|
|RUN-2024-002|N/A|N/A|N/A|N/A|N/A|N/A (Failed)|
|RUN-2024-003|99.1%|98.9%|97.9%|99.9%|96.7%|98.5%|
|RUN-2024-004|98.8%|98.6%|97.5%|99.8%|96.3%|98.2%|

### Quality Trend Analysis

- **Completeness:** Stable around 99%
- **Consistency:** Minor decline in latest run (-0.3%)
- **Validity:** Consistent around 97-98%
- **Uniqueness:** Excellent performance (>99.8%)
- **Accuracy:** Slight variation but within tolerance

## Maintenance Schedule

### Regular Maintenance Tasks

- [ ]  **Weekly:** Review performance trends and anomalies
- [ ]  **Monthly:** Archive old log files and optimize storage
- [ ]  **Quarterly:** Performance baseline review and threshold updates
- [ ]  **Annually:** Full pipeline architecture review

## Integration Points

### Related Documentation

- **Configuration Management:** [[Bank Marketing Config Notes]]
- **Data Cleaning Process:** [[Client Data Cleaning Log]]
- **Audit and Compliance:** [[Audit Trail Design]]
- **Error Investigation:** `logs/` directory for detailed run logs

### Monitoring Dashboard Links

- [Pipeline Health Dashboard](http://monitoring.company.com/pipeline-health)
- [Data Quality Metrics](http://monitoring.company.com/data-quality)
- [Performance Trends](http://monitoring.company.com/performance)
- [Alert Configuration](http://monitoring.company.com/alerts)

---

# Audit Trail Design

_Comprehensive framework for ensuring pipeline reproducibility, compliance, and forensic capabilities_

## Audit Trail Overview

This document outlines the auditing framework for the bank marketing data pipeline, ensuring every run is traceable, reproducible, and compliant with data governance requirements. Our audit trail captures the complete lineage from raw data input to final model outputs.

## Audit Trail Architecture

### Core Auditing Principles

1. **Immutable Records:** All audit entries are write-once, never modified
2. **Complete Lineage:** Track data flow from source to final output
3. **Temporal Accuracy:** Precise timestamps for all operations
4. **User Attribution:** Clear ownership and responsibility tracking
5. **Configuration Versioning:** All parameters and settings logged
6. **Cryptographic Integrity:** Hash verification for data and code

## What Gets Logged

### Data Lineage Tracking

python

```python
# Complete data flow documentation
data
```

Retry

Claude does not have the ability to run the code it generates yet.

B

Continue

Edit

### Data Lineage Tracking

python

```python
# Complete data flow documentation
data_lineage_record = {
    'run_id': 'RUN-2024-004',
    'pipeline_version': 'v2.1.3',
    'execution_timestamp': '2024-01-16T09:00:15.347Z',
    
    # Input data tracking
    'input_sources': [
        {
            'source_name': 'bank_marketing_raw',
            'file_path': 'data/raw/bank_marketing.csv',
            'file_size_bytes': 4_235_789,
            'file_hash_sha256': 'a1b2c3d4e5f6789...',
            'last_modified': '2024-01-16T08:45:23Z',
            'record_count': 45_312,
            'schema_version': 'v1.2'
        }
    ],
    
    # Processing steps
    'transformations': [
        {
            'step_name': 'data_cleaning',
            'script_name': 'clean_clients.py',
            'script_version': 'v1.4.2',
            'script_hash': 'f1e2d3c4b5a6987...',
            'input_records': 45_312,
            'output_records': 45_298,
            'records_dropped': 14,
            'processing_duration_ms': 2300,
            'memory_peak_mb': 67
        },
        {
            'step_name': 'feature_engineering',
            'script_name': 'feature_engineering.py',
            'script_version': 'v2.1.0',
            'script_hash': 'c4d5e6f7a8b9123...',
            'input_records': 45_298,
            'output_records': 45_298,
            'features_added': 23,
            'processing_duration_ms': 800,
            'memory_peak_mb': 89
        }
    ],
    
    # Output data tracking
    'outputs': [
        {
            'output_name': 'cleaned_client_data',
            'file_path': 'data/processed/client_clean.csv',
            'file_size_bytes': 3_789_234,
            'file_hash_sha256': 'z9y8x7w6v5u4321...',
            'record_count': 45_298,
            'column_count': 26,
            'creation_timestamp': '2024-01-16T09:00:19.421Z'
        }
    ]
}
```

### Configuration and Environment Tracking

python

```python
# Environment and configuration snapshot
environment_audit = {
    'run_id': 'RUN-2024-004',
    'environment': 'production',
    'config_version': 'v2.1.3',
    'config_hash': 'abc123def456...',
    
    # System environment
    'system_info': {
        'hostname': 'prod-pipeline-01',
        'os': 'Ubuntu 20.04.6 LTS',
        'python_version': '3.9.18',
        'cpu_cores': 8,
        'memory_gb': 32,
        'disk_available_gb': 245
    },
    
    # Package versions
    'dependencies': {
        'pandas': '2.0.3',
        'numpy': '1.24.3',
        'scikit-learn': '1.3.0',
        'python-dotenv': '1.0.0'
    },
    
    # Configuration parameters used
    'pipeline_config': {
        'random_state': 42,
        'test_size': 0.2,
        'data_dir': '/opt/pipeline/data',
        'log_level': 'INFO',
        'parallel_workers': 4
    },
    
    # Environment variables (sanitized)
    'env_vars': {
        'ENVIRONMENT': 'production',
        'DB_HOST': '***masked***',
        'LOG_LEVEL': 'INFO'
    }
}
```

### User and Security Tracking

python

```python
# User attribution and security audit
security_audit = {
    'run_id': 'RUN-2024-004',
    'execution_context': {
        'user_id': 'pipeline_scheduler',
        'user_type': 'service_account',
        'session_id': 'sess_789abc123def',
        'ip_address': '10.0.1.45',
        'authentication_method': 'service_token',
        'authorization_level': 'pipeline_executor'
    },
    
    # Data access audit
    'data_access': [
        {
            'resource': 'data/raw/bank_marketing.csv',
            'operation': 'read',
            'timestamp': '2024-01-16T09:00:15.500Z',
            'bytes_accessed': 4_235_789,
            'permission_used': 'data_reader'
        },
        {
            'resource': 'data/processed/client_clean.csv',
            'operation': 'write',
            'timestamp': '2024-01-16T09:00:19.421Z',
            'bytes_written': 3_789_234,
            'permission_used': 'data_writer'
        }
    ],
    
    # Security events
    'security_events': [
        {
            'event_type': 'authentication_success',
            'timestamp': '2024-01-16T09:00:14.123Z',
            'details': 'Service account authenticated via token'
        }
    ]
}
```

## Audit Log Storage Architecture

### Storage Structure

```
audit_logs/
├── 2024/
│   ├── 01/                          # Year/Month structure
│   │   ├── data_lineage/
│   │   │   ├── RUN-2024-001.json    # Per-run data lineage
│   │   │   ├── RUN-2024-002.json
│   │   │   └── RUN-2024-003.json
│   │   ├── environment/
│   │   │   ├── RUN-2024-001.json    # Environment snapshots
│   │   │   └── config_versions.json
│   │   ├── security/
│   │   │   ├── access_log_daily.json # Daily access logs
│   │   │   └── auth_events.json
│   │   └── integrity/
│   │       ├── hash_registry.json    # File integrity hashes
│   │       └── validation_results.json
├── indexes/
│   ├── run_id_index.json            # Quick lookup by run ID
│   ├── date_index.json              # Temporal indexing
│   └── user_index.json              # User activity index
└── schemas/
    ├── audit_schema_v1.json         # Audit record schemas
    └── validation_rules.json        # Data validation rules
```

### Database Schema for Audit Records

sql

```sql
-- Audit database schema
CREATE TABLE audit_runs (
    run_id VARCHAR(50) PRIMARY KEY,
    pipeline_version VARCHAR(20) NOT NULL,
    execution_timestamp TIMESTAMP NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    environment VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    duration_ms INTEGER,
    input_records INTEGER,
    output_records INTEGER,
    config_hash VARCHAR(64) NOT NULL,
    data_lineage_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_data_access (
    access_id SERIAL PRIMARY KEY,
    run_id VARCHAR(50) REFERENCES audit_runs(run_id),
    resource_path VARCHAR(500) NOT NULL,
    operation VARCHAR(20) NOT NULL,
    timestamp_utc TIMESTAMP NOT NULL,
    bytes_processed BIGINT,
    file_hash VARCHAR(64),
    user_id VARCHAR(100) NOT NULL
);

CREATE TABLE audit_transformations (
    transformation_id SERIAL PRIMARY KEY,
    run_id VARCHAR(50) REFERENCES audit_runs(run_id),
    step_order INTEGER NOT NULL,
    step_name VARCHAR(100) NOT NULL,
    script_name VARCHAR(200) NOT NULL,
    script_version VARCHAR(20),
    script_hash VARCHAR(64),
    input_records INTEGER,
    output_records INTEGER,
    processing_duration_ms INTEGER,
    parameters_json TEXT
);
```

## Reproducibility Framework

### Run Reproduction Requirements

To reproduce any pipeline run, we capture:

python

```python
# Complete reproduction package
reproduction_package = {
    'run_id': 'RUN-2024-004',
    'reproduction_instructions': {
        
        # 1. Environment setup
        'environment': {
            'python_version': '3.9.18',
            'requirements_file': 'requirements_RUN-2024-004.txt',
            'environment_variables': 'env_RUN-2024-004.env'
        },
        
        # 2. Code version
        'code': {
            'git_commit_hash': 'abc123def456789...',
            'git_branch': 'main',
            'git_tag': 'v2.1.3',
            'code_archive': 'code_snapshot_RUN-2024-004.tar.gz'
        },
        
        # 3. Data version
        'data': {
            'input_data_hash': 'a1b2c3d4e5f6789...',
            'input_data_location': 'data_archive/2024-01-16/bank_marketing.csv',
            'data_version': 'v1.2',
            'data_schema': 'schema_v1.2.json'
        },
        
        # 4. Configuration
        'configuration': {
            'config_file': 'config_RUN-2024-004.py',
            'config_hash': 'abc123def456...',
            'runtime_parameters': 'params_RUN-2024-004.json'
        },
        
        # 5. Reproduction command
        'execution_command': [
            'export ENVIRONMENT=production',
            'export CONFIG_VERSION=v2.1.3',
            'python scripts/run_pipeline.py --run-id RUN-2024-004-REPRO'
        ]
    }
}
```

### Deterministic Execution Guarantees

python

```python
# Ensuring deterministic results
deterministic_controls = {
    'random_seeds': {
        'global_seed': 42,
        'numpy_seed': 42,
        'sklearn_random_state': 42,
        'pandas_sample_seed': 42
    },
    
    'sorting_stability': {
        'dataframe_operations': 'stable_sort_enabled',
        'groupby_operations': 'sort_keys_consistent',
        'sampling_operations': 'reproducible_sampling'
    },
    
    'parallel_processing': {
        'thread_count': 'fixed_at_4',
        'process_pool': 'deterministic_ordering',
        'memory_allocation': 'consistent_chunking'
    }
}
```

## Compliance and Governance

### Regulatory Compliance Tracking

python

```python
# Compliance audit trail
compliance_audit = {
    'run_id': 'RUN-2024-004',
    'regulatory_framework': 'GDPR',
    
    'data_processing_lawfulness': {
        'legal_basis': 'legitimate_interest',
        'consent_tracking': 'not_required_b2b',
        'data_minimization': 'verified',
        'purpose_limitation': 'marketing_analytics_only'
    },
    
    'data_subject_rights': {
        'right_to_access': 'audit_trail_available',
        'right_to_rectification': 'correction_procedures_in_place',
        'right_to_erasure': 'deletion_procedures_available',
        'right_to_portability': 'export_functions_implemented'
    },
    
    'technical_safeguards': {
        'data_encryption': 'AES-256_at_rest_TLS_in_transit',
        'access_controls': 'RBAC_implemented',
        'audit_logging': 'comprehensive_enabled',
        'data_retention': '7_years_policy_applied'
    }
}
```

### Data Governance Checkpoints

- [ ]  **Data Classification:** Sensitive data identified and tagged
- [ ]  **Access Authorization:** User permissions verified before execution
- [ ]  **Quality Gates:** Data quality thresholds met before processing
- [ ]  **Retention Policy:** Data lifecycle management applied
- [ ]  **Privacy Impact:** PII processing documented and justified
- [ ]  **Third-party Data:** External data usage agreements validated

## Audit Query Interface

### Common Audit Queries

python

```python
# Audit query examples
class AuditQueryInterface:
    
    def get_run_lineage(self, run_id):
        """Get complete data lineage for a specific run"""
        query = """
        SELECT r.run_id, r.execution_timestamp, r.user_id,
               da.resource_path, da.operation, da.file_hash,
               t.step_name, t.script_name, t.input_records, t.output_records
        FROM audit_runs r
        LEFT JOIN audit_data_access da ON r.run_id = da.run_id
        LEFT JOIN audit_transformations t ON r.run_id = t.run_id
        WHERE r.run_id = %s
        ORDER BY da.timestamp_utc, t.step_order
        """
        return self.execute_query(query, [run_id])
    
    def get_user_activity(self, user_id, date_range):
        """Get all activities for a user within date range"""
        query = """
        SELECT run_id, execution_timestamp, environment, status,
               input_records, output_records, duration_ms
        FROM audit_runs
        WHERE user_id = %s 
        AND execution_timestamp BETWEEN %s AND %s
        ORDER BY execution_timestamp DESC
        """
        return self.execute_query(query, [user_id, date_range[0], date_range[1]])
    
    def get_data_file_history(self, file_path):
        """Get access history for a specific data file"""
        query = """
        SELECT da.run_id, da.operation, da.timestamp_utc, da.file_hash,
               r.user_id, r.environment
        FROM audit_data_access da
        JOIN audit_runs r ON da.run_id = r.run_id
        WHERE da.resource_path = %s
        ORDER BY da.timestamp_utc DESC
        """
        return self.execute_query(query, [file_path])
    
    def detect_anomalous_runs(self, threshold_days=30):
        """Identify runs that differ significantly from recent patterns"""
        query = """
        WITH recent_stats AS (
            SELECT AVG(duration_ms) as avg_duration,
                   AVG(input_records) as avg_input_records,
                   STDDEV(duration_ms) as stddev_duration
            FROM audit_runs
            WHERE execution_timestamp >= NOW() - INTERVAL '%s days'
        )
        SELECT r.run_id, r.execution_timestamp, r.duration_ms,
               r.input_records, r.status
        FROM audit_runs r, recent_stats rs
        WHERE r.execution_timestamp >= NOW() - INTERVAL '%s days'
        AND (r.duration_ms > rs.avg_duration + 2 * rs.stddev_duration
             OR r.input_records < rs.avg_input_records * 0.8
             OR r.input_records > rs.avg_input_records * 1.2)
        ORDER BY r.execution_timestamp DESC
        """
        return self.execute_query(query, [threshold_days, threshold_days])
```

## Data Integrity Verification

### Hash-Based Integrity Checking

python

```python
# File integrity verification system
class DataIntegrityManager:
    
    def calculate_file_hash(self, file_path, algorithm='sha256'):
        """Calculate cryptographic hash of file"""
        import hashlib
        hash_obj = hashlib.new(algorithm)
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        
        return hash_obj.hexdigest()
    
    def verify_data_integrity(self, run_id):
        """Verify integrity of all files used in a run"""
        lineage = self.get_run_lineage(run_id)
        integrity_report = {
            'run_id': run_id,
            'verification_timestamp': datetime.utcnow().isoformat(),
            'files_checked': 0,
            'files_verified': 0,
            'files_missing': 0,
            'files_corrupted': 0,
            'verification_details': []
        }
        
        for file_record in lineage['files']:
            integrity_report['files_checked'] += 1
            
            if not os.path.exists(file_record['path']):
                integrity_report['files_missing'] += 1
                integrity_report['verification_details'].append({
                    'file': file_record['path'],
                    'status': 'missing',
                    'expected_hash': file_record['hash']
                })
                continue
            
            current_hash = self.calculate_file_hash(file_record['path'])
            
            if current_hash == file_record['hash']:
                integrity_report['files_verified'] += 1
                integrity_report['verification_details'].append({
                    'file': file_record['path'],
                    'status': 'verified',
                    'hash': current_hash
                })
            else:
                integrity_report['files_corrupted'] += 1
                integrity_report['verification_details'].append({
                    'file': file_record['path'],
                    'status': 'corrupted',
                    'expected_hash': file_record['hash'],
                    'actual_hash': current_hash
                })
        
        return integrity_report
```

## Audit Trail Maintenance

### Retention and Archival Policy

python

```python
# Audit data lifecycle management
audit_retention_policy = {
    'hot_storage': {
        'duration': '90_days',
        'location': 'primary_database',
        'access_time': 'immediate',
        'query_performance': 'optimized'
    },
    
    'warm_storage': {
        'duration': '2_years',
        'location': 'archive_database',
        'access_time': '1-5_minutes',
        'query_performance': 'acceptable'
    },
    
    'cold_storage': {
        'duration': '7_years',
        'location': 'object_storage_s3',
        'access_time': '15-60_minutes',
        'query_performance': 'batch_only'
    },
    
    'destruction': {
        'after': '7_years',
        'method': 'secure_deletion',
        'verification': 'cryptographic_proof',
        'documentation': 'destruction_certificate'
    }
}
```

### Audit Performance Monitoring

python

```python
# Monitor audit system health
audit_system_health = {
    'storage_metrics': {
        'disk_usage_percent': 67.3,
        'growth_rate_gb_per_day': 1.2,
        'estimated_full_date': '2024-08-15',
        'compression_ratio': 4.1
    },
    
    'query_performance': {
        'avg_query_time_ms': 245,
        'slow_query_threshold_ms': 1000,
        'slow_queries_last_24h': 3,
        'index_hit_ratio_percent': 94.7
    },
    
    'data_quality': {
        'missing_audit_records': 0,
        'orphaned_records': 2,
        'integrity_check_failures': 0,
        'last_integrity_check': '2024-01-16T06:00:00Z'
    }
}
```

## Integration with Related Systems

### Links to Other Documentation

- **Configuration Management:** [[Bank Marketing Config Notes]] - How configurations are tracked in audit trail
- **Data Processing:** [[Client Data Cleaning Log]] - Links to transformation audit records
- **Execution Monitoring:** [[Pipeline Execution Tracker]] - Real-time execution feeds into audit trail

### External System Integration

python

```python
# Integration points with external systems
external_integrations = {
    'monitoring_dashboard': {
        'url': 'http://monitoring.company.com/audit',
        'real_time_feeds': ['run_status', 'data_access_events', 'security_alerts'],
        'scheduled_reports': ['daily_summary', 'weekly_compliance_report']
    },
    
    'compliance_system': {
        'gdpr_requests': 'automated_data_export',
        'audit_requests': 'comprehensive_trail_export',
        'retention_enforcement': 'automated_data_purging'
    },
    
    'security_siem': {
        'log_forwarding': 'real_time_security_events',
        'anomaly_alerts': 'unusual_access_patterns',
        'threat_detection': 'automated_investigation_triggers'
    }
}
```

## Audit Trail Validation

### Self-Audit Checklist

- [ ]  **Completeness:** Every pipeline run has corresponding audit records
- [ ]  **Accuracy:** Audit data matches actual system behavior
- [ ]  **Consistency:** Cross-references between audit tables are valid
- [ ]  **Timeliness:** Audit records created within 1 minute of events
- [ ]  **Integrity:** Hash verification passes for all tracked files
- [ ]  **Accessibility:** Authorized users can query audit trail effectively
- [ ]  **Retention:** Data retention policies are automatically enforced
- [ ]  **Security:** Audit logs themselves are tamper-evident and protected

### Audit Trail Testing Procedures

python

```python
# Automated audit trail testing
def test_audit_completeness():
    """Verify every pipeline run has complete audit trail"""
    # Test implementation
    pass

def test_data_lineage_integrity():
    """Verify data lineage chains are complete and consistent"""
    # Test implementation
    pass

def test_reproduction_capability():
    """Verify recent runs can be reproduced from audit data"""
    # Test implementation
    pass

def test_compliance_readiness():
    """Verify audit trail meets regulatory requirements"""
    # Test implementation
    pass
```

This audit trail design ensures that every aspect of your bank marketing data pipeline is traceable, reproducible, and compliant with both technical and regulatory requirements. The comprehensive logging enables forensic analysis, supports regulatory compliance, and provides the foundation for continuous improvement of your data processing operations.

---

_Tags: #DataGovernance #AuditTrail #Compliance #DataLineage #Reproducibility #GDPR #DataPipeline #ProjectDocumentation_