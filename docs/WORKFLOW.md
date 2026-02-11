# Workflow Guide: Search and Download PDFs

This guide shows different ways to use `supersearcher` and `superdownloader` together.

## Method 1: Two-Step Command Line

### Step 1: Search for PDFs
```bash
# Search and save URLs to file
python src/supersearcher.py "flight logs"
# Creates: data/flight_logs_urls.txt
```

### Step 2: Download PDFs
```bash
# Download from the URL file
python src/superdownloader.py data/flight_logs_urls.txt
# Downloads to: pdfs/
```

### Custom output locations:
```bash
# Search with custom URL file
python src/supersearcher.py "black book" --output data/blackbook_urls.txt

# Download to custom directory
python src/superdownloader.py data/blackbook_urls.txt --output-dir pdfs/blackbook
```

---

## Method 2: Integrated Workflow Script

Use the combined workflow script:

```bash
# Search and download in one command
python search_and_download.py "flight logs"

# With custom output directory
python search_and_download.py "black book" --output-dir pdfs/blackbook

# With all options
python search_and_download.py "documents" \
    --url-file data/docs.txt \
    --output-dir pdfs/documents
```

---

## Method 3: Python Script

Create a custom Python script:

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from supersearcher import search_pdfs
from superdownloader import download_pdfs

# Step 1: Search
search_term = "flight logs"
url_file = f"data/{search_term.replace(' ', '_')}_urls.txt"
urls = search_pdfs(search_term, url_file)

print(f"Found {len(urls)} URLs")

# Step 2: Download
if urls:
    count = download_pdfs(url_file, output_dir="pdfs")
    print(f"Downloaded {count} PDFs")
```

---

## Method 4: Advanced Python Usage

For more control, use the context managers:

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from supersearcher import PDFSearcher
from superdownloader import PDFDownloader

search_term = "flight logs"

# Search phase
print("Searching...")
with PDFSearcher() as searcher:
    urls = searcher.search_and_extract(search_term)

print(f"Found {len(urls)} URLs")

# Save URLs
url_file = f"data/{search_term.replace(' ', '_')}_urls.txt"
with open(url_file, 'w') as f:
    for url in urls:
        f.write(f"{url}\n")

# Download phase
print("Downloading...")
with PDFDownloader(output_dir="pdfs") as downloader:
    count = downloader.download_from_file(url_file)

print(f"Downloaded {count} PDFs")
```

---

## Common Workflows

### Download multiple searches
```bash
# Search for different terms
python src/supersearcher.py "flight logs" --output data/flights.txt
python src/supersearcher.py "black book" --output data/blackbook.txt
python src/supersearcher.py "documents" --output data/docs.txt

# Download all at once (reuses browser session)
python src/superdownloader.py data/flights.txt data/blackbook.txt data/docs.txt
```

### Search only (no download)
```bash
# Just get the URLs for later
python src/supersearcher.py "term" --output data/urls_for_later.txt
```

### Download only (from existing URL file)
```bash
# If you already have URLs
python src/superdownloader.py data/existing_urls.txt
```

---

## Tips

1. **Browser Windows**: Both tools open browser windows by default. This helps with CAPTCHA/verification.

2. **Age Verification**: Both tools handle the age verification automatically (click "Yes, I am 18+").

3. **Session Reuse**: When downloading multiple URL files, `superdownloader` reuses the browser session, so you only need to pass CAPTCHA once.

4. **Output Files**: 
   - URLs are saved to `data/` by default
   - PDFs are saved to `pdfs/` by default
   - Both can be customized

5. **Error Handling**: If a search finds no results, the download step won't run.

6. **File Naming**: The searcher creates URL files named `data/<search_term>_urls.txt` (spaces become underscores).

---

## Quick Reference

| Task | Command |
|------|---------|
| Search | `python src/supersearcher.py "term"` |
| Download | `python src/superdownloader.py data/urls.txt` |
| Both | `python search_and_download.py "term"` |
| Help | `python <script> --help` |
