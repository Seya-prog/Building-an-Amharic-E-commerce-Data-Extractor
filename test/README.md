# Testing Documentation

This directory contains tests for the Amharic E-commerce Data Extractor project. The tests ensure the reliability and correctness of the data pipeline components.

## Test Structure

The test suite is organized into several components:

1. **Data Pipeline Tests** (`test_scripts.py`)
   - Text cleaning and normalization
   - Data preprocessing workflow
   - View count generation
   - Directory structure validation

## Running Tests

To run all tests:

```bash
# From project root
python -m unittest discover test

# Or run specific test file
python -m unittest test/test_scripts.py
```

## Test Data

The tests create a temporary `test/test_data` directory for test fixtures. This directory is automatically cleaned up after tests complete.

## Test Coverage

Current test coverage includes:

- ✅ Amharic text cleaning
- ✅ Data preprocessing pipeline
- ✅ View count generation
- ✅ Project structure validation

Future test coverage should include:

- [ ] NER model evaluation
- [ ] Vendor metrics calculation
- [ ] Integration tests for full pipeline
- [ ] Font handling for Amharic text

## Adding New Tests

When adding new tests:

1. Follow the existing test structure in `test_scripts.py`
2. Add test data to `test/test_data` if needed
3. Update this README with new test coverage
4. Ensure all tests pass before committing

## Test Dependencies

All test dependencies are included in `requirements.txt`. No additional packages are needed. 