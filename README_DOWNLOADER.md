# PDF Downloader for Justice.gov Epstein Files

A Python-based PDF downloader that handles age verification and CAPTCHA for bulk downloading PDFs from justice.gov.

## Features

- ✅ Automatic age verification handling
- ✅ CAPTCHA requires only one manual click per session
- ✅ Batch processing from multiple URL files
- ✅ Cookie persistence across downloads
- ✅ Can be used as CLI tool or Python module
- ✅ Progress tracking and error reporting

## Installation

1. Ensure you're in the virtual environment:
```bash
source .venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

**Single file:**
```bash
python src/superdownloader.py example_urls.txt
```

**Multiple files (CAPTCHA only needed once!):**
```bash
python src/superdownloader.py urls1.txt urls2.txt urls3.txt
```

### As a Python Module

```python
from src.superdownloader import download_pdfs

# Single file
count = download_pdfs("example_urls.txt")

# Multiple files
count = download_pdfs(["urls1.txt", "urls2.txt", "urls3.txt"])

# Custom output directory
count = download_pdfs("urls.txt", output_dir="./my_pdfs")
```

See `example_module_usage.py` for more examples.

## URL File Format

Create text files with one URL per line. Lines starting with `#` are treated as comments:

```
# Dataset 5 PDFs
https://www.justice.gov/epstein/files/DataSet%205/EFTA00008418.pdf
https://www.justice.gov/epstein/files/DataSet%205/EFTA00008419.pdf
```

## How It Works

1. Browser opens (visible by default)
2. On first download, you click "I am not a robot" once
3. Age verification is automatically handled
4. Cookies persist for all subsequent downloads
5. PDFs are saved to `./pdfs` directory
6. Browser closes when complete

## Important Notes

- **Browser Mode**: Runs in visible mode by default (headless mode has compatibility issues)
- **One CAPTCHA**: When processing multiple files, you only interact with CAPTCHA once
- **Session Persistence**: All downloads in one run share the same browser session
- **Chrome Required**: Uses Chrome browser with undetected-chromedriver

## Troubleshooting

**Browser won't start:**
- Ensure Chrome is installed and up to date
- Version 144 is currently configured

**Downloads fail:**
- Check internet connection
- Verify URLs are accessible
- Ensure output directory is writable

**CAPTCHA issues:**
- Make sure to click "I am not a robot" when prompted
- Wait for the checkmark before the script proceeds

## Technical Details

- Uses `undetected-chromedriver` to bypass bot detection
- Handles age verification via Selenium automation
- Downloads PDFs using `requests` with session cookies
- SSL certificate verification disabled for macOS compatibility
