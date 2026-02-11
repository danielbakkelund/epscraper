# Quick Reference Card

## Installation
```bash
pip install -r requirements.txt
```

## Usage

### Easiest Way
```bash
python search_and_download.py "search terms"
```

### With Options
```bash
python search_and_download.py "search terms" \
    --output-dir pdfs/custom \
    --url-file data/custom.txt
```

## Separate Steps

### Search Only
```bash
python src/supersearcher.py "search terms"
# Output: data/search_terms_urls.txt
```

### Download Only
```bash
python src/superdownloader.py data/urls.txt
# Output: pdfs/
```

## Python Module

```python
# Search
from supersearcher import search_pdfs
urls = search_pdfs('term')

# Download
from superdownloader import download_pdfs
download_pdfs('data/term_urls.txt')
```

## Common Tasks

| Task | Command |
|------|---------|
| Search + Download | `python search_and_download.py "term"` |
| Search only | `python src/supersearcher.py "term"` |
| Download only | `python src/superdownloader.py file.txt` |
| Custom output | `--output-dir pdfs/custom` |
| Help | `--help` flag on any script |

## File Locations

| Type | Default Location |
|------|------------------|
| URL files | `data/<search>_urls.txt` |
| PDF files | `pdfs/` |
| Source code | `src/super*.py` |
| Documentation | `*.md` files |
| Examples | `example*.py` files |

## What Happens

1. Browser opens (Chrome)
2. Age verification clicked automatically
3. Search performed / PDFs downloaded
4. Files saved to disk
5. Browser closes
6. Summary printed

## Documentation

- `QUICKSTART.md` - Getting started
- `WORKFLOW.md` - Detailed workflows
- `INTEGRATION_SUMMARY.md` - Overview
- `README_SEARCHER.md` - Search module
- `README_DOWNLOADER.md` - Download module
