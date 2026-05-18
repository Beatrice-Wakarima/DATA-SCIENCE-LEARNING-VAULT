"""
Data loading module for Google Play Store ETL pipeline.

This module handles loading transformed data into a SQLite database,
including table creation, data insertion, and validation.
"""

import logging
import sqlite3
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd

# Configure logging
logger = logging.getLogger(__name__)


class DataLoader:
    """Handles loading data into SQLite database."""
    
    def __init__(self, db_path: str = "data/playstore.db"):
        """
        Initialize the DataLoader.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"DataLoader initialized with database: {self.db_path}")
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Create and return a database connection.
        
        Returns:
            SQLite connection object
        """
        try:
            conn = sqlite3.connect(self.db_path)
            logger.debug("Database connection established")
            return conn
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise
    
    def create_tables(self) -> None:
        """Create database tables if they don't exist."""
        logger.info("Creating database tables")
        
        apps_table_sql = """
        CREATE TABLE IF NOT EXISTS apps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT NOT NULL,
            category TEXT,
            rating REAL,
            reviews INTEGER,
            size_mb REAL,
            installs INTEGER,
            type TEXT,
            price REAL,
            content_rating TEXT,
            genres TEXT,
            last_updated TEXT,
            current_version TEXT,
            android_version TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(app_name)
        );
        """
        
        reviews_table_sql = """
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT NOT NULL,
            translated_review TEXT,
            sentiment TEXT,
            sentiment_polarity REAL,
            sentiment_subjectivity REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        # Create indexes for better query performance
        apps_index_sql = """
        CREATE INDEX IF NOT EXISTS idx_apps_category ON apps(category);
        CREATE INDEX IF NOT EXISTS idx_apps_rating ON apps(rating);
        CREATE INDEX IF NOT EXISTS idx_apps_installs ON apps(installs);
        """
        
        reviews_index_sql = """
        CREATE INDEX IF NOT EXISTS idx_reviews_app ON reviews(app_name);
        CREATE INDEX IF NOT EXISTS idx_reviews_sentiment ON reviews(sentiment);
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create tables
                cursor.execute(apps_table_sql)
                cursor.execute(reviews_table_sql)
                
                # Create indexes
                for index_sql in apps_index_sql.split(';'):
                    if index_sql.strip():
                        cursor.execute(index_sql)
                
                for index_sql in reviews_index_sql.split(';'):
                    if index_sql.strip():
                        cursor.execute(index_sql)
                
                conn.commit()
                logger.info("Database tables and indexes created successfully")
        
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {str(e)}")
            raise
    
    def load_apps_data(self, df: pd.DataFrame, if_exists: str = 'replace') -> int:
        """
        Load apps data into the database.
        
        Args:
            df: DataFrame containing apps data
            if_exists: How to behave if table exists ('fail', 'replace', 'append')
            
        Returns:
            Number of records loaded
        """
        logger.info(f"Loading {len(df)} app records into database")
        
        # Rename columns to match database schema
        column_mapping = {
            'App': 'app_name',
            'Category': 'category',
            'Rating': 'rating',
            'Reviews': 'reviews',
            'Size': 'size_mb',
            'Installs': 'installs',
            'Type': 'type',
            'Price': 'price',
            'Content Rating': 'content_rating',
            'Genres': 'genres',
            'Last Updated': 'last_updated',
            'Current Ver': 'current_version',
            'Android Ver': 'android_version'
        }
        
        df_to_load = df.rename(columns=column_mapping)
        
        # Select only columns that exist in the database schema
        columns_to_load = [col for col in column_mapping.values() if col in df_to_load.columns]
        df_to_load = df_to_load[columns_to_load]
        
        try:
            with self.get_connection() as conn:
                df_to_load.to_sql('apps', conn, if_exists=if_exists, index=False)
                records_loaded = len(df_to_load)
                logger.info(f"Successfully loaded {records_loaded} app records")
                return records_loaded
        
        except sqlite3.Error as e:
            logger.error(f"Error loading apps data: {str(e)}")
            raise
    
    def load_reviews_data(self, df: pd.DataFrame, if_exists: str = 'replace') -> int:
        """
        Load reviews data into the database.
        
        Args:
            df: DataFrame containing reviews data
            if_exists: How to behave if table exists ('fail', 'replace', 'append')
            
        Returns:
            Number of records loaded
        """
        logger.info(f"Loading {len(df)} review records into database")
        
        # Rename columns to match database schema
        column_mapping = {
            'App': 'app_name',
            'Translated_Review': 'translated_review',
            'Sentiment': 'sentiment',
            'Sentiment_Polarity': 'sentiment_polarity',
            'Sentiment_Subjectivity': 'sentiment_subjectivity'
        }
        
        df_to_load = df.rename(columns=column_mapping)
        
        # Select only columns that exist in the database schema
        columns_to_load = [col for col in column_mapping.values() if col in df_to_load.columns]
        df_to_load = df_to_load[columns_to_load]
        
        try:
            with self.get_connection() as conn:
                df_to_load.to_sql('reviews', conn, if_exists=if_exists, index=False)
                records_loaded = len(df_to_load)
                logger.info(f"Successfully loaded {records_loaded} review records")
                return records_loaded
        
        except sqlite3.Error as e:
            logger.error(f"Error loading reviews data: {str(e)}")
            raise
    
    def validate_load(self) -> Dict[str, Any]:
        """
        Validate data load by checking record counts and data quality.
        
        Returns:
            Dictionary containing validation results
        """
        logger.info("Validating data load")
        
        validation_results = {
            'apps_count': 0,
            'reviews_count': 0,
            'apps_sample': [],
            'reviews_sample': []
        }
        
        try:
            with self.get_connection() as conn:
                # Count records in apps table
                apps_count = pd.read_sql_query("SELECT COUNT(*) as count FROM apps", conn)
                validation_results['apps_count'] = apps_count['count'].iloc[0]
                
                # Count records in reviews table
                reviews_count = pd.read_sql_query("SELECT COUNT(*) as count FROM reviews", conn)
                validation_results['reviews_count'] = reviews_count['count'].iloc[0]
                
                # Get sample records
                apps_sample = pd.read_sql_query("SELECT * FROM apps LIMIT 5", conn)
                validation_results['apps_sample'] = apps_sample.to_dict('records')
                
                reviews_sample = pd.read_sql_query("SELECT * FROM reviews LIMIT 5", conn)
                validation_results['reviews_sample'] = reviews_sample.to_dict('records')
                
                logger.info(f"Validation complete - Apps: {validation_results['apps_count']}, Reviews: {validation_results['reviews_count']}")
        
        except sqlite3.Error as e:
            logger.error(f"Error during validation: {str(e)}")
            raise
        
        return validation_results
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query and return results as DataFrame.
        
        Args:
            query: SQL query to execute
            
        Returns:
            DataFrame containing query results
        """
        logger.info(f"Executing query: {query[:100]}...")
        
        try:
            with self.get_connection() as conn:
                df = pd.read_sql_query(query, conn)
                logger.info(f"Query returned {len(df)} records")
                return df
        
        except sqlite3.Error as e:
            logger.error(f"Error executing query: {str(e)}")
            raise
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        Get information about a database table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary containing table information
        """
        try:
            with self.get_connection() as conn:
                # Get table schema
                schema = pd.read_sql_query(f"PRAGMA table_info({table_name})", conn)
                
                # Get row count
                count = pd.read_sql_query(f"SELECT COUNT(*) as count FROM {table_name}", conn)
                
                info = {
                    'table_name': table_name,
                    'columns': schema.to_dict('records'),
                    'row_count': count['count'].iloc[0]
                }
                
                return info
        
        except sqlite3.Error as e:
            logger.error(f"Error getting table info: {str(e)}")
            raise


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    from extract import DataExtractor
    from transform import DataTransformer
    
    loader = DataLoader(db_path="../data/playstore.db")
    
    try:
        # Create tables
        loader.create_tables()
        
        # Extract and transform data
        extractor = DataExtractor(data_dir="../data")
        transformer = DataTransformer()
        
        apps_df, reviews_df = extractor.extract_all()
        apps_transformed = transformer.transform_apps_data(apps_df)
        reviews_transformed = transformer.transform_reviews_data(reviews_df)
        
        # Load data
        apps_loaded = loader.load_apps_data(apps_transformed)
        reviews_loaded = loader.load_reviews_data(reviews_transformed)
        
        print(f"\nData loaded successfully!")
        print(f"Apps loaded: {apps_loaded}")
        print(f"Reviews loaded: {reviews_loaded}")
        
        # Validate
        validation = loader.validate_load()
        print(f"\nValidation Results:")
        print(f"Apps in database: {validation['apps_count']}")
        print(f"Reviews in database: {validation['reviews_count']}")
    
    except Exception as e:
        logger.error(f"Load failed: {str(e)}")
        raise
