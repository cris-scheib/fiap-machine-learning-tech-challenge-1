# FIAP Machine Learning Engineering - Tech Challenge 1

A comprehensive project that includes both a web scraper for book data extraction and a REST API for data management.

## Features

- **Web Scraper**: Extracts book data from [Books to Scrape](https://books.toscrape.com/)
- **REST API**: Provides endpoints for user management and data access
- **Data Processing**: CSV export with comprehensive book information

![image]()

-----------------------------------

1. [Instalação](#installation)
2. [Web Scraper](#web-scraper)
3. [API](#api)
4. [Estrutura do Projeto](#structure)
5. [Licenciamento, Autores e Agradecimentos](#licensing)

## Instalação <a name="installation"></a>

### Prerequisites
- Python 3.7+
- pip (Python package installer)

## Web Scraper <a name="web-scraper"></a>

The web scraper extracts comprehensive book data from the Books to Scrape website.

### Quick Start

1. Navigate to the scripts directory:
```bash
cd scripts
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the scraper:
```bash
python scrapper.py
```

### Features

- **Complete Data Extraction**: Title, price, rating, availability, category, image URL
- **Robust Error Handling**: Retry logic and comprehensive logging
- **Respectful Scraping**: Configurable delays and rate limiting
- **Pagination Support**: Automatically handles multi-page categories
- **Data Quality**: Text cleaning and normalization

### Demo Mode

To test the scraper with just a few books:
```bash
python demo_scrapper.py
```

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

### Setup

1. Entre na pasta da API
2. Crie e ative o ambiente virtual

- Linux/macOS:

```
python3 -m venv venv
source venv/bin/activate
```
- Windows

```
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências

```
pip install -r requirements.txt
```

4. Rode a API
```
uvicorn main:app --reload
```

## Estrutura do Projeto <a name="structure"></a>

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

## Licenciamento, Autores e Agradecimentos<a name="licensing"></a>
