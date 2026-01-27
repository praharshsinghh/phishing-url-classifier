# 📖 Usage Examples

Comprehensive examples for using the Phishing URL Classifier.

## 🎯 Basic Usage

### 1. Training the Model

```bash
python src/train_model.py
```

**What happens:**
- Loads `data/urls.csv`
- Extracts features from each URL
- Trains 3 ML models
- Compares performance
- Saves best model to `models/phishing_model.joblib`

**Expected output:**
```
Loading data from data/urls.csv...
Dataset loaded: 30 samples
Class distribution:
1    15
0    15

Extracting features from URLs...
Splitting data (80% train, 20% test)...

Training Logistic Regression...
Training Decision Tree...
Training Random Forest...

BEST MODEL: Random Forest (F1 Score: 1.0000)
Model saved successfully!
```

### 2. Web Interface

```bash
streamlit run app.py
```

**Features:**
- Paste any URL
- Get instant prediction
- See confidence scores
- Visual probability breakdown

**Try these URLs:**

✅ **Legitimate:**
```
https://www.google.com
https://www.github.com
https://www.amazon.com
https://www.wikipedia.org
https://www.microsoft.com
```

⚠️ **Phishing:**
```
http://192.168.1.1/login.php
http://secure-paypal-verify.tk/account
http://bit.ly/free-iphone-win
http://www.g00gle.com/signin
https://amaz0n-security-alert.xyz/update
```

### 3. Command Line Interface

**Single URL prediction:**
```bash
python src/predict.py https://www.google.com
```

**Output:**
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

**Phishing URL example:**
```bash
python src/predict.py http://192.168.1.1/login.php
```

**Output:**
```
Analyzing URL: http://192.168.1.1/login.php
------------------------------------------------------------

Prediction: Phishing
Confidence: 98.76%

Probabilities:
  Legitimate: 1.24%
  Phishing:   98.76%

⚠️  WARNING: This URL appears to be a phishing attempt!
```

## 🔧 Advanced Usage

### Using in Your Python Code

```python
import sys
sys.path.insert(0, 'src')

from predict import predict_url, predict_batch, load_model

# Load model once
model = load_model()

# Predict single URL
result = predict_url("https://www.google.com", model=model)
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.2%}")

# Predict multiple URLs
urls = [
    "https://www.google.com",
    "http://phishing-site.tk/login",
    "https://www.github.com"
]

results = predict_batch(urls, model=model)
for r in results:
    print(f"{r['url']}: {r['prediction']} ({r['confidence']:.2%})")
```

### Custom Feature Extraction

```python
import sys
sys.path.insert(0, 'src')

from features import extract_features_from_url, get_feature_names

url = "http://secure-paypal-verify.tk/account"
features = extract_features_from_url(url)
feature_names = get_feature_names()

print(f"Features for: {url}\n")
for name, value in zip(feature_names, features):
    print(f"{name:25s}: {value}")
```

**Output:**
```
Features for: http://secure-paypal-verify.tk/account

url_length               : 38
num_dots                 : 1
num_hyphens              : 2
num_underscores          : 0
num_slashes              : 3
num_question_marks       : 0
num_equals               : 0
num_at_symbols           : 0
num_ampersands           : 0
num_dots_hostname        : 1
has_ip_address           : 0
uses_https               : 0
has_suspicious_tld       : 1
is_shortened             : 0
```

### Adding Custom Training Data

1. Edit `data/urls.csv`:
```csv
url,label
https://www.google.com,legitimate
http://phishing-site.tk/login,phishing
https://your-new-url.com,legitimate
http://suspicious-url.ml/verify,phishing
```

2. Retrain the model:
```bash
python src/train_model.py
```

3. The new model will automatically be used by the app and CLI.

## 🧪 Testing

### Test Feature Extraction

```bash
python test_features.py
```

This will test all feature extraction functions and show results for sample URLs.

### Test Predictions

Create a test script `test_predictions.py`:

```python
import sys
sys.path.insert(0, 'src')

from predict import predict_url

test_cases = [
    ("https://www.google.com", "Legitimate"),
    ("http://192.168.1.1/login", "Phishing"),
    ("http://bit.ly/test", "Phishing"),
    ("https://www.github.com", "Legitimate"),
]

print("Testing predictions...\n")
for url, expected in test_cases:
    result = predict_url(url)
    status = "✓" if result['prediction'] == expected else "✗"
    print(f"{status} {url}")
    print(f"  Expected: {expected}, Got: {result['prediction']}")
    print(f"  Confidence: {result['confidence']:.2%}\n")
```

## 📊 Batch Processing

Process multiple URLs from a file:

```python
import sys
import pandas as pd
sys.path.insert(0, 'src')

from predict import predict_batch, load_model

# Load URLs from file
urls_df = pd.read_csv('urls_to_check.csv')
urls = urls_df['url'].tolist()

# Load model once
model = load_model()

# Predict all URLs
results = predict_batch(urls, model=model)

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv('predictions.csv', index=False)

print(f"Processed {len(results)} URLs")
print(f"Phishing detected: {sum(1 for r in results if r['label'] == 1)}")
print(f"Legitimate: {sum(1 for r in results if r['label'] == 0)}")
```

## 🎨 Customization Examples

### Modify Suspicious TLDs

Edit `src/features.py`:

```python
def has_suspicious_tld(url: str) -> int:
    suspicious_tlds = [
        ".zip", ".tk", ".xyz", ".top", ".gq", ".ml", ".ga", ".cf",
        ".pw", ".cc"  # Add more TLDs
    ]
    hostname = get_hostname(url).lower()
    for tld in suspicious_tlds:
        if hostname.endswith(tld):
            return 1
    return 0
```

### Add URL Shorteners

Edit `src/features.py`:

```python
def is_shortened(url: str) -> int:
    shorteners = [
        "bit.ly", "goo.gl", "tinyurl.com", "t.co", "ow.ly", "bitly.com",
        "short.link", "tiny.cc", "is.gd"  # Add more shorteners
    ]
    hostname = get_hostname(url).lower()
    return 1 if hostname in shorteners else 0
```

### Change Model Parameters

Edit `src/train_model.py`:

```python
models = {
    'Random Forest': RandomForestClassifier(
        n_estimators=200,    # More trees
        max_depth=15,        # Deeper trees
        min_samples_split=5, # More samples required to split
        random_state=42
    )
}
```

## 🔍 Debugging

### Check Model Performance

```python
import joblib
import numpy as np
from sklearn.metrics import classification_report

# Load model
model = joblib.load('models/phishing_model.joblib')

# Load test data
# ... (load your X_test and y_test)

# Make predictions
y_pred = model.predict(X_test)

# Detailed report
print(classification_report(y_test, y_pred, 
                          target_names=['Legitimate', 'Phishing']))
```

### Inspect Feature Importance (Random Forest)

```python
import joblib
import matplotlib.pyplot as plt
from features import get_feature_names

model = joblib.load('models/phishing_model.joblib')

if hasattr(model, 'feature_importances_'):
    importances = model.feature_importances_
    feature_names = get_feature_names()
    
    # Sort by importance
    indices = np.argsort(importances)[::-1]
    
    print("Feature Importance:")
    for i in indices:
        print(f"{feature_names[i]:25s}: {importances[i]:.4f}")
```

## 💡 Tips & Tricks

1. **Improve Accuracy**: Add more diverse training data
2. **Speed Up**: Use `predict_batch()` for multiple URLs
3. **Customize**: Modify features based on your specific needs
4. **Monitor**: Log predictions to track performance over time
5. **Update**: Retrain regularly with new phishing patterns

---

**Need more help? Check the [README.md](README.md) for full documentation!**
