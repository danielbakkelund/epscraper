#!/usr/bin/env python3
"""
Search and Download Workflow

This script combines supersearcher and superdownloader to:
1. Search for PDFs using search terms
2. Download the found PDFs

Usage:
    python search_and_download.py "search terms"
    python search_and_download.py "search terms" --output-dir pdfs/custom
"""

import sys
import os

from epscrape.supersearcher import search_pdfs
from epscrape.superdownloader import download_pdfs


def search_and_download(search_string, output_dir='./pdfs', url_file=None, headless=False, start_page=1, end_page=None):
    """
    Search for PDFs and download them.

    Args:
        search_string: The search query
        output_dir: Directory to save downloaded PDFs (default: './pdfs')
        url_file: Optional custom path for URL file. If None, uses default naming
        headless: Run browsers in headless mode (default: False)
        start_page: First page to extract from (default: 1)
        end_page: Last page to extract from (default: None, meaning all pages)

    Returns:
        tuple: (number of URLs found, number of PDFs downloaded)
    """
    print('=' * 70)
    print('STEP 1: SEARCHING FOR PDFs')
    print('=' * 70)

    # Search and extract URLs
    urls = search_pdfs(search_string, output_file=url_file, headless=headless, 
                      start_page=start_page, end_page=end_page)

    if not urls:
        print('\nNo URLs found. Nothing to download.')
        return (0, 0)

    # Determine the URL file path
    if url_file is None:
        safe_search_string = search_string.replace(' ', '_')
        url_file = f'data/{safe_search_string}_urls.txt'

    print('\n' + '=' * 70)
    print('STEP 2: DOWNLOADING PDFs')
    print('=' * 70)
    print(f'\nDownloading {len(urls)} PDFs to {output_dir}/')
    print(f'Reading from: {url_file}\n')

    # Download PDFs
    downloaded_count = download_pdfs(url_file, output_dir=output_dir, headless=headless)

    print('\n' + '=' * 70)
    print('WORKFLOW COMPLETE')
    print('=' * 70)
    print(f'URLs found: {len(urls)}')
    print(f'PDFs downloaded: {downloaded_count}')
    print('=' * 70)

    return (len(urls), downloaded_count)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h', 'help']:
        print('Usage: python search_and_download.py <search_string> [OPTIONS]')
        print('\nOptions:')
        print('  --output-dir DIR   Directory to save PDFs (default: ./pdfs)')
        print('  --url-file FILE    Custom path for URL file (default: data/<search>_urls.txt)')
        print('  --pages START END  Extract pages START to END (inclusive, default: all pages)')
        print('  --headless         Run browsers in headless mode (experimental)')
        print('\nExamples:')
        print('  python search_and_download.py "flight logs"')
        print('  python search_and_download.py "email" --pages 10 20')
        print('  python search_and_download.py "black book" --output-dir pdfs/blackbook')
        print('  python search_and_download.py "documents" --url-file data/docs.txt')
        sys.exit(0 if len(sys.argv) > 1 else 1)

    # Parse arguments
    search_string = sys.argv[1]
    output_dir = './pdfs'
    url_file = None
    headless = '--headless' in sys.argv
    start_page = 1
    end_page = None

    # Check for output directory option
    if '--output-dir' in sys.argv:
        try:
            idx = sys.argv.index('--output-dir')
            output_dir = sys.argv[idx + 1]
        except (ValueError, IndexError):
            print('Error: --output-dir requires a directory path')
            sys.exit(1)

    # Check for URL file option
    if '--url-file' in sys.argv:
        try:
            idx = sys.argv.index('--url-file')
            url_file = sys.argv[idx + 1]
        except (ValueError, IndexError):
            print('Error: --url-file requires a file path')
            sys.exit(1)

    # Check for page range
    if '--pages' in sys.argv:
        try:
            pages_index = sys.argv.index('--pages')
            start_page = int(sys.argv[pages_index + 1])
            end_page = int(sys.argv[pages_index + 2])
            if start_page < 1 or end_page < start_page:
                print('Error: Invalid page range. START must be >= 1 and END must be >= START')
                sys.exit(1)
        except (ValueError, IndexError):
            print('Error: --pages flag requires two integers (START END)')
            sys.exit(1)

    try:
        urls_found, pdfs_downloaded = search_and_download(
            search_string,
            output_dir=output_dir,
            url_file=url_file,
            headless=headless,
            start_page=start_page,
            end_page=end_page
        )
        sys.exit(0 if pdfs_downloaded > 0 else 1)
    except Exception as e:
        print(f'\nFatal error: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
