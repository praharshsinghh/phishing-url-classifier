# 🎬 Demo Guide

This guide helps you demonstrate the phishing URL classifier effectively.

## 📋 Pre-Demo Checklist

- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Model trained: `python src/train_model.py`
- [ ] Test the app: `streamlit run app.py`

## 🎯 Demo Script (5 minutes)

### 1. Introduction (30 seconds)

"I built a machine learning system that detects phishing URLs. It analyzes URL patterns to identify suspicious websites that might steal your information."

### 2. Show the Web Interface (2 minutes)

Launch the app:
```bash
streamlit run app.py
```

**Test legitimate URLs:**
- `https://www.google.com` → Should show "Legitimate"
- `https://www.github.com` → Should show "Legitimate"

**Test phishing URLs:**
- `http://192.168.1.1/login.php` → Should show "Phishing" (IP address)
- `http://secure-paypal-verify.tk/account` → Should show "Phishing" (suspicious TLD)
- `http://bit.ly/free-iphone-win` → Should show "Phishing" (URL shortener)

### 3. Explain the Technology (1.5 minutes)

"The system works by:
1. **Extracting features** from URLs like length, special characters, and domain patterns
2. **Training ML models** on labeled data (phishing vs legitimate)
3. **Making predictions** with confidence scores

I compared three algorithms - Logistic Regression, Decision Tree, and Random Forest - and the system automatically picks the best one."

### 4. Show the Code (1 minute)

Open `src/features.py` and highlight:
- Simple, interpretable features
- No black-box deep learning
- Pure Python implementation

### 5. Closing

"This project demonstrates end-to-end ML: data preparation, feature engineering, model training, evaluation, and deployment with both web and CLI interfaces."

## 🎤 Key Talking Points

### Technical Highlights
- **14 interpretable features** extracted from URLs
- **3 ML algorithms** compared automatically
- **Train/test split** for unbiased evaluation
- **Modular code** with separate feature extraction, training, and prediction modules

### Practical Application
- Addresses real cybersecurity problem
- Could be integrated into browsers or email clients
- Educational tool for understanding phishing patterns

### Skills Demonstrated
- Python programming
- Machine learning (scikit-learn)
- Web development (Streamlit)
- Software engineering best practices
- Documentation and user experience

## 🧪 Interactive Demo Ideas

### Live Testing
Ask audience members to suggest URLs to test in real-time.

### Feature Explanation
Show how changing URL characteristics affects the prediction:
- Add `.tk` to a legitimate domain
- Replace domain with IP address
- Add suspicious patterns

### Code Walkthrough
Open `src/train_model.py` and show:
- Data loading and normalization
- Model training loop
- Evaluation metrics

## 📊 Expected Results

With the provided sample dataset:
- **Accuracy**: ~90-100% (small dataset)
- **Training time**: < 5 seconds
- **Prediction time**: < 100ms per URL

## 🎓 Q&A Preparation

**Q: How accurate is it?**
A: On the test set, it achieves high accuracy. In production, it would need more data and features, but this demonstrates the core concepts.

**Q: Why not use deep learning?**
A: For this problem, simple features work well and are more interpretable. Deep learning would be overkill and harder to explain.

**Q: Can it detect new phishing patterns?**
A: It generalizes to similar patterns, but would need retraining for completely new attack types. That's why continuous learning is important in production systems.

**Q: How would you improve it?**
A: Add more features (page content analysis, WHOIS data, reputation scores), collect more training data, implement online learning, and add explainability features.

## 🚀 Bonus: CLI Demo

Show the command-line interface:
```bash
python src/predict.py https://www.google.com
python src/predict.py http://phishing-site.tk/login
```

This demonstrates versatility - same model, multiple interfaces.

---

**Good luck with your demo! 🎉**
