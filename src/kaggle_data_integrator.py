"""
Kaggle dataset integrator for phishing URL classification.
This script helps download and integrate large phishing datasets from Kaggle.
"""

import pandas as pd
import os
import zipfile
import requests
from typing import List, Dict, Optional
import subprocess
import sys


class KaggleDatasetIntegrator:
    """Integrate large phishing datasets from Kaggle."""
    
    def __init__(self):
        self.data_dir = 'data'
        self.kaggle_dir = os.path.join(self.data_dir, 'kaggle')
        os.makedirs(self.kaggle_dir, exist_ok=True)
        
        # Main recommended Kaggle dataset
        self.main_dataset = {
            'name': 'Malicious URLs Dataset',
            'dataset_id': 'sid321axn/malicious-urls-dataset',
            'size': '~650,000 URLs',
            'description': 'Large dataset with malicious, suspicious, and benign URLs',
            'files': ['malicious_phish.csv']
        }
        
        # Alternative datasets (smaller, backup options)
        self.alternative_datasets = {
            'phishing-site-urls': {
                'name': 'Phishing Site URLs',
                'dataset_id': 'taruntiwarihp/phishing-site-urls',
                'size': '~11,000 URLs',
                'description': 'Comprehensive phishing and legitimate URL dataset',
                'files': ['phishing_site_urls.csv']
            }
        }
    
    def check_kaggle_setup(self) -> bool:
        """Check if Kaggle API is properly set up."""
        try:
            # Check if kaggle command is available
            result = subprocess.run(['kaggle', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✓ Kaggle CLI is installed")
                return True
            else:
                print("✗ Kaggle CLI not working properly")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("✗ Kaggle CLI not found")
            return False
    
    def setup_kaggle_instructions(self):
        """Provide instructions for setting up Kaggle API."""
        print("\n" + "="*60)
        print("KAGGLE API SETUP REQUIRED")
        print("="*60)
        print("\nTo download datasets from Kaggle, you need to:")
        print("\n1. Install Kaggle API:")
        print("   pip install kaggle")
        print("\n2. Get your Kaggle API credentials:")
        print("   - Go to https://www.kaggle.com/account")
        print("   - Click 'Create New API Token'")
        print("   - Download kaggle.json file")
        print("\n3. Place kaggle.json in the right location:")
        print("   Windows: C:\\Users\\<username>\\.kaggle\\kaggle.json")
        print("   Mac/Linux: ~/.kaggle/kaggle.json")
        print("\n4. Set file permissions (Mac/Linux only):")
        print("   chmod 600 ~/.kaggle/kaggle.json")
        print("\n5. Run this script again")
        print("\nAlternatively, you can manually download datasets from Kaggle")
        print("and place them in the data/kaggle/ folder.")
    
    def list_recommended_datasets(self):
        """List the main recommended Kaggle dataset."""
        print("\nRecommended Kaggle Dataset for Phishing Detection:")
        print("="*60)
        
        print(f"\nMain Dataset: {self.main_dataset['name']}")
        print(f"   Dataset ID: {self.main_dataset['dataset_id']}")
        print(f"   Size: {self.main_dataset['size']}")
        print(f"   Description: {self.main_dataset['description']}")
        print(f"   Files: {', '.join(self.main_dataset['files'])}")
        
        print(f"\nAlternative (smaller) datasets:")
        for key, dataset in self.alternative_datasets.items():
            print(f"   - {dataset['name']} ({dataset['size']})")
    
    def download_main_dataset(self) -> bool:
        """Download the main recommended dataset."""
        return self.download_dataset('malicious-urls-dataset')
    
    def download_dataset(self, dataset_key: str) -> bool:
        """Download a specific dataset from Kaggle."""
        if dataset_key == 'malicious-urls-dataset':
            dataset = self.main_dataset
        elif dataset_key in self.alternative_datasets:
            dataset = self.alternative_datasets[dataset_key]
        else:
            print(f"Unknown dataset: {dataset_key}")
            return False
        dataset_id = dataset['dataset_id']
        
        print(f"\nDownloading {dataset['name']}...")
        print(f"Dataset ID: {dataset_id}")
        
        try:
            # Create dataset-specific directory
            dataset_dir = os.path.join(self.kaggle_dir, dataset_key)
            os.makedirs(dataset_dir, exist_ok=True)
            
            # Download using Kaggle API
            cmd = ['kaggle', 'datasets', 'download', '-d', dataset_id, '-p', dataset_dir, '--unzip']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✓ Successfully downloaded {dataset['name']}")
                
                # List downloaded files
                files = os.listdir(dataset_dir)
                print(f"Downloaded files: {files}")
                return True
            else:
                print(f"✗ Failed to download {dataset['name']}")
                print(f"Error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"✗ Download timeout for {dataset['name']}")
            return False
        except Exception as e:
            print(f"✗ Error downloading {dataset['name']}: {e}")
            return False
    
    def process_phishing_site_urls(self) -> pd.DataFrame:
        """Process the Phishing Site URLs dataset."""
        dataset_dir = os.path.join(self.kaggle_dir, 'phishing-site-urls')
        csv_file = os.path.join(dataset_dir, 'phishing_site_urls.csv')
        
        if not os.path.exists(csv_file):
            print(f"Dataset file not found: {csv_file}")
            return pd.DataFrame()
        
        try:
            df = pd.read_csv(csv_file)
            print(f"Loaded {len(df)} URLs from Phishing Site URLs dataset")
            
            # Standardize column names
            if 'URL' in df.columns and 'Label' in df.columns:
                df = df.rename(columns={'URL': 'url', 'Label': 'label'})
            
            # Standardize labels
            if 'label' in df.columns:
                df['label'] = df['label'].str.lower()
                df['label'] = df['label'].replace({'bad': 'phishing', 'good': 'legitimate'})
            
            return df
            
        except Exception as e:
            print(f"Error processing Phishing Site URLs dataset: {e}")
            return pd.DataFrame()
    
    def process_malicious_urls_dataset(self) -> pd.DataFrame:
        """Process the Malicious URLs dataset."""
        dataset_dir = os.path.join(self.kaggle_dir, 'malicious-urls-dataset')
        csv_file = os.path.join(dataset_dir, 'malicious_phish.csv')
        
        if not os.path.exists(csv_file):
            print(f"Dataset file not found: {csv_file}")
            return pd.DataFrame()
        
        try:
            df = pd.read_csv(csv_file)
            print(f"Loaded {len(df)} URLs from Malicious URLs dataset")
            
            # Standardize column names
            if 'url' in df.columns and 'type' in df.columns:
                df = df.rename(columns={'type': 'label'})
            
            # Standardize labels - this dataset has multiple categories
            if 'label' in df.columns:
                # Map categories to binary classification
                label_mapping = {
                    'benign': 'legitimate',
                    'defacement': 'phishing',
                    'phishing': 'phishing',
                    'malware': 'phishing'
                }
                df['label'] = df['label'].str.lower().map(label_mapping)
                
                # Remove rows with unmapped labels
                df = df.dropna(subset=['label'])
            
            return df
            
        except Exception as e:
            print(f"Error processing Malicious URLs dataset: {e}")
            return pd.DataFrame()
    
    def process_phishing_websites_dataset(self) -> pd.DataFrame:
        """Process the Phishing Websites dataset."""
        dataset_dir = os.path.join(self.kaggle_dir, 'phishing-websites-dataset')
        csv_file = os.path.join(dataset_dir, 'dataset_phishing.csv')
        
        if not os.path.exists(csv_file):
            print(f"Dataset file not found: {csv_file}")
            return pd.DataFrame()
        
        try:
            df = pd.read_csv(csv_file)
            print(f"Loaded {len(df)} entries from Phishing Websites dataset")
            
            # This dataset might have features instead of raw URLs
            # Check if it has URL column
            if 'url' not in df.columns:
                print("This dataset contains features, not raw URLs. Skipping for URL-based training.")
                return pd.DataFrame()
            
            # Standardize labels
            if 'Result' in df.columns:
                df = df.rename(columns={'Result': 'label'})
                df['label'] = df['label'].map({1: 'phishing', 0: 'legitimate', -1: 'phishing'})
            
            return df
            
        except Exception as e:
            print(f"Error processing Phishing Websites dataset: {e}")
            return pd.DataFrame()
    
    def combine_kaggle_datasets(self, max_size_per_dataset: int = 20000) -> pd.DataFrame:
        """Use the main Kaggle dataset."""
        print("Loading main Kaggle dataset...")
        
        # Try to load the main dataset first
        main_dataset_dir = os.path.join(self.kaggle_dir, 'malicious-urls-dataset')
        if os.path.exists(main_dataset_dir):
            df = self.process_malicious_urls_dataset()
            if not df.empty:
                # Limit size to prevent memory issues
                if len(df) > max_size_per_dataset:
                    df = df.sample(n=max_size_per_dataset, random_state=42)
                    print(f"Sampled {max_size_per_dataset} URLs from main dataset")
                
                print(f"Loaded {len(df)} URLs from main Kaggle dataset")
                
                # Show class distribution
                if 'label' in df.columns:
                    print("Class distribution:")
                    print(df['label'].value_counts())
                
                return df
        
        # Fall back to alternative datasets
        print("Main dataset not found, trying alternatives...")
        alternative_data = []
        
        for dataset_key in self.alternative_datasets.keys():
            dataset_dir = os.path.join(self.kaggle_dir, dataset_key)
            if os.path.exists(dataset_dir):
                if dataset_key == 'phishing-site-urls':
                    df = self.process_phishing_site_urls()
                    if not df.empty:
                        alternative_data.append(df)
        
        if alternative_data:
            combined_df = pd.concat(alternative_data, ignore_index=True)
            print(f"Loaded {len(combined_df)} URLs from alternative datasets")
            return combined_df
        
        print("No Kaggle datasets found")
        return pd.DataFrame()
    
    def create_mega_dataset(self, target_size: int = 20000) -> pd.DataFrame:
        """Create a dataset combining Kaggle data with synthetic data (fixed at 20,000 URLs)."""
        print(f"Creating dataset with {target_size} URLs using Kaggle data")
        print("="*60)
        
        # Get Kaggle data
        kaggle_df = self.combine_kaggle_datasets()
        
        if kaggle_df.empty:
            print("No Kaggle data available. Using synthetic data only.")
            # Fall back to synthetic data
            from data_generator import URLDatasetGenerator
            generator = URLDatasetGenerator()
            return generator.generate_balanced_dataset(target_size)
        
        # Balance Kaggle data
        phishing_df = kaggle_df[kaggle_df['label'] == 'phishing']
        legitimate_df = kaggle_df[kaggle_df['label'] == 'legitimate']
        
        print(f"Kaggle data - Phishing: {len(phishing_df)}, Legitimate: {len(legitimate_df)}")
        
        # Calculate how much synthetic data we need
        kaggle_size = len(kaggle_df)
        remaining_size = max(0, target_size - kaggle_size)
        
        if remaining_size > 0:
            print(f"Adding {remaining_size} synthetic URLs to reach target size")
            
            # Generate synthetic data to fill the gap
            from data_generator import URLDatasetGenerator
            generator = URLDatasetGenerator()
            synthetic_df = generator.generate_balanced_dataset(remaining_size)
            
            # Combine Kaggle and synthetic data
            mega_df = pd.concat([kaggle_df, synthetic_df], ignore_index=True)
        else:
            # We have enough Kaggle data, just sample it
            mega_df = kaggle_df.sample(n=target_size, random_state=42)
        
        # Final balancing
        phishing_final = mega_df[mega_df['label'] == 'phishing']
        legitimate_final = mega_df[mega_df['label'] == 'legitimate']
        
        # Balance to equal sizes
        min_class_size = min(len(phishing_final), len(legitimate_final))
        target_each = min(min_class_size, target_size // 2)
        
        if len(phishing_final) > target_each:
            phishing_final = phishing_final.sample(n=target_each, random_state=42)
        
        if len(legitimate_final) > target_each:
            legitimate_final = legitimate_final.sample(n=target_each, random_state=42)
        
        # Combine and shuffle
        final_df = pd.concat([phishing_final, legitimate_final], ignore_index=True)
        final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        print(f"\nFinal dataset:")
        print(f"Total URLs: {len(final_df)}")
        print(f"Phishing: {len(final_df[final_df['label'] == 'phishing'])}")
        print(f"Legitimate: {len(final_df[final_df['label'] == 'legitimate'])}")
        
        return final_df


def main():
    """Main function to integrate Kaggle datasets."""
    integrator = KaggleDatasetIntegrator()
    
    print("Kaggle Dataset Integrator for Phishing URL Classification")
    print("="*60)
    
    # Check Kaggle setup
    if not integrator.check_kaggle_setup():
        integrator.setup_kaggle_instructions()
        return
    
    # Show available datasets
    integrator.list_recommended_datasets()
    
    print("Options:")
    print("1. Download main dataset (Malicious URLs - 650K URLs)")
    print("2. Create 20,000 URL dataset from existing downloads")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            print("\nDownloading main Kaggle dataset...")
            integrator.download_main_dataset()
            break
            
        elif choice == '2':
            print("\nCreating 20,000 URL dataset from existing downloads...")
            mega_df = integrator.create_mega_dataset(20000)
            
            if not mega_df.empty:
                output_path = os.path.join('data', 'urls_kaggle_20k.csv')
                mega_df.to_csv(output_path, index=False)
                print(f"\nDataset saved to: {output_path}")
                print("This dataset uses real Kaggle data balanced with synthetic URLs!")
            break
            
        elif choice == '3':
            print("Exiting...")
            return
            
        else:
            print("Invalid choice. Please enter 1-3.")


if __name__ == "__main__":
    main()