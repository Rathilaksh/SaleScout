"""
Flipkart scraper for SaleScout.
Fetches product title, image URL, and price.
"""
from typing import Optional, Dict
import time
import requests
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT, MAX_RETRIES
from utils import clean_price_string

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


class FlipkartScrapeError(Exception):
    """Raised when scraping fails after retries."""


def _fetch_html(url: str) -> str:
    last_exc = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                return resp.text
            last_exc = Exception(f"Status {resp.status_code}")
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
        time.sleep(1.5 * attempt)
    raise FlipkartScrapeError(f"Failed to fetch URL after retries: {last_exc}")


def _extract_title(soup: BeautifulSoup) -> Optional[str]:
    title_selectors = [
        "span.B_NuCI",
        "h1.yhB1nd",
        "span.VU-ZEz",
    ]
    for selector in title_selectors:
        el = soup.select_one(selector)
        if el and el.get_text(strip=True):
            return el.get_text(strip=True)
    return None


def _extract_image(soup: BeautifulSoup) -> Optional[str]:
    image_selectors = [
        "img._396cs4._2amPTt._3qGmMb._3exPp9",
        "img._396cs4._2amPTt._3qGmMb",
        "img._396cs4",
        "div.CXW8mj img",
    ]
    for selector in image_selectors:
        el = soup.select_one(selector)
        if el and el.get("src"):
            return el.get("src")
    return None


def _extract_price(soup: BeautifulSoup) -> Optional[float]:
    price_selectors = [
        "div._30jeq3._16Jk6d",
        "div._25b18c div._30jeq3",
        "div._30jeq3",
        "._16Jk6d",
    ]
    for selector in price_selectors:
        el = soup.select_one(selector)
        if el and el.get_text(strip=True):
            price_val = clean_price_string(el.get_text())
            if price_val is not None:
                return price_val
    return None


def scrape_flipkart(url: str) -> Dict[str, Optional[str]]:
    """
    Scrape Flipkart product page for title, image, and price.
    Returns dict with keys: title, image_url, price (float or None).
    """
    html = _fetch_html(url)
    soup = BeautifulSoup(html, "lxml")

    title = _extract_title(soup)
    image_url = _extract_image(soup)
    price = _extract_price(soup)

    return {
        "title": title,
        "image_url": image_url,
        "price": price,
    }
