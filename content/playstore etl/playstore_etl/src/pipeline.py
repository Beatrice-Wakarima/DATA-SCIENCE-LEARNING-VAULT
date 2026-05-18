"""
Main ETL pipeline orchestrator for Google Play Store data.

This module coordinates the Extract, Transform, and Load operations
to create a complete data pipeline.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from extract import DataExtractor
from transform import DataTransformer
from load import DataLoader


class PlayStoreETLPipeline:
    """Orchestrates the complete ETL pipeline."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the ETL pipeline.
        
        Args:
            config: Configuration dictionary with pipeline settings
        """
        # Default configuration
        self.config = {
            'data_dir': 'data',
            'db_path': 'data/playstore.db',
            'log_level': 'INFO'
        }
        
        # Update with provided config
        if config:
            self.config.update(config)
        
        # Initialize components
        self.extractor = DataExtractor(data_dir=self.config['data_dir'])
        self.transformer = DataTransformer()
        self.loader = DataLoader(db_path=self.config['db_path'])
        
        # Pipeline metrics
        self.metrics = {
            'start_time': None,
            'end_time': None,
            'duration_seconds': None,
            'apps_extracted': 0,
            'reviews_extracted': 0,
            'apps_transformed': 0,
            'reviews_transformed': 0,
            'apps_loaded': 0,
            'reviews_loaded': 0,
            'errors': []
        }
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("PlayStoreETLPipeline initialized")
    
    def run(self) -> Dict[str, Any]:
        """
        Execute the complete ETL pipeline.
        
        Returns:
            Dictionary containing pipeline execution metrics
        """
        self.metrics['start_time'] = datetime.now()
        self.logger.info("=" * 80)
        self.logger.info("Starting ETL Pipeline Execution")
        self.logger.info("=" * 80)
        
        try:
            # EXTRACT
            self.logger.info("\n[STEP 1/3] EXTRACTING DATA")
            self.logger.info("-" * 80)
            apps_df, reviews_df = self._extract_data()
            
            # TRANSFORM
            self.logger.info("\n[STEP 2/3] TRANSFORMING DATA")
            self.logger.info("-" * 80)
            apps_transformed, reviews_transformed = self._transform_data(apps_df, reviews_df)
            
            # LOAD
            self.logger.info("\n[STEP 3/3] LOADING DATA")
            self.logger.info("-" * 80)
            self._load_data(apps_transformed, reviews_transformed)
            
            # VALIDATE
            self.logger.info("\n[VALIDATION] VALIDATING LOAD")
            self.logger.info("-" * 80)
            validation_results = self._validate()
            
            # Calculate metrics
            self.metrics['end_time'] = datetime.now()
            self.metrics['duration_seconds'] = (
                self.metrics['end_time'] - self.metrics['start_time']
            ).total_seconds()
            
            # Log summary
            self._log_summary()
            
            return self.metrics
        
        except Exception as e:
            self.logger.error(f"Pipeline execution failed: {str(e)}")
            self.metrics['errors'].append(str(e))
            raise
    
    def _extract_data(self):
        """Extract data from source files."""
        try:
            apps_df, reviews_df = self.extractor.extract_all()
            
            self.metrics['apps_extracted'] = len(apps_df)
            self.metrics['reviews_extracted'] = len(reviews_df)
            
            self.logger.info(f"✓ Extracted {len(apps_df)} apps and {len(reviews_df)} reviews")
            return apps_df, reviews_df
        
        except Exception as e:
            self.logger.error(f"✗ Extraction failed: {str(e)}")
            raise
    
    def _transform_data(self, apps_df, reviews_df):
        """Transform and clean the data."""
        try:
            apps_transformed = self.transformer.transform_apps_data(apps_df)
            reviews_transformed = self.transformer.transform_reviews_data(reviews_df)
            
            self.metrics['apps_transformed'] = len(apps_transformed)
            self.metrics['reviews_transformed'] = len(reviews_transformed)
            
            apps_removed = len(apps_df) - len(apps_transformed)
            reviews_removed = len(reviews_df) - len(reviews_transformed)
            
            self.logger.info(f"✓ Transformed {len(apps_transformed)} apps ({apps_removed} removed)")
            self.logger.info(f"✓ Transformed {len(reviews_transformed)} reviews ({reviews_removed} removed)")
            
            return apps_transformed, reviews_transformed
        
        except Exception as e:
            self.logger.error(f"✗ Transformation failed: {str(e)}")
            raise
    
    def _load_data(self, apps_df, reviews_df):
        """Load data into the database."""
        try:
            # Create tables
            self.loader.create_tables()
            self.logger.info("✓ Database tables created/verified")
            
            # Load apps
            apps_loaded = self.loader.load_apps_data(apps_df)
            self.metrics['apps_loaded'] = apps_loaded
            self.logger.info(f"✓ Loaded {apps_loaded} apps into database")
            
            # Load reviews
            reviews_loaded = self.loader.load_reviews_data(reviews_df)
            self.metrics['reviews_loaded'] = reviews_loaded
            self.logger.info(f"✓ Loaded {reviews_loaded} reviews into database")
        
        except Exception as e:
            self.logger.error(f"✗ Loading failed: {str(e)}")
            raise
    
    def _validate(self):
        """Validate the loaded data."""
        try:
            validation_results = self.loader.validate_load()
            
            self.logger.info(f"✓ Validation complete")
            self.logger.info(f"  - Apps in database: {validation_results['apps_count']}")
            self.logger.info(f"  - Reviews in database: {validation_results['reviews_count']}")
            
            return validation_results
        
        except Exception as e:
            self.logger.error(f"✗ Validation failed: {str(e)}")
            raise
    
    def _log_summary(self):
        """Log pipeline execution summary."""
        self.logger.info("\n" + "=" * 80)
        self.logger.info("PIPELINE EXECUTION SUMMARY")
        self.logger.info("=" * 80)
        self.logger.info(f"Start Time:    {self.metrics['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"End Time:      {self.metrics['end_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"Duration:      {self.metrics['duration_seconds']:.2f} seconds")
        self.logger.info("-" * 80)
        self.logger.info(f"Apps:          {self.metrics['apps_extracted']} extracted → "
                        f"{self.metrics['apps_transformed']} transformed → "
                        f"{self.metrics['apps_loaded']} loaded")
        self.logger.info(f"Reviews:       {self.metrics['reviews_extracted']} extracted → "
                        f"{self.metrics['reviews_transformed']} transformed → "
                        f"{self.metrics['reviews_loaded']} loaded")
        self.logger.info("=" * 80)
        
        if not self.metrics['errors']:
            self.logger.info("✓ Pipeline completed successfully!")
        else:
            self.logger.warning(f"⚠ Pipeline completed with {len(self.metrics['errors'])} errors")


def setup_logging(log_dir: str = "logs", log_level: str = "INFO"):
    """
    Configure logging for the pipeline.
    
    Args:
        log_dir: Directory to store log files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Create logs directory
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Create log filename with timestamp
    log_filename = log_path / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured. Log file: {log_filename}")


def main():
    """Main entry point for the pipeline."""
    # Setup logging
    setup_logging(log_dir="../logs", log_level="INFO")
    
    # Pipeline configuration
    config = {
        'data_dir': '../data',
        'db_path': '../data/playstore.db',
        'log_level': 'INFO'
    }
    
    # Initialize and run pipeline
    pipeline = PlayStoreETLPipeline(config=config)
    
    try:
        metrics = pipeline.run()
        sys.exit(0)  # Success
    
    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        sys.exit(1)  # Failure


if __name__ == "__main__":
    main()
