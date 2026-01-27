# 🚀 Quick Start Guide

Get up and running in 3 minutes!

## Step 1: Install Dependencies (30 seconds)

```bash
pip install -r requirements.txt
```

## Step 2: Train the Model (1 minute)

```bash
python src/train_model.py
```

You should see output showing model training and evaluation.

## Step 3: Try It Out!

### Option A: Web Interface (Recommended)

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501` and test these URLs:

**Legitimate URLs:**
- `https://www.google.com`
- `https://www.github.com`
- `https://www.amazon.com`

**Phishing URLs:**
- `http://192.168.1.1/login.php`
- `http://secure-paypal-verify.tk/account`
- `http://bit.ly/free-iphone-win`

### Option B: Command Line

```bash
python src/predict.py https://www.google.com
python src/predict.py http://phishing-site.tk/login
```

## 🎉 That's It!

You now have a working phishing URL classifier!

## Next Steps

1. **Add more data**: Edit `data/urls.csv` to add more training examples
2. **Retrain**: Run `python src/train_model.py` again
3. **Customize**: Modify features in `src/features.py`
4. **Share**: Show off your project!

## Need Help?

Check the main [README.md](README.md) for detailed documentation.
