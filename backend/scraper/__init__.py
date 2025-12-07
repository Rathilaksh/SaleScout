"""
Scraper package exports.
"""
from .amazon_scraper import scrape_amazon, scrape_amazon_playwright
from .flipkart_scraper import scrape_flipkart

__all__ = [
    "scrape_amazon",
    "scrape_amazon_playwright",
    "scrape_flipkart",
]
