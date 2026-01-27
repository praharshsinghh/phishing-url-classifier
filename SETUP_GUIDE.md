# 🚀 Complete Setup Guide

Step-by-step guide to set up and run the Phishing URL Classifier.

## 📋 Prerequisites

Before you begin, ensure you have:

- ✅ **Python 3.8 or higher** installed
  - Check: `python --version` or `python3 --version`
  - Download: https://www.python.org/downloads/

- ✅ **pip** (Python package manager)
  - Usually comes with Python
  - Check: `pip --version`

- ✅ **Command line / Terminal access**
  - Windows: Command Prompt or PowerShell
  - Mac/Linux: Terminal

## 🔧 Installation Steps

### Step 1: Navigate to Project Directory

```bash
cd phishing-url-classifier
```

### Step 2: (Optional) Create Virtual Environment

**Recommended to avoid dependency conflicts**

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your command prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Collecting pandas>=1.5.0
Collecting numpy>=1.23.0
Collecting scikit-learn>=1.2.0
Collecting joblib>=1.2.0
Collecting streamlit>=1.28.0
...
Successfully installed pandas-X.X.X numpy-X.X.X scikit-learn-X.X.X ...
```

**Troubleshooting:**
- If `pip` doesn't work, try `pip3`
- If you get permission errors, try `pip install --user -r requirements.txt`
- On some systems, you may need to upgrade pip first: `pip install --upgrade pip`

### Step 4: Verify Installation

```bash
python test_features.py
```

**Expected output:**
```
======================================================================
INDIVIDUAL FUNCTION TESTS
======================================================================
...
✓ All tests completed successfully!
```

If you see this, installation is successful! ✅

## 🎓 Training the Model

### Step 5: Train the ML Model

```bash
python src/train_model.py
```

**What happens:**
1. Loads training data from `data/urls.csv`
2. Extracts features from each URL
3. Trains 3 different ML models
4. Compares their performance
5. Saves the best model to `models/phishing_model.joblib`

**Expected output:**
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

============================================================
MODEL TRAINING AND EVALUATION
============================================================

Training Logistic Regression...

Logistic Regression Results:
  Accuracy:  1.0000
  Precision: 1.0000
  Recall:    1.0000
  F1 Score:  1.0000

Training Decision Tree...
...

BEST MODEL: Random Forest (F1 Score: 1.0000)
============================================================

Model saved successfully!
```

**Time:** Should take less than 5 seconds

**Troubleshooting:**
- If you get "File not found" error, make sure you're in the `phishing-url-classifier` directory
- If you get import errors, verify Step 3 completed successfully

## 🌐 Running the Web Application

### Step 6: Launch Streamlit App

```bash
streamlit run app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

**What happens:**
- Streamlit starts a local web server
- Your default browser opens automatically
- If not, manually open: http://localhost:8501

### Step 7: Test the Web App

**Try these URLs:**

1. **Legitimate URL:**
   - Paste: `https://www.google.com`
   - Click "Analyze URL"
   - Should show: ✓ LEGITIMATE

2. **Phishing URL:**
   - Paste: `http://192.168.1.1/login.php`
   - Click "Analyze URL"
   - Should show: ⚠️ PHISHING DETECTED

**Stopping the app:**
- Press `Ctrl+C` in the terminal

## 💻 Using the Command Line Interface

### Step 8: Test CLI Predictions

**Legitimate URL:**
```bash
python src/predict.py https://www.google.com
```

**Expected output:**
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

**Phishing URL:**
```bash
python src/predict.py http://phishing-site.tk/login
```

**Expected output:**
```
Analyzing URL: http://phishing-site.tk/login
------------------------------------------------------------

Prediction: Phishing
Confidence: 98.76%

Probabilities:
  Legitimate: 1.24%
  Phishing:   98.76%

⚠️  WARNING: This URL appears to be a phishing attempt!
```

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Dependencies installed (`pip list` shows pandas, numpy, scikit-learn, streamlit, joblib)
- [ ] Feature tests pass (`python test_features.py`)
- [ ] Model trained successfully (`models/phishing_model.joblib` exists)
- [ ] Web app launches (`streamlit run app.py`)
- [ ] CLI works (`python src/predict.py <URL>`)

## 🎯 Next Steps

Now that everything is set up:

1. **Explore the Web App:**
   - Try different URLs
   - Check confidence scores
   - Understand the predictions

2. **Try the CLI:**
   - Test various URLs
   - See how different patterns are detected

3. **Customize:**
   - Add more training data to `data/urls.csv`
   - Retrain: `python src/train_model.py`
   - Modify features in `src/features.py`

4. **Learn:**
   - Read `README.md` for detailed documentation
   - Check `USAGE_EXAMPLES.md` for advanced usage
   - Review `DEMO.md` for presentation tips

## 🐛 Common Issues & Solutions

### Issue: "python: command not found"
**Solution:** Try `python3` instead of `python`

### Issue: "pip: command not found"
**Solution:** Try `pip3` instead of `pip`, or `python -m pip`

### Issue: "ModuleNotFoundError: No module named 'sklearn'"
**Solution:** Run `pip install -r requirements.txt` again

### Issue: "Model not found" error
**Solution:** Run `python src/train_model.py` to train the model first

### Issue: Streamlit won't start
**Solution:** 
- Check if port 8501 is available
- Try: `streamlit run app.py --server.port 8502`

### Issue: Import errors in Python scripts
**Solution:** Make sure you're running commands from the `phishing-url-classifier` directory

### Issue: Virtual environment not activating
**Solution:**
- Windows: Make sure you're using the correct path: `venv\Scripts\activate`
- Mac/Linux: Use `source venv/bin/activate`

## 📞 Getting Help

If you encounter issues:

1. **Check the documentation:**
   - `README.md` - Main documentation
   - `USAGE_EXAMPLES.md` - Usage examples
   - `FILES_OVERVIEW.md` - File descriptions

2. **Verify your setup:**
   - Python version: `python --version` (should be 3.8+)
   - Pip version: `pip --version`
   - Installed packages: `pip list`

3. **Test components individually:**
   - Features: `python test_features.py`
   - Training: `python src/train_model.py`
   - Prediction: `python src/predict.py https://www.google.com`

## 🎉 Success!

If you've completed all steps, you now have a fully functional phishing URL classifier!

**What you can do:**
- ✅ Detect phishing URLs in real-time
- ✅ Use both web interface and command line
- ✅ Understand how ML-based URL classification works
- ✅ Customize and extend the system

**Happy phishing detection! 🔒**

---

**Quick Commands Reference:**

```bash
# Install
pip install -r requirements.txt

# Train
python src/train_model.py

# Test
python test_features.py

# Web App
streamlit run app.py

# CLI
python src/predict.py <URL>
```
