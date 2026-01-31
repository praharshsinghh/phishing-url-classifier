# How to Run the Phishing URL Classifier

Simple step-by-step guide to run your phishing URL classifier.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Generate Dataset (Choose One)

You need a larger dataset than the default 30 URLs for better results.

### Option A: Synthetic Data (Recommended for beginners)
```bash
python generate_dataset.py
# Choose option 1
```
- **Size**: 20,000 URLs (10,000 legitimate + 10,000 phishing)
- **Pros**: Works offline, fast generation (~30 seconds)
- **Cons**: Synthetic patterns only

### Option B: Real-world Kaggle Data (Best results)
```bash
python generate_dataset.py
# Choose option 2
```
- **Size**: 20,000 URLs from real Kaggle datasets
- **Pros**: Real phishing URLs, better performance
- **Cons**: Requires Kaggle API setup (see below)

## Step 3: Train Your Model

```bash
python src/train_model.py
```

The script automatically uses the largest dataset available:
1. `urls_kaggle_20k.csv` (if you chose Kaggle option)
2. `urls_synthetic_20k.csv` (if you chose synthetic option)
3. `urls.csv` (original 30 URLs as fallback)

## Step 4: Test Your Model

### Web Interface (Recommended)
```bash
streamlit run app.py
```
Open `http://localhost:8501` and test URLs.

### Command Line
```bash
python src/predict.py https://www.google.com
python src/predict.py http://suspicious-site.tk/login
```

## Kaggle API Setup (For Option B)

1. Go to [Kaggle Account Settings](https://www.kaggle.com/account)
2. Click "Create New API Token"
3. Download `kaggle.json` file
4. Place it at:
   - **Windows**: `C:\Users\<username>\.kaggle\kaggle.json`
   - **Mac/Linux**: `~/.kaggle/kaggle.json`
5. Set permissions (Mac/Linux): `chmod 600 ~/.kaggle/kaggle.json`

## Compare Performance

See how the larger datasets improve performance:

```bash
python compare_datasets.py
```

## Troubleshooting

**"Model not found" error:**
```bash
python src/train_model.py  # Train the model first
```

**"No dataset found" error:**
```bash
python generate_dataset.py  # Generate a dataset first
```

**"Module not found" error:**
```bash
pip install -r requirements.txt  # Install dependencies
```

**Streamlit port in use:**
```bash
streamlit run app.py --server.port 8502
```

## Quick Commands Summary

```bash
# Complete setup
pip install -r requirements.txt
python generate_dataset.py  # Choose 1 or 2
python src/train_model.py
streamlit run app.py

# Test a URL
python src/predict.py https://example.com
```

## Expected Results

### With 20,000 URL Dataset:
- **Training time**: 1-3 minutes
- **Better generalization**: Works better on new URLs
- **More stable**: Consistent results across runs
- **Realistic performance**: Good for learning ML concepts

### Performance Comparison:
- **30 URLs**: Variable results, good for quick testing
- **20,000 URLs**: More reliable, better real-world performance

Remember: This is an educational project. Real phishing detection requires multiple security layers!