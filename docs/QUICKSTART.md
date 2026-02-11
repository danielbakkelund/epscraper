# Quick Start Guide

## Search and Download PDFs from justice.gov/epstein

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure Chrome browser is installed on your system.

---

### Option A: One Command (Easiest)

Search and download in a single command:

```bash
python search_and_download.py "your search terms"
```

Example:
```bash
python search_and_download.py "flight logs"
```

This will:
- Search for "flight logs" on justice.gov/epstein
- Save URLs to `data/flight_logs_urls.txt`
- Download PDFs to `pdfs/` directory

---

### Option B: Two Steps (More Control)

**Step 1: Search**
```bash
python src/supersearcher.py "your search terms"
```

**Step 2: Download**
```bash
python src/superdownloader.py data/your_search_terms_urls.txt
```

Example:
```bash
# Search
python src/supersearcher.py "black book"

# Download
python src/superdownloader.py data/black_book_urls.txt
```

---

### Custom Output Directories

Save PDFs to a specific folder:

```bash
python search_and_download.py "documents" --output-dir pdfs/my_documents
```

Or with two steps:
```bash
python src/supersearcher.py "documents"
python src/superdownloader.py data/documents_urls.txt --output-dir pdfs/my_documents
```

---

### What to Expect

1. **Browser Window**: A Chrome window will open (this is normal)
2. **Age Verification**: The script automatically clicks "Yes, I am 18+"
3. **Search**: The script enters your search terms and waits for results
4. **Download**: Each PDF download is shown with progress
5. **Completion**: Summary shows how many files were downloaded

---

### Common Issues

**"Module not found"**: Make sure you're in the project root directory

**"Chrome version mismatch"**: The script will auto-download the correct driver

**No results found**: Try different search terms or check if the site is accessible

---

### See Also

- `WORKFLOW.md` - Detailed workflow documentation
- `README_SEARCHER.md` - Supersearcher module documentation
- `README_DOWNLOADER.md` - Superdownloader module documentation
