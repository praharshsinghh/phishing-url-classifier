#!/usr/bin/env python3
"""
Compare model performance across different dataset sizes.
This helps demonstrate the value of larger datasets.
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt

# Add src to path
sys.path.append('src')
from features import extract_features_from_url


def load_and_prepare_data(csv_path):
    """Load and prepare data for training."""
    df = pd.read_csv(csv_path)
    
    # Normalize labels
    df['label'] = df['label'].map({'legitimate': 0, 'phishing': 1})
    
    # Extract features
    features_list = []
    for url in df['url']:
        features_list.append(extract_features_from_url(url))
    
    X = np.array(features_list)
    y = df['label'].values
    
    return X, y


def evaluate_model_on_dataset(dataset_path, dataset_name):
    """Evaluate model performance on a specific dataset."""
    print(f"\nEvaluating on {dataset_name}...")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset not found: {dataset_path}")
        return None
    
    # Load data
    X, y = load_and_prepare_data(dataset_path)
    
    print(f"Dataset size: {len(X)} samples")
    print(f"Class distribution: {np.bincount(y)}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    
    metrics = {
        'dataset_name': dataset_name,
        'dataset_size': len(X),
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred)
    }
    
    print(f"Results:")
    print(f"  Accuracy:  {metrics['accuracy']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  Recall:    {metrics['recall']:.4f}")
    print(f"  F1 Score:  {metrics['f1_score']:.4f}")
    
    return metrics


def main():
    """Compare performance across different datasets."""
    print("Dataset Size vs Model Performance Comparison")
    print("=" * 60)
    
    # Define datasets to compare
    datasets = [
        ('data/urls.csv', 'Original Small Dataset (30 URLs)'),
        ('data/urls_synthetic_20k.csv', 'Synthetic Dataset (20,000 URLs)'),
        ('data/urls_kaggle_20k.csv', 'Kaggle Real-world Dataset (20,000 URLs)')
    ]
    
    results = []
    
    # Evaluate each dataset
    for dataset_path, dataset_name in datasets:
        result = evaluate_model_on_dataset(dataset_path, dataset_name)
        if result:
            results.append(result)
    
    if not results:
        print("\nNo datasets found to compare!")
        print("Please run: python generate_dataset.py")
        print("Choose option 1 for synthetic data or option 2 for Kaggle data.")
        return
    
    # Display comparison
    print("\n" + "=" * 60)
    print("COMPARISON RESULTS")
    print("=" * 60)
    
    print(f"{'Dataset':<35} {'Size':<8} {'Accuracy':<10} {'Precision':<11} {'Recall':<8} {'F1':<8}")
    print("-" * 80)
    
    for result in results:
        print(f"{result['dataset_name']:<35} "
              f"{result['dataset_size']:<8} "
              f"{result['accuracy']:<10.4f} "
              f"{result['precision']:<11.4f} "
              f"{result['recall']:<8.4f} "
              f"{result['f1_score']:<8.4f}")
    
    # Create visualization if matplotlib is available
    try:
        create_comparison_plot(results)
    except ImportError:
        print("\nNote: Install matplotlib to see performance visualization")
        print("pip install matplotlib")


def create_comparison_plot(results):
    """Create a visualization comparing dataset performance."""
    if len(results) < 2:
        return
    
    # Prepare data for plotting
    dataset_names = [r['dataset_name'] for r in results]
    dataset_sizes = [r['dataset_size'] for r in results]
    accuracies = [r['accuracy'] for r in results]
    f1_scores = [r['f1_score'] for r in results]
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Dataset Size vs Accuracy
    ax1.bar(range(len(results)), accuracies, color='skyblue', alpha=0.7)
    ax1.set_xlabel('Dataset')
    ax1.set_ylabel('Accuracy')
    ax1.set_title('Model Accuracy by Dataset Size')
    ax1.set_xticks(range(len(results)))
    ax1.set_xticklabels([f"{name}\n({size} URLs)" for name, size in zip(dataset_names, dataset_sizes)], 
                        rotation=45, ha='right')
    ax1.set_ylim(0, 1)
    
    # Add value labels on bars
    for i, v in enumerate(accuracies):
        ax1.text(i, v + 0.01, f'{v:.3f}', ha='center', va='bottom')
    
    # Plot 2: Dataset Size vs F1 Score
    ax2.bar(range(len(results)), f1_scores, color='lightcoral', alpha=0.7)
    ax2.set_xlabel('Dataset')
    ax2.set_ylabel('F1 Score')
    ax2.set_title('Model F1 Score by Dataset Size')
    ax2.set_xticks(range(len(results)))
    ax2.set_xticklabels([f"{name}\n({size} URLs)" for name, size in zip(dataset_names, dataset_sizes)], 
                        rotation=45, ha='right')
    ax2.set_ylim(0, 1)
    
    # Add value labels on bars
    for i, v in enumerate(f1_scores):
        ax2.text(i, v + 0.01, f'{v:.3f}', ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Save plot
    plot_path = 'dataset_comparison.png'
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"\nComparison plot saved to: {plot_path}")
    
    # Show plot if running interactively
    try:
        plt.show()
    except:
        pass


if __name__ == "__main__":
    main()