"""
Utility package initialization.
"""
from .helpers import (
    clean_price_string,
    is_amazon_url,
    is_flipkart_url,
    get_platform_from_url,
    calculate_price_change_percentage,
    format_price,
    truncate_string
)
from .notifications import send_email_notification

__all__ = [
    "clean_price_string",
    "is_amazon_url",
    "is_flipkart_url",
    "get_platform_from_url",
    "calculate_price_change_percentage",
    "format_price",
    "truncate_string",
    "send_email_notification",
]
