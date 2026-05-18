# Google Play Store ETL Pipeline

A production-grade ETL (Extract, Transform, Load) pipeline for processing Google Play Store app and review data. This pipeline extracts data from CSV files, transforms and cleans it, and loads it into a SQLite database for analysis.

## Features

- **Modular Architecture**: Separated Extract, Transform, and Load components for maintainability
- **Robust Error Handling**: Comprehensive logging and error handling throughout the pipeline
- **Data Quality**: Built-in data validation and cleaning operations
- **Production-Ready**: Logging, metrics, and configuration management
- **Testable**: Unit tests for all major components
- **Type Hints**: Fully typed Python code for better IDE support and code quality

## Project Structure

```
playstore_etl/
├── config/
│   └── config.py              # Configuration settings
├── data/
│   ├── apps_data.csv          # Source: App information (place here)
│   ├── review_data.csv        # Source: Review data (place here)
│   └── playstore.db           # Target: SQLite database (generated)
├── logs/
│   └── pipeline_*.log         # Execution logs (generated)
├── src/
│   ├── __init__.py           # Package initialization
│   ├── extract.py            # Data extraction module
│   ├── transform.py          # Data transformation module
│   ├── load.py               # Data loading module
│   └── pipeline.py           # Main pipeline orchestrator
├── tests/
│   └── test_pipeline.py      # Unit tests
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
└── README.md                # This file
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**

```bash
cd playstore_etl
```

2. **Create a virtual environment** (recommended)

```bash
python -m venv venv
source venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Place your data files**

Put your CSV files in the `data/` directory:
- `data/apps_data.csv` - Google Play Store apps data
- `data/review_data.csv` - User reviews data

### Running the Pipeline

**Option 1: Run the complete pipeline**

```bash
cd src
python pipeline.py
```

**Option 2: Run individual components**

```bash
# Extract data only
python extract.py

# Transform data only
python transform.py

# Load data only
python load.py
```

**Option 3: Use as a Python module**

```python
from src.pipeline import PlayStoreETLPipeline

# Configure pipeline
config = {
    'data_dir': 'data',
    'db_path': 'data/playstore.db',
    'log_level': 'INFO'
}

# Initialize and run
pipeline = PlayStoreETLPipeline(config=config)
metrics = pipeline.run()

print(f"Pipeline completed in {metrics['duration_seconds']} seconds")
```

## Pipeline Components

### 1. Extract (`extract.py`)

Handles data extraction from CSV files.

**Features:**
- CSV file reading with pandas
- File validation
- Column and data type inspection
- Extraction logging and metrics

**Key Classes:**
- `DataExtractor`: Main extraction class

**Example:**
```python
from extract import DataExtractor

extractor = DataExtractor(data_dir='data')
apps_df, reviews_df = extractor.extract_all()
```

### 2. Transform (`transform.py`)

Performs data cleaning and transformation.

**Operations:**
- **Size column**: Converts "10M", "500k" to numeric MB values
- **Installs column**: Removes "+" and "," (e.g., "1,000+" → 1000)
- **Reviews column**: Converts to numeric
- **Price column**: Removes "$" and converts to float
- **Date parsing**: Converts date strings to datetime
- **Duplicate removal**: Removes duplicate apps
- **Missing values**: Handles NaN values with configurable strategies

**Key Classes:**
- `DataTransformer`: Main transformation class

**Example:**
```python
from transform import DataTransformer

transformer = DataTransformer()
apps_clean = transformer.transform_apps_data(apps_df)
reviews_clean = transformer.transform_reviews_data(reviews_df)
```

### 3. Load (`load.py`)

Loads transformed data into SQLite database.

**Features:**
- Automatic table creation with proper schema
- Index creation for query performance
- Data validation after loading
- SQL query execution interface

**Database Schema:**

**apps table:**
- id (PRIMARY KEY)
- app_name (TEXT, UNIQUE)
- category, rating, reviews, size_mb, installs
- type, price, content_rating, genres
- last_updated, current_version, android_version
- created_at (TIMESTAMP)

**reviews table:**
- id (PRIMARY KEY)
- app_name (TEXT)
- translated_review (TEXT)
- sentiment, sentiment_polarity, sentiment_subjectivity
- created_at (TIMESTAMP)

**Key Classes:**
- `DataLoader`: Main loading class

**Example:**
```python
from load import DataLoader

loader = DataLoader(db_path='data/playstore.db')
loader.create_tables()
loader.load_apps_data(apps_df)
loader.load_reviews_data(reviews_df)
```

### 4. Pipeline (`pipeline.py`)

Orchestrates the complete ETL process.

**Features:**
- End-to-end pipeline execution
- Comprehensive logging
- Performance metrics
- Error handling and recovery
- Execution summary

**Key Classes:**
- `PlayStoreETLPipeline`: Main pipeline orchestrator

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_pipeline.py -v
```

## Configuration

Edit `config/config.py` to customize:

```python
# Data file paths
APPS_DATA_FILE = "apps_data.csv"
REVIEWS_DATA_FILE = "review_data.csv"

# Database configuration
DATABASE_NAME = "playstore.db"

# Logging configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Missing value strategy
MISSING_VALUE_STRATEGY = {
    'Rating': 0.0,
    'Price': 0.0
}
```

## Querying the Database

After running the pipeline, query the SQLite database:

```python
from load import DataLoader

loader = DataLoader(db_path='data/playstore.db')

# Get top-rated apps
top_apps = loader.execute_query("""
    SELECT app_name, category, rating, installs
    FROM apps
    WHERE rating > 4.5
    ORDER BY installs DESC
    LIMIT 10
""")

# Get sentiment distribution
sentiment_dist = loader.execute_query("""
    SELECT sentiment, COUNT(*) as count
    FROM reviews
    GROUP BY sentiment
""")

print(top_apps)
print(sentiment_dist)
```

Or use SQLite directly:

```bash
sqlite3 data/playstore.db

# Example queries
SELECT * FROM apps LIMIT 5;
SELECT category, AVG(rating) FROM apps GROUP BY category;
SELECT sentiment, COUNT(*) FROM reviews GROUP BY sentiment;
```

## Pipeline Metrics

The pipeline tracks and logs:

- **Extraction metrics**: Records extracted from each source
- **Transformation metrics**: Records transformed and removed
- **Load metrics**: Records successfully loaded
- **Execution time**: Total pipeline duration
- **Data quality**: Missing values, duplicates removed

Example output:
```
================================================================================
PIPELINE EXECUTION SUMMARY
================================================================================
Start Time:    2025-02-13 10:30:15
End Time:      2025-02-13 10:30:47
Duration:      32.45 seconds
--------------------------------------------------------------------------------
Apps:          10841 extracted → 10840 transformed → 10840 loaded
Reviews:       64295 extracted → 37427 transformed → 37427 loaded
================================================================================
✓ Pipeline completed successfully!
```

## Data Quality Checks

The pipeline includes built-in data quality checks:

1. **Schema Validation**: Ensures expected columns are present
2. **Type Conversion**: Validates data type conversions
3. **Duplicate Detection**: Identifies and removes duplicates
4. **Missing Value Handling**: Reports and handles null values
5. **Load Validation**: Verifies record counts in database

## Troubleshooting

### Common Issues

**Issue: FileNotFoundError**
```
Solution: Ensure CSV files are in the data/ directory
```

**Issue: Import errors**
```
Solution: Run from the src/ directory or ensure PYTHONPATH includes src/
```

**Issue: Database locked**
```
Solution: Close any other connections to the database file
```

**Issue: Memory errors with large datasets**
```
Solution: Process data in chunks or increase available RAM
```

## Best Practices

1. **Always use a virtual environment** to isolate dependencies
2. **Check logs** in `logs/` directory for detailed execution info
3. **Backup your database** before re-running the pipeline with `if_exists='replace'`
4. **Version control your data** or keep backups of source CSV files
5. **Run tests** before deploying to production
6. **Monitor disk space** for large datasets

## Production Deployment

For production use:

1. **Set up proper logging** to a centralized logging system
2. **Add monitoring** for pipeline failures and performance
3. **Schedule pipeline execution** using cron or airflow
4. **Implement data versioning** for tracking changes
5. **Set up alerts** for pipeline failures
6. **Use environment variables** for sensitive configuration
7. **Implement retry logic** for transient failures

Example cron job (daily at 2 AM):
```bash
0 2 * * * cd /path/to/playstore_etl/src && /path/to/venv/bin/python pipeline.py
```

## 📄 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📧 Support

For issues or questions:
- Check the logs in `logs/` directory
- Review the troubleshooting section
- Open an issue on the project repository

## 🎓 Learning Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python Logging](https://docs.python.org/3/library/logging.html)
- [ETL Best Practices](https://en.wikipedia.org/wiki/Extract,_transform,_load)

---

**Built with ❤️ for data engineering excellence**
