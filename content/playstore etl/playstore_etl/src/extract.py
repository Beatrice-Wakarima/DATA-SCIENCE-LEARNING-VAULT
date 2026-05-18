"""
Data extraction module for Google Play Store ETL pipeline.

This module handles the extraction of data from CSV files containing
app information and user reviews.
"""

import logging
from pathlib import Path
from typing import Tuple
import pandas as pd

# Configure logging
logger = logging.getLogger(__name__)


class DataExtractor:
    """Handles data extraction from various sources."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the DataExtractor.
        
        Args:
            data_dir: Directory containing source data files
        """
        self.data_dir = Path(data_dir)
        logger.info(f"DataExtractor initialized with data directory: {self.data_dir}")
    
    def extract_csv(self, filename: str) -> pd.DataFrame:
        """
        Extract data from a CSV file.
        
        Args:
            filename: Name of the CSV file to extract
            
        Returns:
            DataFrame containing the extracted data
            
        Raises:
            FileNotFoundError: If the specified file doesn't exist
            pd.errors.EmptyDataError: If the CSV file is empty
        """
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            logger.error(f"File not found: {filepath}")
            raise FileNotFoundError(f"Could not find file: {filepath}")
        
        logger.info(f"Extracting data from: {filepath}")
        
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Successfully extracted {len(df)} records from {filename}")
            logger.debug(f"Columns: {list(df.columns)}")
            logger.debug(f"Shape: {df.shape}")
            logger.debug(f"Data types:\n{df.dtypes}")
            return df
        
        except pd.errors.EmptyDataError as e:
            logger.error(f"Empty CSV file: {filepath}")
            raise
        
        except Exception as e:
            logger.error(f"Error extracting data from {filepath}: {str(e)}")
            raise
    
    def extract_apps_data(self) -> pd.DataFrame:
        """
        Extract app data from apps_data.csv.
        
        Returns:
            DataFrame containing app information
        """
        logger.info("Extracting apps data")
        return self.extract_csv("apps_data.csv")
    
    def extract_reviews_data(self) -> pd.DataFrame:
        """
        Extract review data from review_data.csv.
        
        Returns:
            DataFrame containing review information
        """
        logger.info("Extracting reviews data")
        return self.extract_csv("review_data.csv")
    
    def extract_all(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Extract all datasets.
        
        Returns:
            Tuple containing (apps_df, reviews_df)
        """
        logger.info("Starting extraction of all datasets")
        apps_df = self.extract_apps_data()
        reviews_df = self.extract_reviews_data()
        logger.info("Successfully extracted all datasets")
        return apps_df, reviews_df
    
    def validate_extraction(self, df: pd.DataFrame, expected_columns: list) -> bool:
        """
        Validate that extracted data contains expected columns.
        
        Args:
            df: DataFrame to validate
            expected_columns: List of expected column names
            
        Returns:
            True if validation passes, False otherwise
        """
        missing_columns = set(expected_columns) - set(df.columns)
        
        if missing_columns:
            logger.warning(f"Missing expected columns: {missing_columns}")
            return False
        
        logger.info("Extraction validation passed")
        return True


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    extractor = DataExtractor(data_dir="../data")
    
    try:
        apps_df, reviews_df = extractor.extract_all()
        print(f"\nApps data shape: {apps_df.shape}")
        print(f"Reviews data shape: {reviews_df.shape}")
        print(f"\nApps data preview:\n{apps_df.head()}")
        print(f"\nReviews data preview:\n{reviews_df.head()}")
    
    except Exception as e:
        logger.error(f"Extraction failed: {str(e)}")
        raise
