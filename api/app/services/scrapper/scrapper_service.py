#!/usr/bin/env python3
"""
Books to Scrape Web Scraper

This script extracts book information from https://books.toscrape.com/
and saves the data to a CSV file in the data folder.

Required information for each book:
- Title
- Price
- Rating
- Availability
- Category
- Image URL

Author: AI Assistant
Date: 2024
"""

import os
import sys
import time
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
import pandas as pd
from bs4 import BeautifulSoup
import logging
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...models.book_model import Book

logger = logging.getLogger(__name__)


# Add the scripts directory to the path to import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.services.scrapper.scrapper_utils import (
    clean_text, extract_price, extract_rating, check_availability,
    safe_request, validate_url, create_filename, logger
)

# Configuration
BASE_URL = "https://books.toscrape.com/"
CATALOG_URL = urljoin(BASE_URL, "catalogue/")
DELAY_BETWEEN_REQUESTS = 1.0  # Delay between requests to be respectful
MAX_RETRIES = 3


class BooksToScrapeScraper:
    """
    Web scraper for extracting book data from Books to Scrape website.
    """
    
    def __init__(self, base_url: str = BASE_URL, delay: float = DELAY_BETWEEN_REQUESTS):
        """
        Initialize the scraper.
        
        Args:
            base_url (str): Base URL of the website
            delay (float): Delay between requests in seconds
        """
        self.base_url = base_url
        self.delay = delay
        self.session_data = []
        self.categories = {}
        
        # Validate base URL
        if not validate_url(base_url):
            raise ValueError(f"Invalid base URL: {base_url}")
    
    def get_all_category_urls(self) -> List[str]:
        """
        Get all category URLs from the main page.
        
        Returns:
            List[str]: List of category URLs
        """
        logger.info("Fetching category URLs...")
        
        response_data = safe_request(self.base_url)
        if not response_data:
            logger.error("Failed to fetch main page")
            return []
        
        soup = BeautifulSoup(response_data['content'], 'html.parser')
        category_links = []
        
        # Find category links in the sidebar
        sidebar = soup.find('div', class_='side_categories')
        if sidebar:
            links = sidebar.find_all('a')
            for link in links:
                href = link.get('href')
                if href and 'category' in href:
                    #full_url = urljoin(self.base_url, href)
                    full_url = urljoin('https://books.toscrape.com/', href)
                    category_name = clean_text(link.get_text())
                    self.categories[full_url] = category_name
                    category_links.append(full_url)
        
        logger.info(f"Found {len(category_links)} categories")

        #Sending just the valid categories
        return category_links[1:2]
    
    def get_all_book_urls_from_category(self, category_url: str) -> List[str]:
        """
        Get all book URLs from a category page, handling pagination.
        
        Args:
            category_url (str): URL of the category page
            
        Returns:
            List[str]: List of book URLs
        """
        book_urls = []
        current_url = category_url

        while current_url:
            response_data = safe_request(current_url)
            if not response_data:
                logger.error(f"Failed to fetch category page: {current_url}")
                break

            soup = BeautifulSoup(response_data['content'], 'html.parser')

            book_links = soup.find_all('h3')
            for link in book_links:
                parent_link = link.find('a')
                if parent_link:
                    href = parent_link.get('href')
                    if href:
                        full_url = urljoin(current_url, href)
                        book_urls.append(full_url)

            # Check the pagination
            next_button = soup.select_one('li.next > a')
            if next_button:
                next_href = next_button.get('href')
                current_url = urljoin(current_url, next_href)
            else:
                break

        return book_urls

    
    def extract_book_data(self, book_url: str) -> Optional[Dict[str, Any]]:
        """
        Extract book information from a book detail page.
        
        Args:
            book_url (str): URL of the book detail page
            
        Returns:
            Optional[Dict[str, Any]]: Book data dictionary or None if failed
        """
        logger.info(f"Extracting data from: {book_url}")
        print(f'book_url: {book_url}')
        response_data = safe_request(book_url)
        if not response_data:
            logger.error(f"Failed to fetch book page: {book_url}")
            return None
        
        soup = BeautifulSoup(response_data['content'], 'html.parser')
        
        try:
            # Extract title
            title_element = soup.find('h1')
            title = clean_text(title_element.get_text()) if title_element else ""
            
            # Extract price
            price_element = soup.find('p', class_='price_color')
            price_text = price_element.get_text() if price_element else ""
            price = extract_price(price_text)
            
            # Extract rating
            rating_element = soup.find('p', class_='star-rating')
            rating_class = ' '.join(rating_element.get('class', [])) if rating_element else ""
            rating = extract_rating(rating_class)
            
            # Extract availability
            availability_element = soup.find('p', class_='instock availability')
            availability_text = availability_element.get_text() if availability_element else ""
            availability = check_availability(availability_text)
            
            # Extract category
            breadcrumb = soup.find('ul', class_='breadcrumb')
            category = ""
            if breadcrumb:
                category_links = breadcrumb.find_all('a')
                if len(category_links) >= 2:  # Skip home, get category
                    category = clean_text(category_links[2].get_text())
            
            # Extract image URL
            image_element = soup.find('div', class_='item active').find('img') if soup.find('div', class_='item active') else None
            image_url = ""
            if image_element:
                image_src = image_element.get('src')
                if image_src:
                    image_url = urljoin(book_url, image_src)
            
            book_data = {
                'title': title,
                'price': price,
                'rating': rating,
                'availability': availability,
                'category': category,
                'image_url': image_url,
                'book_url': book_url
            }
            
            logger.info(f"Successfully extracted data for: {title}")
            return book_data
            
        except Exception as e:
            logger.error(f"Error extracting data from {book_url}: {e}")
            return None
    
    def scrape_all_books(self) -> List[Dict[str, Any]]:
        """
        Scrape all books from all categories.
        
        Returns:
            List[Dict[str, Any]]: List of all book data
        """
        logger.info("Starting to scrape all books...")
        
        all_books = []
        
        # Get all category URLs
        category_urls = self.get_all_category_urls()
        
        if not category_urls:
            logger.error("No categories found")
            return all_books
        print([url.split('/')[6] for url in category_urls])

        # Scrape books from each category
        for category_url in category_urls:
            category_name = self.categories.get(category_url, "Unknown")
            logger.info(f"Scraping category: {category_name}")
            
            book_urls = self.get_all_book_urls_from_category(category_url)
            
            for book_url in book_urls:
                book_data = self.extract_book_data(book_url)
                if book_data:
                    all_books.append(book_data)
                
                # Be respectful with delays
                time.sleep(self.delay)
        
        logger.info(f"Scraping completed. Total books extracted: {len(all_books)}")
        return all_books
    
    def save_to_csv(self, books_data: List[Dict[str, Any]], output_dir: str = "../data") -> str:
        """
        Save book data to CSV file.
        
        Args:
            books_data (List[Dict[str, Any]]): List of book data dictionaries
            output_dir (str): Output directory for the CSV file
            
        Returns:
            str: Path to the created CSV file
        """
        if not books_data:
            logger.warning("No data to save")
            return ""
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create DataFrame
        df = pd.DataFrame(books_data)
        
        # Create filename with timestamp
        filename = create_filename("books_data")
        filepath = os.path.join(output_dir, filename)
        
        # Save to CSV
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        logger.info(f"Data saved to: {filepath}")
        logger.info(f"Total records: {len(df)}")
        
        # Display summary statistics
        logger.info("Data Summary:")
        logger.info(f"- Total books: {len(df)}")
        logger.info(f"- Categories: {df['category'].nunique()}")
        logger.info(f"- Price range: £{df['price'].min():.2f} - £{df['price'].max():.2f}")
        logger.info(f"- Average price: £{df['price'].mean():.2f}")
        logger.info(f"- Rating distribution: {df['rating'].value_counts().to_dict()}")
        
        return filepath
    
    def save_to_db(self, books_data: List[Dict[str, Any]], db: Session) -> int:
        """
        Salva os dados dos livros no banco via SQLAlchemy.
        
        Args:
            books_data (List[Dict[str, Any]]): lista de dicionários dos livros
            db (Session): sessão do SQLAlchemy para o banco
            
        Returns:
            int: número de registros inseridos
        """
        if not books_data:
            logger.warning("No data to save")
            return 0
        
        books_to_add = []
        for book in books_data:
            b = Book(
                title=book.get("title", ""),
                price=float(book.get("price", 0)),
                category=book.get("category", ""),
                rating=book.get("rating", ""),
                availability=book.get("availability", "")
            )
            books_to_add.append(b)
        
        db.add_all(books_to_add)
        db.commit()
        
        logger.info(f"Inserted {len(books_to_add)} records into the database.")
        return len(books_to_add)

def main():
    """
    Main function to run the scraper.
    """
    try:
        logger.info("Starting Books to Scrape scraper...")
        
        # Initialize scraper
        scraper = BooksToScrapeScraper()
        
        # Scrape all books
        books_data = scraper.scrape_all_books()
        
        if not books_data:
            logger.error("No books were scraped. Exiting.")
            sys.exit(1)
        
        # Save to CSV
        db = next(get_db())
        output_file = scraper.save_to_db(books_data, db)
        
        if output_file:
            logger.info("Scraping completed successfully!")
            logger.info(f"Data saved to: {output_file}")
        else:
            logger.error("Failed to save data")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
