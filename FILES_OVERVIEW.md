# 📁 Project Files Overview

Complete guide to all files in the Phishing URL Classifier project.

## 📂 Directory Structure

```
phishing-url-classifier/
│
├── 📁 data/                    # Training data
│   └── urls.csv                # Sample dataset (30 URLs)
│
├── 📁 models/                  # Trained models
│   └── phishing_model.joblib   # Saved model (created after training)
│
├── 📁 src/                     # Source code
│   ├── __init__.py             # Package initialization
│   ├── features.py             # Feature extraction utilities
│   ├── train_model.py          # Model training script
│   └── predict.py              # Prediction functions + CLI
│
├── 📄 app.py                   # Streamlit web application
├── 📄 test_features.py         # Feature extraction tests
│
├── 📄 requirements.txt         # Python dependencies
├── 📄 .gitignore              # Git ignore rules
│
└── 📚 Documentation/
    ├── README.md               # Main documentation
    ├── QUICKSTART.md           # Quick start guide
    ├── USAGE_EXAMPLES.md       # Detailed usage examples
    ├── DEMO.md                 # Demo presentation guide
    ├── PROJECT_SUMMARY.md      # Project summary for judges
    └── FILES_OVERVIEW.md       # This file
```

## 📄 File Descriptions

### Core Application Files

#### `src/features.py` (120 lines)
**Purpose:** URL feature extraction utilities

**Key Functions:**
- `url_length()` - Get URL length
- `count_char()` - Count specific characters
- `get_hostname()` - Extract hostname
- `num_dots_in_hostname()` - Count dots in domain
- `has_ip_address()` - Detect IP addresses
- `uses_https()` - Check HTTPS usage
- `has_suspicious_tld()` - Detect suspicious TLDs
- `is_shortened()` - Detect URL shorteners
- `extract_features_from_url()` - Main feature extraction
- `get_feature_names()` - Get feature names

**Dependencies:** `re`, `urllib.parse`

---

#### `src/train_model.py` (150 lines)
**Purpose:** Model training and evaluation

**Key Functions:**
- `normalize_labels()` - Convert labels to 0/1
- `load_and_prepare_data()` - Load CSV and extract features
- `train_and_evaluate_models()` - Train multiple models
- `main()` - Main training pipeline

**Models Trained:**
- Logistic Regression
- Decision Tree
- Random Forest

**Output:** Saves best model to `models/phishing_model.joblib`

**Dependencies:** `pandas`, `numpy`, `scikit-learn`, `joblib`

---

#### `src/predict.py` (150 lines)
**Purpose:** Prediction utilities and CLI

**Key Functions:**
- `load_model()` - Load trained model
- `predict_url()` - Predict single URL
- `predict_batch()` - Predict multiple URLs
- `main()` - CLI interface

**Usage:**
```bash
python src/predict.py <URL>
```

**Dependencies:** `joblib`, `numpy`, `features`

---

#### `app.py` (200 lines)
**Purpose:** Streamlit web application

**Features:**
- URL input form
- Real-time prediction
- Confidence scores
- Visual probability breakdown
- Styled results (green for safe, red for phishing)
- Sidebar with information

**Usage:**
```bash
streamlit run app.py
```

**Dependencies:** `streamlit`, `predict`, `features`

---

### Data Files

#### `data/urls.csv`
**Purpose:** Training dataset

**Format:**
```csv
url,label
https://www.google.com,legitimate
http://phishing-site.tk/login,phishing
```

**Contents:**
- 30 sample URLs
- 15 legitimate
- 15 phishing
- Mix of different phishing patterns

**Label Formats Supported:**
- Integers: `0` (legitimate), `1` (phishing)
- Strings: `"legitimate"`, `"benign"`, `"safe"` → 0
- Strings: `"phishing"`, `"malicious"` → 1

---

### Configuration Files

#### `requirements.txt`
**Purpose:** Python dependencies

**Contents:**
```
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.2.0
joblib>=1.2.0
streamlit>=1.28.0
```

**Installation:**
```bash
pip install -r requirements.txt
```

---

#### `.gitignore`
**Purpose:** Git ignore rules

**Ignores:**
- Python cache files (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)
- Streamlit cache (`.streamlit/`)

---

### Testing Files

#### `test_features.py`
**Purpose:** Test feature extraction

**Functions:**
- `test_feature_extraction()` - Test on sample URLs
- `test_individual_functions()` - Test each function

**Usage:**
```bash
python test_features.py
```

**Output:** Shows extracted features for test URLs

---

### Documentation Files

#### `README.md` (300+ lines)
**Purpose:** Main project documentation

**Sections:**
- Project overview
- Features
- Installation instructions
- Training guide
- Web app usage
- CLI usage
- Project structure
- ML approach explanation
- Dataset format
- Customization guide
- Troubleshooting
- For hackathon judges
- Limitations

**Audience:** All users (beginners to advanced)

---

#### `QUICKSTART.md` (60 lines)
**Purpose:** Get started in 3 minutes

**Sections:**
- Install dependencies
- Train model
- Try web interface
- Try CLI
- Next steps

**Audience:** New users who want to try it quickly

---

#### `USAGE_EXAMPLES.md` (400+ lines)
**Purpose:** Comprehensive usage examples

**Sections:**
- Basic usage (training, web, CLI)
- Advanced usage (Python API, custom features)
- Testing examples
- Batch processing
- Customization examples
- Debugging tips

**Audience:** Developers integrating the classifier

---

#### `DEMO.md` (200+ lines)
**Purpose:** Guide for presenting the project

**Sections:**
- Pre-demo checklist
- 5-minute demo script
- Key talking points
- Interactive demo ideas
- Expected results
- Q&A preparation
- Bonus CLI demo

**Audience:** Presenters at hackathons/demos

---

#### `PROJECT_SUMMARY.md` (250+ lines)
**Purpose:** Project summary for judges

**Sections:**
- One-line pitch
- Problem statement
- Solution overview
- Technical implementation
- Results
- Tech stack
- Learning outcomes
- Future enhancements
- Real-world applications
- Competitive advantages
- Project stats
- Elevator pitch

**Audience:** Hackathon judges, evaluators

---

#### `FILES_OVERVIEW.md` (This file)
**Purpose:** Guide to all project files

**Audience:** Developers exploring the codebase

---

## 🎯 Quick Reference

### To Get Started:
1. Read: `QUICKSTART.md`
2. Run: `pip install -r requirements.txt`
3. Train: `python src/train_model.py`
4. Use: `streamlit run app.py`

### To Understand the Code:
1. Start with: `src/features.py`
2. Then: `src/train_model.py`
3. Then: `src/predict.py`
4. Finally: `app.py`

### To Present:
1. Read: `DEMO.md`
2. Review: `PROJECT_SUMMARY.md`
3. Practice with: `USAGE_EXAMPLES.md`

### To Customize:
1. Read: `USAGE_EXAMPLES.md` (Customization section)
2. Modify: `src/features.py` (add features)
3. Retrain: `python src/train_model.py`

### To Debug:
1. Test features: `python test_features.py`
2. Check diagnostics in: `src/train_model.py` output
3. Review: `USAGE_EXAMPLES.md` (Debugging section)

---

## 📊 File Statistics

| Category | Files | Lines of Code |
|----------|-------|---------------|
| Source Code | 4 | ~620 |
| Application | 1 | ~200 |
| Tests | 1 | ~80 |
| Documentation | 6 | ~1500 |
| Configuration | 2 | ~20 |
| **Total** | **14** | **~2420** |

---

## 🔄 Typical Workflow

1. **Setup**: Install dependencies from `requirements.txt`
2. **Data**: Review/modify `data/urls.csv`
3. **Train**: Run `src/train_model.py`
4. **Test**: Run `test_features.py` and try CLI
5. **Deploy**: Launch `app.py` with Streamlit
6. **Iterate**: Modify features, retrain, test

---

**All files are well-documented and beginner-friendly! 🎉**
