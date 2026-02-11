# Epstein Files - Search, Download & OCR

Command-line tools for searching, downloading, and extracting text from PDFs on justice.gov/epstein.

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

## Installation

```bash
pip install -r requirements.txt
```

Requires Chrome browser and Tesseract OCR to be installed on your system.

## More Documentation

- `docs/` - Detailed user guides and workflows
- `instrs/` - Development instructions
