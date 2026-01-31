#!/usr/bin/env python3
"""
Simple script to generate datasets for phishing URL classification.
Two options: Real-world Kaggle data or Synthetic data (20,000 URLs each).
"""

import os
import sys

# Add src to path so we can import our modules
sys.path.append('src')


def main():
    print("Phishing URL Dataset Generator")
    print("=" * 50)
    print()
    print("Choose your dataset option:")
    print("1. Synthetic Data (20,000 URLs) - Works offline, fast generation")
    print("2. Real-world Kaggle Data (20,000 URLs) - Requires Kaggle API setup")
    print("3. Exit")
    print()
    
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            generate_synthetic_dataset()
            break
        elif choice == '2':
            generate_kaggle_dataset()
            break
        elif choice == '3':
            print("Exiting...")
            return
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def generate_synthetic_dataset():
    """Generate synthetic dataset with 20,000 URLs."""
    print("\nGenerating synthetic dataset with 20,000 URLs...")
    print("This creates realistic phishing patterns and works offline.")
    
    from data_generator import URLDatasetGenerator
    
    generator = URLDatasetGenerator()
    df = generator.generate_balanced_dataset(20000)
    
    # Save dataset
    output_path = os.path.join('data', 'urls_synthetic_20k.csv')
    df.to_csv(output_path, index=False)
    
    print(f"\nDataset saved to: {output_path}")
    print(f"Generated {len(df)} URLs total")
    print("- 10,000 legitimate URLs")
    print("- 10,000 phishing URLs")
    print("\nYou can now run: python src/train_model.py")


def generate_kaggle_dataset():
    """Generate dataset using Kaggle real-world data."""
    print("\nGenerating real-world dataset with 20,000 URLs...")
    print("This uses actual phishing URLs from Kaggle datasets.")
    print("Requires Kaggle API setup (kaggle.json credentials).")
    
    try:
        from kaggle_data_integrator import KaggleDatasetIntegrator
        
        integrator = KaggleDatasetIntegrator()
        
        # Check if Kaggle is set up
        if not integrator.check_kaggle_setup():
            print("\nKaggle API not set up. Please follow these steps:")
            print("1. Go to https://www.kaggle.com/account")
            print("2. Click 'Create New API Token'")
            print("3. Download kaggle.json file")
            print("4. Place it at:")
            print("   Windows: C:\\Users\\<username>\\.kaggle\\kaggle.json")
            print("   Mac/Linux: ~/.kaggle/kaggle.json")
            print("5. Run this script again")
            return
        
        print("\nDownloading and processing Kaggle dataset...")
        print("This may take several minutes...")
        
        # Create dataset with 20,000 URLs
        df = integrator.create_mega_dataset(20000)
        
        if not df.empty:
            output_path = os.path.join('data', 'urls_kaggle_20k.csv')
            df.to_csv(output_path, index=False)
            
            print(f"\nKaggle dataset saved to: {output_path}")
            print(f"Generated {len(df)} URLs total")
            print("- Real phishing URLs from Kaggle")
            print("- Legitimate URLs from popular websites")
            print("- Balanced dataset for training")
            print("\nYou can now run: python src/train_model.py")
        else:
            print("\nFailed to create Kaggle dataset.")
            print("Try the synthetic option instead.")
            
    except ImportError:
        print("Error importing Kaggle integrator. Please check the installation.")


if __name__ == "__main__":
    main()