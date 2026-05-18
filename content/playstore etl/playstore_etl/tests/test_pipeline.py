"""
Unit tests for the Google Play Store ETL pipeline.
"""

import pytest
import pandas as pd
import tempfile
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from extract import DataExtractor
from transform import DataTransformer
from load import DataLoader


class TestDataExtractor:
    """Test cases for DataExtractor class."""
    
    def test_extractor_initialization(self):
        """Test that DataExtractor initializes correctly."""
        extractor = DataExtractor(data_dir="test_data")
        assert extractor.data_dir == Path("test_data")
    
    def test_extract_csv_file_not_found(self):
        """Test that FileNotFoundError is raised for missing files."""
        extractor = DataExtractor(data_dir="nonexistent_dir")
        
        with pytest.raises(FileNotFoundError):
            extractor.extract_csv("nonexistent.csv")


class TestDataTransformer:
    """Test cases for DataTransformer class."""
    
    def test_transformer_initialization(self):
        """Test that DataTransformer initializes correctly."""
        transformer = DataTransformer()
        assert transformer is not None
    
    def test_clean_size_column(self):
        """Test size column cleaning."""
        transformer = DataTransformer()
        
        # Create sample data
        df = pd.DataFrame({
            'Size': ['10M', '500k', 'Varies with device', '25M']
        })
        
        result = transformer.clean_size_column(df)
        
        # Check conversions
        assert result['Size'].iloc[0] == 10.0
        assert abs(result['Size'].iloc[1] - 0.488) < 0.01  # 500k in MB
        assert pd.isna(result['Size'].iloc[2])
        assert result['Size'].iloc[3] == 25.0
    
    def test_clean_installs_column(self):
        """Test installs column cleaning."""
        transformer = DataTransformer()
        
        df = pd.DataFrame({
            'Installs': ['1,000+', '10,000+', '100,000+']
        })
        
        result = transformer.clean_installs_column(df)
        
        assert result['Installs'].iloc[0] == 1000
        assert result['Installs'].iloc[1] == 10000
        assert result['Installs'].iloc[2] == 100000
    
    def test_clean_price_column(self):
        """Test price column cleaning."""
        transformer = DataTransformer()
        
        df = pd.DataFrame({
            'Price': ['$0', '$4.99', '$9.99', 'Free']
        })
        
        result = transformer.clean_price_column(df)
        
        assert result['Price'].iloc[0] == 0.0
        assert result['Price'].iloc[1] == 4.99
        assert result['Price'].iloc[2] == 9.99
    
    def test_remove_duplicates(self):
        """Test duplicate removal."""
        transformer = DataTransformer()
        
        df = pd.DataFrame({
            'App': ['App1', 'App2', 'App1', 'App3'],
            'Rating': [4.5, 4.0, 4.5, 4.8]
        })
        
        result = transformer.remove_duplicates(df, subset=['App'])
        
        assert len(result) == 3  # One duplicate removed


class TestDataLoader:
    """Test cases for DataLoader class."""
    
    def test_loader_initialization(self):
        """Test that DataLoader initializes correctly."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            loader = DataLoader(db_path=tmp.name)
            assert loader.db_path == Path(tmp.name)
    
    def test_create_tables(self):
        """Test database table creation."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            loader = DataLoader(db_path=tmp.name)
            
            # Should not raise any errors
            loader.create_tables()
            
            # Verify tables exist
            apps_info = loader.get_table_info('apps')
            reviews_info = loader.get_table_info('reviews')
            
            assert apps_info['table_name'] == 'apps'
            assert reviews_info['table_name'] == 'reviews'
            assert len(apps_info['columns']) > 0
            assert len(reviews_info['columns']) > 0


class TestPipelineIntegration:
    """Integration tests for the complete pipeline."""
    
    def test_pipeline_components_integration(self):
        """Test that all pipeline components work together."""
        # This would require sample data files
        # For now, just verify components can be instantiated
        extractor = DataExtractor(data_dir="test_data")
        transformer = DataTransformer()
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            loader = DataLoader(db_path=tmp.name)
        
        assert extractor is not None
        assert transformer is not None
        assert loader is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
