# FIAP Machine Learning Engineering - Tech Challenge 1

A comprehensive project that includes both a web scraper for book data extraction and a REST API for data management.

## Features

- **Web Scraper**: Extracts book data from [Books to Scrape](https://books.toscrape.com/)
- **REST API**: Provides endpoints for user management and data access
- **Data Processing**: CSV export with comprehensive book information

![image]()

-----------------------------------

1. [Installation](#installation)
2. [Web Scraper](#web-scraper)
3. [API](#api)
4. [Project Structure](#structure)
5. [Licensing, Authors and Acknowledgments](#licensing)

## Installation <a name="installation"></a>

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Setup 

 1. Clone the project
 2. Create/activate the virtual environment

Linux/macOS:

```
python3 -m venv venv
source venv/bin/activate
```
Windows

```
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```
pip install -r requirements.txt
```


## Web Scraper <a name="web-scraper"></a>

The web scraper extracts comprehensive book data from the Books to Scrape website.

### Quick Start

1. Navigate to the scripts directory:
```bash
cd api
```
2. Run the scraper:
```bash
python -m app.services.scrapper.scrapper_service
```

### Features

- **Complete Data Extraction**: Title, price, rating, availability, category, image URL
- **Robust Error Handling**: Retry logic and comprehensive logging
- **Respectful Scraping**: Configurable delays and rate limiting
- **Pagination Support**: Automatically handles multi-page categories
- **Data Quality**: Text cleaning and normalization

### Output

The scraper creates a CSV file in the `data/` directory with the following columns:
- `title`: Book title
- `price`: Numeric price value
- `rating`: Star rating (One, Two, Three, Four, Five)
- `availability`: Availability status
- `category`: Book category
- `image_url`: Full URL to the book cover image
- `book_url`: URL to the book detail page

### Configuration

You can modify the following in `scripts/scrapper.py`:
- `DELAY_BETWEEN_REQUESTS`: Delay between requests (default: 1.0 seconds)
- `MAX_RETRIES`: Maximum retry attempts (default: 3)

## API <a name="api"></a>

### Quick Start

1. Create and activate a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
# Option 1: Using pip directly
pip install -r requirements.txt

# Option 2: Using the installation script
python install_dependencies.py
```

> **Note**: If you encounter import errors, make sure to run the installation script to properly install all dependencies.

3. Run the script to start the server:
```bash
# Option 1: Standard startup
python start_server.py

# Option 2: Startup with dependency checks (recommended if you have import errors)
python start_server_with_checks.py
```

4. Or navigate to the API directory and run:
```bash
cd api
uvicorn main:app --reload
```

### Available Endpoints

- `GET /api/v1/books`: List all books
- `GET /api/v1/books/search?title=&category=`: Search books by title and category
- `GET /api/v1/books/{id}`: Get a book by ID

### Endpoint GET /api/v1/books/{id}

This endpoint returns the details of a specific book by its ID.

**Example Response (Book found):**
```json
{
  "id": 1,
  "title": "A Light in the Attic",
  "price": 51.77,
  "availability": "In stock",
  "rating": "Three",
  "category": "Poetry"
}
```

**Example Response (Book not found):**
```json
{
  "detail": "Error Book not found."
}
```

### Compatibility Issues

If you encounter compatibility issues when running the API, try:

1. Using Python 3.9 or 3.10 instead of newer versions
2. Running the `simulate_endpoint.py` script to test functionality without starting the server
3. Checking if the dependency versions in `requirements.txt` are compatible with your Python version

## Project Structure <a name="structure"></a>

```
fiap-machine-learning-tech-challenge-1/
├── api/                    # REST API application
│   ├── app/
│   │   ├── controllers/    # API controllers
│   │   ├── core/          # Core functionality (auth, database)
│   │   ├── models/        # Data models
│   │   ├── schemas/       # Pydantic schemas
│   │   └── services/      # Business logic
│   ├── main.py            # FastAPI application entry point
│   └── requirements.txt   # API dependencies
├── scripts/               # Web scraping tools
│   ├── scrapper.py        # Main scraper script
│   ├── demo_scrapper.py   # Demo version for testing
│   ├── test_scrapper.py   # Test script
│   ├── utils.py           # Utility functions
│   ├── requirements.txt   # Scraper dependencies
│   ├── run_scrapper.bat   # Windows batch file
│   └── README.md          # Scraper documentation
├── data/                  # Output directory for scraped data
└── README.md              # This file
```

![image]()

## Troubleshooting

### Import Errors

If you encounter import errors like `Unable to import 'fastapi'` or `Unable to import 'sqlalchemy'`, follow these steps:

1. Make sure you have activated your virtual environment
2. Run the environment check script to diagnose and fix issues:
   ```bash
   python check_environment.py
   ```
   This script will check your Python version, installed dependencies, and project structure, and offer to install any missing dependencies.

3. Alternatively, run the installation script to install all dependencies:
   ```bash
   python install_dependencies.py
   ```

4. If the issue persists, try installing the dependencies manually:
   ```bash
   pip install fastapi==0.95.2 uvicorn==0.22.0 pydantic==1.10.8 sqlalchemy==1.4.48 beautifulsoup4==4.12.2 requests==2.31.0
   ```

## Compatibility Issues

This project was developed and tested with Python 3.8+. Some compatibility issues may occur with older versions.

## Licensing, Authors and Acknowledgments<a name="licensing"></a>
