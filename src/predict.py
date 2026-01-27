"""Prediction utilities and CLI for phishing URL classifier."""

import os
import sys
import joblib
import numpy as np
from features import extract_features_from_url


def load_model(model_path: str = None):
    """Load the trained model from disk."""
    if model_path is None:
        model_path = os.path.join('models', 'phishing_model.joblib')
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found at {model_path}. "
            "Please train the model first by running: python src/train_model.py"
        )
    
    return joblib.load(model_path)


def predict_url(url: str, model=None, model_path: str = None) -> dict:
    """
    Predict if a URL is phishing or legitimate.
    
    Args:
        url: The URL to classify
        model: Pre-loaded model (optional)
        model_path: Path to model file (optional)
    
    Returns:
        dict with keys:
            - 'url': the input URL
            - 'prediction': 'Phishing' or 'Legitimate'
            - 'label': 1 for phishing, 0 for legitimate
            - 'confidence': probability of the predicted class
            - 'probabilities': dict with probabilities for each class
    """
    # Load model if not provided
    if model is None:
        model = load_model(model_path)
    
    # Extract features
    features = extract_features_from_url(url)
    features_array = np.array(features).reshape(1, -1)
    
    # Make prediction
    prediction_label = model.predict(features_array)[0]
    prediction_text = "Phishing" if prediction_label == 1 else "Legitimate"
    
    # Get probabilities if available
    if hasattr(model, 'predict_proba'):
        probabilities = model.predict_proba(features_array)[0]
        prob_legitimate = probabilities[0]
        prob_phishing = probabilities[1]
        confidence = probabilities[prediction_label]
    else:
        # For models without predict_proba, use binary confidence
        prob_legitimate = 0.0 if prediction_label == 1 else 1.0
        prob_phishing = 1.0 if prediction_label == 1 else 0.0
        confidence = 1.0
    
    return {
        'url': url,
        'prediction': prediction_text,
        'label': int(prediction_label),
        'confidence': float(confidence),
        'probabilities': {
            'legitimate': float(prob_legitimate),
            'phishing': float(prob_phishing)
        }
    }


def predict_batch(urls: list, model=None, model_path: str = None) -> list:
    """
    Predict multiple URLs at once.
    
    Args:
        urls: List of URLs to classify
        model: Pre-loaded model (optional)
        model_path: Path to model file (optional)
    
    Returns:
        list of prediction dictionaries
    """
    # Load model once for all predictions
    if model is None:
        model = load_model(model_path)
    
    results = []
    for url in urls:
        result = predict_url(url, model=model)
        results.append(result)
    
    return results


def main():
    """CLI interface for URL prediction."""
    if len(sys.argv) < 2:
        print("Usage: python src/predict.py <URL>")
        print("\nExample:")
        print("  python src/predict.py http://example.com")
        print("  python src/predict.py https://suspicious-site.tk/login")
        sys.exit(1)
    
    url = sys.argv[1]
    
    try:
        print(f"\nAnalyzing URL: {url}")
        print("-" * 60)
        
        result = predict_url(url)
        
        print(f"\nPrediction: {result['prediction']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"\nProbabilities:")
        print(f"  Legitimate: {result['probabilities']['legitimate']:.2%}")
        print(f"  Phishing:   {result['probabilities']['phishing']:.2%}")
        
        if result['prediction'] == 'Phishing':
            print("\n⚠️  WARNING: This URL appears to be a phishing attempt!")
        else:
            print("\n✓ This URL appears to be legitimate.")
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during prediction: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
