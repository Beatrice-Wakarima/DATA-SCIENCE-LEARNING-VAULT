"""
Example usage script for the Google Play Store ETL Pipeline.

This script demonstrates various ways to use the pipeline components.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from extract import DataExtractor
from transform import DataTransformer
from load import DataLoader
from pipeline import PlayStoreETLPipeline, setup_logging


def example_1_complete_pipeline():
    """Example 1: Run the complete pipeline with default configuration."""
    print("=" * 80)
    print("EXAMPLE 1: Complete Pipeline Execution")
    print("=" * 80)
    
    setup_logging(log_dir="../logs", log_level="INFO")
    
    config = {
        'data_dir': '../data',
        'db_path': '../data/playstore.db',
        'log_level': 'INFO'
    }
    
    pipeline = PlayStoreETLPipeline(config=config)
    metrics = pipeline.run()
    
    print(f"\n✓ Pipeline completed in {metrics['duration_seconds']:.2f} seconds")
    print(f"  Apps processed: {metrics['apps_loaded']}")
    print(f"  Reviews processed: {metrics['reviews_loaded']}")


def example_2_step_by_step():
    """Example 2: Run each pipeline step individually."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Step-by-Step Execution")
    print("=" * 80)
    
    # Step 1: Extract
    print("\n[Step 1] Extracting data...")
    extractor = DataExtractor(data_dir='../data')
    apps_df, reviews_df = extractor.extract_all()
    print(f"  Extracted {len(apps_df)} apps and {len(reviews_df)} reviews")
    
    # Step 2: Transform
    print("\n[Step 2] Transforming data...")
    transformer = DataTransformer()
    apps_clean = transformer.transform_apps_data(apps_df)
    reviews_clean = transformer.transform_reviews_data(reviews_df)
    print(f"  Cleaned {len(apps_clean)} apps and {len(reviews_clean)} reviews")
    
    # Step 3: Load
    print("\n[Step 3] Loading data...")
    loader = DataLoader(db_path='../data/playstore.db')
    loader.create_tables()
    apps_loaded = loader.load_apps_data(apps_clean)
    reviews_loaded = loader.load_reviews_data(reviews_clean)
    print(f"  Loaded {apps_loaded} apps and {reviews_loaded} reviews")
    
    # Step 4: Validate
    print("\n[Step 4] Validating...")
    validation = loader.validate_load()
    print(f"  Database contains {validation['apps_count']} apps and {validation['reviews_count']} reviews")


def example_3_custom_queries():
    """Example 3: Query the loaded data."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Custom Database Queries")
    print("=" * 80)
    
    loader = DataLoader(db_path='../data/playstore.db')
    
    # Query 1: Top 10 highest rated apps
    print("\n[Query 1] Top 10 Highest Rated Apps:")
    top_rated = loader.execute_query("""
        SELECT app_name, category, rating, installs
        FROM apps
        WHERE rating > 4.5
        ORDER BY rating DESC, installs DESC
        LIMIT 10
    """)
    print(top_rated.to_string(index=False))
    
    # Query 2: Apps by category
    print("\n[Query 2] Apps Count by Category:")
    category_count = loader.execute_query("""
        SELECT category, COUNT(*) as count, AVG(rating) as avg_rating
        FROM apps
        GROUP BY category
        ORDER BY count DESC
        LIMIT 10
    """)
    print(category_count.to_string(index=False))
    
    # Query 3: Sentiment distribution
    print("\n[Query 3] Sentiment Distribution:")
    sentiment_dist = loader.execute_query("""
        SELECT sentiment, COUNT(*) as count
        FROM reviews
        GROUP BY sentiment
        ORDER BY count DESC
    """)
    print(sentiment_dist.to_string(index=False))
    
    # Query 4: Price distribution
    print("\n[Query 4] Price Distribution:")
    price_dist = loader.execute_query("""
        SELECT 
            CASE 
                WHEN price = 0 THEN 'Free'
                WHEN price < 5 THEN '$0-$5'
                WHEN price < 10 THEN '$5-$10'
                ELSE '$10+'
            END as price_range,
            COUNT(*) as count
        FROM apps
        GROUP BY price_range
        ORDER BY count DESC
    """)
    print(price_dist.to_string(index=False))


def example_4_data_quality_checks():
    """Example 4: Perform data quality checks."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Data Quality Checks")
    print("=" * 80)
    
    loader = DataLoader(db_path='../data/playstore.db')
    
    # Check 1: Missing ratings
    print("\n[Check 1] Apps with Missing Ratings:")
    missing_ratings = loader.execute_query("""
        SELECT COUNT(*) as count
        FROM apps
        WHERE rating IS NULL OR rating = 0
    """)
    print(f"  Apps with missing ratings: {missing_ratings['count'].iloc[0]}")
    
    # Check 2: Data ranges
    print("\n[Check 2] Data Range Statistics:")
    stats = loader.execute_query("""
        SELECT 
            MIN(rating) as min_rating,
            MAX(rating) as max_rating,
            AVG(rating) as avg_rating,
            MIN(price) as min_price,
            MAX(price) as max_price,
            AVG(price) as avg_price
        FROM apps
    """)
    print(stats.to_string(index=False))
    
    # Check 3: Table information
    print("\n[Check 3] Table Information:")
    apps_info = loader.get_table_info('apps')
    print(f"  Apps table: {apps_info['row_count']} rows, {len(apps_info['columns'])} columns")
    
    reviews_info = loader.get_table_info('reviews')
    print(f"  Reviews table: {reviews_info['row_count']} rows, {len(reviews_info['columns'])} columns")


def main():
    """Run all examples."""
    try:
        # Choose which example to run
        print("\nSelect an example to run:")
        print("1. Complete Pipeline Execution")
        print("2. Step-by-Step Execution")
        print("3. Custom Database Queries")
        print("4. Data Quality Checks")
        print("5. Run All Examples")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            example_1_complete_pipeline()
        elif choice == '2':
            example_2_step_by_step()
        elif choice == '3':
            example_3_custom_queries()
        elif choice == '4':
            example_4_data_quality_checks()
        elif choice == '5':
            example_1_complete_pipeline()
            example_2_step_by_step()
            example_3_custom_queries()
            example_4_data_quality_checks()
        else:
            print("Invalid choice. Please run again and select 1-5.")
        
        print("\n" + "=" * 80)
        print("Examples completed successfully!")
        print("=" * 80)
    
    except Exception as e:
        print(f"\n✗ Error running examples: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
