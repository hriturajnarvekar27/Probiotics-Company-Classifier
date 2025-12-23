# scraper_utils.py
# Utility functions to fetch website pages safely

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "DT-Probiotics-Classifier/1.0"
}

TIMEOUT = 8


def fetch_page(url, errors):
    """
    Fetches a webpage.
    If it fails, logs error instead of crashing.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        return response.text
    except Exception as e:
        errors.append(f"Failed to fetch {url}: {str(e)}")
        return None


def extract_visible_text(html):
    """
    Extracts visible text from a webpage.
    """
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(" ", strip=True)
