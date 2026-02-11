# Integration Summary: Search + Download Workflow

## Overview

You can now search for PDFs on justice.gov/epstein and download them automatically. The workflow integrates `supersearcher` and `superdownloader` modules.

---

## Quick Start

### Easiest: One Command
```bash
python search_and_download.py "flight logs"
```

### Two Steps: More Control
```bash
# Step 1: Search
python src/supersearcher.py "black book"

# Step 2: Download
python src/superdownloader.py data/black_book_urls.txt
```

---

## Files Created

| File | Purpose |
|------|---------|
| `search_and_download.py` | Integrated workflow script |
| `QUICKSTART.md` | Quick start guide |
| `WORKFLOW.md` | Detailed workflow documentation |
| `examples_complete.py` | Complete examples showing all approaches |

---

## Usage Patterns

### 1. Command Line Integration

**Integrated script:**
```bash
python search_and_download.py "search term" --output-dir pdfs/custom
```

**Separate commands:**
```bash
python src/supersearcher.py "search term"
python src/superdownloader.py data/search_term_urls.txt
```

### 2. Python Module Integration

```python
from supersearcher import search_pdfs
from superdownloader import download_pdfs

# Search
urls = search_pdfs('flight logs')

# Download
if urls:
    download_pdfs('data/flight_logs_urls.txt')
```

### 3. Advanced Integration

```python
from supersearcher import PDFSearcher
from superdownloader import PDFDownloader

# Search phase
with PDFSearcher() as searcher:
    urls = searcher.search_and_extract('term')
    # Save URLs to file

# Download phase
with PDFDownloader() as downloader:
    downloader.download_from_file('urls.txt')
```

---

## Key Features

✅ **Single browser session** - Age verification only once  
✅ **Automatic pagination** - Gets all search results  
✅ **Flexible output** - Custom directories for URLs and PDFs  
✅ **Multiple searches** - Batch process multiple search terms  
✅ **Error handling** - Graceful failures with informative messages  

---

## File Flow

```
Search Term
    ↓
supersearcher.py
    ↓
data/<search_term>_urls.txt
    ↓
superdownloader.py
    ↓
pdfs/<filename>.pdf
```

---

## Common Workflows

### Download specific search results
```bash
python search_and_download.py "flight logs" --output-dir pdfs/flights
```

### Search multiple terms, download all
```bash
# Search
python src/supersearcher.py "term1" --output data/t1.txt
python src/supersearcher.py "term2" --output data/t2.txt

# Download all (single browser session)
python src/superdownloader.py data/t1.txt data/t2.txt
```

### Just search (no download)
```bash
python src/supersearcher.py "term" --output data/urls_for_later.txt
```

### Just download (from existing URLs)
```bash
python src/superdownloader.py data/existing_urls.txt
```

---

## Next Steps

1. **Read the guides:**
   - `QUICKSTART.md` - Get started quickly
   - `WORKFLOW.md` - Detailed usage patterns
   - `examples_complete.py` - Code examples

2. **Run a test:**
   ```bash
   python search_and_download.py "test" --output-dir pdfs/test
   ```

3. **Customize:**
   - Modify output directories
   - Filter URLs before downloading
   - Process PDFs after downloading

---

## Support

- Module docs: `README_SEARCHER.md`, `README_DOWNLOADER.md`
- Instructions: `instrs/searcher_instructions.md`
- Help: `python <script> --help`
