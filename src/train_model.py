"""Model training and evaluation script for phishing URL classifier."""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import joblib
from features import extract_features_from_url, get_feature_names


def normalize_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize labels to integers: 1 for phishing, 0 for legitimate.
    Handles both integer and string labels.
    """
    df = df.copy()
    
    # If labels are already integers, ensure they're 0 or 1
    if df['label'].dtype in [np.int64, np.int32, int]:
        if set(df['label'].unique()).issubset({0, 1}):
            return df
        else:
            raise ValueError(f"Integer labels must be 0 or 1. Found: {df['label'].unique()}")
    
    # If labels are strings, map them
    label_map = {
        'phishing': 1,
        'malicious': 1,
        'legitimate': 0,
        'benign': 0,
        'safe': 0
    }
    
    # Convert to lowercase for case-insensitive matching
    df['label'] = df['label'].str.lower().map(label_map)
    
    # Check for any unmapped labels
    if df['label'].isna().any():
        unknown_labels = df[df['label'].isna()]['label'].unique()
        raise ValueError(f"Unknown labels found: {unknown_labels}. Expected: {list(label_map.keys())}")
    
    df['label'] = df['label'].astype(int)
    return df


def load_and_prepare_data(csv_path: str):
    """Load CSV data and extract features."""
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Validate required columns
    if 'url' not in df.columns or 'label' not in df.columns:
        raise ValueError("CSV must contain 'url' and 'label' columns")
    
    # Normalize labels
    df = normalize_labels(df)
    
    print(f"Dataset loaded: {len(df)} samples")
    print(f"Class distribution:\n{df['label'].value_counts()}")
    
    # Extract features
    print("\nExtracting features from URLs...")
    features_list = []
    for url in df['url']:
        features_list.append(extract_features_from_url(url))
    
    X = np.array(features_list)
    y = df['label'].values
    
    return X, y


def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """Train multiple models and return the best one."""
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Decision Tree': DecisionTreeClassifier(max_depth=10, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    }
    
    results = {}
    best_model = None
    best_score = 0
    best_name = ""
    
    print("\n" + "="*60)
    print("MODEL TRAINING AND EVALUATION")
    print("="*60)
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        results[name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'model': model
        }
        
        print(f"\n{name} Results:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1 Score:  {f1:.4f}")
        
        # Track best model based on F1 score
        if f1 > best_score:
            best_score = f1
            best_model = model
            best_name = name
    
    print("\n" + "="*60)
    print(f"BEST MODEL: {best_name} (F1 Score: {best_score:.4f})")
    print("="*60)
    
    # Detailed classification report for best model
    y_pred_best = best_model.predict(X_test)
    print(f"\nDetailed Classification Report for {best_name}:")
    print(classification_report(y_test, y_pred_best, target_names=['Legitimate', 'Phishing']))
    
    return best_model, best_name, results


def main():
    """Main training pipeline."""
    # Paths
    data_path = os.path.join('data', 'urls.csv')
    model_dir = 'models'
    model_path = os.path.join(model_dir, 'phishing_model.joblib')
    
    # Create models directory if it doesn't exist
    os.makedirs(model_dir, exist_ok=True)
    
    # Load and prepare data
    X, y = load_and_prepare_data(data_path)
    
    # Split data
    print("\nSplitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    
    # Train and evaluate models
    best_model, best_name, results = train_and_evaluate_models(X_train, X_test, y_train, y_test)
    
    # Save the best model
    print(f"\nSaving best model ({best_name}) to {model_path}...")
    joblib.dump(best_model, model_path)
    print("Model saved successfully!")
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE")
    print("="*60)
    print(f"Best model: {best_name}")
    print(f"Model saved at: {model_path}")
    print("\nYou can now use this model for predictions!")


if __name__ == "__main__":
    main()
