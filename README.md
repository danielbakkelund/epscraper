# Epstein Files - Search, Download & OCR

Command-line tools for searching, downloading, and extracting text from PDFs on justice.gov/epstein.

## Installation

### Prerequisites

**Required:**
- Python 3.8 or higher
- Google Chrome browser
- Tesseract OCR
- Poppler (for PDF processing)

**Install system dependencies:**

**macOS:**
```bash
brew install tesseract poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils
```

**Windows:**
- Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
- Download Poppler from: https://github.com/oschwartz10612/poppler-windows/releases/
- Add both to your PATH environment variable

### Setup

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd epstein
   ```

2. **Create and activate a virtual environment (recommended)**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate it
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set PYTHONPATH** (required for importing the package)
   ```bash
   # On macOS/Linux:
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   
   # On Windows:
   set PYTHONPATH=%PYTHONPATH%;%CD%\src
   ```

5. **Verify installation**
   ```bash
   python -c "import pytesseract; print('OCR ready')"
   python -c "from epscrape import search_and_download, process_all_pdfs; print('Package ready')"
   ```

## Quick Start

### 1. Search and Download PDFs

**Command-line:**
```bash
python src/epscrape/search_and_download.py "flight logs" --pages <start> <end>
```

**Or use as a Python package:**
```python
from epscrape import search_and_download

search_and_download("flight logs", output_dir="./pdfs")
```

Downloads PDFs matching your search to `pdfs/` directory and saves URLs to `data/flight_logs_urls.txt`.

**Options:**
```bash
# Custom output directory
python src/epscrape/search_and_download.py "black book" --output-dir pdfs/blackbook

# Extract specific page range (pages 10-20)
python src/epscrape/search_and_download.py "email" --pages 10 20

# Custom URL file location
python src/epscrape/search_and_download.py "documents" --url-file data/custom.txt

# Headless mode (experimental)
python src/epscrape/search_and_download.py "term" --headless
```

### 2. Extract Text from PDFs (OCR)

**Command-line:**
```bash
python src/epscrape/superocr.py
```

**Or use as a Python package:**
```python
from epscrape import process_all_pdfs

process_all_pdfs(pdf_dir="pdfs", output_dir="texts", num_cores=5)
```

Processes all PDFs in `pdfs/` directory and saves extracted text to `texts/` directory.

**Options:**
```bash
# Custom directories
python src/epscrape/superocr.py --pdf-dir my_pdfs --output-dir my_texts

# Use more CPU cores (faster processing)
python src/epscrape/superocr.py --cores 10

# Different language (e.g., Spanish)
python src/epscrape/superocr.py --language spa

# Verbose logging
python src/epscrape/superocr.py --verbose
```

## Usage as Python Package

The `epscrape` package provides two main functions for programmatic use:

```python
from epscrape import search_and_download, process_all_pdfs

# Search and download PDFs
num_urls, num_downloaded = search_and_download(
    search_string="flight logs",
    output_dir="./pdfs",
    url_file=None,           # Optional custom URL file path
    headless=False,          # Set to True for headless browser
    start_page=1,            # First page to extract from
    end_page=None            # Last page (None = all pages)
)

# Extract text from PDFs using OCR
stats = process_all_pdfs(
    pdf_dir="pdfs",          # Directory containing PDFs
    output_dir="texts",      # Directory for extracted text
    language="eng",          # Tesseract language code
    num_cores=5              # Number of parallel processes
)
```

## Typical Workflow

**Command-line:**
```bash
# 1. Search and download PDFs
python src/epscrape/search_and_download.py "flight logs"

# 2. Extract text from downloaded PDFs
python src/epscrape/superocr.py

# 3. Text files are now in texts/ directory
ls texts/
```

**Python package:**
```python
from epscrape import search_and_download, process_all_pdfs

# 1. Search and download PDFs
search_and_download("flight logs")

# 2. Extract text from downloaded PDFs
process_all_pdfs()

# 3. Text files are now in texts/ directory
```

## Notes

- **Browser windows** will open during search/download (required for age verification)
- **Age verification** is handled automatically
- **CAPTCHA** may require one manual click per session
- **Already processed** files are automatically skipped by OCR
- **Empty/image-only** PDFs are marked as "empty file"

## Troubleshooting

**"Tesseract not found" error:**
- Ensure Tesseract is installed and in your PATH
- On macOS: `which tesseract` should show the installation path
- On Windows: Add Tesseract installation directory to PATH

**Chrome driver issues:**
- The tool uses `undetected-chromedriver` which auto-downloads drivers
- Ensure Chrome browser is up to date

**PDF processing errors:**
- Verify Poppler is installed: `pdftoppm -v`
- On macOS: `brew install poppler`

## More Documentation

- `docs/` - Detailed user guides and workflows
- `instrs/` - Development instructions
