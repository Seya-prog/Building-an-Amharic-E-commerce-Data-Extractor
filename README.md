# EthioMart – Amharic E-commerce Data Extractor

A comprehensive data pipeline for extracting and analyzing Amharic e-commerce data from Telegram channels, with Named Entity Recognition (NER) capabilities and vendor analytics.

## 🎯 Project Overview

This project provides tools to:
1. Collect and preprocess Amharic e-commerce data from Telegram
2. Extract structured information using NER (products, prices, locations)
3. Analyze vendor performance and calculate lending scores
4. Visualize results with proper Amharic text rendering

## 📁 Project Structure

```
.
├── data/                  # Data storage
│   ├── ner/              # NER annotation files
│   ├── preprocessed/     # Cleaned data
│   └── raw/             # Raw scraped data
├── Models/               # Trained NER models
├── notebooks/           # Analysis notebooks
├── scripts/            # Core pipeline scripts
├── test/              # Unit tests
└── requirements.txt   # Dependencies
```

## 🚀 Getting Started

1. **Setup Environment**:
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

2. **Configure Telegram API**:
```bash
# Windows
set TG_API_ID=your_api_id
set TG_API_HASH=your_api_hash

# Linux/Mac
export TG_API_ID=your_api_id
export TG_API_HASH=your_api_hash
```

3. **Run Data Pipeline**:
```bash
# 1. Collect and preprocess data
python scripts/telegram_ingest_preprocess.py

# 2. Add view counts
python scripts/fetch_telegram_views.py
```

4. **Run Tests**:
```bash
python -m unittest discover test
```

## 📊 Features

### 1. Data Collection
- Automated Telegram channel scraping
- Amharic text normalization
- Media file downloading
- View count tracking

### 2. Named Entity Recognition
- Fine-tuned XLM-RoBERTa model
- Entities: Products, Prices, Locations
- Model interpretability with SHAP/LIME
- Performance metrics:
  | Model | F1 Score |
  |-------|----------|
  | XLM-RoBERTa-base | 0.75 |
  | Afro-XLM-R-base | 0.53 |
  | BERT-tiny-Amharic | 0.14 |

### 3. Vendor Analytics
- Posting frequency analysis
- Engagement metrics (views)
- Price extraction
- Lending score calculation

### 4. Visualization
- Proper Amharic font rendering
- Interactive notebooks
- Performance dashboards
- Vendor comparisons

## 📝 Documentation

- [Scripts Documentation](scripts/README.md)
- [Testing Documentation](test/README.md)
- [Notebook Guides](notebooks/README.md)

## 🧪 Testing

The project includes comprehensive tests for:
- Data pipeline components
- Text preprocessing
- Directory structure
- View count generation

Run tests with:
   ```bash
python -m unittest discover test
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update relevant documentation
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 