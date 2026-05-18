"""
Data transformation module for Google Play Store ETL pipeline.

This module handles data cleaning, transformation, and preparation
for loading into the target database.
"""

import logging
import re
from typing import Dict, Any
import pandas as pd
import numpy as np

# Configure logging
logger = logging.getLogger(__name__)


class DataTransformer:
    """Handles data transformation and cleaning operations."""
    
    def __init__(self):
        """Initialize the DataTransformer."""
        logger.info("DataTransformer initialized")
    
    def clean_size_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and convert the Size column to numeric (MB).
        
        Args:
            df: DataFrame containing Size column
            
        Returns:
            DataFrame with cleaned Size column
        """
        logger.info("Cleaning Size column")
        df = df.copy()
        
        def convert_size(size_str):
            """Convert size string to numeric MB value."""
            if pd.isna(size_str) or size_str == 'Varies with device':
                return np.nan
            
            # Remove 'M' or 'k' and convert
            if 'M' in size_str:
                return float(size_str.replace('M', ''))
            elif 'k' in size_str:
                return float(size_str.replace('k', '')) / 1024
            else:
                return np.nan
        
        df['Size'] = df['Size'].apply(convert_size)
        logger.debug(f"Size column converted. Non-null values: {df['Size'].notna().sum()}")
        return df
    
    def clean_installs_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and convert the Installs column to numeric.
        
        Args:
            df: DataFrame containing Installs column
            
        Returns:
            DataFrame with cleaned Installs column
        """
        logger.info("Cleaning Installs column")
        df = df.copy()
        
        # Remove '+' and ',' characters and convert to integer
        df['Installs'] = df['Installs'].str.replace('+', '', regex=False)
        df['Installs'] = df['Installs'].str.replace(',', '', regex=False)
        df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')
        
        logger.debug(f"Installs column converted. Non-null values: {df['Installs'].notna().sum()}")
        return df
    
    def clean_reviews_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert Reviews column to numeric.
        
        Args:
            df: DataFrame containing Reviews column
            
        Returns:
            DataFrame with cleaned Reviews column
        """
        logger.info("Cleaning Reviews column")
        df = df.copy()
        
        df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
        logger.debug(f"Reviews column converted. Non-null values: {df['Reviews'].notna().sum()}")
        return df
    
    def clean_price_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and convert the Price column to numeric.
        
        Args:
            df: DataFrame containing Price column
            
        Returns:
            DataFrame with cleaned Price column
        """
        logger.info("Cleaning Price column")
        df = df.copy()
        
        # Remove '$' symbol and convert to float
        df['Price'] = df['Price'].str.replace('$', '', regex=False)
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        
        logger.debug(f"Price column converted. Non-null values: {df['Price'].notna().sum()}")
        return df
    
    def parse_date_column(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """
        Parse date column to datetime format.
        
        Args:
            df: DataFrame containing date column
            column: Name of the column to parse
            
        Returns:
            DataFrame with parsed date column
        """
        logger.info(f"Parsing date column: {column}")
        df = df.copy()
        
        df[column] = pd.to_datetime(df[column], errors='coerce')
        logger.debug(f"{column} column converted. Non-null values: {df[column].notna().sum()}")
        return df
    
    def remove_duplicates(self, df: pd.DataFrame, subset: list = None) -> pd.DataFrame:
        """
        Remove duplicate rows from DataFrame.
        
        Args:
            df: DataFrame to deduplicate
            subset: Columns to consider for identifying duplicates
            
        Returns:
            DataFrame with duplicates removed
        """
        initial_count = len(df)
        df = df.drop_duplicates(subset=subset, keep='first')
        removed_count = initial_count - len(df)
        
        logger.info(f"Removed {removed_count} duplicate rows")
        return df
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Handle missing values in DataFrame.
        
        Args:
            df: DataFrame with missing values
            strategy: Dictionary mapping column names to fill strategies
                     (e.g., {'Rating': 0, 'Price': 0})
            
        Returns:
            DataFrame with missing values handled
        """
        logger.info("Handling missing values")
        df = df.copy()
        
        if strategy:
            for column, fill_value in strategy.items():
                if column in df.columns:
                    missing_before = df[column].isna().sum()
                    df[column] = df[column].fillna(fill_value)
                    logger.debug(f"Filled {missing_before} missing values in {column} with {fill_value}")
        
        return df
    
    def transform_apps_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply all transformations to apps data.
        
        Args:
            df: Raw apps DataFrame
            
        Returns:
            Transformed apps DataFrame
        """
        logger.info("Starting apps data transformation")
        
        # Apply transformations in sequence
        df = self.clean_reviews_column(df)
        df = self.clean_size_column(df)
        df = self.clean_installs_column(df)
        df = self.clean_price_column(df)
        df = self.parse_date_column(df, 'Last Updated')
        df = self.remove_duplicates(df, subset=['App'])
        
        # Handle missing values with sensible defaults
        missing_strategy = {
            'Rating': 0.0,
            'Price': 0.0
        }
        df = self.handle_missing_values(df, missing_strategy)
        
        logger.info("Apps data transformation complete")
        logger.info(f"Final shape: {df.shape}")
        
        return df
    
    def transform_reviews_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply all transformations to reviews data.
        
        Args:
            df: Raw reviews DataFrame
            
        Returns:
            Transformed reviews DataFrame
        """
        logger.info("Starting reviews data transformation")
        
        # Remove duplicates
        df = self.remove_duplicates(df)
        
        # Drop rows with missing sentiment values
        initial_count = len(df)
        df = df.dropna(subset=['Sentiment', 'Sentiment_Polarity'])
        dropped_count = initial_count - len(df)
        logger.info(f"Dropped {dropped_count} rows with missing sentiment data")
        
        logger.info("Reviews data transformation complete")
        logger.info(f"Final shape: {df.shape}")
        
        return df
    
    def create_summary_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate summary statistics for transformed data.
        
        Args:
            df: Transformed DataFrame
            
        Returns:
            Dictionary containing summary statistics
        """
        stats = {
            'total_records': len(df),
            'total_columns': len(df.columns),
            'missing_values': df.isna().sum().to_dict(),
            'numeric_summary': df.describe().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {}
        }
        
        logger.info(f"Generated summary statistics for {len(df)} records")
        return stats


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    from extract import DataExtractor
    
    extractor = DataExtractor(data_dir="../data")
    transformer = DataTransformer()
    
    try:
        # Extract data
        apps_df, reviews_df = extractor.extract_all()
        
        # Transform data
        apps_transformed = transformer.transform_apps_data(apps_df)
        reviews_transformed = transformer.transform_reviews_data(reviews_df)
        
        print(f"\nTransformed Apps data shape: {apps_transformed.shape}")
        print(f"Transformed Reviews data shape: {reviews_transformed.shape}")
        
        # Generate statistics
        apps_stats = transformer.create_summary_statistics(apps_transformed)
        print(f"\nApps Statistics:")
        print(f"Total Records: {apps_stats['total_records']}")
        print(f"Total Columns: {apps_stats['total_columns']}")
    
    except Exception as e:
        logger.error(f"Transformation failed: {str(e)}")
        raise
