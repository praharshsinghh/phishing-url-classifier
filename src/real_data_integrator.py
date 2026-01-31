"""
Real dataset integrator for phishing URL classification.
This script helps download and integrate real phishing datasets from public sources.
"""

import pandas as pd
import requests
import os
import json
import time
from typing import List, Dict, Optional
import csv
from urllib.parse import urlparse


class RealDatasetIntegrator:
    """Integrate real phishing datasets from various public sources."""
    
    def __init__(self):
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)
    
    def download_phishtank_data(self) -> pd.DataFrame:
        """
        Download phishing URLs from PhishTank.
        Note: PhishTank requires registration for API access.
        """
        print("Downloading PhishTank data...")
        
        try:
            # PhishTank provides a free CSV download (no API key needed for basic access)
            url = "http://data.phishtank.com/data/online-valid.csv"
            
            print("Fetching PhishTank CSV data...")
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                # Save raw data
                csv_path = os.path.join(self.data_dir, 'phishtank_raw.csv')
                with open(csv_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                # Parse CSV
                df = pd.read_csv(csv_path)
                
                # Extract URLs and mark as phishing
                if 'url' in df.columns:
                    phishing_df = pd.DataFrame({
                        'url': df['url'],
                        'label': 'phishing'
                    })
                    
                    print(f"Downloaded {len(phishing_df)} phishing URLs from PhishTank")
                    return phishing_df
                else:
                    print("PhishTank CSV format unexpected")
                    return pd.DataFrame()
            
            else:
                print(f"Failed to download PhishTank data: HTTP {response.status_code}")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"Error downloading PhishTank data: {e}")
            return pd.DataFrame()
    
    def download_openphish_data(self) -> pd.DataFrame:
        """
        Download phishing URLs from OpenPhish feed.
        """
        print("Downloading OpenPhish data...")
        
        try:
            # OpenPhish provides a free feed
            url = "https://openphish.com/feed.txt"
            
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                urls = response.text.strip().split('\n')
                urls = [url.strip() for url in urls if url.strip()]
                
                phishing_df = pd.DataFrame({
                    'url': urls,
                    'label': 'phishing'
                })
                
                print(f"Downloaded {len(phishing_df)} phishing URLs from OpenPhish")
                return phishing_df
            else:
                print(f"Failed to download OpenPhish data: HTTP {response.status_code}")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"Error downloading OpenPhish data: {e}")
            return pd.DataFrame()
    
    def get_alexa_top_sites(self, count: int = 1000) -> pd.DataFrame:
        """
        Get legitimate URLs from popular sites.
        Note: Alexa top sites service was discontinued, using alternative approach.
        """
        print(f"Generating {count} legitimate URLs from popular sites...")
        
        # Popular legitimate domains (manually curated list)
        popular_domains = [
            'google.com', 'youtube.com', 'facebook.com', 'twitter.com', 'instagram.com',
            'linkedin.com', 'reddit.com', 'wikipedia.org', 'amazon.com', 'ebay.com',
            'netflix.com', 'spotify.com', 'apple.com', 'microsoft.com', 'adobe.com',
            'github.com', 'stackoverflow.com', 'medium.com', 'wordpress.com', 'blogger.com',
            'paypal.com', 'stripe.com', 'shopify.com', 'etsy.com', 'walmart.com',
            'target.com', 'bestbuy.com', 'homedepot.com', 'lowes.com', 'costco.com',
            'cnn.com', 'bbc.com', 'nytimes.com', 'washingtonpost.com', 'reuters.com',
            'espn.com', 'nfl.com', 'nba.com', 'mlb.com', 'yahoo.com',
            'gmail.com', 'outlook.com', 'hotmail.com', 'icloud.com', 'dropbox.com',
            'zoom.us', 'slack.com', 'discord.com', 'whatsapp.com', 'telegram.org',
            'uber.com', 'lyft.com', 'airbnb.com', 'booking.com', 'expedia.com',
            'tripadvisor.com', 'yelp.com', 'foursquare.com', 'pinterest.com', 'tumblr.com'
        ]
        
        legitimate_urls = []
        
        # Generate variations of legitimate URLs
        import random
        
        subdomains = ['www', 'mail', 'blog', 'shop', 'support', 'api', 'mobile', 'secure']
        paths = ['/', '/home', '/about', '/contact', '/login', '/register', '/help', '/support']
        
        for _ in range(count):
            domain = random.choice(popular_domains)
            
            # Sometimes add subdomain
            if random.random() < 0.4:
                subdomain = random.choice(subdomains)
                domain = f"{subdomain}.{domain}"
            
            # Sometimes add path
            path = random.choice(paths) if random.random() < 0.6 else '/'
            
            # Use HTTPS for most legitimate sites
            protocol = 'https' if random.random() < 0.9 else 'http'
            
            url = f"{protocol}://{domain}{path}"
            legitimate_urls.append(url)
        
        legitimate_df = pd.DataFrame({
            'url': legitimate_urls,
            'label': 'legitimate'
        })
        
        print(f"Generated {len(legitimate_df)} legitimate URLs")
        return legitimate_df
    
    def clean_and_validate_urls(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate URLs in the dataset."""
        print("Cleaning and validating URLs...")
        
        initial_count = len(df)
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['url'])
        
        # Remove invalid URLs
        valid_urls = []
        for _, row in df.iterrows():
            try:
                parsed = urlparse(row['url'])
                if parsed.scheme in ['http', 'https'] and parsed.netloc:
                    valid_urls.append(row)
            except:
                continue
        
        cleaned_df = pd.DataFrame(valid_urls)
        
        print(f"Cleaned dataset: {initial_count} -> {len(cleaned_df)} URLs")
        return cleaned_df
    
    def create_comprehensive_dataset(self, target_size: int = 10000) -> pd.DataFrame:
        """Create a comprehensive dataset combining multiple sources."""
        print(f"Creating comprehensive dataset with target size: {target_size}")
        print("=" * 60)
        
        all_data = []
        
        # Try to get real phishing data
        print("\n1. Downloading real phishing data...")
        
        # PhishTank data
        phishtank_data = self.download_phishtank_data()
        if not phishtank_data.empty:
            # Limit to reasonable size
            if len(phishtank_data) > target_size // 4:
                phishtank_data = phishtank_data.sample(n=target_size // 4, random_state=42)
            all_data.append(phishtank_data)
        
        # OpenPhish data
        openphish_data = self.download_openphish_data()
        if not openphish_data.empty:
            # Limit to reasonable size
            if len(openphish_data) > target_size // 4:
                openphish_data = openphish_data.sample(n=target_size // 4, random_state=42)
            all_data.append(openphish_data)
        
        # Get legitimate URLs
        print("\n2. Generating legitimate URLs...")
        legitimate_data = self.get_alexa_top_sites(target_size // 2)
        all_data.append(legitimate_data)
        
        # Combine all data
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
        else:
            print("No data sources available, creating empty dataset")
            return pd.DataFrame(columns=['url', 'label'])
        
        # Clean and validate
        combined_df = self.clean_and_validate_urls(combined_df)
        
        # Balance the dataset
        print("\n3. Balancing dataset...")
        phishing_count = len(combined_df[combined_df['label'] == 'phishing'])
        legitimate_count = len(combined_df[combined_df['label'] == 'legitimate'])
        
        print(f"Before balancing - Phishing: {phishing_count}, Legitimate: {legitimate_count}")
        
        # If we have too few phishing URLs, supplement with synthetic ones
        if phishing_count < target_size // 2:
            print("Supplementing with synthetic phishing URLs...")
            from data_generator import URLDatasetGenerator
            generator = URLDatasetGenerator()
            
            needed_phishing = (target_size // 2) - phishing_count
            synthetic_phishing = generator.generate_phishing_urls(needed_phishing)
            synthetic_df = pd.DataFrame(synthetic_phishing, columns=['url', 'label'])
            combined_df = pd.concat([combined_df, synthetic_df], ignore_index=True)
        
        # Balance by sampling
        phishing_df = combined_df[combined_df['label'] == 'phishing']
        legitimate_df = combined_df[combined_df['label'] == 'legitimate']
        
        target_each = target_size // 2
        
        if len(phishing_df) > target_each:
            phishing_df = phishing_df.sample(n=target_each, random_state=42)
        
        if len(legitimate_df) > target_each:
            legitimate_df = legitimate_df.sample(n=target_each, random_state=42)
        
        final_df = pd.concat([phishing_df, legitimate_df], ignore_index=True)
        final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle
        
        print(f"\nFinal dataset statistics:")
        print(f"Total URLs: {len(final_df)}")
        print(f"Phishing: {len(final_df[final_df['label'] == 'phishing'])}")
        print(f"Legitimate: {len(final_df[final_df['label'] == 'legitimate'])}")
        
        return final_df


def main():
    """Main function to create comprehensive dataset."""
    integrator = RealDatasetIntegrator()
    
    print("Real Dataset Integrator for Phishing URL Classification")
    print("=" * 60)
    
    # Create comprehensive dataset
    dataset_sizes = {
        'small': 2000,
        'medium': 5000,
        'large': 10000,
        'xlarge': 20000
    }
    
    print("Available dataset sizes:")
    for name, size in dataset_sizes.items():
        print(f"  {name}: {size} URLs")
    
    # Use medium size by default
    target_size = dataset_sizes['medium']
    
    print(f"\nCreating comprehensive dataset with {target_size} URLs...")
    
    df = integrator.create_comprehensive_dataset(target_size)
    
    if not df.empty:
        # Save the dataset
        output_path = os.path.join('data', 'urls_comprehensive.csv')
        df.to_csv(output_path, index=False)
        
        print(f"\nComprehensive dataset saved to: {output_path}")
        print("\nThis dataset combines:")
        print("- Real phishing URLs from PhishTank and OpenPhish")
        print("- Legitimate URLs from popular websites")
        print("- Synthetic phishing URLs (if needed for balance)")
        
        print(f"\nTo use this dataset, update your training script to load '{output_path}'")
    else:
        print("Failed to create dataset. Check your internet connection and try again.")


if __name__ == "__main__":
    main()