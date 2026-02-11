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

4. **Verify installation**
   ```bash
   python -c "import pytesseract; print('OCR ready')"
   ```

## Quick Start

### 1. Search and Download PDFs

```bash
python src/search_and_download.py "flight logs" --pages <start> <end>
```

Downloads PDFs matching your search to `pdfs/` directory and saves URLs to `data/flight_logs_urls.txt`.

**Options:**
```bash
# Custom output directory
python src/search_and_download.py "black book" --output-dir pdfs/blackbook

# Extract specific page range (pages 10-20)
python src/search_and_download.py "email" --pages 10 20

# Custom URL file location
python src/search_and_download.py "documents" --url-file data/custom.txt

# Headless mode (experimental)
python src/search_and_download.py "term" --headless
```

### 2. Extract Text from PDFs (OCR)

```bash
python src/superocr.py
```

Processes all PDFs in `pdfs/` directory and saves extracted text to `texts/` directory.

**Options:**
```bash
# Custom directories
python src/superocr.py --pdf-dir my_pdfs --output-dir my_texts

# Use more CPU cores (faster processing)
python src/superocr.py --cores 10

# Different language (e.g., Spanish)
python src/superocr.py --language spa

# Verbose logging
python src/superocr.py --verbose
```

## Typical Workflow

```bash
# 1. Search and download PDFs
python src/search_and_download.py "flight logs"

# 2. Extract text from downloaded PDFs
python src/superocr.py

# 3. Text files are now in texts/ directory
ls texts/
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
