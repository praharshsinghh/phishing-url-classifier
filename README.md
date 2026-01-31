# 🔒 Phishing URL Classifier

A machine learning project that detects phishing URLs using interpretable features and classical ML algorithms. Built with Python, scikit-learn, and Streamlit.

## 📋 What This Project Does

This project provides a phishing detection system that:
- Analyzes URLs to identify potential phishing attempts
- Uses interpretable features (URL length, special characters, domain patterns, etc.)
- Trains and compares multiple ML models (Logistic Regression, Decision Tree, Random Forest)
- Provides both a web interface (Streamlit) and command-line interface for predictions
- Works reasonably well on common phishing patterns

## 🎯 Features

- **Feature Extraction**: 14 interpretable features including:
  - URL structure analysis (length, special characters)
  - Domain characteristics (dots in hostname, IP addresses)
  - Security indicators (HTTPS usage)
  - Suspicious patterns (URL shorteners, suspicious TLDs)

- **Multiple ML Models**: Trains and evaluates:
  - Logistic Regression
  - Decision Tree
  - Random Forest
  - Automatically selects the best performing model

- **Web Interface**: User-friendly Streamlit app with:
  - Real-time URL analysis
  - Confidence scores and probability breakdown
  - Visual indicators for phishing/legitimate classification

- **CLI Tool**: Command-line interface for quick predictions

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or download this project

2. Navigate to the project directory:
```bash
cd phishing-url-classifier
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 📊 Training the Model

Before using the classifier, you need to train the model:

```bash
python src/train_model.py
```

This will:
- Load the dataset (automatically detects the largest available dataset)
- Extract features from each URL
- Train three different ML models
- Evaluate and compare their performance
- Save the best model to `models/phishing_model.joblib`

### Available Datasets

The system will automatically use the largest dataset available:

1. **`urls_mega_kaggle.csv`** - Large dataset from Kaggle (if generated)
2. **`urls_comprehensive.csv`** - Real + synthetic data (if generated)  
3. **`urls_expanded.csv`** - Synthetic expanded data (if generated)
4. **`urls.csv`** - Original small dataset (30 URLs)

### Expanding Your Dataset

To improve model performance, you can generate larger datasets:

```bash
python generate_dataset.py
```

Choose from:
- **Synthetic data**: Generated phishing patterns (works offline)
- **Real + synthetic**: Downloads real phishing URLs from public sources
- **Kaggle datasets**: Large-scale real-world datasets (requires Kaggle API setup)

**Expected Output:**
```
Loading data from data/urls.csv...
Dataset loaded: 30 samples
Class distribution:
1    15
0    15

Extracting features from URLs...
Splitting data (80% train, 20% test)...
Training samples: 24
Testing samples: 6

Training Logistic Regression...
Training Decision Tree...
Training Random Forest...

BEST MODEL: Random Forest (F1 Score: 1.0000)
Model saved successfully!
```

## 🌐 Running the Web App

Launch the Streamlit web interface:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

**How to use:**
1. Enter a URL in the text input field
2. Click "Analyze URL"
3. View the prediction, confidence score, and probability breakdown


## 💻 Using the CLI

For quick predictions from the command line:

```bash
python src/predict.py <URL>
```

**Examples:**

```bash
# Check a legitimate URL
python src/predict.py https://www.google.com

# Check a suspicious URL
python src/predict.py http://192.168.1.1/login.php
```

**Sample Output:**
```
Analyzing URL: https://www.google.com
------------------------------------------------------------

Prediction: Legitimate
Confidence: 95.23%

Probabilities:
  Legitimate: 95.23%
  Phishing:   4.77%

✓ This URL appears to be legitimate.
```

## 📁 Project Structure

```
phishing-url-classifier/
│
├─ data/
│   ├─ urls.csv                    # Original small dataset (30 URLs)
│   ├─ urls_expanded.csv           # Synthetic expanded dataset (optional)
│   ├─ urls_comprehensive.csv      # Real + synthetic dataset (optional)
│   └─ urls_mega_kaggle.csv        # Large Kaggle dataset (optional)
│
├─ models/
│   └─ phishing_model.joblib       # Trained model (created after training)
│
├─ src/
│   ├─ features.py                 # Feature extraction utilities
│   ├─ train_model.py              # Model training script
│   ├─ predict.py                  # Prediction functions + CLI
│   ├─ data_generator.py           # Synthetic data generation
│   ├─ real_data_integrator.py     # Real phishing data integration
│   ├─ kaggle_data_integrator.py   # Kaggle dataset integration
│   └─ __init__.py
│
├─ app.py                          # Streamlit web application
├─ generate_dataset.py             # Dataset generation interface
├─ compare_datasets.py             # Performance comparison tool
├─ requirements.txt                # Python dependencies
└─ README.md                       # This file
```

## 🧠 How It Works (ML Approach)

### 1. Feature Engineering

The classifier extracts 14 interpretable features from each URL:

**Structural Features:**
- URL length
- Count of special characters (dots, hyphens, underscores, slashes, etc.)

**Domain Features:**
- Number of dots in hostname
- Presence of IP address instead of domain name
- HTTPS usage

**Suspicious Indicators:**
- Suspicious top-level domains (.tk, .xyz, .ml, etc.)
- URL shortener services (bit.ly, tinyurl.com, etc.)

### 2. Model Training

Three classical ML algorithms are trained and compared:

- **Logistic Regression**: Fast, interpretable linear model
- **Decision Tree**: Non-linear, rule-based classifier
- **Random Forest**: Ensemble method combining multiple decision trees

The model with the highest F1 score is automatically selected and saved.

### 3. Prediction

For a new URL:
1. Extract the 14 features
2. Pass features to the trained model
3. Get prediction (Phishing/Legitimate) with confidence score

### Why This Approach?

- **Interpretable**: Features are human-understandable
- **Fast**: No deep learning, runs on any machine
- **Effective**: Simple patterns catch most phishing attempts
- **Educational**: Great for learning ML fundamentals

## 📈 Dataset Format

The training data (`data/urls.csv`) should have two columns:

```csv
url,label
https://www.google.com,legitimate
http://phishing-site.tk/login,phishing
```

**Label formats supported:**
- Integers: `0` (legitimate), `1` (phishing)
- Strings: `"legitimate"`, `"benign"`, `"safe"` → 0
- Strings: `"phishing"`, `"malicious"` → 1


## 🔧 Customization

### Adding More Training Data

The easiest way to improve your model is to use larger datasets:

```bash
python generate_dataset.py
```

This will help you create datasets with thousands of URLs instead of just 30.

You can also manually add URLs to `data/urls.csv`:
1. Add URLs and labels to the CSV file
2. Re-run the training script:
```bash
python src/train_model.py
```

### Modifying Features

Edit `src/features.py` to add or modify feature extraction functions. Remember to update the `extract_features_from_url()` function to include new features.

### Tuning Model Parameters

Edit `src/train_model.py` to adjust hyperparameters:
```python
models = {
    'Random Forest': RandomForestClassifier(
        n_estimators=200,  # Increase trees
        max_depth=15,      # Adjust depth
        random_state=42
    )
}
```

## 🎓 For Hackathon Judges

This project demonstrates:

1. **Complete ML Pipeline**: Data loading → Feature engineering → Training → Evaluation → Deployment
2. **Best Practices**: 
   - Train/test split for unbiased evaluation
   - Model comparison and selection
   - Proper error handling and validation
3. **User Experience**: Both web UI and CLI for different use cases
4. **Interpretability**: Features are explainable, not black-box
5. **Practical Application**: Addresses real cybersecurity problem

**Technical Skills Showcased:**
- Python programming
- Machine learning (scikit-learn)
- Web development (Streamlit)
- Data processing (pandas, numpy)
- Software engineering (modular code, documentation)

## ⚠️ Limitations & Disclaimer

- This is an educational project for learning ML concepts
- The model works on common phishing patterns but won't catch all sophisticated attacks
- Larger datasets improve performance, but no model is 100% accurate
- Always verify suspicious URLs through multiple sources
- Not intended for production security systems without additional validation


## 🐛 Troubleshooting

**Model not found error:**
```
Error: Model not found at models/phishing_model.joblib
```
Solution: Run `python src/train_model.py` first to train the model.

**Import errors:**
```
ModuleNotFoundError: No module named 'sklearn'
```
Solution: Install dependencies with `pip install -r requirements.txt`

**Streamlit not opening:**
Solution: Check if port 8501 is available, or specify a different port:
```bash
streamlit run app.py --server.port 8502
```
## 🔮 Future Work

- Expand the dataset with more real-world phishing URLs
- Add more sophisticated features like domain age and SSL certificate analysis
- Experiment with different ML algorithms and hyperparameter tuning
- Improve the web interface with better visualizations
- Add API endpoints for integration with other tools

## 📚 Learning Resources

- [scikit-learn Documentation](https://scikit-learn.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Phishing Detection Research](https://scholar.google.com/scholar?q=phishing+url+detection)

## 🤝 Contributing

Feel free to:
- Add more features to improve accuracy
- Expand the dataset
- Improve the UI/UX
- Add more model types
- Enhance documentation

## 📝 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Built as a machine learning project for educational purposes. 

---

**Happy Learning! 🔒**

Remember: This is a learning project. Real phishing detection is complex and requires multiple layers of security.

# phishing-url-classifier
A machine learning project that identifies phishing URLs using pattern analysis and provides an easy-to-use web and CLI interface. 
