"""
Configuration settings for the Google Play Store ETL pipeline.
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
DB_DIR = DATA_DIR

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Data file paths
APPS_DATA_FILE = "apps_data.csv"
REVIEWS_DATA_FILE = "review_data.csv"

# Database configuration
DATABASE_NAME = "playstore.db"
DATABASE_PATH = DB_DIR / DATABASE_NAME

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Data transformation settings
MISSING_VALUE_STRATEGY = {
    'Rating': 0.0,
    'Price': 0.0
}

# Database schema
APPS_TABLE_COLUMNS = [
    'app_name',
    'category',
    'rating',
    'reviews',
    'size_mb',
    'installs',
    'type',
    'price',
    'content_rating',
    'genres',
    'last_updated',
    'current_version',
    'android_version'
]

REVIEWS_TABLE_COLUMNS = [
    'app_name',
    'translated_review',
    'sentiment',
    'sentiment_polarity',
    'sentiment_subjectivity'
]

# Pipeline configuration
PIPELINE_CONFIG = {
    'data_dir': str(DATA_DIR),
    'db_path': str(DATABASE_PATH),
    'log_level': LOG_LEVEL,
    'apps_file': APPS_DATA_FILE,
    'reviews_file': REVIEWS_DATA_FILE
}
