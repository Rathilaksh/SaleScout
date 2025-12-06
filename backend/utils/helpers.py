"""
Helper utility functions for SaleScout.
"""
import re
from typing import Optional
from urllib.parse import urlparse


def clean_price_string(price_str: str) -> Optional[float]:
    """
    Extract numeric price from a string containing currency symbols and formatting.
    
    Examples:
        "₹1,234.56" -> 1234.56
        "$1,234.99" -> 1234.99
        "Rs. 999" -> 999.0
        "1234" -> 1234.0
    
    Args:
        price_str: String containing price with possible currency symbols
        
    Returns:
        Float value of price, or None if parsing fails
    """
    if not price_str:
        return None
    
    # Remove currency symbols, commas, and whitespace
    cleaned = re.sub(r'[₹$,\s]', '', price_str)
    
    # Remove 'Rs' or 'rs' if present
    cleaned = re.sub(r'[Rr]s\.?', '', cleaned)
    
    # Extract first number (handles cases like "1,234.56 - 2,345.67")
    match = re.search(r'[\d]+\.?\d*', cleaned)
    if match:
        try:
            return float(match.group())
        except ValueError:
            return None
    
    return None


def is_amazon_url(url: str) -> bool:
    """
    Check if a URL is from Amazon.
    
    Args:
        url: Product URL
        
    Returns:
        True if Amazon URL, False otherwise
    """
    parsed = urlparse(url)
    return 'amazon' in parsed.netloc.lower()


def is_flipkart_url(url: str) -> bool:
    """
    Check if a URL is from Flipkart.
    
    Args:
        url: Product URL
        
    Returns:
        True if Flipkart URL, False otherwise
    """
    parsed = urlparse(url)
    return 'flipkart' in parsed.netloc.lower()


def get_platform_from_url(url: str) -> Optional[str]:
    """
    Determine the e-commerce platform from a URL.
    
    Args:
        url: Product URL
        
    Returns:
        Platform name ('amazon', 'flipkart') or None if unknown
    """
    if is_amazon_url(url):
        return 'amazon'
    elif is_flipkart_url(url):
        return 'flipkart'
    return None


def calculate_price_change_percentage(old_price: float, new_price: float) -> float:
    """
    Calculate percentage change between two prices.
    
    Args:
        old_price: Previous price
        new_price: Current price
        
    Returns:
        Percentage change (negative for price drop, positive for increase)
    """
    if old_price == 0:
        return 0.0
    
    change = ((new_price - old_price) / old_price) * 100
    return round(change, 2)


def format_price(price: float, currency: str = "₹") -> str:
    """
    Format a price value with currency symbol and proper formatting.
    
    Args:
        price: Price value
        currency: Currency symbol (default: ₹)
        
    Returns:
        Formatted price string
    """
    return f"{currency}{price:,.2f}"


def truncate_string(text: str, max_length: int = 100) -> str:
    """
    Truncate a string to maximum length, adding ellipsis if needed.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
