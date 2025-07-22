"""
Utility functions for web scraping operations.
"""

import re
import time
from typing import Optional, Dict, Any
from urllib.parse import urljoin, urlparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """
    Clean and normalize text by removing extra whitespace and special characters.
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    cleaned = re.sub(r'\s+', ' ', text.strip())
    return cleaned


def extract_price(price_text: str) -> float:
    """
    Extract numeric price from price text.
    
    Args:
        price_text (str): Price text (e.g., "£51.77")
        
    Returns:
        float: Numeric price value
    """
    if not price_text:
        return 0.0
    
    # Extract numeric value from price string
    price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
    if price_match:
        return float(price_match.group())
    return 0.0


def extract_rating(rating_class: str) -> str:
    """
    Extract rating from CSS class name.
    
    Args:
        rating_class (str): CSS class containing rating (e.g., "star-rating One")
        
    Returns:
        str: Rating text (e.g., "One", "Two", etc.)
    """
    if not rating_class:
        return "Not rated"
    
    # Extract rating from class name
    rating_match = re.search(r'star-rating\s+(\w+)', rating_class)
    if rating_match:
        return rating_match.group(1)
    return "Not rated"


def check_availability(availability_text: str) -> str:
    """
    Check and normalize availability status.
    
    Args:
        availability_text (str): Availability text from website
        
    Returns:
        str: Normalized availability status
    """
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
    """
    Make a safe HTTP request with retry logic and error handling.
    
    Args:
        url (str): URL to request
        max_retries (int): Maximum number of retry attempts
        delay (float): Delay between retries in seconds
        
    Returns:
        Optional[Dict[str, Any]]: Response data or None if failed
    """
    import requests
    
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
    """
    Validate if a URL is properly formatted.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def create_filename(base_name: str, extension: str = "csv") -> str:
    """
    Create a filename with timestamp to avoid overwriting.
    
    Args:
        base_name (str): Base name for the file
        extension (str): File extension
        
    Returns:
        str: Formatted filename with timestamp
    """
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.{extension}"
