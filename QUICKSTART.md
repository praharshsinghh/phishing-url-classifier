# 🚀 Quick Start Guide

Get your phishing URL classifier running in 3 simple steps!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Generate Dataset & Train

```bash
# Generate 20,000 URL dataset
python generate_dataset.py
# Choose option 1 (synthetic) or option 2 (Kaggle real-world data)

# Train the model
python src/train_model.py
```

## Step 3: Test It Out!

### Web Interface (Recommended)

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501` and test these URLs:

**Try these legitimate URLs:**
- `https://www.google.com`
- `https://www.github.com`
- `https://www.amazon.com`

**Try these suspicious URLs:**
- `http://192.168.1.1/login.php`
- `http://secure-paypal-verify.tk/account`
- `http://g00gle.com/signin`

### Command Line Interface

```bash
python src/predict.py https://www.google.com
python src/predict.py http://suspicious-site.tk/login
```

## 🎉 You're Done!

Your phishing URL classifier is now working with 20,000 URLs!

## Two Dataset Options:

1. **Synthetic Data (Option 1)**: Fast, works offline, good for learning
2. **Kaggle Real-world Data (Option 2)**: Better performance, requires Kaggle API setup

## Need Help?

- **Detailed guide**: See [HOW_TO_RUN.md](HOW_TO_RUN.md)
- **Kaggle setup**: See [KAGGLE_INTEGRATION.md](KAGGLE_INTEGRATION.md)
- **Full documentation**: Check [README.md](README.md)
