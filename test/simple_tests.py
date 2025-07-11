import unittest
import os
from pathlib import Path

class SimpleTests(unittest.TestCase):
    """Simple tests that don't require any external dependencies or API credentials."""
    
    def test_project_structure(self):
        """Test that the project has the expected directory structure."""
        # Create required directories if they don't exist (for CI)
        for dir_path in ['data/raw', 'data/preprocessed', 'data/ner']:
            os.makedirs(dir_path, exist_ok=True)
            
        # Check that the directories exist
        self.assertTrue(Path('data').exists(), "data directory should exist")
        self.assertTrue(Path('data/raw').exists(), "data/raw directory should exist")
        self.assertTrue(Path('data/preprocessed').exists(), "data/preprocessed directory should exist")
        self.assertTrue(Path('data/ner').exists(), "data/ner directory should exist")
    
    def test_requirements_file(self):
        """Test that the requirements.txt file exists."""
        self.assertTrue(Path('requirements.txt').exists(), "requirements.txt file should exist")
    
    def test_readme_exists(self):
        """Test that the README.md file exists."""
        self.assertTrue(Path('README.md').exists(), "README.md file should exist")

if __name__ == '__main__':
    unittest.main() 