# Books to Scrape Web Scraper

A comprehensive web scraper for extracting book data from [Books to Scrape](https://books.toscrape.com/), a demo website designed for web scraping practice.

## Features

- **Complete Data Extraction**: Extracts all required book information:
  - Title
  - Price (numeric format)
  - Rating (star rating)
  - Availability status
  - Category
  - Image URL
  - Book URL

- **Robust Error Handling**: 
  - Retry logic for failed requests
  - Graceful handling of network errors
  - Comprehensive logging

- **Respectful Scraping**:
  - Configurable delays between requests
  - User-Agent headers
  - Rate limiting to avoid overwhelming the server

- **Pagination Support**: Automatically handles multi-page categories

- **Data Quality**: 
  - Text cleaning and normalization
  - Price extraction and formatting
  - Rating normalization
  - Availability status standardization

## Requirements

- Python 3.7+
- Internet connection

## Installation

1. Navigate to the scripts directory:
```bash
cd scripts
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper from the scripts directory:

```bash
python scrapper.py
```

The script will:
1. Fetch all category URLs from the main page
2. Extract all book URLs from each category (handling pagination)
3. Scrape detailed information from each book page
4. Save all data to a CSV file in the `../data/` directory

### Output

The scraper creates a CSV file with the following columns:
- `title`: Book title
- `price`: Numeric price value
- `rating`: Star rating (One, Two, Three, Four, Five)
- `availability`: Availability status (In Stock, Out of Stock, etc.)
- `category`: Book category
- `image_url`: Full URL to the book cover image
- `book_url`: URL to the book detail page

### Configuration

You can modify the following constants in `scrapper.py`:

- `DELAY_BETWEEN_REQUESTS`: Delay between requests (default: 1.0 seconds)
- `MAX_RETRIES`: Maximum retry attempts for failed requests (default: 3)

## File Structure

```
scripts/
├── scrapper.py          # Main scraper script
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
└── README.md           # This file

data/                   # Output directory (created automatically)
└── books_data_YYYYMMDD_HHMMSS.csv  # Generated CSV file
```

## Error Handling

The scraper includes comprehensive error handling:

- **Network Errors**: Automatic retry with exponential backoff
- **Missing Data**: Graceful handling of missing elements
- **Invalid URLs**: URL validation before requests
- **Keyboard Interrupt**: Clean shutdown on Ctrl+C

## Logging

The scraper provides detailed logging including:
- Progress updates for each category and book
- Error messages with context
- Summary statistics after completion
- Request status and timing information

## Example Output

```
2024-01-15 10:30:00 - INFO - Starting Books to Scrape scraper...
2024-01-15 10:30:01 - INFO - Fetching category URLs...
2024-01-15 10:30:02 - INFO - Found 50 categories
2024-01-15 10:30:02 - INFO - Scraping category: Travel
2024-01-15 10:30:03 - INFO - Found 11 books in category
2024-01-15 10:30:04 - INFO - Successfully extracted data for: A Light in the Attic
...
2024-01-15 10:35:00 - INFO - Scraping completed. Total books extracted: 1000
2024-01-15 10:35:01 - INFO - Data saved to: ../data/books_data_20240115_103500.csv
2024-01-15 10:35:01 - INFO - Data Summary:
2024-01-15 10:35:01 - INFO - - Total books: 1000
2024-01-15 10:35:01 - INFO - - Categories: 50
2024-01-15 10:35:01 - INFO - - Price range: £10.00 - £60.00
2024-01-15 10:35:01 - INFO - - Average price: £35.50
```

## Notes

- This scraper is designed for educational purposes and respects the target website
- The Books to Scrape website is specifically designed for web scraping practice
- All prices and ratings on the website are randomly assigned and have no real meaning
- The scraper includes appropriate delays to avoid overwhelming the server

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're running from the scripts directory and have installed requirements
2. **Network Timeouts**: Increase the timeout value in `utils.py` if needed
3. **Permission Errors**: Ensure you have write permissions for the data directory

### Performance

- The scraper processes approximately 1 book per second (with 1-second delays)
- For 1000 books, expect the process to take about 20-30 minutes
- You can reduce delays for faster scraping, but be respectful of the server

## License

This project is for educational purposes. Please respect the target website's terms of service and robots.txt file. 