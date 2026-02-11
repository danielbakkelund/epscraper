# Supersearcher Module

A Python module for searching and extracting PDF URLs from the justice.gov Epstein library search page.

## Overview

This module simulates a user interacting with the search functionality on `https://www.justice.gov/epstein/search`. It:

1. Navigates to the search page
2. Handles age verification (clicks "Yes, I am 18+")
3. Enters search terms in the search field
4. Extracts PDF URLs from search results
5. Handles pagination to get all results
6. Saves URLs to a text file

## Requirements

- Python 3.7+
- undetected-chromedriver
- selenium
- Chrome browser installed

Install dependencies:
```bash
pip install -r requirements.txt
```

## Command Line Usage

Basic search:
```bash
python src/supersearcher.py "search terms"
```

With custom output file:
```bash
python src/supersearcher.py "search terms" --output data/custom.txt
```

Headless mode (experimental):
```bash
python src/supersearcher.py "search terms" --headless
```

## Module Usage

```python
from supersearcher import search_pdfs

# Basic search - saves to data/flight_logs_urls.txt
urls = search_pdfs('flight logs')

# Custom output file
urls = search_pdfs('black book', 'data/blackbook.txt')

# Get URLs without automatic saving
from supersearcher import PDFSearcher

with PDFSearcher() as searcher:
    urls = searcher.search_and_extract('documents')
    # Process URLs as needed
```

## Output

URLs are appended to the output file (one per line). The default output file is:
```
data/<search_terms>_urls.txt
```

Where spaces in search terms are replaced with underscores.

## Notes

- The browser runs in visible mode by default (Chrome window will appear)
- Age verification is automatically handled
- Search results are dynamically loaded via JavaScript
- Pagination is automatically handled to retrieve all results
- The module uses undetected-chromedriver to avoid bot detection

## See Also

- `instrs/searcher_instructions.md` - Detailed requirements
- `example_searcher_usage.py` - Usage examples
- `src/superscraper.py` - Related scraper module
- `src/superdownloader.py` - PDF downloader module
