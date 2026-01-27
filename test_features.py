"""Test script to verify feature extraction works correctly."""

import sys
import os
sys.path.insert(0, 'src')

from features import (
    url_length, count_char, get_hostname, num_dots_in_hostname,
    has_ip_address, uses_https, has_suspicious_tld, is_shortened,
    extract_features_from_url, get_feature_names
)


def test_feature_extraction():
    """Test feature extraction on sample URLs."""
    
    test_urls = [
        "https://www.google.com",
        "http://192.168.1.1/login.php",
        "http://secure-paypal-verify.tk/account",
        "http://bit.ly/free-iphone-win"
    ]
    
    print("="*70)
    print("FEATURE EXTRACTION TEST")
    print("="*70)
    
    feature_names = get_feature_names()
    
    for url in test_urls:
        print(f"\nURL: {url}")
        print("-"*70)
        
        features = extract_features_from_url(url)
        
        for name, value in zip(feature_names, features):
            print(f"  {name:25s}: {value}")
        
        print()


def test_individual_functions():
    """Test individual feature functions."""
    
    print("="*70)
    print("INDIVIDUAL FUNCTION TESTS")
    print("="*70)
    
    test_url = "http://secure-paypal-verify.tk/account?user=test&id=123"
    
    print(f"\nTest URL: {test_url}\n")
    
    tests = [
        ("url_length", url_length(test_url)),
        ("count_char('.', url)", count_char(test_url, '.')),
        ("count_char('-', url)", count_char(test_url, '-')),
        ("get_hostname", get_hostname(test_url)),
        ("num_dots_in_hostname", num_dots_in_hostname(test_url)),
        ("has_ip_address", has_ip_address(test_url)),
        ("uses_https", uses_https(test_url)),
        ("has_suspicious_tld", has_suspicious_tld(test_url)),
        ("is_shortened", is_shortened(test_url)),
    ]
    
    for name, result in tests:
        print(f"  {name:30s}: {result}")
    
    print("\n" + "="*70)
    print("✓ All tests completed successfully!")
    print("="*70)


if __name__ == "__main__":
    test_individual_functions()
    print("\n")
    test_feature_extraction()
