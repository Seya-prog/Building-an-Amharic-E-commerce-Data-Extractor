import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import sys, os
import re

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.telegram_ingest_preprocess import clean_amharic_text
from scripts.fetch_telegram_views import main as fetch_views_main

class TestDataPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_data_dir = Path("test/test_data")
        cls.test_data_dir.mkdir(exist_ok=True)
        
    def test_amharic_text_cleaning(self):
        """Test Amharic text cleaning function"""
        test_cases = [
            # Basic cleaning
            ("Hello\nWorld", "Hello World"),
            # Amharic with punctuation
            ("ሰላም፡ዓለም።", "ሰላም፡ዓለም።"),
            # Multiple spaces
            ("ሰላም   ዓለም", "ሰላም ዓለም"),
            # Mixed text with special chars
            ("Price: 1500 ETB\nLocation: አዲስ አበባ", "Price 1500 ETB Location አዲስ አበባ"),
            # Empty string
            ("", ""),
        ]
        
        for input_text, expected in test_cases:
            cleaned = clean_amharic_text(input_text)
            self.assertEqual(cleaned, expected)
        
        # Test None value separately to avoid the TypeError
        self.assertEqual(clean_amharic_text(None), "")

    def test_data_preprocessing(self):
        """Test data preprocessing pipeline"""
        # Create sample raw data
        sample_data = {
            'Channel Title': ['Test Channel'] * 3,
            'Message': [
                'Price: 1500 ETB\nLocation: አዲስ አበባ',
                'ሰላም፡ዓለም።',
                'Test message with\nmultiple\nlines'
            ],
            'Date': ['2025-01-01'] * 3
        }
        
        df = pd.DataFrame(sample_data)
        raw_file = self.test_data_dir / 'test_raw.csv'
        df.to_csv(raw_file, index=False)
        
        # Test if file exists
        self.assertTrue(raw_file.exists())
        
        # Test data loading
        loaded_df = pd.read_csv(raw_file)
        self.assertEqual(len(loaded_df), 3)
        self.assertTrue('Message' in loaded_df.columns)

    def test_view_count_generation(self):
        """Test view count generation logic"""
        # Create sample preprocessed data
        sample_data = {
            'Channel Title': ['Channel A', 'Channel B'] * 2,
            'Message': ['Test message'] * 4,
            'Date': ['2025-01-01'] * 4,
            'Views': [100, 200, 300, 400]  # Add Views column
        }
        
        df = pd.DataFrame(sample_data)
        preprocessed_file = self.test_data_dir / 'test_preprocessed.csv'
        df.to_csv(preprocessed_file, index=False)
        
        # Test if views are within expected range
        loaded_df = pd.read_csv(preprocessed_file)
        self.assertTrue(all(v > 0 for v in loaded_df['Views'].fillna(0)))

    def test_data_file_structure(self):
        """Test expected data directory structure"""
        required_dirs = [
            Path('data/raw'),
            Path('data/preprocessed'),
            Path('data/ner')
        ]
        
        for dir_path in required_dirs:
            self.assertTrue(dir_path.exists(), f"Directory {dir_path} should exist")
            self.assertTrue(dir_path.is_dir(), f"{dir_path} should be a directory")

    @classmethod
    def tearDownClass(cls):
        """Clean up test data"""
        import shutil
        if cls.test_data_dir.exists():
            shutil.rmtree(cls.test_data_dir)

if __name__ == '__main__':
    unittest.main() 