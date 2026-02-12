# Epstein Files

Search, download, and extract text from PDFs on justice.gov/epstein.

## Install

```bash
pip install epstein-files
```

## Quick Start

```bash
# Search and download PDFs
epstein-search "flight logs"

# Extract text with OCR
epstein-ocr
```

## Requirements

- Python 3.8+
- Google Chrome
- Tesseract OCR
- Poppler

**Install dependencies:**
```bash
# macOS
brew install tesseract poppler

# Ubuntu/Debian
sudo apt-get install tesseract-ocr poppler-utils

# Windows
# Download and add to PATH:
# Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
# Poppler: https://github.com/oschwartz10612/poppler-windows/releases/
```

## Install from Source

```bash
pip install git+https://github.com/<username>/<repository>.git
```

## Usage

### CLI

```bash
# Search and download
epstein-search "flight logs" --output-dir pdfs --pages 10 20

# Extract text
epstein-ocr --pdf-dir pdfs --output-dir texts --cores 10
```

### Python API

```python
from epscrape import search_and_download, process_all_pdfs

# Download PDFs
search_and_download("flight logs", output_dir="pdfs")

# Extract text
process_all_pdfs(pdf_dir="pdfs", output_dir="texts", num_cores=5)
```

## Options

**search_and_download:**
- `search_string` - Search term
- `output_dir` - PDF output directory (default: "pdfs")
- `url_file` - Save URLs to file (default: auto-generated)
- `headless` - Run browser headless (default: False)
- `start_page`, `end_page` - Page range to extract

**process_all_pdfs:**
- `pdf_dir` - Input PDF directory (default: "pdfs")
- `output_dir` - Text output directory (default: "texts")
- `language` - Tesseract language code (default: "eng")
- `num_cores` - Parallel processes (default: 5)

## Notes

- Browser windows open for age verification (handled automatically)
- CAPTCHA may require one manual click
- Already processed files are skipped
- Empty PDFs are marked as "empty file"

## Troubleshooting

- **Tesseract not found**: Ensure it's in PATH (`which tesseract` on macOS/Linux)
- **Chrome driver issues**: Update Chrome browser (driver auto-downloads)
- **PDF errors**: Verify Poppler is installed (`pdftoppm -v`)
