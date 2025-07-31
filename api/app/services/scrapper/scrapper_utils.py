import re
import requests
import time
from datetime import datetime
from typing import Optional, Dict, Any
from urllib.parse import urlparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    if not text:
        return ""

    cleaned = re.sub(r'\s+', ' ', text.strip())
    return cleaned


def extract_price(price_text: str) -> float:
    if not price_text:
        return 0.0

    price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
    if price_match:
        return float(price_match.group())
    return 0.0


def extract_rating(rating_class: str) -> str:
    if not rating_class:
        return "Not rated"

    rating_match = re.search(r'star-rating\s+(\w+)', rating_class)
    if rating_match:
        return rating_match.group(1)
    return "Not rated"


def check_availability(availability_text: str) -> str:
    if not availability_text:
        return "Unknown"

    availability = clean_text(availability_text).lower()

    if "in stock" in availability:
        return "In Stock"
    elif "out of stock" in availability:
        return "Out of Stock"
    else:
        return availability.title()


def safe_request(url: str, max_retries: int = 3, delay: float = 1.0) -> Optional[Dict[str, Any]]:
    for attempt in range(max_retries):
        try:
            logger.info(f"Requesting: {url} (attempt {attempt + 1}/{max_retries})")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            return {
                'status_code': response.status_code,
                'content': response.content,
                'url': response.url
            }

        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                logger.error(f"All retry attempts failed for {url}")
                return None

    return None


def validate_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def create_filename(base_name: str, extension: str = "csv") -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.{extension}"
