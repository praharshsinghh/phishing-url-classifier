# Kaggle Dataset Integration Guide

This guide shows you how to integrate a large-scale, real-world phishing dataset from Kaggle to improve your phishing URL classifier.

## Quick Start

### 1. Install Kaggle API
```bash
pip install kaggle
```

### 2. Set up Kaggle Credentials
1. Go to [Kaggle Account Settings](https://www.kaggle.com/account)
2. Click "Create New API Token"
3. Download `kaggle.json` file
4. Place it in the correct location:
   - **Windows**: `C:\Users\<username>\.kaggle\kaggle.json`
   - **Mac/Linux**: `~/.kaggle/kaggle.json`
5. Set permissions (Mac/Linux): `chmod 600 ~/.kaggle/kaggle.json`

### 3. Generate Dataset
```bash
python generate_dataset.py
```
Choose option 3 for Kaggle datasets.

## Main Dataset

### Malicious URLs Dataset (Recommended)
- **Dataset ID**: `sid321axn/malicious-urls-dataset`
- **Size**: ~650,000 URLs
- **Categories**: Benign, Phishing, Malware, Defacement
- **Quality**: Large-scale real-world data
- **Source**: Research-grade dataset with good diversity

This is the primary dataset we recommend because:
- Large size provides good training data
- Real-world URLs from actual threats
- Multiple categories that map to phishing/legitimate
- Well-maintained and frequently used in research

## Dataset Sizes Available

| Size | URLs | Use Case |
|------|------|----------|
| Small | 5,000 | Quick testing |
| Medium | 15,000 | Development |
| Large | 30,000 | Production training |
| Custom | Your choice | Specific needs |

## Expected Improvements

With the Kaggle dataset, you should see improvements over the small 30-URL dataset:

| Metric | Small Dataset (30 URLs) | Kaggle Dataset (15K+ URLs) |
|--------|-------------------------|---------------------------|
| **Training Stability** | Variable | More consistent |
| **Generalization** | Limited | Better on new URLs |
| **Pattern Recognition** | Basic | More sophisticated |

*Note: Actual performance depends on many factors including data quality, feature engineering, and the specific URLs being tested.*

## Manual Download (Alternative)

If you prefer manual download:

1. Visit the [Malicious URLs Dataset](https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset) on Kaggle
2. Click "Download" button
3. Extract files to `data/kaggle/malicious-urls-dataset/`
4. Run the integration script

Example structure:
```
data/
├── kaggle/
│   └── malicious-urls-dataset/
│       └── malicious_phish.csv
└── urls_mega_kaggle.csv (generated)
```

## Advanced Usage

### Download the Main Dataset
```python
from src.kaggle_data_integrator import KaggleDatasetIntegrator

integrator = KaggleDatasetIntegrator()
integrator.download_main_dataset()
```

### Create Custom Dataset
```python
# Create dataset with specific size
mega_df = integrator.create_mega_dataset(target_size=25000)
mega_df.to_csv('data/custom_dataset.csv', index=False)
```

### Dataset Processing
The system automatically:
- Downloads the main Kaggle dataset
- Processes and cleans the data
- Balances classes (phishing vs legitimate)
- Combines with synthetic data if needed
- Removes duplicates

## Dataset Quality Features

### Real Phishing URLs Include:
- **Typosquatting**: g00gle.com, amaz0n.com
- **Domain spoofing**: paypal-security.tk
- **Suspicious TLDs**: .tk, .ml, .ga domains
- **URL shorteners**: bit.ly, tinyurl.com
- **IP addresses**: 192.168.1.1/login
- **Subdomain abuse**: secure.paypal.fake.com

### Legitimate URLs Include:
- Popular websites (Google, Amazon, GitHub)
- Banking and financial sites
- E-commerce platforms
- Social media sites
- News and media sites

## Troubleshooting

### Common Issues

1. **"Kaggle API not found"**
   ```bash
   pip install kaggle
   ```

2. **"401 Unauthorized"**
   - Check kaggle.json placement
   - Verify file permissions
   - Ensure valid API token

3. **"Dataset not found"**
   - Check dataset ID spelling
   - Verify dataset is public
   - Try manual download

4. **Memory issues with large datasets**
   - Start with smaller sizes
   - Use sampling in the code
   - Monitor system resources

### Performance Tips

1. **Start Small**: Begin with 10K URLs, scale up
2. **Monitor Memory**: Large datasets need 4GB+ RAM
3. **Use SSD**: Faster disk I/O helps with large files
4. **Parallel Processing**: Enable if available

## Integration with Training

The training script automatically detects and uses datasets in this order:

1. `urls_mega_kaggle.csv` (Kaggle mega dataset) ⭐
2. `urls_comprehensive.csv` (Real + synthetic)
3. `urls_expanded.csv` (Synthetic only)
4. `urls.csv` (Original small)

## Best Practices

### For Development
- Use 10K-25K URLs for faster iteration
- Test with synthetic data first
- Validate on real Kaggle data

### For Production
- Use 50K+ URLs for maximum accuracy
- Combine multiple Kaggle datasets
- Regular updates with fresh data

### For Research
- Use 100K+ URLs for comprehensive analysis
- Include all available datasets
- Document data sources and preprocessing

## Expected Results

With the Kaggle Dataset:
- **Training Time**: 2-10 minutes (vs 30 seconds for small dataset)
- **Model Size**: 1-3MB (vs 500KB for small dataset)
- **Better Generalization**: Works better on new, unseen URLs
- **More Stable Training**: Less variance in results
- **Improved Pattern Recognition**: Learns from real-world examples

*Note: Performance improvements depend on data quality, feature engineering, and the specific types of URLs being tested. No model is perfect.*

## Limitations

- **Not 100% Accurate**: Even large datasets won't catch all sophisticated phishing
- **Bias**: Dataset reflects the types of phishing that were detected and labeled
- **Evolving Threats**: New phishing techniques may not be in historical data
- **False Positives**: Some legitimate URLs may be flagged as suspicious

## Next Steps

1. **Set up Kaggle API** following the guide above
2. **Download the main dataset** using the integration script
3. **Train your model** with the larger dataset
4. **Test on real URLs** to see the improvement
5. **Iterate and improve** based on results

The Kaggle integration provides a significant upgrade from the small demo dataset to a more realistic training set, but remember that phishing detection is an ongoing challenge that requires continuous updates and multiple layers of security.