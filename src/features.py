"""URL feature extraction utilities for phishing detection."""

import re
from urllib.parse import urlparse


def url_length(url: str) -> int:
    """Return total number of characters in the URL string."""
    return len(url)


def count_char(url: str, ch: str) -> int:
    """Return the number of occurrences of a specific character in the URL."""
    return url.count(ch)


def get_hostname(url: str) -> str:
    """
    Extract hostname from URL using urllib.parse.
    If empty, try adding http:// prefix before parsing.
    """
    parsed = urlparse(url)
    hostname = parsed.netloc
    
    # If no hostname found, try adding scheme
    if not hostname:
        parsed = urlparse(f"http://{url}")
        hostname = parsed.netloc
    
    return hostname


def num_dots_in_hostname(url: str) -> int:
    """Parse hostname and count occurrences of '.'."""
    hostname = get_hostname(url)
    return hostname.count('.')


def has_ip_address(url: str) -> int:
    """Return 1 if hostname looks like an IPv4 address, else 0."""
    hostname = get_hostname(url)
    # Simple IPv4 pattern: digits.digits.digits.digits
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    return 1 if re.match(ip_pattern, hostname) else 0


def uses_https(url: str) -> int:
    """Return 1 if URL scheme is https, else 0."""
    parsed = urlparse(url)
    return 1 if parsed.scheme == 'https' else 0


def has_suspicious_tld(url: str) -> int:
    """
    Return 1 if the hostname ends with a suspicious TLD, else 0.
    Suspicious TLDs: .zip, .tk, .xyz, .top, .gq, .ml, .ga, .cf
    """
    suspicious_tlds = [".zip", ".tk", ".xyz", ".top", ".gq", ".ml", ".ga", ".cf"]
    hostname = get_hostname(url).lower()
    
    for tld in suspicious_tlds:
        if hostname.endswith(tld):
            return 1
    return 0


def is_shortened(url: str) -> int:
    """
    Return 1 if hostname belongs to a URL shortener, else 0.
    Common shorteners: bit.ly, goo.gl, tinyurl.com, t.co, ow.ly, bitly.com
    """
    shorteners = ["bit.ly", "goo.gl", "tinyurl.com", "t.co", "ow.ly", "bitly.com"]
    hostname = get_hostname(url).lower()
    
    return 1 if hostname in shorteners else 0


def extract_features_from_url(url: str) -> list:
    """
    Return a list of numeric features for a single URL, in a fixed order.
    
    Features (in order):
    1. URL length
    2. Number of dots (.) in URL
    3. Number of hyphens (-) in URL
    4. Number of underscores (_) in URL
    5. Number of slashes (/) in URL
    6. Number of question marks (?) in URL
    7. Number of equals (=) in URL
    8. Number of at symbols (@) in URL
    9. Number of ampersands (&) in URL
    10. Number of dots in hostname
    11. Has IP address (1/0)
    12. Uses HTTPS (1/0)
    13. Has suspicious TLD (1/0)
    14. Is shortened URL (1/0)
    
    Returns:
        list: A list of 14 numeric features
    """
    features = [
        url_length(url),
        count_char(url, '.'),
        count_char(url, '-'),
        count_char(url, '_'),
        count_char(url, '/'),
        count_char(url, '?'),
        count_char(url, '='),
        count_char(url, '@'),
        count_char(url, '&'),
        num_dots_in_hostname(url),
        has_ip_address(url),
        uses_https(url),
        has_suspicious_tld(url),
        is_shortened(url)
    ]
    
    return features


def get_feature_names() -> list:
    """Return the names of all features in order."""
    return [
        'url_length',
        'num_dots',
        'num_hyphens',
        'num_underscores',
        'num_slashes',
        'num_question_marks',
        'num_equals',
        'num_at_symbols',
        'num_ampersands',
        'num_dots_hostname',
        'has_ip_address',
        'uses_https',
        'has_suspicious_tld',
        'is_shortened'
    ]
