"""
Data generator for creating a larger, more diverse phishing URL dataset.
This script generates synthetic URLs and can also integrate real datasets.
"""

import pandas as pd
import random
import string
import os
from urllib.parse import urlparse
import requests
from typing import List, Tuple


class URLDatasetGenerator:
    """Generate synthetic phishing and legitimate URLs for training."""
    
    def __init__(self):
        # Common legitimate domains
        self.legitimate_domains = [
            'google.com', 'facebook.com', 'amazon.com', 'microsoft.com', 'apple.com',
            'netflix.com', 'youtube.com', 'instagram.com', 'twitter.com', 'linkedin.com',
            'github.com', 'stackoverflow.com', 'reddit.com', 'wikipedia.org', 'medium.com',
            'paypal.com', 'ebay.com', 'walmart.com', 'target.com', 'bestbuy.com',
            'adobe.com', 'dropbox.com', 'spotify.com', 'zoom.us', 'slack.com',
            'salesforce.com', 'oracle.com', 'ibm.com', 'intel.com', 'nvidia.com',
            'tesla.com', 'uber.com', 'airbnb.com', 'booking.com', 'expedia.com',
            'cnn.com', 'bbc.com', 'nytimes.com', 'washingtonpost.com', 'reuters.com'
        ]
        
        # Suspicious TLDs commonly used in phishing
        self.suspicious_tlds = [
            '.tk', '.ml', '.ga', '.cf', '.gq', '.top', '.click', '.download',
            '.stream', '.science', '.racing', '.review', '.faith', '.accountant',
            '.loan', '.win', '.bid', '.trade', '.date', '.party', '.cricket'
        ]
        
        # Common phishing keywords
        self.phishing_keywords = [
            'verify', 'secure', 'update', 'confirm', 'login', 'account', 'suspended',
            'locked', 'expired', 'urgent', 'immediate', 'action', 'required',
            'security', 'alert', 'warning', 'prize', 'winner', 'free', 'claim',
            'bonus', 'reward', 'gift', 'promotion', 'limited', 'offer'
        ]
        
        # Common legitimate paths
        self.legitimate_paths = [
            '/home', '/about', '/contact', '/products', '/services', '/blog',
            '/news', '/support', '/help', '/faq', '/login', '/register',
            '/account', '/profile', '/settings', '/dashboard', '/search',
            '/category', '/product', '/article', '/page', '/index'
        ]
    
    def generate_legitimate_urls(self, count: int) -> List[Tuple[str, str]]:
        """Generate legitimate-looking URLs."""
        urls = []
        
        for _ in range(count):
            domain = random.choice(self.legitimate_domains)
            
            # Add subdomain sometimes
            if random.random() < 0.3:
                subdomains = ['www', 'mail', 'blog', 'shop', 'support', 'api', 'mobile']
                subdomain = random.choice(subdomains)
                domain = f"{subdomain}.{domain}"
            
            # Add path sometimes
            if random.random() < 0.7:
                path = random.choice(self.legitimate_paths)
                if random.random() < 0.3:  # Add parameters
                    params = f"?id={random.randint(1, 1000)}"
                    path += params
            else:
                path = ""
            
            # Use HTTPS most of the time for legitimate sites
            protocol = 'https' if random.random() < 0.9 else 'http'
            url = f"{protocol}://{domain}{path}"
            
            urls.append((url, 'legitimate'))
        
        return urls
    
    def generate_phishing_urls(self, count: int) -> List[Tuple[str, str]]:
        """Generate phishing URLs with various suspicious patterns."""
        urls = []
        
        for _ in range(count):
            url_type = random.choice(['typosquatting', 'suspicious_tld', 'ip_address', 
                                    'subdomain_spoofing', 'url_shortener', 'keyword_stuffing'])
            
            if url_type == 'typosquatting':
                url = self._generate_typosquatting_url()
            elif url_type == 'suspicious_tld':
                url = self._generate_suspicious_tld_url()
            elif url_type == 'ip_address':
                url = self._generate_ip_url()
            elif url_type == 'subdomain_spoofing':
                url = self._generate_subdomain_spoofing_url()
            elif url_type == 'url_shortener':
                url = self._generate_url_shortener_url()
            else:  # keyword_stuffing
                url = self._generate_keyword_stuffing_url()
            
            urls.append((url, 'phishing'))
        
        return urls
    
    def _generate_typosquatting_url(self) -> str:
        """Generate URLs with typos in legitimate domain names."""
        domain = random.choice(self.legitimate_domains)
        
        # Common typosquatting techniques
        techniques = [
            lambda d: d.replace('o', '0'),  # Replace o with 0
            lambda d: d.replace('e', '3'),  # Replace e with 3
            lambda d: d.replace('a', '@'),  # Replace a with @
            lambda d: d.replace('i', '1'),  # Replace i with 1
            lambda d: d.replace('l', '1'),  # Replace l with 1
            lambda d: d.replace('.com', '.co'),  # Remove m
            lambda d: d + 'm',  # Add extra m
            lambda d: d.replace('google', 'g00gle'),  # Mix of techniques
            lambda d: d.replace('amazon', 'amaz0n'),
            lambda d: d.replace('paypal', 'payp4l'),
        ]
        
        technique = random.choice(techniques)
        fake_domain = technique(domain)
        
        protocol = 'http' if random.random() < 0.8 else 'https'
        path = f"/{random.choice(self.phishing_keywords)}"
        
        return f"{protocol}://{fake_domain}{path}"
    
    def _generate_suspicious_tld_url(self) -> str:
        """Generate URLs with suspicious TLDs."""
        base_name = random.choice(['secure', 'verify', 'account', 'login', 'update'])
        brand = random.choice(['paypal', 'amazon', 'google', 'microsoft', 'apple'])
        tld = random.choice(self.suspicious_tlds)
        
        domain = f"{base_name}-{brand}{tld}"
        path = f"/{random.choice(self.phishing_keywords)}"
        
        return f"http://{domain}{path}"
    
    def _generate_ip_url(self) -> str:
        """Generate URLs with IP addresses instead of domain names."""
        # Generate random IP (avoiding reserved ranges for realism)
        ip_parts = []
        for i in range(4):
            if i == 0:
                ip_parts.append(str(random.randint(1, 223)))  # Avoid 0 and reserved
            else:
                ip_parts.append(str(random.randint(0, 255)))
        
        ip = '.'.join(ip_parts)
        path = f"/{random.choice(['login', 'admin', 'secure', 'verify'])}.php"
        
        return f"http://{ip}{path}"
    
    def _generate_subdomain_spoofing_url(self) -> str:
        """Generate URLs that use legitimate domains as subdomains."""
        legitimate = random.choice(self.legitimate_domains).replace('.com', '').replace('.org', '')
        fake_tld = random.choice(self.suspicious_tlds)
        fake_domain = f"secure-{legitimate}{fake_tld}"
        
        path = f"/{random.choice(self.phishing_keywords)}"
        
        return f"http://{fake_domain}{path}"
    
    def _generate_url_shortener_url(self) -> str:
        """Generate suspicious URL shortener links."""
        shorteners = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly']
        shortener = random.choice(shorteners)
        
        # Generate random short code
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        
        return f"http://{shortener}/{short_code}"
    
    def _generate_keyword_stuffing_url(self) -> str:
        """Generate URLs stuffed with phishing keywords."""
        keywords = random.sample(self.phishing_keywords, 2)
        domain_name = '-'.join(keywords)
        tld = random.choice(['.com', '.net'] + self.suspicious_tlds)
        
        return f"http://{domain_name}{tld}/index.php"
    
    def download_real_datasets(self) -> pd.DataFrame:
        """
        Download and combine real phishing datasets from public sources.
        Note: This requires internet connection and the datasets to be available.
        """
        print("Attempting to download real phishing datasets...")
        
        # This is a placeholder for real dataset integration
        # In practice, you would download from sources like:
        # - PhishTank API
        # - OpenPhish feeds
        # - Academic datasets
        
        real_data = []
        
        # Example of how you might integrate PhishTank data
        # (This is commented out as it requires API key and proper setup)
        """
        try:
            # PhishTank API example (requires API key)
            response = requests.get('http://data.phishtank.com/data/online-valid.csv')
            if response.status_code == 200:
                # Process PhishTank data
                pass
        except Exception as e:
            print(f"Could not download PhishTank data: {e}")
        """
        
        print("Real dataset download not implemented in this demo.")
        print("Consider integrating datasets from:")
        print("- PhishTank (https://www.phishtank.com/)")
        print("- OpenPhish (https://openphish.com/)")
        print("- URLVoid API")
        print("- Academic phishing datasets")
        
        return pd.DataFrame(real_data)
    
    def generate_balanced_dataset(self, total_size: int = 10000) -> pd.DataFrame:
        """Generate a balanced dataset with equal phishing and legitimate URLs."""
        half_size = total_size // 2
        
        print(f"Generating {half_size} legitimate URLs...")
        legitimate_urls = self.generate_legitimate_urls(half_size)
        
        print(f"Generating {half_size} phishing URLs...")
        phishing_urls = self.generate_phishing_urls(half_size)
        
        # Combine and shuffle
        all_urls = legitimate_urls + phishing_urls
        random.shuffle(all_urls)
        
        # Create DataFrame
        df = pd.DataFrame(all_urls, columns=['url', 'label'])
        
        print(f"\nGenerated dataset statistics:")
        print(f"Total URLs: {len(df)}")
        print(f"Legitimate: {len(df[df['label'] == 'legitimate'])}")
        print(f"Phishing: {len(df[df['label'] == 'phishing'])}")
        
        return df


def main():
    """Generate expanded dataset and save to CSV."""
    generator = URLDatasetGenerator()
    
    # Generate different sized datasets
    sizes = {
        'small': 1000,
        'medium': 5000,
        'large': 10000,
        'xlarge': 20000
    }
    
    print("URL Dataset Generator")
    print("=" * 50)
    print("Available dataset sizes:")
    for name, size in sizes.items():
        print(f"  {name}: {size} URLs")
    
    # Default to medium size
    dataset_size = sizes['medium']
    
    # Generate dataset
    print(f"\nGenerating dataset with {dataset_size} URLs...")
    df = generator.generate_balanced_dataset(dataset_size)
    
    # Save to CSV
    output_path = os.path.join('data', 'urls_expanded.csv')
    df.to_csv(output_path, index=False)
    
    print(f"\nDataset saved to: {output_path}")
    print("\nTo use this expanded dataset, update your training script to load 'urls_expanded.csv'")
    
    # Also create a backup of original small dataset
    original_path = os.path.join('data', 'urls_original_small.csv')
    if os.path.exists(os.path.join('data', 'urls.csv')) and not os.path.exists(original_path):
        import shutil
        shutil.copy(os.path.join('data', 'urls.csv'), original_path)
        print(f"Original small dataset backed up to: {original_path}")


if __name__ == "__main__":
    main()